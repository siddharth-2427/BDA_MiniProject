const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

export async function fetchHealth() {
  const res = await fetch(`${API_BASE_URL}/health`);
  return res.json();
}

export async function fetchOverview() {
  const res = await fetch(`${API_BASE_URL}/analytics/overview`);
  return res.json();
}

export async function fetchDailyAnalytics() {
  const res = await fetch(`${API_BASE_URL}/analytics/daily`);
  return res.json();
}

export async function fetchMonthlyAnalytics() {
  const res = await fetch(`${API_BASE_URL}/analytics/monthly`);
  return res.json();
}

export async function fetchWeatherAnalytics() {
  const res = await fetch(`${API_BASE_URL}/analytics/weather`);
  return res.json();
}

export async function fetchIrradianceVsGen() {
  const res = await fetch(`${API_BASE_URL}/analytics/irradiance-vs-generation`);
  return res.json();
}

export async function fetchPerformanceSummary() {
  const res = await fetch(`${API_BASE_URL}/analytics/performance`);
  return res.json();
}

export async function fetchPipelineStatus() {
  const res = await fetch(`${API_BASE_URL}/pipeline/status`);
  return res.json();
}

export async function fetchJobDetails(jobId) {
  const res = await fetch(`${API_BASE_URL}/pipeline/jobs/${jobId}`);
  return res.json();
}

export async function runPipelineStep(stepName) {
  const res = await fetch(`${API_BASE_URL}/pipeline/run/${stepName}`, { method: 'POST' });
  return res.json();
}

export async function runFullPipeline() {
  const res = await fetch(`${API_BASE_URL}/pipeline/run`, { method: 'POST' });
  return res.json();
}

export async function fetchModels() {
  const res = await fetch(`${API_BASE_URL}/models`);
  return res.json();
}

export async function fetchModelMetrics(plantId) {
  const res = await fetch(`${API_BASE_URL}/models/${plantId}/metrics`);
  return res.json();
}

export async function fetchTestPredictions(plantId) {
  const res = await fetch(`${API_BASE_URL}/models/${plantId}/test-predictions`);
  return res.json();
}

export async function postPrediction(plantId, rows) {
  const res = await fetch(`${API_BASE_URL}/predict`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ plant_id: plantId, rows })
  });
  return res.json();
}

export async function validateDataset(formData) {
  const res = await fetch(`${API_BASE_URL}/datasets/validate`, {
    method: 'POST',
    body: formData
  });
  return res.json();
}

export async function uploadDataset(formData) {
  const res = await fetch(`${API_BASE_URL}/datasets/upload`, {
    method: 'POST',
    body: formData
  });
  return res.json();
}

export async function fetchDatasetsList() {
  const res = await fetch(`${API_BASE_URL}/datasets`);
  return res.json();
}
