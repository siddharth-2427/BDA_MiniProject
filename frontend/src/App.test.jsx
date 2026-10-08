import { render, screen } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import React from 'react';
import App from './App';

// Mock fetch calls for UI unit tests
global.fetch = vi.fn((url) => {
  if (url.includes('/health')) {
    return Promise.resolve({
      json: () => Promise.resolve({ status: 'HEALTHY' }),
    });
  }
  return Promise.resolve({
    json: () => Promise.resolve({ total_energy_kwh: 12500.5, peak_power_kw: 450.0, total_rows_stored: 288, rows: [] }),
  });
});

describe('App Router & UI', () => {
  it('renders top navigation bar with SolarAnalytics branding', () => {
    render(<App />);
    expect(screen.getByText(/SolarAnalytics/i)).toBeInTheDocument();
  });
});
