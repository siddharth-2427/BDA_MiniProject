import React from 'react';
import { Server, ExternalLink, HardDrive, Cpu, Database, Activity } from 'lucide-react';

export default function ArchitecturePage() {
  const uis = [
    { name: 'HDFS NameNode UI', url: 'http://localhost:9870', icon: HardDrive, desc: 'Block storage report & HDFS file browser' },
    { name: 'YARN ResourceManager UI', url: 'http://localhost:8088', icon: Cpu, desc: 'Cluster nodes, active jobs, and executor resource logs' },
    { name: 'HiveServer2 Web UI', url: 'http://localhost:10002', icon: Database, desc: 'Hive query sessions and metadata status' },
    { name: 'FastAPI REST Server Docs', url: 'http://localhost:8000/docs', icon: Activity, desc: 'Interactive OpenAPI endpoint documentation' },
  ];

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-navy-900">Big Data System Architecture</h1>
        <p className="text-sm text-slate-500">End-to-end distributed processing pipeline topology & cluster links</p>
      </div>

      {/* Local Cluster Banner Notice */}
      <div className="bg-slate-100 border border-slate-300 p-4 rounded-lg text-slate-800 text-sm">
        <p className="font-semibold">Cluster Deployment Specification</p>
        <p className="mt-1">This setup runs as a functional <strong>single-host pseudo-distributed cluster</strong> inside Docker containers on WSL2. It models production YARN resource allocation, distributed HDFS block replication, and Hive metastore queries.</p>
      </div>

      {/* Cluster UIs Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {uis.map((ui) => {
          const Icon = ui.icon;
          return (
            <a
              key={ui.name}
              href={ui.url}
              target="_blank"
              rel="noopener noreferrer"
              className="bg-white p-5 rounded-lg border border-slate-200 shadow-sm hover:border-solar-green transition flex items-center space-x-4 group"
            >
              <div className="p-3 bg-navy-900 text-solar-yellow rounded-lg group-hover:scale-105 transition">
                <Icon className="h-6 w-6" />
              </div>
              <div className="flex-1">
                <div className="flex items-center space-x-2">
                  <span className="font-bold text-navy-900 group-hover:text-emerald-600 transition">{ui.name}</span>
                  <ExternalLink className="h-4 w-4 text-slate-400" />
                </div>
                <p className="text-xs text-slate-500 mt-1">{ui.desc}</p>
              </div>
            </a>
          );
        })}
      </div>

      {/* Pipeline Component Mapping Table */}
      <div className="bg-white p-6 rounded-lg border border-slate-200 shadow-sm">
        <h2 className="text-lg font-semibold text-navy-900 mb-4">Pipeline Layer Responsibilities</h2>
        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm text-slate-600">
            <thead className="bg-slate-100 text-navy-900 border-b font-semibold">
              <tr>
                <th className="p-3">Layer</th>
                <th className="p-3">Technology</th>
                <th className="p-3">Functionality</th>
              </tr>
            </thead>
            <tbody>
              <tr className="border-b">
                <td className="p-3 font-semibold">Storage</td>
                <td className="p-3">Hadoop HDFS 3.3.6</td>
                <td className="p-3">Stores raw CSV datasets, processed Parquet partitions, and analytics outputs.</td>
              </tr>
              <tr className="border-b">
                <td className="p-3 font-semibold">Distributed Compute</td>
                <td className="p-3">Apache Spark 3.5.3 (YARN)</td>
                <td className="p-3">Runs schema cleaning, inverter aggregation, solar-weather join, and feature engineering.</td>
              </tr>
              <tr className="border-b">
                <td className="p-3 font-semibold">MapReduce</td>
                <td className="p-3">Hadoop Streaming (Python)</td>
                <td className="p-3">Computes daily energy totals directly from raw CSV for cross-verification.</td>
              </tr>
              <tr className="border-b">
                <td className="p-3 font-semibold">Data Warehousing</td>
                <td className="p-3">Apache Hive 3.1.3</td>
                <td className="p-3">External SQL tables over HDFS Parquet for analytical trend queries.</td>
              </tr>
              <tr className="border-b">
                <td className="p-3 font-semibold">Machine Learning</td>
                <td className="p-3">Scikit-Learn & Joblib</td>
                <td className="p-3">Weather-conditioned regression models evaluated using chronological split.</td>
              </tr>
              <tr className="border-b">
                <td className="p-3 font-semibold">Serving & UI</td>
                <td className="p-3">FastAPI & React Dashboard</td>
                <td className="p-3">RESTful endpoints and modern Recharts dashboard for interactive prediction and metrics.</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
