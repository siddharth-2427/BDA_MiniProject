import React, { useEffect, useState } from 'react';
import { fetchIrradianceVsGen, fetchWeatherAnalytics } from '../api';
import { ResponsiveContainer, ScatterChart, Scatter, XAxis, YAxis, Tooltip, CartesianGrid } from 'recharts';
import { CloudSun, Info, Thermometer } from 'lucide-react';

export default function WeatherPage() {
  const [scatterData, setScatterData] = useState([]);
  const [weatherStats, setWeatherStats] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadData() {
      try {
        setLoading(true);
        const irr = await fetchIrradianceVsGen();
        const weather = await fetchWeatherAnalytics();
        
        if (irr && irr.rows) {
          const points = irr.rows.map(row => ({
            plant_id: row[0],
            irradiation: parseFloat(row[1]) || 0,
            ac_power: parseFloat(row[3]) || 0,
          }));
          setScatterData(points);
        }
        
        if (weather && weather.rows) {
          setWeatherStats(weather.rows);
        }
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    }
    loadData();
  }, []);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-navy-900">Weather Analytics & Solar Correlations</h1>
        <p className="text-sm text-slate-500">Hive SQL insights on irradiance vs generation relationship and panel temperature dynamics</p>
      </div>

      {/* Dataset Limitation Alert Banner */}
      <div className="bg-amber-50 border border-amber-200 p-4 rounded-lg flex items-start space-x-3 text-amber-900 text-sm">
        <Info className="h-5 w-5 text-amber-600 flex-shrink-0 mt-0.5" />
        <div>
          <p className="font-semibold">Dataset Limitation Notice</p>
          <p className="mt-0.5">The Kaggle solar dataset contains ambient temperature, module temperature, and solar irradiance. It does <strong>not</strong> contain relative humidity, cloud cover fraction, or wind speed. Models rely strictly on available sensors.</p>
        </div>
      </div>

      {/* Weather Stats Cards */}
      <div className="bg-white p-6 rounded-lg border border-slate-200 shadow-sm">
        <h2 className="text-lg font-semibold text-navy-900 mb-4 flex items-center space-x-2">
          <Thermometer className="h-5 w-5 text-red-500" />
          <span>Hive Weather Parameter Statistics</span>
        </h2>
        {weatherStats.length === 0 ? (
          <p className="text-sm text-slate-500">Run Hive warehousing to view ambient & module temperature statistics.</p>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-sm text-slate-600">
              <thead className="bg-slate-100 text-navy-900 border-b">
                <tr>
                  <th className="p-3">Plant ID</th>
                  <th className="p-3">Min / Avg / Max Ambient (°C)</th>
                  <th className="p-3">Min / Avg / Max Module (°C)</th>
                  <th className="p-3">Avg Irradiance (kW/m²)</th>
                </tr>
              </thead>
              <tbody>
                {weatherStats.map((row, i) => (
                  <tr key={i} className="border-b">
                    <td className="p-3 font-semibold">{row[0]}</td>
                    <td className="p-3">{row[1]} / {row[2]} / {row[3]}</td>
                    <td className="p-3">{row[4]} / {row[5]} / {row[6]}</td>
                    <td className="p-3 text-emerald-600 font-medium">{row[7]}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Irradiance vs AC Power Scatter Plot */}
      <div className="bg-white p-6 rounded-lg border border-slate-200 shadow-sm">
        <h2 className="text-lg font-semibold text-navy-900 mb-4">Solar Irradiance (kW/m²) vs AC Generation (kW)</h2>
        {scatterData.length === 0 ? (
          <div className="p-12 text-center text-slate-500 bg-slate-50 rounded border border-dashed">
            No irradiance correlation data available yet. Please execute the pipeline.
          </div>
        ) : (
          <div className="h-80 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <ScatterChart margin={{ top: 20, right: 20, bottom: 20, left: 20 }}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis type="number" dataKey="irradiation" name="Irradiance" unit=" kW/m²" />
                <YAxis type="number" dataKey="ac_power" name="AC Power" unit=" kW" />
                <Tooltip cursor={{ strokeDasharray: '3 3' }} />
                <Scatter name="Solar Plant Output" data={scatterData} fill="#F59E0B" />
              </ScatterChart>
            </ResponsiveContainer>
          </div>
        )}
      </div>
    </div>
  );
}
