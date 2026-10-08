import os
from pathlib import Path
from fastapi import APIRouter
from app.services.hive import execute_beeline_query
from app.core.config import settings

router = APIRouter()

def read_hql_and_execute(hql_filename: str):
    hql_path = Path(settings.PROJECT_ROOT) / "hive" / "sql" / hql_filename
    if not hql_path.exists():
        return {"query_name": hql_filename, "headers": [], "rows": [], "execution_time_sec": 0.0, "error": "Query file not found"}
    with open(hql_path) as f:
        sql = f.read()
    res = execute_beeline_query(sql)
    res["query_name"] = hql_filename
    return res

@router.get("/analytics/overview")
def get_analytics_overview():
    res = read_hql_and_execute("05_performance_summary.hql")
    rows = res.get("rows", [])
    
    total_energy = 0.0
    peak_kw = 0.0
    if rows:
        try:
            total_energy = sum(float(r[2]) for r in rows if len(r) > 2 and r[2])
            peak_kw = max(float(r[3]) for r in rows if len(r) > 3 and r[3])
        except Exception:
            pass
            
    return {
        "total_energy_kwh": round(total_energy, 2),
        "peak_power_kw": round(peak_kw, 2),
        "total_rows_stored": len(rows),
        "active_plants": [4135001, 4136001],
        "query_execution": res
    }

@router.get("/analytics/daily")
def get_daily_analytics():
    return read_hql_and_execute("01_daily_generation.hql")

@router.get("/analytics/monthly")
def get_monthly_analytics():
    return read_hql_and_execute("02_monthly_trend.hql")

@router.get("/analytics/weather")
def get_weather_analytics():
    return read_hql_and_execute("03_weather_stats.hql")

@router.get("/analytics/irradiance-vs-generation")
def get_irradiance_vs_gen_analytics():
    return read_hql_and_execute("04_irradiance_vs_gen.hql")

@router.get("/analytics/performance")
def get_performance_summary_analytics():
    return read_hql_and_execute("05_performance_summary.hql")
