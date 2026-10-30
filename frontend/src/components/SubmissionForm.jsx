import React, { useState } from 'react';
import {
  FileText,
  Link2,
  UploadCloud,
  Search,
  CheckCircle2,
  Info,
  X,
  FileCheck2,
  Sparkles,
} from 'lucide-react';

export default function SubmissionForm({ isOnline }) {
  const [description, setDescription] = useState('');
  const [opportunityUrl, setOpportunityUrl] = useState('');
  const [opportunityType, setOpportunityType] = useState('job');
  const [showStatusModal, setShowStatusModal] = useState(false);
  const [validationError, setValidationError] = useState('');

  const sampleDescriptions = {
    job: "Received an unexpected offer letter via Telegram for a 'Remote Data Analyst' position at Apex Technologies LLC. Salary offered: $65/hr without interview. Recruiter requested $150 software license fee before onboarding.",
    internship: "Summer 2026 AI Research Internship listing found on an unverified careers board. No company website domain matches the recruiter's @gmail.com contact address.",
    scholarship: "Global STEM Leadership Fellowship claiming $10,000 grant, requiring a non-refundable $75 application processing fee sent via cryptocurrency.",
  };

  const handleApplySample = (type) => {
    setOpportunityType(type);
    setDescription(sampleDescriptions[type]);
    if (type === 'job') setOpportunityUrl('https://example-unverified-career-portal.com/jobs/9843');
    if (type === 'internship') setOpportunityUrl('https://example-internships.net/apply');
    if (type === 'scholarship') setOpportunityUrl('https://stem-fellowship-grants-2026.org');
    setValidationError('');
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!description.trim() && !opportunityUrl.trim()) {
      setValidationError('Please provide either an opportunity description or a URL to submit.');
      return;
    }
    setValidationError('');
    setShowStatusModal(true);
  };

  const handleReset = () => {
    setDescription('');
    setOpportunityUrl('');
    setValidationError('');
    setShowStatusModal(false);
  };

  return (
    <section id="submit" className="py-16 bg-slate-900/40">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Section Header */}
        <div className="mb-8 text-center sm:text-left sm:flex sm:items-end sm:justify-between">
          <div>
            <span className="text-xs font-mono uppercase tracking-wider text-blue-400 font-semibold">
              Evaluation Intake
            </span>
            <h2 className="text-2xl sm:text-3xl font-bold text-white mt-1">
              Submit Opportunity for Verification
            </h2>
            <p className="text-sm text-slate-400 mt-1">
              Provide offer text, communications, or application URLs for structural evidence analysis.
            </p>
          </div>

          {/* Quick preset selector */}
          <div className="mt-4 sm:mt-0 flex items-center gap-2 text-xs">
            <span className="text-slate-400 flex items-center gap-1">
              <Sparkles className="w-3.5 h-3.5 text-blue-400" />
              Load sample:
            </span>
            <button
              type="button"
              onClick={() => handleApplySample('job')}
              className="px-2 py-1 rounded bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700 transition-colors"
            >
              Job
            </button>
            <button
              type="button"
              onClick={() => handleApplySample('internship')}
              className="px-2 py-1 rounded bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700 transition-colors"
            >
              Internship
            </button>
            <button
              type="button"
              onClick={() => handleApplySample('scholarship')}
              className="px-2 py-1 rounded bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700 transition-colors"
            >
              Scholarship
            </button>
          </div>
        </div>

        {/* Form Container */}
        <div className="rounded-2xl bg-slate-900 border border-slate-800 p-6 sm:p-8 shadow-xl">
          <form onSubmit={handleSubmit} className="space-y-6">
            {/* Category tabs */}
            <div>
              <label className="block text-xs font-mono uppercase tracking-wider text-slate-300 mb-2">
                Opportunity Category
              </label>
              <div className="grid grid-cols-3 gap-2 sm:w-80">
                {['job', 'internship', 'scholarship'].map((type) => (
                  <button
                    key={type}
                    type="button"
                    onClick={() => setOpportunityType(type)}
                    className={`py-2 px-3 text-xs font-medium rounded-lg capitalize border transition-all ${
                      opportunityType === type
                        ? 'bg-blue-600 border-blue-500 text-white shadow-sm shadow-blue-500/20'
                        : 'bg-slate-800/60 border-slate-700/80 text-slate-400 hover:text-slate-200 hover:bg-slate-800'
                    }`}
                  >
                    {type}
                  </button>
                ))}
              </div>
            </div>

            {/* Description Textarea */}
            <div>
              <div className="flex items-center justify-between mb-2">
                <label
                  htmlFor="description"
                  className="block text-xs font-mono uppercase tracking-wider text-slate-300"
                >
                  Opportunity Description / Offer Content
                </label>
                <span className="text-[11px] font-mono text-slate-500">
                  {description.length} characters
                </span>
              </div>
              <div className="relative">
                <textarea
                  id="description"
                  rows={5}
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                  placeholder="Paste the job description, recruiter email, offer message, interview request, or terms..."
                  className="w-full rounded-xl bg-slate-950/80 border border-slate-700 px-4 py-3 text-sm text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
                />
              </div>
              <p className="text-[11px] text-slate-500 mt-1">
                Tip: Include recruiter contact addresses, salary details, and any requested fees.
              </p>
            </div>

            {/* URL input */}
            <div>
              <label
                htmlFor="opportunityUrl"
                className="block text-xs font-mono uppercase tracking-wider text-slate-300 mb-2"
              >
                Opportunity / Application Link
              </label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-slate-500">
                  <Link2 className="w-4 h-4" />
                </div>
                <input
                  id="opportunityUrl"
                  type="url"
                  value={opportunityUrl}
                  onChange={(e) => setOpportunityUrl(e.target.value)}
                  placeholder="https://company.com/careers/listing-123"
                  className="w-full rounded-xl bg-slate-950/80 border border-slate-700 pl-10 pr-4 py-2.5 text-sm text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
                />
              </div>
            </div>

            {/* Document Upload Placeholder */}
            <div>
              <div className="flex items-center justify-between mb-2">
                <label className="block text-xs font-mono uppercase tracking-wider text-slate-300">
                  Offer Document / Contract (Coming in Phase 2)
                </label>
                <span className="text-[10px] uppercase font-mono px-2 py-0.5 rounded bg-slate-800 text-slate-400 border border-slate-700">
                  Phase 2 Feature
                </span>
              </div>
              <div className="rounded-xl border border-dashed border-slate-700 bg-slate-950/40 p-6 text-center hover:border-slate-600 transition-colors cursor-not-allowed">
                <div className="mx-auto w-10 h-10 rounded-full bg-slate-800/80 border border-slate-700 flex items-center justify-center text-slate-400 mb-3">
                  <UploadCloud className="w-5 h-5" />
                </div>
                <p className="text-xs font-medium text-slate-300">
                  PDF & Image Attachment Parser Placeholder
                </p>
                <p className="text-[11px] text-slate-500 mt-1">
                  Document OCR and cryptographic letterhead analysis will be activated in Phase 2.
                </p>
              </div>
            </div>

            {/* Validation alert */}
            {validationError && (
              <div className="p-3 rounded-lg bg-rose-950/50 border border-rose-500/40 text-rose-300 text-xs flex items-center gap-2">
                <Info className="w-4 h-4 shrink-0" />
                <span>{validationError}</span>
              </div>
            )}

            {/* Submit & Reset actions */}
            <div className="pt-2 flex flex-col sm:flex-row items-center gap-3">
              <button
                type="submit"
                className="w-full sm:w-auto flex-1 inline-flex items-center justify-center gap-2 px-6 py-3 rounded-xl bg-blue-600 hover:bg-blue-500 active:bg-blue-700 text-white font-semibold text-sm transition-all shadow-md shadow-blue-600/25"
              >
                <Search className="w-4 h-4" />
                <span>Analyse Opportunity</span>
              </button>

              {(description || opportunityUrl) && (
                <button
                  type="button"
                  onClick={handleReset}
                  className="w-full sm:w-auto px-4 py-3 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 text-sm font-medium border border-slate-700 transition-colors"
                >
                  Clear Fields
                </button>
              )}
            </div>
          </form>
        </div>
      </div>

      {/* Phase 1 Status / Confirmation Modal */}
      {showStatusModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-sm animate-fade-in">
          <div className="bg-slate-900 border border-slate-800 rounded-2xl max-w-lg w-full p-6 shadow-2xl relative">
            <button
              onClick={() => setShowStatusModal(false)}
              className="absolute top-4 right-4 p-1.5 text-slate-400 hover:text-white rounded-lg hover:bg-slate-800 transition-colors"
              aria-label="Close modal"
            >
              <X className="w-5 h-5" />
            </button>

            <div className="flex items-center gap-3 mb-4">
              <div className="w-10 h-10 rounded-xl bg-blue-500/10 border border-blue-500/20 text-blue-400 flex items-center justify-center">
                <FileCheck2 className="w-5 h-5" />
              </div>
              <div>
                <h3 className="text-base font-semibold text-white">
                  Intake Captured — Phase 1 Foundation
                </h3>
                <p className="text-xs text-slate-400 font-mono">
                  Category: <span className="uppercase text-blue-400">{opportunityType}</span>
                </p>
              </div>
            </div>

            <div className="space-y-3 text-xs text-slate-300 bg-slate-950/60 p-4 rounded-xl border border-slate-800 mb-5">
              <div className="flex items-start gap-2">
                <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />
                <div>
                  <span className="font-semibold text-slate-200">Form & API Pipeline Ready:</span>
                  <p className="text-slate-400 mt-0.5">
                    The UI state and client-server connectivity are active and verified.
                  </p>
                </div>
              </div>

              <div className="flex items-start gap-2">
                <Info className="w-4 h-4 text-blue-400 shrink-0 mt-0.5" />
                <div>
                  <span className="font-semibold text-slate-200">Verification Engine Scope:</span>
                  <p className="text-slate-400 mt-0.5">
                    Per Phase 1 guidelines, no simulated or placeholder fraud scores are produced. Full
                    AI extraction, entity cross-referencing, and registry auditing are scheduled for
                    Phase 2 implementation.
                  </p>
                </div>
              </div>
            </div>

            <div className="text-xs text-slate-400 mb-5">
              <span className="text-slate-300 font-medium">Submitted Content Preview:</span>
              <p className="mt-1 font-mono text-[11px] bg-slate-950 p-2.5 rounded border border-slate-800/80 truncate text-slate-300">
                {opportunityUrl ? `URL: ${opportunityUrl}` : ''}
                {opportunityUrl && description ? ' | ' : ''}
                {description ? `Text: ${description}` : ''}
              </p>
            </div>

            <div className="flex justify-end gap-2">
              <button
                type="button"
                onClick={() => setShowStatusModal(false)}
                className="px-4 py-2 rounded-lg bg-blue-600 hover:bg-blue-500 text-white text-xs font-semibold transition-colors"
              >
                Acknowledge & Close
              </button>
            </div>
          </div>
        </div>
      )}
    </section>
  );
}
