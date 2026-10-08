import React, { useEffect, useState } from 'react';
import { fetchOverview, fetchDailyAnalytics } from '../api';
import { ResponsiveContainer, AreaChart, Area, XAxis, YAxis, Tooltip, CartesianGrid } from 'recharts';
import { Zap, Activity, Database, Award } from 'lucide-react';

export default function OverviewPage() {
  const [overview, setOverview] = useState(null);
  const [dailyData, setDailyData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function loadData() {
      try {
        setLoading(true);
        const ov = await fetchOverview();
        const daily = await fetchDailyAnalytics();
        setOverview(ov);
        
        if (daily && daily.rows) {
          const chartData = daily.rows.map(row => ({
            plant_id: row[0],
            date: row[1],
            energy: parseFloat(row[2]) || 0,
            peak: parseFloat(row[3]) || 0
          }));
          setDailyData(chartData);
        }
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }
    loadData();
  }, []);

  if (loading) return <div className="p-8 text-center text-slate-600">Loading dashboard metrics...</div>;
  if (error) return <div className="p-8 text-center text-red-600">Failed to load overview: {error}</div>;

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-navy-900">Executive Overview</h1>
        <p className="text-sm text-slate-500">Real-time solar plant generation metrics & Big Data analytics</p>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-white p-5 rounded-lg border border-slate-200 shadow-sm flex items-center space-x-4">
          <div className="p-3 bg-amber-100 rounded-full text-amber-600">
            <Zap className="h-6 w-6" />
          </div>
          <div>
            <p className="text-xs font-semibold text-slate-500 uppercase">Total Energy (kWh)</p>
            <p className="text-2xl font-bold text-navy-900">{overview?.total_energy_kwh || 'Run pipeline'}</p>
          </div>
        </div>

        <div className="bg-white p-5 rounded-lg border border-slate-200 shadow-sm flex items-center space-x-4">
          <div className="p-3 bg-emerald-100 rounded-full text-emerald-600">
            <Activity className="h-6 w-6" />
          </div>
          <div>
            <p className="text-xs font-semibold text-slate-500 uppercase">Peak Recorded (kW)</p>
            <p className="text-2xl font-bold text-navy-900">{overview?.peak_power_kw || 'Run pipeline'}</p>
          </div>
        </div>

        <div className="bg-white p-5 rounded-lg border border-slate-200 shadow-sm flex items-center space-x-4">
          <div className="p-3 bg-blue-100 rounded-full text-blue-600">
            <Database className="h-6 w-6" />
          </div>
          <div>
            <p className="text-xs font-semibold text-slate-500 uppercase">Hive Summaries</p>
            <p className="text-2xl font-bold text-navy-900">{overview?.total_rows_stored || 0} rows</p>
          </div>
        </div>

        <div className="bg-white p-5 rounded-lg border border-slate-200 shadow-sm flex items-center space-x-4">
          <div className="p-3 bg-purple-100 rounded-full text-purple-600">
            <Award className="h-6 w-6" />
          </div>
          <div>
            <p className="text-xs font-semibold text-slate-500 uppercase">Active Solar Plants</p>
            <p className="text-2xl font-bold text-navy-900">Plant 1 & 2</p>
          </div>
        </div>
      </div>

      {/* Generation Trend Chart */}
      <div className="bg-white p-6 rounded-lg border border-slate-200 shadow-sm">
        <h2 className="text-lg font-semibold text-navy-900 mb-4">Daily Solar Generation Trend (kWh)</h2>
        {dailyData.length === 0 ? (
          <div className="p-12 text-center text-slate-500 bg-slate-50 rounded border border-dashed border-slate-300">
            Run the Big Data pipeline to populate Hive tables and render generation trends.
          </div>
        ) : (
          <div className="h-80 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={dailyData}>
                <defs>
                  <linearGradient id="energyGrad" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#10B981" stopOpacity={0.8}/>
                    <stop offset="95%" stopColor="#10B981" stopOpacity={0.0}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" />
                <YAxis />
                <Tooltip />
                <Area type="monotone" dataKey="energy" stroke="#10B981" fillOpacity={1} fill="url(#energyGrad)" name="Daily kWh" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        )}
      </div>
    </div>
  );
}
