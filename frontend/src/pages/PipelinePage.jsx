import React, { useState, useEffect } from 'react';
import { fetchPipelineStatus, fetchJobDetails, runPipelineStep, runFullPipeline } from '../api';
import { Play, Terminal, Layers, RefreshCw } from 'lucide-react';

const STEPS = [
  { id: 'ingest', label: '1. Data Ingestion', desc: 'CSVs to HDFS Raw Zone' },
  { id: 'spark_etl', label: '2. Spark ETL & Join', desc: 'PySpark on YARN (Parquet)' },
  { id: 'spark_analytics', label: '3. Spark Daily Aggs', desc: 'Summary Energy Metrics' },
  { id: 'mapreduce', label: '4. MapReduce Cross-Check', desc: 'Hadoop Streaming Job' },
  { id: 'hive', label: '5. Hive Warehousing', desc: 'External Table DDLs' },
  { id: 'train', label: '6. Scikit-Learn Training', desc: 'Model Fitting & Registry' },
];

export default function PipelinePage() {
  const [pipelineStatus, setPipelineStatus] = useState(null);
  const [activeJobId, setActiveJobId] = useState(null);
  const [jobDetails, setJobDetails] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadStatus();
    const interval = setInterval(loadStatus, 3000);
    return () => clearInterval(interval);
  }, [activeJobId]);

  async function loadStatus() {
    try {
      const status = await fetchPipelineStatus();
      setPipelineStatus(status);
      if (status.active_job_id) {
        setActiveJobId(status.active_job_id);
      }
      if (activeJobId) {
        const details = await fetchJobDetails(activeJobId);
        setJobDetails(details);
      }
    } catch (err) {
      console.error(err);
    }
  }

  async function handleRunStep(stepId) {
    try {
      setLoading(true);
      const res = await runPipelineStep(stepId);
      setActiveJobId(res.job_id);
    } catch (err) {
      alert(`Error starting step: ${err.message}`);
    } finally {
      setLoading(false);
    }
  }

  async function handleRunAll() {
    try {
      setLoading(true);
      const res = await runFullPipeline();
      setActiveJobId(res.job_id);
    } catch (err) {
      alert(`Error starting pipeline: ${err.message}`);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-navy-900">Big Data Orchestration Pipeline</h1>
          <p className="text-sm text-slate-500">Monitor distributed Spark on YARN, MapReduce, and Hive table creation</p>
        </div>
        <button
          onClick={handleRunAll}
          disabled={loading || pipelineStatus?.is_running}
          className="bg-solar-green text-navy-900 px-5 py-2.5 rounded-lg font-bold flex items-center space-x-2 hover:bg-emerald-400 transition disabled:opacity-50"
        >
          <Play className="h-5 w-5 fill-current" />
          <span>{pipelineStatus?.is_running ? 'Pipeline Executing...' : 'Run Full Pipeline'}</span>
        </button>
      </div>

      {/* Stepper Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {STEPS.map((step) => (
          <div key={step.id} className="bg-white p-5 rounded-lg border border-slate-200 shadow-sm flex justify-between items-center">
            <div>
              <p className="font-semibold text-navy-900">{step.label}</p>
              <p className="text-xs text-slate-500">{step.desc}</p>
            </div>
            <button
              onClick={() => handleRunStep(step.id)}
              disabled={loading || pipelineStatus?.is_running}
              className="text-xs font-semibold text-navy-900 bg-slate-100 hover:bg-slate-200 px-3 py-1.5 rounded border transition"
            >
              Run Step
            </button>
          </div>
        ))}
      </div>

      {/* Active YARN Apps */}
      <div className="bg-white p-6 rounded-lg border border-slate-200 shadow-sm">
        <h2 className="text-lg font-semibold text-navy-900 mb-3 flex items-center space-x-2">
          <Layers className="h-5 w-5 text-solar-amber" />
          <span>YARN ResourceManager Application Monitor</span>
        </h2>
        {pipelineStatus?.yarn_apps?.length === 0 ? (
          <p className="text-sm text-slate-500">No active or historical YARN applications reported yet.</p>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-sm text-slate-600">
              <thead className="bg-slate-100 text-navy-900 border-b">
                <tr>
                  <th className="p-2">App ID</th>
                  <th className="p-2">Name</th>
                  <th className="p-2">State</th>
                  <th className="p-2">Final Status</th>
                </tr>
              </thead>
              <tbody>
                {pipelineStatus?.yarn_apps?.map((app) => (
                  <tr key={app.id} className="border-b font-mono text-xs">
                    <td className="p-2 text-blue-600">{app.id}</td>
                    <td className="p-2">{app.name}</td>
                    <td className="p-2">{app.state}</td>
                    <td className="p-2">{app.finalStatus}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Real Live Log Console */}
      <div className="bg-navy-900 text-slate-200 p-6 rounded-lg border border-navy-700 font-mono text-xs shadow-inner">
        <div className="flex justify-between items-center mb-3 pb-2 border-b border-navy-700">
          <span className="flex items-center space-x-2 text-solar-yellow font-bold">
            <Terminal className="h-4 w-4" />
            <span>Execution Log Tail (Job ID: {activeJobId || 'None'})</span>
          </span>
          <span className="text-slate-400">Status: {jobDetails?.status || 'IDLE'}</span>
        </div>
        <div className="h-64 overflow-y-auto space-y-1 bg-navy-800 p-4 rounded border border-navy-700">
          {jobDetails?.logs?.length === 0 || !jobDetails?.logs ? (
            <p className="text-slate-500 italic">Select and run a step to stream live Hadoop / Spark / Hive logs...</p>
          ) : (
            jobDetails.logs.map((line, idx) => (
              <div key={idx} className="whitespace-pre-wrap">{line}</div>
            ))
          )}
        </div>
      </div>
    </div>
  );
}
