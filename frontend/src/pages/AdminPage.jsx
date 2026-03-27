import { useState, useEffect } from 'react';
import Navbar from '../components/layout/Navbar';
import {
  uploadDocument,
  listDocuments,
  deleteDocument,
} from '../api/documents';

const NAMESPACES = [
  {
    value: 'public',
    label: '📢 Public',
    desc: 'Visible to all users including customers',
  },
  { value: 'sop', label: '📋 SOPs', desc: 'Operations staff and above' },
  { value: 'hr', label: '👥 HR', desc: 'All employees' },
  {
    value: 'compliance',
    label: '⚖️ Compliance',
    desc: 'Compliance officers and above',
  },
  { value: 'internal', label: '🔒 Internal', desc: 'Admin and executive only' },
  { value: 'executive', label: '👑 Executive', desc: 'Executive only' },
];

export default function AdminPage() {
  const [file, setFile] = useState(null);
  const [namespace, setNamespace] = useState('sop');
  const [version, setVersion] = useState('v1.0');
  const [uploading, setUploading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');
  const [docs, setDocs] = useState({});
  const [loadingDocs, setLoadingDocs] = useState(true);
  const [dragOver, setDragOver] = useState(false);

  useEffect(() => {
    loadDocs();
  }, []);

  const loadDocs = () => {
    setLoadingDocs(true);
    listDocuments()
      .then(setDocs)
      .catch(() => setDocs({}))
      .finally(() => setLoadingDocs(false));
  };

  const handleUpload = async () => {
    if (!file) return;
    setUploading(true);
    setResult(null);
    setError('');
    try {
      const res = await uploadDocument(file, namespace, version);
      setResult(res);
      setFile(null);
      loadDocs();
    } catch (err) {
      setError(err.response?.data?.detail || 'Upload failed.');
    } finally {
      setUploading(false);
    }
  };

  const handleDelete = async (ns, filename) => {
    if (!confirm(`Delete "${filename}" from "${ns}"?`)) return;
    try {
      await deleteDocument(ns, filename);
      loadDocs();
    } catch (err) {
      alert('Delete failed: ' + err.response?.data?.detail);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setDragOver(false);
    const dropped = e.dataTransfer.files[0];
    if (dropped) setFile(dropped);
  };

  const totalDocs = Object.values(docs).flat().length;

  return (
    <div className="min-h-screen bg-gray-950">
      <Navbar />
      <div className="max-w-5xl mx-auto px-6 py-8">
        <div className="mb-8">
          <h1 className="text-white font-bold text-2xl">Admin Panel</h1>
          <p className="text-gray-500 text-sm mt-1">
            Upload and manage knowledge base documents — admin only
          </p>
        </div>

        {/* Stats Row */}
        <div className="grid grid-cols-3 gap-4 mb-8">
          <div className="bg-gray-900 border border-gray-800 rounded-xl p-5">
            <div className="text-2xl font-bold text-cyan-400">{totalDocs}</div>
            <div className="text-gray-500 text-sm mt-1">Total Documents</div>
          </div>
          <div className="bg-gray-900 border border-gray-800 rounded-xl p-5">
            <div className="text-2xl font-bold text-green-400">
              {Object.keys(docs).length}
            </div>
            <div className="text-gray-500 text-sm mt-1">Active Namespaces</div>
          </div>
          <div className="bg-gray-900 border border-gray-800 rounded-xl p-5">
            <div className="text-2xl font-bold text-purple-400">
              PDF · DOCX · TXT
            </div>
            <div className="text-gray-500 text-sm mt-1">Supported Formats</div>
          </div>
        </div>

        <div className="grid grid-cols-2 gap-6">
          {/* Upload Panel */}
          <div className="bg-gray-900 border border-gray-800 rounded-xl p-6">
            <h2 className="text-white font-semibold text-lg mb-5">
              ⬆️ Upload New Document
            </h2>

            {/* Drop Zone */}
            <div
              onDragOver={(e) => {
                e.preventDefault();
                setDragOver(true);
              }}
              onDragLeave={() => setDragOver(false)}
              onDrop={handleDrop}
              onClick={() => document.getElementById('fileInput').click()}
              className={`border-2 border-dashed rounded-xl p-8 text-center cursor-pointer transition-all mb-4
                ${
                  dragOver
                    ? 'border-cyan-400 bg-cyan-500/5'
                    : file
                      ? 'border-green-500/40 bg-green-500/5'
                      : 'border-gray-700 hover:border-gray-600'
                }`}
            >
              <input
                type="file"
                id="fileInput"
                className="hidden"
                accept=".pdf,.docx,.txt"
                onChange={(e) => setFile(e.target.files[0])}
              />
              {file ? (
                <div>
                  <div className="text-2xl mb-2">
                    {file.name.endsWith('.pdf')
                      ? '📄'
                      : file.name.endsWith('.docx')
                        ? '📝'
                        : '📃'}
                  </div>
                  <div className="text-green-400 font-medium text-sm">
                    {file.name}
                  </div>
                  <div className="text-gray-600 text-xs mt-1">
                    {(file.size / 1024).toFixed(1)} KB
                  </div>
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      setFile(null);
                    }}
                    className="text-gray-600 hover:text-red-400 text-xs mt-2 transition-colors"
                  >
                    Remove
                  </button>
                </div>
              ) : (
                <div>
                  <div className="text-3xl mb-3">📂</div>
                  <div className="text-gray-400 text-sm font-medium">
                    Drop file here or click to browse
                  </div>
                  <div className="text-gray-600 text-xs mt-1">
                    PDF, DOCX, TXT supported
                  </div>
                </div>
              )}
            </div>

            {/* Namespace */}
            <div className="mb-4">
              <label className="text-gray-400 text-sm block mb-2">
                Namespace (who can access this document)
              </label>
              <select
                value={namespace}
                onChange={(e) => setNamespace(e.target.value)}
                className="w-full bg-gray-800 border border-gray-700 text-white rounded-lg px-3 py-2.5 text-sm focus:outline-none focus:border-cyan-500"
              >
                {NAMESPACES.map((n) => (
                  <option key={n.value} value={n.value}>
                    {n.label} — {n.desc}
                  </option>
                ))}
              </select>
            </div>

            {/* Version */}
            <div className="mb-5">
              <label className="text-gray-400 text-sm block mb-2">
                Document Version
              </label>
              <input
                type="text"
                value={version}
                onChange={(e) => setVersion(e.target.value)}
                placeholder="e.g. v1.0, v2.3, Jan-2025"
                className="w-full bg-gray-800 border border-gray-700 text-white rounded-lg px-3 py-2.5 text-sm focus:outline-none focus:border-cyan-500 placeholder-gray-600"
              />
            </div>

            {/* Error */}
            {error && (
              <div className="bg-red-500/10 border border-red-500/20 text-red-400 text-sm rounded-lg px-4 py-2.5 mb-4">
                {error}
              </div>
            )}

            {/* Success */}
            {result && (
              <div className="bg-green-500/10 border border-green-500/20 rounded-lg px-4 py-3 mb-4">
                <div className="text-green-400 text-sm font-medium mb-1">
                  ✅ {result.file} uploaded successfully
                </div>
                <div className="text-gray-500 text-xs">
                  {result.pages} pages · {result.chunks} chunks · namespace:{' '}
                  {result.namespace}
                </div>
              </div>
            )}

            <button
              onClick={handleUpload}
              disabled={!file || uploading}
              className="w-full bg-cyan-500 hover:bg-cyan-400 disabled:bg-gray-700 disabled:text-gray-500 text-gray-950 font-semibold rounded-xl py-2.5 text-sm transition-colors"
            >
              {uploading ? '⏳ Processing...' : '⬆️ Upload & Ingest'}
            </button>
          </div>

          {/* Document Library */}
          <div className="bg-gray-900 border border-gray-800 rounded-xl p-6">
            <div className="flex items-center justify-between mb-5">
              <h2 className="text-white font-semibold text-lg">
                📚 Document Library
              </h2>
              <button
                onClick={loadDocs}
                className="text-xs text-gray-500 hover:text-white transition-colors"
              >
                Refresh
              </button>
            </div>

            {loadingDocs ? (
              <div className="text-center py-12 text-gray-600 text-sm">
                Loading...
              </div>
            ) : Object.keys(docs).length === 0 ? (
              <div className="text-center py-12">
                <div className="text-3xl mb-3">📭</div>
                <div className="text-gray-600 text-sm">
                  No documents uploaded yet
                </div>
              </div>
            ) : (
              <div
                className="space-y-4 overflow-y-auto"
                style={{ maxHeight: '420px' }}
              >
                {Object.entries(docs).map(([ns, files]) => (
                  <div key={ns}>
                    <div className="text-xs font-medium text-gray-500 uppercase tracking-wider mb-2 flex items-center gap-2">
                      <span>
                        {NAMESPACES.find((n) => n.value === ns)?.label || ns}
                      </span>
                      <span className="bg-gray-800 text-gray-600 px-1.5 py-0.5 rounded text-xs">
                        {files.length}
                      </span>
                    </div>
                    {files.map((filename) => (
                      <div
                        key={filename}
                        className="flex items-center justify-between bg-gray-800 rounded-lg px-3 py-2 mb-1.5"
                      >
                        <div className="flex items-center gap-2 min-w-0">
                          <span className="text-sm">
                            {filename.endsWith('.pdf')
                              ? '📄'
                              : filename.endsWith('.docx')
                                ? '📝'
                                : '📃'}
                          </span>
                          <span className="text-gray-300 text-xs truncate">
                            {filename}
                          </span>
                        </div>
                        <button
                          onClick={() => handleDelete(ns, filename)}
                          className="text-gray-600 hover:text-red-400 text-xs ml-2 flex-shrink-0 transition-colors"
                        >
                          Delete
                        </button>
                      </div>
                    ))}
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
