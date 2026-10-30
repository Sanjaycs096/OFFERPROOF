import React from 'react';
import { RefreshCw, Wifi, WifiOff, CheckCircle2, AlertCircle } from 'lucide-react';

export default function StatusBadge({ isChecking, isOnline, latencyMs, error, onRefresh }) {
  return (
    <div className="flex items-center gap-2">
      <div
        className={`inline-flex items-center gap-2 px-3 py-1.5 rounded-full text-xs font-medium border transition-colors ${
          isChecking
            ? 'bg-slate-800/80 border-slate-700 text-slate-300'
            : isOnline
            ? 'bg-emerald-950/60 border-emerald-500/40 text-emerald-300'
            : 'bg-rose-950/60 border-rose-500/40 text-rose-300'
        }`}
        title={isOnline ? `Connected to FastAPI Backend (${latencyMs}ms)` : error || 'Backend Disconnected'}
      >
        <span className="relative flex h-2 w-2">
          {isOnline && !isChecking && (
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
          )}
          <span
            className={`relative inline-flex rounded-full h-2 w-2 ${
              isChecking
                ? 'bg-amber-400'
                : isOnline
                ? 'bg-emerald-400'
                : 'bg-rose-400'
            }`}
          ></span>
        </span>

        <span className="font-mono">
          {isChecking
            ? 'Connecting...'
            : isOnline
            ? `API Online (${latencyMs}ms)`
            : 'API Offline'}
        </span>

        <button
          onClick={onRefresh}
          disabled={isChecking}
          aria-label="Refresh API connection status"
          className="ml-1 text-slate-400 hover:text-white disabled:opacity-40 transition-transform active:rotate-180"
          title="Re-check backend connection"
        >
          <RefreshCw className={`w-3 h-3 ${isChecking ? 'animate-spin' : ''}`} />
        </button>
      </div>
    </div>
  );
}
