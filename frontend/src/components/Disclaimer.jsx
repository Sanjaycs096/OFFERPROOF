import React from 'react';
import { ShieldAlert, Lock, HelpCircle } from 'lucide-react';

export default function Disclaimer() {
  return (
    <section id="disclaimer" className="py-12 bg-slate-900/30 border-t border-slate-800">
      <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="rounded-2xl bg-slate-900 border border-slate-800 p-6 sm:p-8">
          <div className="flex items-center gap-3 mb-4">
            <div className="p-2 rounded-lg bg-amber-500/10 border border-amber-500/20 text-amber-400">
              <ShieldAlert className="w-5 h-5" />
            </div>
            <div>
              <h3 className="text-base font-semibold text-white">
                Safety & Privacy Disclaimer
              </h3>
              <p className="text-xs text-slate-400">
                Ethical verification standards and data protection guidelines
              </p>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 text-xs text-slate-300 leading-relaxed mt-4">
            <div className="space-y-2">
              <div className="flex items-center gap-2 font-medium text-slate-200">
                <Lock className="w-3.5 h-3.5 text-blue-400" />
                <span>Protect Your Personal Information (PII)</span>
              </div>
              <p className="text-slate-400">
                Please do not submit sensitive personal details such as Social Security Numbers,
                national identity identifiers, personal bank accounts, or private passwords. OFFERPROOF
                only evaluates organizational claims, contact domains, and offer legitimacy indicators.
              </p>
            </div>

            <div className="space-y-2">
              <div className="flex items-center gap-2 font-medium text-slate-200">
                <HelpCircle className="w-3.5 h-3.5 text-blue-400" />
                <span>Decision Support, Not Legal Counsel</span>
              </div>
              <p className="text-slate-400">
                OFFERPROOF's verification scorecards are evidence-grounded risk assessments designed to
                assist candidates during their due diligence. They do not constitute formal legal
                certifications or background checks.
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
