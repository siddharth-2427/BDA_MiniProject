import React, { useState } from 'react';
import { postPrediction } from '../api';
import { ResponsiveContainer, LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid } from 'recharts';
import { AlertCircle, Zap, Calculator } from 'lucide-react';

const INITIAL_ROWS = [
  { timestamp: '2020-05-16 08:00:00', IRRADIATION: 0.25, AMBIENT_TEMPERATURE: 24.5, MODULE_TEMPERATURE: 28.0, minute_of_day: 480 },
  { timestamp: '2020-05-16 10:00:00', IRRADIATION: 0.65, AMBIENT_TEMPERATURE: 28.0, MODULE_TEMPERATURE: 38.5, minute_of_day: 600 },
  { timestamp: '2020-05-16 12:00:00', IRRADIATION: 0.95, AMBIENT_TEMPERATURE: 31.2, MODULE_TEMPERATURE: 45.0, minute_of_day: 720 },
  { timestamp: '2020-05-16 14:00:00', IRRADIATION: 0.75, AMBIENT_TEMPERATURE: 32.0, MODULE_TEMPERATURE: 42.1, minute_of_day: 840 },
  { timestamp: '2020-05-16 16:00:00', IRRADIATION: 0.35, AMBIENT_TEMPERATURE: 29.5, MODULE_TEMPERATURE: 33.0, minute_of_day: 960 },
];

export default function PredictPage() {
  const [plantId, setPlantId] = useState(4135001);
  const [inputRows, setInputRows] = useState(INITIAL_ROWS);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  function handleInputChange(index, field, value) {
    const updated = [...inputRows];
    updated[index][field] = parseFloat(value) || 0;
    setInputRows(updated);
  }

  async function handlePredict() {
    try {
      setLoading(true);
      setError(null);
      const res = await postPrediction(plantId, inputRows);
      setResult(res);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-navy-900">Weather-Conditioned Solar Power Prediction</h1>
        <p className="text-sm text-slate-500">FastAPI model serving for real-time AC power output inference</p>
      </div>

      {/* Mandatory Problem Framing Banner */}
      <div className="bg-blue-50 border border-blue-200 p-4 rounded-lg flex items-start space-x-3 text-blue-900 text-sm">
        <AlertCircle className="h-5 w-5 text-blue-600 flex-shrink-0 mt-0.5" />
        <div>
          <p className="font-semibold">Model Scope Disclaimer</p>
          <p className="mt-0.5">Predictions are conditioned on the weather inputs you provide; this is <strong>not</strong> a weather forecaster. AC Power (kW) is predicted given specified irradiance and temperature profiles.</p>
        </div>
      </div>

      {/* Inputs Form */}
      <div className="bg-white p-6 rounded-lg border border-slate-200 shadow-sm space-y-4">
        <div className="flex justify-between items-center">
          <h2 className="text-lg font-semibold text-navy-900">Weather Input Parameters</h2>
          <div className="flex items-center space-x-2">
            <label className="text-sm font-medium text-navy-900">Select Solar Plant:</label>
            <select
              value={plantId}
              onChange={(e) => setPlantId(parseInt(e.target.value))}
              className="border border-slate-300 rounded px-3 py-1.5 text-sm bg-slate-50 font-semibold"
            >
              <option value={4135001}>Plant 1 (ID: 4135001)</option>
              <option value={4136001}>Plant 2 (ID: 4136001)</option>
            </select>
          </div>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm text-slate-600">
            <thead className="bg-slate-100 text-navy-900 font-semibold border-b">
              <tr>
                <th className="p-2">Timestamp</th>
                <th className="p-2">Irradiance (kW/m²)</th>
                <th className="p-2">Ambient Temp (°C)</th>
                <th className="p-2">Module Temp (°C)</th>
              </tr>
            </thead>
            <tbody>
              {inputRows.map((row, idx) => (
                <tr key={idx} className="border-b">
                  <td className="p-2 font-mono text-xs">{row.timestamp}</td>
                  <td className="p-2">
                    <input
                      type="number"
                      step="0.05"
                      value={row.IRRADIATION}
                      onChange={(e) => handleInputChange(idx, 'IRRADIATION', e.target.value)}
                      className="border rounded px-2 py-1 w-24 text-sm"
                    />
                  </td>
                  <td className="p-2">
                    <input
                      type="number"
                      step="0.5"
                      value={row.AMBIENT_TEMPERATURE}
                      onChange={(e) => handleInputChange(idx, 'AMBIENT_TEMPERATURE', e.target.value)}
                      className="border rounded px-2 py-1 w-24 text-sm"
                    />
                  </td>
                  <td className="p-2">
                    <input
                      type="number"
                      step="0.5"
                      value={row.MODULE_TEMPERATURE}
                      onChange={(e) => handleInputChange(idx, 'MODULE_TEMPERATURE', e.target.value)}
                      className="border rounded px-2 py-1 w-24 text-sm"
                    />
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        <button
          onClick={handlePredict}
          disabled={loading}
          className="bg-solar-green text-navy-900 px-6 py-2.5 rounded font-bold text-sm flex items-center space-x-2 hover:bg-emerald-400 transition"
        >
          <Calculator className="h-5 w-5" />
          <span>{loading ? 'Running Model Inference...' : 'Generate Prediction'}</span>
        </button>

        {error && <p className="text-sm text-red-600 font-semibold">{error}</p>}
      </div>

      {/* Results Output */}
      {result && (
        <div className="bg-white p-6 rounded-lg border border-slate-200 shadow-sm space-y-4">
          <div className="flex justify-between items-center pb-3 border-b border-slate-200">
            <h2 className="text-lg font-semibold text-navy-900">Model Prediction Results</h2>
            <div className="text-right">
              <span className="text-xs uppercase font-semibold text-slate-500">Estimated Total Energy</span>
              <p className="text-2xl font-bold text-solar-green">{result.total_energy_kwh} kWh</p>
            </div>
          </div>

          <div className="h-72 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={result.predictions}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="timestamp" />
                <YAxis unit=" kW" />
                <Tooltip />
                <Line type="monotone" dataKey="predicted_kw" stroke="#10B981" strokeWidth={3} name="Predicted AC Power (kW)" />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>
      )}
    </div>
  );
}
