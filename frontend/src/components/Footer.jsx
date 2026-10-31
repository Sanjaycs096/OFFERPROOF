import React from 'react';
import { ShieldCheck, Github, Heart, Code2 } from 'lucide-react';

export default function Footer({ apiData }) {
  return (
    <footer className="border-t border-slate-800 bg-slate-950 text-slate-400 text-xs">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
          {/* Brand info */}
          <div className="md:col-span-2 space-y-3">
            <div className="flex items-center gap-2">
              <ShieldCheck className="w-5 h-5 text-blue-500" />
              <span className="text-base font-bold text-white font-mono">
                OFFER<span className="text-blue-500">PROOF</span>
              </span>
            </div>
            <p className="text-slate-400 max-w-md leading-relaxed">
              An AI-assisted, evidence-based opportunity verification platform empowering job
              seekers, students, and interns to detect fraud before committing their trust or resources.
            </p>
            <p className="font-mono text-slate-500 text-[11px]">
              Tagline: <span className="text-slate-300">"Don't trust the offer. Verify the evidence."</span>
            </p>
          </div>

          {/* Quick Links */}
          <div className="space-y-2">
            <h4 className="font-semibold text-slate-200 text-xs uppercase tracking-wider font-mono">
              Quick Navigation
            </h4>
            <ul className="space-y-1.5">
              <li>
                <a href="#submit" className="hover:text-blue-400 transition-colors">
                  Opportunity Intake
                </a>
              </li>
              <li>
                <a href="#how-it-works" className="hover:text-blue-400 transition-colors">
                  Verification Pipeline
                </a>
              </li>
              <li>
                <a href="#disclaimer" className="hover:text-blue-400 transition-colors">
                  Safety & Privacy
                </a>
              </li>
            </ul>
          </div>

          {/* System & Architecture Info */}
          <div className="space-y-2">
            <h4 className="font-semibold text-slate-200 text-xs uppercase tracking-wider font-mono">
              Environment & Status
            </h4>
            <div className="space-y-1 font-mono text-[11px] text-slate-400">
              <p>Phase: <span className="text-blue-400">Phase 3 Evidence Verification</span></p>
              <p>Frontend: <span className="text-slate-300">React + Vite + Tailwind</span></p>
              <p>Backend: <span className="text-slate-300">FastAPI + Python</span></p>
              {apiData?.version && (
                <p>API Version: <span className="text-emerald-400">v{apiData.version}</span></p>
              )}
            </div>
          </div>
        </div>

        <div className="pt-8 border-t border-slate-800/80 flex flex-col sm:flex-row items-center justify-between gap-4">
          <p className="text-slate-500 text-[11px]">
            &copy; {new Date().getFullYear()} OFFERPROOF. Built for Devpost Hackathon.
          </p>
          <div className="flex items-center gap-4">
            <a
              href="https://github.com/Sanjaycs096/OFFERPROOF"
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-1.5 text-slate-400 hover:text-white transition-colors"
            >
              <Github className="w-3.5 h-3.5" />
              <span>GitHub Repository</span>
            </a>
          </div>
        </div>
      </div>
    </footer>
  );
}
