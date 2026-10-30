import React from 'react';
import Navbar from '../components/Navbar';
import Hero from '../components/Hero';
import SubmissionForm from '../components/SubmissionForm';
import HowItWorks from '../components/HowItWorks';
import Disclaimer from '../components/Disclaimer';
import Footer from '../components/Footer';
import { useHealthCheck } from '../hooks/useHealthCheck';
import { AlertCircle, Terminal } from 'lucide-react';

export default function LandingPage() {
  const healthState = useHealthCheck(15000);

  return (
    <div className="min-h-screen flex flex-col bg-slate-950 text-slate-100">
      <Navbar healthState={healthState} />

      {/* Backend connection banner if offline */}
      {!healthState.isChecking && !healthState.isOnline && (
        <div className="bg-amber-950/40 border-b border-amber-500/30 px-4 py-2 text-xs text-amber-200">
          <div className="max-w-7xl mx-auto flex flex-col sm:flex-row items-start sm:items-center justify-between gap-2">
            <div className="flex items-center gap-2">
              <AlertCircle className="w-4 h-4 text-amber-400 shrink-0" />
              <span>
                Backend API is currently offline. Start the FastAPI server on port 8000 to enable full integration.
              </span>
            </div>
            <div className="flex items-center gap-2 font-mono text-[11px] text-amber-300/80 bg-amber-950/60 px-2 py-1 rounded border border-amber-800/50">
              <Terminal className="w-3 h-3 text-amber-400" />
              <span>uvicorn app.main:app --reload</span>
            </div>
          </div>
        </div>
      )}

      <main className="flex-1">
        <Hero />
        <SubmissionForm isOnline={healthState.isOnline} />
        <HowItWorks />
        <Disclaimer />
      </main>

      <Footer apiData={healthState.data} />
    </div>
  );
}
