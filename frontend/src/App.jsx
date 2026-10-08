import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import OverviewPage from './pages/OverviewPage';
import DatasetsPage from './pages/DatasetsPage';
import PipelinePage from './pages/PipelinePage';
import WeatherPage from './pages/WeatherPage';
import PredictPage from './pages/PredictPage';
import ModelPerformancePage from './pages/ModelPerformancePage';
import ArchitecturePage from './pages/ArchitecturePage';

export default function App() {
  return (
    <Router>
      <div className="min-h-screen flex flex-col bg-slate-50 text-navy-900">
        <Navbar />
        <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <Routes>
            <Route path="/" element={<OverviewPage />} />
            <Route path="/datasets" element={<DatasetsPage />} />
            <Route path="/pipeline" element={<PipelinePage />} />
            <Route path="/weather" element={<WeatherPage />} />
            <Route path="/predict" element={<PredictPage />} />
            <Route path="/models" element={<ModelPerformancePage />} />
            <Route path="/architecture" element={<ArchitecturePage />} />
          </Routes>
        </main>
        <footer className="bg-white border-t border-slate-200 py-4 text-center text-xs text-slate-500">
          Renewable Energy Generation Prediction • Big Data Architecture Academic Mini Project
        </footer>
      </div>
    </Router>
  );
}
