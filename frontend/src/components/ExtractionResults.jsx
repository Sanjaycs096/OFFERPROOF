import React, { useState } from 'react';
import {
  FileText,
  Building2,
  Briefcase,
  DollarSign,
  UserCheck,
  Calendar,
  AlertTriangle,
  CheckCircle2,
  ShieldAlert,
  Cpu,
  Sparkles,
  Copy,
  Check,
  ChevronDown,
  ChevronUp,
  FileSpreadsheet,
  CornerDownRight,
  Info,
} from 'lucide-react';

export default function ExtractionResults({ result, onReset }) {
  const [activeTab, setActiveTab] = useState('claims');
  const [showJson, setShowJson] = useState(false);
  const [copiedJson, setCopiedJson] = useState(false);

  if (!result) return null;

  const {
    extraction_mode,
    source_type,
    extracted_information = {},
    claims = [],
    suspicious_indicators = [],
    extraction_summary = {},
    url_metadata,
    errors,
  } = result;

  const {
    organisation = {},
    opportunity = {},
    financial_details = {},
    recruiter = {},
    application = {},
  } = extracted_information;

  const handleCopyJson = () => {
    navigator.clipboard.writeText(JSON.stringify(result, null, 2));
    setCopiedJson(true);
    setTimeout(() => setCopiedJson(false), 2000);
  };

  const getCategoryColor = (cat) => {
    switch (cat?.toLowerCase()) {
      case 'financial':
        return 'bg-emerald-950/80 border-emerald-500/40 text-emerald-300';
      case 'organisation':
        return 'bg-blue-950/80 border-blue-500/40 text-blue-300';
      case 'opportunity':
        return 'bg-indigo-950/80 border-indigo-500/40 text-indigo-300';
      case 'deadline':
        return 'bg-purple-950/80 border-purple-500/40 text-purple-300';
      case 'recruiter':
        return 'bg-cyan-950/80 border-cyan-500/40 text-cyan-300';
      case 'suspicious_indicator':
        return 'bg-amber-950/80 border-amber-500/40 text-amber-300';
      default:
        return 'bg-slate-800 border-slate-700 text-slate-300';
    }
  };

  return (
    <div className="mt-8 space-y-6 animate-fade-in">
      {/* Top Meta Bar */}
      <div className="rounded-2xl bg-slate-900 border border-slate-800 p-5 sm:p-6 shadow-xl">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-5 border-b border-slate-800/80">
          <div>
            <div className="flex items-center gap-3">
              <span className="text-xs font-mono uppercase tracking-wider text-blue-400 font-semibold">
                Phase 2 Ingestion Complete
              </span>

              {/* Extraction Mode Badge */}
              {extraction_mode === 'ai' ? (
                <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium bg-blue-950/80 border border-blue-500/40 text-blue-300">
                  <Sparkles className="w-3.5 h-3.5 text-blue-400" />
                  <span>AI Structured Extraction</span>
                </span>
              ) : (
                <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium bg-amber-950/80 border border-amber-500/40 text-amber-300">
                  <Cpu className="w-3.5 h-3.5 text-amber-400" />
                  <span>Rule-Based Extraction</span>
                </span>
              )}

              <span className="text-xs font-mono px-2 py-0.5 rounded bg-slate-800 text-slate-300 uppercase">
                {source_type}
              </span>
            </div>

            <h3 className="text-xl font-bold text-white mt-1">
              {opportunity.title || opportunity.role || 'Opportunity Claims & Entities'}
            </h3>
            {organisation.name && (
              <p className="text-xs text-slate-400 mt-0.5">
                Stated Entity: <span className="text-slate-200 font-medium">{organisation.name}</span>
                {url_metadata?.hostname && (
                  <span className="ml-2 font-mono text-slate-500">({url_metadata.hostname})</span>
                )}
              </p>
            )}
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={handleCopyJson}
              className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-medium border border-slate-700 transition-colors"
              title="Copy response JSON to clipboard"
            >
              {copiedJson ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
              <span>{copiedJson ? 'Copied' : 'Export JSON'}</span>
            </button>
            <button
              onClick={onReset}
              className="px-3 py-1.5 rounded-lg bg-slate-800/80 hover:bg-slate-700 text-slate-300 text-xs font-medium border border-slate-700 transition-colors"
            >
              New Input
            </button>
          </div>
        </div>

        {/* Aggregation Counters */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 pt-5">
          <div className="p-3 rounded-xl bg-slate-950/60 border border-slate-800/80">
            <span className="text-[11px] font-mono uppercase tracking-wider text-slate-400">Total Claims</span>
            <p className="text-2xl font-bold text-blue-400 mt-1">{extraction_summary.total_claims ?? claims.length}</p>
          </div>

          <div className="p-3 rounded-xl bg-slate-950/60 border border-slate-800/80">
            <span className="text-[11px] font-mono uppercase tracking-wider text-slate-400">Entities Detected</span>
            <p className="text-2xl font-bold text-white mt-1">{extraction_summary.total_entities ?? 0}</p>
          </div>

          <div className="p-3 rounded-xl bg-slate-950/60 border border-slate-800/80">
            <span className="text-[11px] font-mono uppercase tracking-wider text-slate-400">Language Indicators</span>
            <p className="text-2xl font-bold text-amber-400 mt-1">
              {extraction_summary.detected_indicators ?? suspicious_indicators.length}
            </p>
          </div>

          <div className="p-3 rounded-xl bg-slate-950/60 border border-slate-800/80">
            <span className="text-[11px] font-mono uppercase tracking-wider text-slate-400">Verification Status</span>
            <div className="flex items-center gap-1.5 mt-2">
              <span className="h-2 w-2 rounded-full bg-slate-400"></span>
              <span className="text-xs font-mono font-semibold text-slate-300 uppercase">NOT CHECKED</span>
            </div>
          </div>
        </div>

        {/* Non-fatal error notice if fallback was triggered */}
        {errors && errors.length > 0 && (
          <div className="mt-4 p-3 rounded-xl bg-amber-950/40 border border-amber-500/30 text-amber-300 text-xs flex items-center gap-2">
            <Info className="w-4 h-4 text-amber-400 shrink-0" />
            <span>{errors[0]}</span>
          </div>
        )}
      </div>

      {/* Tabs */}
      <div className="flex items-center gap-2 border-b border-slate-800 pb-2">
        <button
          onClick={() => setActiveTab('claims')}
          className={`px-4 py-2 text-xs font-semibold rounded-lg transition-all ${
            activeTab === 'claims'
              ? 'bg-blue-600 text-white shadow-sm shadow-blue-500/20'
              : 'text-slate-400 hover:text-slate-200 hover:bg-slate-900'
          }`}
        >
          Extracted Claims ({claims.length})
        </button>

        <button
          onClick={() => setActiveTab('entities')}
          className={`px-4 py-2 text-xs font-semibold rounded-lg transition-all ${
            activeTab === 'entities'
              ? 'bg-blue-600 text-white shadow-sm shadow-blue-500/20'
              : 'text-slate-400 hover:text-slate-200 hover:bg-slate-900'
          }`}
        >
          Entity Breakdown
        </button>

        <button
          onClick={() => setActiveTab('indicators')}
          className={`px-4 py-2 text-xs font-semibold rounded-lg transition-all ${
            activeTab === 'indicators'
              ? 'bg-blue-600 text-white shadow-sm shadow-blue-500/20'
              : 'text-slate-400 hover:text-slate-200 hover:bg-slate-900'
          }`}
        >
          Language Indicators ({suspicious_indicators.length})
        </button>
      </div>

      {/* Tab 1: Claims List */}
      {activeTab === 'claims' && (
        <div className="space-y-3">
          <div className="p-3.5 rounded-xl bg-slate-900/60 border border-slate-800 text-xs text-slate-400 flex items-start gap-2.5">
            <Info className="w-4 h-4 text-blue-400 shrink-0 mt-0.5" />
            <span>
              Each item represents an isolated factual claim made in the submitted document. At this ingestion
              stage, every claim is marked <strong className="text-slate-200">not_checked</strong>. Independent
              evidence corroboration will be conducted in Phase 3.
            </span>
          </div>

          {claims.length === 0 ? (
            <div className="p-8 text-center text-slate-500 text-xs bg-slate-900/40 rounded-xl border border-slate-800">
              No distinct claims could be isolated from the submitted content.
            </div>
          ) : (
            claims.map((claim) => (
              <div
                key={claim.claim_id}
                className="p-5 rounded-xl bg-slate-900 border border-slate-800 hover:border-slate-700 transition-colors"
              >
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 mb-3">
                  <div className="flex items-center gap-2">
                    <span className="font-mono text-xs font-bold text-blue-400 px-2 py-0.5 rounded bg-blue-950 border border-blue-800/60">
                      {claim.claim_id}
                    </span>
                    <span className={`px-2 py-0.5 text-[11px] font-mono capitalize rounded border ${getCategoryColor(claim.claim_category)}`}>
                      {claim.claim_category}
                    </span>
                    {claim.extracted_value && (
                      <span className="text-[11px] font-mono text-slate-300 bg-slate-950 px-2 py-0.5 rounded border border-slate-800">
                        Value: {claim.extracted_value}
                      </span>
                    )}
                  </div>

                  <div className="flex items-center gap-2">
                    <span className="text-[11px] font-mono text-slate-500">
                      Confidence: {Math.round(claim.confidence * 100)}%
                    </span>
                    <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-slate-800 text-slate-300 border border-slate-700">
                      <span className="h-1.5 w-1.5 rounded-full bg-slate-400"></span>
                      NOT CHECKED
                    </span>
                  </div>
                </div>

                <p className="text-sm font-medium text-slate-100 mb-2.5">
                  {claim.claim_text}
                </p>

                {claim.source_text && (
                  <div className="bg-slate-950/70 p-2.5 rounded-lg border border-slate-800/80 text-xs text-slate-400 font-mono flex items-start gap-2">
                    <CornerDownRight className="w-3.5 h-3.5 text-blue-400 shrink-0 mt-0.5" />
                    <span className="italic truncate">"{claim.source_text}"</span>
                  </div>
                )}
              </div>
            ))
          )}
        </div>
      )}

      {/* Tab 2: Entity Cards */}
      {activeTab === 'entities' && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {/* Organisation Card */}
          <div className="p-5 rounded-xl bg-slate-900 border border-slate-800 space-y-3">
            <div className="flex items-center gap-2.5 pb-2 border-b border-slate-800 text-white font-semibold text-sm">
              <Building2 className="w-4 h-4 text-blue-400" />
              <span>Organisation Claims</span>
            </div>
            <div className="space-y-2 text-xs">
              <div className="flex justify-between">
                <span className="text-slate-400">Entity Name:</span>
                <span className="text-slate-100 font-medium">{organisation.name || 'Not stated'}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-400">Official Website:</span>
                <span className="text-slate-100 font-mono">{organisation.website || 'Not stated'}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-400">Entity Type:</span>
                <span className="text-slate-100 capitalize">{organisation.organisation_type || 'Unspecified'}</span>
              </div>
            </div>
          </div>

          {/* Opportunity Details */}
          <div className="p-5 rounded-xl bg-slate-900 border border-slate-800 space-y-3">
            <div className="flex items-center gap-2.5 pb-2 border-b border-slate-800 text-white font-semibold text-sm">
              <Briefcase className="w-4 h-4 text-blue-400" />
              <span>Opportunity Specifics</span>
            </div>
            <div className="space-y-2 text-xs">
              <div className="flex justify-between">
                <span className="text-slate-400">Title / Role:</span>
                <span className="text-slate-100 font-medium">{opportunity.role || opportunity.title || 'Not stated'}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-400">Category:</span>
                <span className="text-slate-100 capitalize">{opportunity.category || 'job'}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-400">Work Setup:</span>
                <span className="text-slate-100 capitalize">{opportunity.work_arrangement || 'Not specified'}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-400">Location:</span>
                <span className="text-slate-100">{opportunity.location || 'Not specified'}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-400">Deadline:</span>
                <span className="text-slate-100 font-medium">{opportunity.application_deadline || 'Not stated'}</span>
              </div>
            </div>
          </div>

          {/* Financial Card */}
          <div className="p-5 rounded-xl bg-slate-900 border border-slate-800 space-y-3">
            <div className="flex items-center gap-2.5 pb-2 border-b border-slate-800 text-white font-semibold text-sm">
              <DollarSign className="w-4 h-4 text-emerald-400" />
              <span>Financial Claims</span>
            </div>
            <div className="space-y-2 text-xs">
              <div className="flex justify-between">
                <span className="text-slate-400">Stipend:</span>
                <span className="text-emerald-400 font-semibold">{financial_details.stipend || 'None stated'}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-400">Salary / Compensation:</span>
                <span className="text-emerald-400 font-semibold">{financial_details.salary || 'None stated'}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-400">Registration Fees:</span>
                <span className="text-rose-400 font-semibold">{financial_details.registration_fees || 'None stated'}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-400">Training / Other Fees:</span>
                <span className="text-slate-200">
                  {financial_details.training_fees || financial_details.processing_fees || 'None stated'}
                </span>
              </div>
            </div>
          </div>

          {/* Recruiter & Contact Card */}
          <div className="p-5 rounded-xl bg-slate-900 border border-slate-800 space-y-3">
            <div className="flex items-center gap-2.5 pb-2 border-b border-slate-800 text-white font-semibold text-sm">
              <UserCheck className="w-4 h-4 text-cyan-400" />
              <span>Recruiter & Contact Details</span>
            </div>
            <div className="space-y-2 text-xs">
              <div className="flex justify-between">
                <span className="text-slate-400">Contact Person:</span>
                <span className="text-slate-100">{recruiter.name || 'Not stated'}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-400">Email Address:</span>
                <span className="text-slate-100 font-mono">{recruiter.email || 'None stated'}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-400">Phone / WhatsApp:</span>
                <span className="text-slate-100 font-mono">{recruiter.phone || 'None stated'}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-400">Messaging Handle:</span>
                <span className="text-slate-100 font-mono">{recruiter.contact_info || 'None stated'}</span>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Tab 3: Suspicious Indicators */}
      {activeTab === 'indicators' && (
        <div className="space-y-4">
          <div className="p-4 rounded-xl bg-amber-950/30 border border-amber-500/30 text-xs text-amber-200 flex items-start gap-3">
            <ShieldAlert className="w-5 h-5 text-amber-400 shrink-0 mt-0.5" />
            <div>
              <p className="font-semibold text-amber-300">Phase 2 Language Observation</p>
              <p className="mt-1 text-slate-300 leading-relaxed">
                The indicators below identify linguistic patterns commonly associated with recruitment
                abuses (e.g., upfront payment demands, unauthenticated channels, artificial urgency).
                Per Phase 2 guidelines, these statements are extracted as evidence objects and do
                NOT conclude that the opportunity is fraudulent.
              </p>
            </div>
          </div>

          {suspicious_indicators.length === 0 ? (
            <div className="p-8 text-center text-slate-400 text-xs bg-slate-900/40 rounded-xl border border-slate-800 flex items-center justify-center gap-2">
              <CheckCircle2 className="w-4 h-4 text-emerald-400" />
              <span>No obvious suspicious language indicators or upfront fee patterns were detected in the text.</span>
            </div>
          ) : (
            suspicious_indicators.map((ind, idx) => (
              <div
                key={idx}
                className="p-4 rounded-xl bg-slate-900 border border-amber-500/30 space-y-2"
              >
                <div className="flex items-center justify-between">
                  <span className="text-xs font-mono font-bold uppercase text-amber-400 px-2 py-0.5 rounded bg-amber-950/80 border border-amber-700/50">
                    {ind.indicator_type.replace(/_/g, ' ')}
                  </span>
                </div>
                <p className="text-sm font-semibold text-white">
                  "{ind.statement}"
                </p>
                <p className="text-xs text-slate-400 leading-relaxed">
                  {ind.description}
                </p>
                {ind.source_quote && (
                  <p className="text-[11px] font-mono text-slate-400 bg-slate-950 p-2 rounded border border-slate-800">
                    Source quote: "{ind.source_quote}"
                  </p>
                )}
              </div>
            ))
          )}
        </div>
      )}

      {/* Expandable JSON Inspector */}
      <div className="pt-2">
        <button
          onClick={() => setShowJson(!showJson)}
          className="flex items-center gap-2 text-xs font-mono text-slate-400 hover:text-slate-200 transition-colors"
        >
          {showJson ? <ChevronUp className="w-3.5 h-3.5" /> : <ChevronDown className="w-3.5 h-3.5" />}
          <span>{showJson ? 'Hide' : 'Inspect'} Raw Extraction Payload (JSON)</span>
        </button>

        {showJson && (
          <div className="mt-3 p-4 rounded-xl bg-slate-950 border border-slate-800 font-mono text-[11px] text-slate-300 overflow-x-auto max-h-96">
            <pre>{JSON.stringify(result, null, 2)}</pre>
          </div>
        )}
      </div>
    </div>
  );
}
