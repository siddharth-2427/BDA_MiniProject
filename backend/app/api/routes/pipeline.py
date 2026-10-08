import os
import threading
from pathlib import Path
from fastapi import APIRouter, HTTPException, BackgroundTasks, status
from app.services.jobs import job_manager
from app.services.yarn import get_yarn_applications
from app.services.hdfs import run_hdfs_cmd
from app.services.spark import submit_spark_job
from app.services.mapreduce import submit_mapreduce_job
from app.services.hive import execute_beeline_query
from app.core.config import settings
from ml.train import train_plant_model
import pandas as pd

router = APIRouter()

def execute_pipeline_step(job_id: str, step_name: str):
    job_manager.append_log(job_id, f"=== Starting step: {step_name} ===")
    
    try:
        if step_name == "ingest":
            # Upload local sample files in data/dev_sample or data/raw to HDFS
            raw_dir = Path(settings.DATA_DIR) / "raw"
            sample_dir = Path(settings.DATA_DIR) / "dev_sample"
            
            target_dir = raw_dir if any(raw_dir.glob("*.csv")) else sample_dir
            job_manager.append_log(job_id, f"Ingesting CSVs from {target_dir} to HDFS /solar/raw/")
            
            run_hdfs_cmd(["-mkdir", "-p", "/solar/raw/generation/plant_id=4135001/batch_init"])
            run_hdfs_cmd(["-mkdir", "-p", "/solar/raw/weather/plant_id=4135001/batch_init"])
            
            for csv_file in target_dir.glob("*.csv"):
                if "Generation" in csv_file.name:
                    run_hdfs_cmd(["-put", "-f", str(csv_file), "/solar/raw/generation/plant_id=4135001/batch_init/"])
                elif "Weather" in csv_file.name:
                    run_hdfs_cmd(["-put", "-f", str(csv_file), "/solar/raw/weather/plant_id=4135001/batch_init/"])
            
            job_manager.update_job_status(job_id, "COMPLETED")
            job_manager.append_log(job_id, "Ingestion completed successfully.")

        elif step_name == "spark_etl":
            script_path = os.path.join(settings.PROJECT_ROOT, "spark_jobs", "etl_clean_join.py")
            code, stdout, stderr, app_id = submit_spark_job(script_path, [])
            job_manager.append_log(job_id, stdout)
            if code == 0:
                job_manager.update_job_status(job_id, "COMPLETED", yarn_app_id=app_id)
            else:
                job_manager.update_job_status(job_id, "FAILED", error=stderr[:500])

        elif step_name == "spark_analytics":
            script_path = os.path.join(settings.PROJECT_ROOT, "spark_jobs", "analytics_daily.py")
            code, stdout, stderr, app_id = submit_spark_job(script_path, [])
            job_manager.append_log(job_id, stdout)
            if code == 0:
                job_manager.update_job_status(job_id, "COMPLETED", yarn_app_id=app_id)
            else:
                job_manager.update_job_status(job_id, "FAILED", error=stderr[:500])

        elif step_name == "mapreduce":
            code, stdout, stderr, app_id = submit_mapreduce_job()
            job_manager.append_log(job_id, stdout)
            if code == 0:
                job_manager.update_job_status(job_id, "COMPLETED", yarn_app_id=app_id)
            else:
                job_manager.update_job_status(job_id, "FAILED", error=stderr[:500])

        elif step_name == "hive":
            hql_path = os.path.join(settings.PROJECT_ROOT, "hive", "sql", "00_init_tables.hql")
            with open(hql_path) as f:
                hql_content = f.read()
            res = execute_beeline_query(hql_content)
            if res.get("error") is None:
                job_manager.update_job_status(job_id, "COMPLETED")
            else:
                job_manager.update_job_status(job_id, "FAILED", error=res.get("error"))

        elif step_name == "train":
            # Export processed features from HDFS to pandas
            features_dir = Path(settings.DATA_DIR) / "dev_sample"
            # Read dev sample or export
            gen_path = list(features_dir.glob("*Generation*.csv"))
            weather_path = list(features_dir.glob("*Weather*.csv"))
            
            if gen_path and weather_path:
                gen_df = pd.read_csv(gen_path[0])
                weather_df = pd.read_csv(weather_path[0])
                gen_df["timestamp"] = pd.to_datetime(gen_df["DATE_TIME"], errors="coerce")
                weather_df["timestamp"] = pd.to_datetime(weather_df["DATE_TIME"], errors="coerce")
                
                gen_plant = gen_df.groupby(["PLANT_ID", "timestamp"])["AC_POWER"].sum().reset_index()
                gen_plant.rename(columns={"AC_POWER": "AC_POWER_KW", "PLANT_ID": "plant_id"}, inplace=True)
                weather_plant = weather_df.groupby(["PLANT_ID", "timestamp"]).agg({
                    "IRRADIATION": "mean",
                    "AMBIENT_TEMPERATURE": "mean",
                    "MODULE_TEMPERATURE": "mean"
                }).reset_index()
                weather_plant.rename(columns={"PLANT_ID": "plant_id"}, inplace=True)
                
                joined = pd.merge(gen_plant, weather_plant, on=["plant_id", "timestamp"], how="inner")
                joined["minute_of_day"] = joined["timestamp"].dt.hour * 60 + joined["timestamp"].dt.minute
                joined["sin_time"] = np.sin(joined["minute_of_day"] * (2 * np.pi / 1440.0))
                joined["cos_time"] = np.cos(joined["minute_of_day"] * (2 * np.pi / 1440.0))
                
                metrics = train_plant_model(joined, 4135001, Path(settings.MODELS_DIR))
                job_manager.update_job_status(job_id, "COMPLETED", metrics=metrics)
            else:
                job_manager.update_job_status(job_id, "FAILED", error="No feature data found for training.")

        else:
            job_manager.update_job_status(job_id, "FAILED", error=f"Unknown pipeline step: {step_name}")

    except Exception as e:
        job_manager.update_job_status(job_id, "FAILED", error=str(e))

