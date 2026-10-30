import React from 'react';
import { ShieldCheck, SearchCheck, Building2, AlertTriangle, ArrowDown } from 'lucide-react';

export default function Hero() {
  return (
    <section className="relative pt-16 pb-12 border-b border-slate-800/80 bg-slate-950">
      <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
        {/* Security Tagline Pill */}
        <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-blue-950/60 border border-blue-700/40 text-blue-300 text-xs font-mono uppercase tracking-wider mb-6">
          <ShieldCheck className="w-3.5 h-3.5 text-blue-400" />
          <span>Don't trust the offer. Verify the evidence.</span>
        </div>

        {/* Main Title */}
        <h1 className="text-4xl sm:text-5xl lg:text-6xl font-bold tracking-tight text-white mb-6">
          AI-Assisted Opportunity <br />
          <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 via-blue-200 to-indigo-300">
            Evidence Verification
          </span>
        </h1>

        {/* Subtitle */}
        <p className="max-w-2xl mx-auto text-base sm:text-lg text-slate-300 leading-relaxed mb-10">
          Protecting students, fresh graduates, and job seekers from ghost jobs, deceptive recruiters,
          and fake internships. We cross-examine claims against verifiable organizational records.
        </p>

        {/* Trust & Capability Highlights */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 max-w-3xl mx-auto text-left mb-10">
          <div className="p-4 rounded-xl bg-slate-900/60 border border-slate-800">
            <div className="flex items-center gap-3 mb-2">
              <div className="p-2 rounded-lg bg-blue-500/10 text-blue-400 border border-blue-500/20">
                <Building2 className="w-4 h-4" />
              </div>
              <h2 className="text-sm font-semibold text-white">Entity Corroboration</h2>
            </div>
            <p className="text-xs text-slate-400 leading-relaxed">
              Cross-references corporate registries, active domain records, and public career listings.
            </p>
          </div>

          <div className="p-4 rounded-xl bg-slate-900/60 border border-slate-800">
            <div className="flex items-center gap-3 mb-2">
              <div className="p-2 rounded-lg bg-amber-500/10 text-amber-400 border border-amber-500/20">
                <AlertTriangle className="w-4 h-4" />
              </div>
              <h2 className="text-sm font-semibold text-white">Red Flag Auditing</h2>
            </div>
            <p className="text-xs text-slate-400 leading-relaxed">
              Detects high-risk signals including upfront payment requests, disposable emails, and spoofed headers.
            </p>
          </div>

          <div className="p-4 rounded-xl bg-slate-900/60 border border-slate-800">
            <div className="flex items-center gap-3 mb-2">
              <div className="p-2 rounded-lg bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                <SearchCheck className="w-4 h-4" />
              </div>
              <h2 className="text-sm font-semibold text-white">Evidence Scorecards</h2>
            </div>
            <p className="text-xs text-slate-400 leading-relaxed">
              Provides transparent, step-by-step verification reports instead of black-box conjectures.
            </p>
          </div>
        </div>

        {/* Call-to-action anchor */}
        <div className="flex justify-center">
          <a
            href="#submit"
            className="inline-flex items-center gap-2 px-5 py-2.5 rounded-lg bg-blue-600 hover:bg-blue-500 text-white font-medium text-sm transition-colors shadow-lg shadow-blue-600/20"
          >
            <span>Inspect an Opportunity</span>
            <ArrowDown className="w-4 h-4" />
          </a>
        </div>
      </div>
    </section>
  );
}
