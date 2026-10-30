import React from 'react';
import { ShieldCheck, Github, ExternalLink } from 'lucide-react';
import StatusBadge from './StatusBadge';

export default function Navbar({ healthState }) {
  return (
    <header className="sticky top-0 z-50 backdrop-blur-md bg-slate-950/80 border-b border-slate-800">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        {/* Brand */}
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-lg bg-blue-600/10 border border-blue-500/30 flex items-center justify-center text-blue-500 shadow-sm shadow-blue-500/10">
            <ShieldCheck className="w-6 h-6 text-blue-400" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="text-lg font-bold tracking-tight text-white font-mono">
                OFFER<span className="text-blue-500">PROOF</span>
              </span>
              <span className="px-1.5 py-0.5 text-[10px] uppercase font-mono tracking-wider font-semibold rounded bg-blue-950 border border-blue-800 text-blue-300">
                Phase 1
              </span>
            </div>
            <p className="text-[11px] text-slate-400 hidden sm:block">
              Evidence-Based Opportunity Verification
            </p>
          </div>
        </div>

        {/* Navigation links */}
        <nav className="hidden md:flex items-center gap-6 text-sm text-slate-300">
          <a href="#submit" className="hover:text-blue-400 transition-colors">
            Verify Opportunity
          </a>
          <a href="#how-it-works" className="hover:text-blue-400 transition-colors">
            How It Works
          </a>
          <a href="#disclaimer" className="hover:text-blue-400 transition-colors">
            Privacy & Trust
          </a>
        </nav>

        {/* Backend Status & Github */}
        <div className="flex items-center gap-3">
          <StatusBadge
            isChecking={healthState.isChecking}
            isOnline={healthState.isOnline}
            latencyMs={healthState.latencyMs}
            error={healthState.error}
            onRefresh={healthState.refresh}
          />
          <a
            href="https://github.com/Sanjaycs096/OFFERPROOF"
            target="_blank"
            rel="noopener noreferrer"
            className="p-2 text-slate-400 hover:text-white hover:bg-slate-800/60 rounded-lg border border-transparent hover:border-slate-700 transition-colors"
            title="View on GitHub"
            aria-label="View on GitHub"
          >
            <Github className="w-5 h-5" />
          </a>
        </div>
      </div>
    </header>
  );
}
