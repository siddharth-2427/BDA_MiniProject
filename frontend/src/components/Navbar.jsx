import React from 'react';
import { NavLink } from 'react-router-dom';
import { Sun, Database, Cpu, CloudSun, Target, BarChart2, Server } from 'lucide-react';

export default function Navbar() {
  const navItems = [
    { to: '/', label: 'Overview', icon: Sun },
    { to: '/datasets', label: 'Datasets', icon: Database },
    { to: '/pipeline', label: 'Big Data Pipeline', icon: Cpu },
    { to: '/weather', label: 'Weather Analytics', icon: CloudSun },
    { to: '/predict', label: 'Prediction', icon: Target },
    { to: '/models', label: 'Model Performance', icon: BarChart2 },
    { to: '/architecture', label: 'Architecture', icon: Server },
  ];

  return (
    <header className="bg-navy-900 text-white shadow-md border-b border-navy-700">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center space-x-3">
            <Sun className="h-8 w-8 text-solar-yellow animate-pulse" />
            <div>
              <span className="font-bold text-lg tracking-wide text-white">SolarAnalytics</span>
              <span className="text-xs bg-solar-green text-navy-900 font-semibold px-2 py-0.5 rounded ml-2">Big Data</span>
            </div>
          </div>
          <nav className="flex space-x-1 sm:space-x-4">
            {navItems.map((item) => {
              const Icon = item.icon;
              return (
                <NavLink
                  key={item.to}
                  to={item.to}
                  end={item.to === '/'}
                  className={({ isActive }) =>
                    `flex items-center space-x-1.5 px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                      isActive
                        ? 'bg-navy-700 text-solar-yellow border-b-2 border-solar-yellow'
                        : 'text-slate-300 hover:bg-navy-800 hover:text-white'
                    }`
                  }
                >
                  <Icon className="h-4 w-4" />
                  <span>{item.label}</span>
                </NavLink>
              );
            })}
          </nav>
        </div>
      </div>
    </header>
  );
}
