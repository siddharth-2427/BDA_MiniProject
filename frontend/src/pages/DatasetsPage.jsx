import React, { useState, useEffect } from 'react';
import { validateDataset, uploadDataset, fetchDatasetsList } from '../api';
import { Upload, CheckCircle, AlertTriangle, FileText } from 'lucide-react';

export default function DatasetsPage() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [validation, setValidation] = useState(null);
  const [uploadStatus, setUploadStatus] = useState(null);
  const [datasetList, setDatasetList] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadDatasetList();
  }, []);

  async function loadDatasetList() {
    try {
      const data = await fetchDatasetsList();
      if (data && data.raw_datasets) {
        setDatasetList(data.raw_datasets);
      }
    } catch (err) {
      console.error("Failed to list datasets:", err);
    }
  }

  async function handleFileSelect(e) {
    const file = e.target.files[0];
    if (!file) return;
    setSelectedFile(file);
    setValidation(null);
    setUploadStatus(null);

    const formData = new FormData();
    formData.append('file', file);
    try {
      setLoading(true);
      const res = await validateDataset(formData);
      setValidation(res);
    } catch (err) {
      setValidation({ valid: false, errors: [err.message] });
    } finally {
      setLoading(false);
    }
  }

  async function handleUpload() {
    if (!selectedFile || !validation?.valid) return;
    const formData = new FormData();
    formData.append('file', selectedFile);
    try {
      setLoading(true);
      const res = await uploadDataset(formData);
      setUploadStatus(res);
      loadDatasetList();
    } catch (err) {
      setUploadStatus({ status: 'FAILED', error: err.message });
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-navy-900">Dataset Management</h1>
        <p className="text-sm text-slate-500">Upload compatible weather/generation CSVs and stage raw ingestion batches</p>
      </div>

      <div className="bg-white p-6 rounded-lg border border-slate-200 shadow-sm space-y-4">
        <h2 className="text-lg font-semibold text-navy-900">CSV Schema Validation & Upload</h2>
        
        <div className="border-2 border-dashed border-slate-300 p-8 text-center rounded-lg bg-slate-50">
          <input
            type="file"
            accept=".csv"
            onChange={handleFileSelect}
            className="hidden"
            id="csv-upload-input"
          />
          <label htmlFor="csv-upload-input" className="cursor-pointer flex flex-col items-center">
            <Upload className="h-10 w-10 text-slate-400 mb-2" />
            <span className="text-sm font-medium text-navy-900">Click to select generation or weather CSV</span>
            <span className="text-xs text-slate-500 mt-1">Must match Kaggle schema headers</span>
          </label>
        </div>

        {loading && <div className="text-sm text-blue-600 font-medium">Processing file...</div>}

        {validation && (
          <div className={`p-4 rounded border ${validation.valid ? 'bg-emerald-50 border-emerald-200 text-emerald-900' : 'bg-red-50 border-red-200 text-red-900'}`}>
            <div className="flex items-center space-x-2 font-semibold">
              {validation.valid ? <CheckCircle className="h-5 w-5 text-emerald-600" /> : <AlertTriangle className="h-5 w-5 text-red-600" />}
              <span>{validation.valid ? `Schema Validated: ${validation.dataset_type?.toUpperCase()} (${validation.row_count} rows)` : 'Schema Validation Failed'}</span>
            </div>
            {validation.errors && validation.errors.length > 0 && (
              <ul className="list-disc list-inside text-sm mt-2 text-red-700">
                {validation.errors.map((err, i) => (
                  <li key={i}>{err}</li>
                ))}
              </ul>
            )}
            {validation.valid && (
              <button
                onClick={handleUpload}
                disabled={loading}
                className="mt-3 bg-solar-green text-navy-900 px-4 py-2 rounded font-semibold text-sm hover:bg-emerald-400 transition"
              >
                Upload Batch to HDFS & Raw Zone
              </button>
            )}
          </div>
        )}

        {uploadStatus && (
          <div className="p-4 bg-blue-50 border border-blue-200 rounded text-blue-900 text-sm">
            <span className="font-semibold">Batch Staged: {uploadStatus.batch_id}</span>
            <p>HDFS Path: {uploadStatus.hdfs_path}</p>
          </div>
        )}
      </div>

      {/* Raw datasets list */}
      <div className="bg-white p-6 rounded-lg border border-slate-200 shadow-sm">
        <h2 className="text-lg font-semibold text-navy-900 mb-4">Ingested Raw Datasets</h2>
        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm text-slate-600">
            <thead className="bg-slate-100 text-navy-900 font-semibold border-b">
              <tr>
                <th className="p-3">Filename</th>
                <th className="p-3">Size (KB)</th>
                <th className="p-3">Status</th>
              </tr>
            </thead>
            <tbody>
              {datasetList.length === 0 ? (
                <tr>
                  <td colSpan="3" className="p-4 text-center text-slate-500">No custom uploads yet. Standard Kaggle / dev sample dataset ready.</td>
                </tr>
              ) : (
                datasetList.map((file, idx) => (
                  <tr key={idx} className="border-b hover:bg-slate-50">
                    <td className="p-3 flex items-center space-x-2 font-mono text-xs">
                      <FileText className="h-4 w-4 text-slate-400" />
                      <span>{file.filename}</span>
                    </td>
                    <td className="p-3">{(file.size_bytes / 1024).toFixed(1)}</td>
                    <td className="p-3"><span className="bg-emerald-100 text-emerald-800 text-xs px-2 py-0.5 rounded">Staged</span></td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