def run_full_pipeline(job_id: str):
    steps = ["ingest", "spark_etl", "spark_analytics", "mapreduce", "hive", "train"]
    for step in steps:
        job_manager.append_log(job_id, f"\n=== RUNNING PIPELINE STEP: {step} ===")
        execute_pipeline_step(job_id, step)
        job = job_manager.get_job(job_id)
        if job and job.get("status") == "FAILED":
            job_manager.append_log(job_id, f"Pipeline halted due to failure in step: {step}")
            break

@router.post("/pipeline/run")
def start_pipeline_run(background_tasks: BackgroundTasks):
    try:
        job = job_manager.create_job("full_pipeline")
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    
    background_tasks.add_task(run_full_pipeline, job["job_id"])
    return {"job_id": job["job_id"], "status": "RUNNING", "message": "Pipeline run started."}

@router.post("/pipeline/run/{step_name}")
def start_pipeline_step(step_name: str, background_tasks: BackgroundTasks):
    try:
        job = job_manager.create_job(step_name)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    
    background_tasks.add_task(execute_pipeline_step, job["job_id"], step_name)
    return {"job_id": job["job_id"], "step": step_name, "status": "RUNNING"}

@router.get("/pipeline/status")
def get_pipeline_status():
    yarn_apps = get_yarn_applications()
    return {
        "active_job_id": job_manager.active_job_id,
        "is_running": job_manager.active_job_id is not None,
        "yarn_apps": yarn_apps
    }

@router.get("/pipeline/jobs/{job_id}")
def get_job_details(job_id: str):
    job = job_manager.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail=f"Job {job_id} not found.")
    logs = job_manager.get_logs(job_id, tail=100)
    job["logs"] = logs
    return job
