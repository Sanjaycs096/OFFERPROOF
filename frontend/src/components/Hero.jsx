import React from 'react';
import { ShieldCheck, SearchCheck, Building2, AlertTriangle, ArrowDown, HelpCircle, FileText, CheckCircle2 } from 'lucide-react';

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

        {/* Subtitle - Clear Problem & Solution */}
        <p className="max-w-3xl mx-auto text-base sm:text-lg text-slate-300 leading-relaxed mb-10">
          Students struggle to distinguish genuine career opportunities from misleading or impersonated recruitment announcements.
          OFFERPROOF extracts opportunity claims, cross-references independent technical evidence, and explains what students should independently verify before applying or paying.
        </p>

        {/* Problem, Solution, Differentiator Triad */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 max-w-4xl mx-auto text-left mb-10">
          {/* 1. The Problem */}
          <div className="p-4 rounded-xl bg-slate-900/60 border border-slate-800 hover:border-slate-700 transition-colors">
            <div className="flex items-center gap-3 mb-2">
              <div className="p-2 rounded-lg bg-rose-500/10 text-rose-400 border border-rose-500/20">
                <AlertTriangle className="w-4 h-4" />
              </div>
              <h2 className="text-sm font-semibold text-white">The Student Challenge</h2>
            </div>
            <p className="text-xs text-slate-400 leading-relaxed">
              Job seekers face deceptive offers with upfront fees, lookalike domains, and unauthenticated webmail masquerading as verified recruiters.
            </p>
          </div>

          {/* 2. The Solution */}
          <div className="p-4 rounded-xl bg-slate-900/60 border border-slate-800 hover:border-slate-700 transition-colors">
            <div className="flex items-center gap-3 mb-2">
              <div className="p-2 rounded-lg bg-blue-500/10 text-blue-400 border border-blue-500/20">
                <SearchCheck className="w-4 h-4" />
              </div>
              <h2 className="text-sm font-semibold text-white">Evidence Cross-Checking</h2>
            </div>
            <p className="text-xs text-slate-400 leading-relaxed">
              Audits technical signals via public RDAP registries, Cloudflare DNS-over-HTTPS routing, and recruiter email consistency without visiting untrusted URLs.
            </p>
          </div>

          {/* 3. The Differentiator */}
          <div className="p-4 rounded-xl bg-slate-900/60 border border-slate-800 hover:border-slate-700 transition-colors">
            <div className="flex items-center gap-3 mb-2">
              <div className="p-2 rounded-lg bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                <CheckCircle2 className="w-4 h-4" />
              </div>
              <h2 className="text-sm font-semibold text-white">Transparent Uncertainty</h2>
            </div>
            <p className="text-xs text-slate-400 leading-relaxed">
              No black-box risk percentages. Clear separation between verified technical facts, unverified claims (salaries, openings), and prioritized next steps.
            </p>
          </div>
        </div>

        {/* Call-to-action anchor */}
        <div className="flex flex-col sm:flex-row items-center justify-center gap-3">
          <a
            href="#submit"
            className="inline-flex items-center gap-2 px-5 py-2.5 rounded-lg bg-blue-600 hover:bg-blue-500 text-white font-medium text-sm transition-colors shadow-lg shadow-blue-600/20"
          >
            <span>Inspect an Opportunity</span>
            <ArrowDown className="w-4 h-4" />
          </a>
          <a
            href="#how-it-works"
            className="inline-flex items-center gap-2 px-4 py-2.5 rounded-lg bg-slate-900 hover:bg-slate-800 text-slate-300 font-medium text-sm border border-slate-800 transition-colors"
          >
            <span>How Verification Works</span>
          </a>
        </div>
      </div>
    </section>
  );
}
