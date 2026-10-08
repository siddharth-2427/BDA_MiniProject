import React, { useEffect, useState } from 'react';
import { fetchModelMetrics, fetchTestPredictions } from '../api';
import { ResponsiveContainer, LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid } from 'recharts';
import { Award, RefreshCw, Layers } from 'lucide-react';

export default function ModelPerformancePage() {
  const [plantId, setPlantId] = useState(4135001);
  const [metrics, setMetrics] = useState(null);
  const [testPreds, setTestPreds] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadModelDetails();
  }, [plantId]);

  async function loadModelDetails() {
    try {
      setLoading(true);
      const m = await fetchModelMetrics(plantId);
      setMetrics(m);
      const p = await fetchTestPredictions(plantId);
      if (p && p.rows) {
        setTestPreds(p.rows);
      }
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-navy-900">Machine Learning Model Evaluation</h1>
          <p className="text-sm text-slate-500">Rigorous chronological split, overall vs daylight-only metrics comparison</p>
        </div>
        <select
          value={plantId}
          onChange={(e) => setPlantId(parseInt(e.target.value))}
          className="border border-slate-300 rounded px-4 py-2 text-sm font-semibold bg-white"
        >
          <option value={4135001}>Plant 1 (ID: 4135001)</option>
          <option value={4136001}>Plant 2 (ID: 4136001)</option>
        </select>
      </div>

      {loading ? (
        <div className="p-8 text-center text-slate-500">Loading model registry metrics...</div>
      ) : !metrics ? (
        <div className="p-12 text-center text-slate-500 bg-white rounded border border-dashed">
          No trained model metrics found for Plant {plantId}. Please run the machine learning stage in the Big Data Pipeline.
        </div>
      ) : (
        <>
          {/* Selected Champion Model Card */}
          <div className="bg-white p-6 rounded-lg border border-slate-200 shadow-sm flex justify-between items-center">
            <div>
              <span className="text-xs uppercase font-semibold text-slate-500">Primary Champion Model</span>
              <h2 className="text-2xl font-bold text-navy-900 flex items-center space-x-2">
                <Award className="h-6 w-6 text-solar-amber" />
                <span>{metrics.metrics?.selected_model}</span>
              </h2>
            </div>
            <div className="text-right">
              <span className="text-xs uppercase font-semibold text-slate-500">Chronological Test Split</span>
              <p className="text-sm font-mono text-slate-700">{metrics.split_info?.test_range?.[0]} to {metrics.split_info?.test_range?.[1]}</p>
            </div>
          </div>

          {/* Candidate Models Evaluation Table */}
          <div className="bg-white p-6 rounded-lg border border-slate-200 shadow-sm">
            <h3 className="text-lg font-semibold text-navy-900 mb-4">Candidate Model Performance Comparison</h3>
            <div className="overflow-x-auto">
              <table className="w-full text-left text-sm text-slate-600">
                <thead className="bg-slate-100 text-navy-900 border-b font-semibold">
                  <tr>
                    <th className="p-3">Model Architecture</th>
                    <th className="p-3">Overall MAE</th>
                    <th className="p-3">Overall RMSE</th>
                    <th className="p-3">Overall R²</th>
                    <th className="p-3">Daylight-Only R²</th>
                  </tr>
                </thead>
                <tbody>
                  {Object.entries(metrics.metrics?.test_metrics || {}).map(([modelName, m]) => (
                    <tr key={modelName} className={`border-b ${modelName === metrics.metrics?.selected_model ? 'bg-emerald-50 font-semibold text-emerald-900' : ''}`}>
                      <td className="p-3">{modelName}</td>
                      <td className="p-3">{m.overall?.mae}</td>
                      <td className="p-3">{m.overall?.rmse}</td>
                      <td className="p-3">{m.overall?.r2}</td>
                      <td className="p-3 text-emerald-700">{m.daylight_only?.r2 ?? 'N/A'}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          {/* Actual vs Predicted Test Set Chart */}
          <div className="bg-white p-6 rounded-lg border border-slate-200 shadow-sm">
            <h3 className="text-lg font-semibold text-navy-900 mb-4">Test Set: Actual vs Predicted Solar Generation (kW)</h3>
            {testPreds.length === 0 ? (
              <p className="text-sm text-slate-500">No test predictions plot available.</p>
            ) : (
              <div className="h-80 w-full">
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={testPreds}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="timestamp" />
                    <YAxis unit=" kW" />
                    <Tooltip />
                    <Line type="monotone" dataKey="actual_kw" stroke="#0B1F3A" dot={false} name="Actual AC Power" />
                    <Line type="monotone" dataKey="predicted_kw" stroke="#10B981" dot={false} strokeWidth={2} name="Predicted AC Power" />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            )}
          </div>
        </>
      )}
    </div>
  );
}
