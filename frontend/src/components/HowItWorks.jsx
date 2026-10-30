import React from 'react';
import {
  FileSearch,
  Building,
  ShieldAlert,
  FileCheck,
  CheckCircle,
  ArrowRight,
} from 'lucide-react';

export default function HowItWorks() {
  const steps = [
    {
      step: '01',
      title: 'Entity & Claim Extraction',
      description:
        'The ingestion layer parses company names, recruiter identities, communication channels, job roles, and compensation structures from submitted offers.',
      icon: FileSearch,
      details: ['Natural language parsing', 'Entity recognition', 'Claim isolation'],
    },
    {
      step: '02',
      title: 'Evidence Cross-Referencing',
      description:
        'Corroborates claims against verifiable external records: active domain registries, company registries, official career boards, and DNS mail security records.',
      icon: Building,
      details: ['Domain age & MX records', 'Registered corporate entity lookup', 'Official careers page matching'],
    },
    {
      step: '03',
      title: 'Risk & Anomaly Auditing',
      description:
        'Audits for high-frequency fraudulent patterns such as requested onboarding fees, unauthenticated communication channels, and spoofed headers.',
      icon: ShieldAlert,
      details: ['Upfront fee detection', 'Channel legitimacy check', 'Spoofing & impersonation tests'],
    },
    {
      step: '04',
      title: 'Verifiable Proof Report',
      description:
        'Generates an objective, transparent scorecard detailing verified facts, unconfirmed claims, identified risks, and recommended next steps.',
      icon: FileCheck,
      details: ['Itemized evidence citations', 'Confidence & risk index', 'Actionable candidate advice'],
    },
  ];

  return (
    <section id="how-it-works" className="py-20 border-t border-slate-800 bg-slate-950">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center max-w-3xl mx-auto mb-16">
          <span className="text-xs font-mono uppercase tracking-wider text-blue-400 font-semibold">
            Methodology & Architecture
          </span>
          <h2 className="text-3xl sm:text-4xl font-bold text-white mt-2 mb-4">
            How OFFERPROOF Verifies Opportunities
          </h2>
          <p className="text-slate-400 text-sm sm:text-base leading-relaxed">
            Unlike superficial review sites or opaque scanners, OFFERPROOF relies on auditable,
            evidence-grounded cross-examination to protect candidates from recruitment fraud.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {steps.map((item) => {
            const Icon = item.icon;
            return (
              <div
                key={item.step}
                className="relative rounded-2xl bg-slate-900/70 border border-slate-800 p-6 flex flex-col justify-between hover:border-blue-500/40 transition-colors"
              >
                <div>
                  <div className="flex items-center justify-between mb-5">
                    <span className="text-xs font-mono font-bold text-blue-400 px-2.5 py-1 rounded-md bg-blue-950/80 border border-blue-800/50">
                      STEP {item.step}
                    </span>
                    <div className="p-2.5 rounded-xl bg-slate-800 text-slate-300">
                      <Icon className="w-5 h-5 text-blue-400" />
                    </div>
                  </div>

                  <h3 className="text-base font-semibold text-white mb-2">
                    {item.title}
                  </h3>
                  <p className="text-xs text-slate-400 leading-relaxed mb-6">
                    {item.description}
                  </p>
                </div>

                <div className="pt-4 border-t border-slate-800/80 space-y-2">
                  {item.details.map((detail, idx) => (
                    <div key={idx} className="flex items-center gap-2 text-[11px] text-slate-300">
                      <CheckCircle className="w-3.5 h-3.5 text-blue-400 shrink-0" />
                      <span>{detail}</span>
                    </div>
                  ))}
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
}
