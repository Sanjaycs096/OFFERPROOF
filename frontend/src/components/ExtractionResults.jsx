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
  ShieldCheck,
  Cpu,
  Sparkles,
  Copy,
  Check,
  ChevronDown,
  ChevronUp,
  ExternalLink,
  CornerDownRight,
  Info,
  Globe,
  Server,
  Mail,
  Link2,
  HelpCircle,
  XCircle,
} from 'lucide-react';

export default function ExtractionResults({ result, onReset }) {
  const [activeTab, setActiveTab] = useState('claims');
  const [showJson, setShowJson] = useState(false);
  const [copiedJson, setCopiedJson] = useState(false);
  const [selectedEvidenceId, setSelectedEvidenceId] = useState(null);

  if (!result) return null;

  const {
    extraction_mode = 'rule_based',
    source_type = 'text',
    extracted_information = {},
    claims = [],
    suspicious_indicators = [],
    extraction_summary = {},
    verification_summary = {},
    evidence = [],
    technical_observations = [],
    limitations = [],
    url_metadata,
    errors,
  } = result;

  const {
    organisation = {},
    opportunity = {},
    financial_details = {},
    recruiter = {},
  } = extracted_information;

  const handleCopyJson = () => {
    navigator.clipboard.writeText(JSON.stringify(result, null, 2));
    setCopiedJson(true);
    setTimeout(() => setCopiedJson(false), 2000);
  };

  const getVerificationStatusBadge = (status) => {
    switch (status?.toLowerCase()) {
      case 'supported':
        return {
          bg: 'bg-emerald-950/80 border-emerald-500/50 text-emerald-300',
          dot: 'bg-emerald-400',
          label: 'SUPPORTED',
          icon: CheckCircle2,
        };
      case 'contradicted':
        return {
          bg: 'bg-rose-950/80 border-rose-500/50 text-rose-300',
          dot: 'bg-rose-400',
          label: 'CONTRADICTED',
          icon: XCircle,
        };
      case 'inconclusive':
        return {
          bg: 'bg-amber-950/80 border-amber-500/50 text-amber-300',
          dot: 'bg-amber-400',
          label: 'INCONCLUSIVE',
          icon: AlertTriangle,
        };
      case 'not_checked':
      default:
        return {
          bg: 'bg-slate-800/90 border-slate-700 text-slate-300',
          dot: 'bg-slate-400',
          label: 'NOT CHECKED',
          icon: HelpCircle,
        };
    }
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

  const getEvidenceStatusPill = (status) => {
    switch (status?.toLowerCase()) {
      case 'available':
        return 'bg-emerald-950/80 border-emerald-500/40 text-emerald-300';
      case 'not_available':
        return 'bg-slate-800 border-slate-700 text-slate-400';
      case 'error':
        return 'bg-rose-950/80 border-rose-500/40 text-rose-300';
      case 'not_applicable':
      default:
        return 'bg-slate-900 border-slate-800 text-slate-500';
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
                Phase 3 Evidence Analysis
              </span>

              {extraction_mode === 'ai' ? (
                <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium bg-blue-950/80 border border-blue-500/40 text-blue-300">
                  <Sparkles className="w-3.5 h-3.5 text-blue-400" />
                  <span>AI Claim Extraction</span>
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
              {opportunity.title || opportunity.role || 'Opportunity Claims & Technical Evidence'}
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
              title="Copy verification response JSON to clipboard"
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

        {/* Verification Summary Chips */}
        <div className="grid grid-cols-2 sm:grid-cols-5 gap-3 pt-5">
          <div className="p-3 rounded-xl bg-slate-950/60 border border-slate-800/80">
            <span className="text-[11px] font-mono uppercase tracking-wider text-slate-400">Total Claims</span>
            <p className="text-2xl font-bold text-white mt-1">{verification_summary.total_claims ?? claims.length}</p>
          </div>

          <div className="p-3 rounded-xl bg-slate-950/60 border border-emerald-900/30">
            <span className="text-[11px] font-mono uppercase tracking-wider text-emerald-400">Supported</span>
            <p className="text-2xl font-bold text-emerald-400 mt-1">{verification_summary.supported ?? 0}</p>
          </div>

          <div className="p-3 rounded-xl bg-slate-950/60 border border-amber-900/30">
            <span className="text-[11px] font-mono uppercase tracking-wider text-amber-400">Inconclusive</span>
            <p className="text-2xl font-bold text-amber-400 mt-1">{verification_summary.inconclusive ?? 0}</p>
          </div>

          <div className="p-3 rounded-xl bg-slate-950/60 border border-slate-800/80">
            <span className="text-[11px] font-mono uppercase tracking-wider text-slate-400">Not Checked</span>
            <p className="text-2xl font-bold text-slate-300 mt-1">{verification_summary.not_checked ?? 0}</p>
          </div>

          <div className="p-3 rounded-xl bg-slate-950/60 border border-blue-900/30 col-span-2 sm:col-span-1">
            <span className="text-[11px] font-mono uppercase tracking-wider text-blue-400">Evidence Items</span>
            <p className="text-2xl font-bold text-blue-400 mt-1">{verification_summary.evidence_items ?? evidence.length}</p>
          </div>
        </div>

        {/* Global Principle Banner */}
        <div className="mt-5 p-3.5 rounded-xl bg-blue-950/30 border border-blue-500/30 text-xs text-blue-200 flex items-start gap-3">
          <Info className="w-4 h-4 text-blue-400 shrink-0 mt-0.5" />
          <div className="leading-relaxed">
            <strong className="text-blue-300">Evidence-Grounding Principle: </strong>
            These checks evaluate available technical evidence (RDAP domain registration, DNS routing, and recruiter email consistency).
            Technical connectivity does not establish whether an opportunity or recruiter is genuine. Financial claims and job offerings remain strictly <code className="px-1 py-0.5 bg-slate-900 text-slate-300 rounded font-mono">not_checked</code>.
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex items-center gap-2 border-b border-slate-800 pb-2 overflow-x-auto">
        <button
          onClick={() => setActiveTab('claims')}
          className={`px-4 py-2 text-xs font-semibold rounded-lg transition-all shrink-0 ${
            activeTab === 'claims'
              ? 'bg-blue-600 text-white shadow-sm shadow-blue-500/20'
              : 'text-slate-400 hover:text-slate-200 hover:bg-slate-900'
          }`}
        >
          Claims & Verification ({claims.length})
        </button>

        <button
          onClick={() => setActiveTab('evidence')}
          className={`px-4 py-2 text-xs font-semibold rounded-lg transition-all shrink-0 ${
            activeTab === 'evidence'
              ? 'bg-blue-600 text-white shadow-sm shadow-blue-500/20'
              : 'text-slate-400 hover:text-slate-200 hover:bg-slate-900'
          }`}
        >
          Evidence Intelligence ({evidence.length})
        </button>

        <button
          onClick={() => setActiveTab('observations')}
          className={`px-4 py-2 text-xs font-semibold rounded-lg transition-all shrink-0 ${
            activeTab === 'observations'
              ? 'bg-blue-600 text-white shadow-sm shadow-blue-500/20'
              : 'text-slate-400 hover:text-slate-200 hover:bg-slate-900'
          }`}
        >
          Technical Observations ({technical_observations.length})
        </button>

        <button
          onClick={() => setActiveTab('entities')}
          className={`px-4 py-2 text-xs font-semibold rounded-lg transition-all shrink-0 ${
            activeTab === 'entities'
              ? 'bg-blue-600 text-white shadow-sm shadow-blue-500/20'
              : 'text-slate-400 hover:text-slate-200 hover:bg-slate-900'
          }`}
        >
          Entity Breakdown
        </button>

        <button
          onClick={() => setActiveTab('indicators')}
          className={`px-4 py-2 text-xs font-semibold rounded-lg transition-all shrink-0 ${
            activeTab === 'indicators'
              ? 'bg-blue-600 text-white shadow-sm shadow-blue-500/20'
              : 'text-slate-400 hover:text-slate-200 hover:bg-slate-900'
          }`}
        >
          Linguistic Indicators ({suspicious_indicators.length})
        </button>
      </div>

      {/* Tab 1: Claims List with Verification Statuses */}
      {activeTab === 'claims' && (
        <div className="space-y-4">
          {claims.length === 0 ? (
            <div className="p-8 text-center text-slate-500 text-xs bg-slate-900/40 rounded-xl border border-slate-800">
              No claims evaluated.
            </div>
          ) : (
            claims.map((claim) => {
              const statusBadge = getVerificationStatusBadge(claim.verification_status);
              const StatusIcon = statusBadge.icon;

              return (
                <div
                  key={claim.claim_id}
                  className="p-5 rounded-xl bg-slate-900 border border-slate-800 hover:border-slate-700 transition-colors space-y-3"
                >
                  <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
                    <div className="flex items-center gap-2 flex-wrap">
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
                      <span className={`inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded text-[11px] font-mono font-bold border ${statusBadge.bg}`}>
                        <span className={`h-1.5 w-1.5 rounded-full ${statusBadge.dot}`}></span>
                        <span>{statusBadge.label}</span>
                      </span>
                    </div>
                  </div>

                  {/* Claim Text */}
                  <p className="text-sm font-medium text-slate-100">
                    {claim.claim_text}
                  </p>

                  {/* Verbatim quote */}
                  {claim.source_text && (
                    <div className="bg-slate-950/70 p-2.5 rounded-lg border border-slate-800/80 text-xs text-slate-400 font-mono flex items-start gap-2">
                      <CornerDownRight className="w-3.5 h-3.5 text-blue-400 shrink-0 mt-0.5" />
                      <span className="italic truncate">"{claim.source_text}"</span>
                    </div>
                  )}

                  {/* Verification Explanation */}
                  {claim.verification_explanation && (
                    <div className="p-3 rounded-lg bg-slate-950/80 border border-slate-800/90 text-xs text-slate-300 flex items-start gap-2.5">
                      <Info className="w-4 h-4 text-blue-400 shrink-0 mt-0.5" />
                      <div>
                        <span className="font-semibold text-slate-200">Evidence Basis: </span>
                        <span>{claim.verification_explanation}</span>
                      </div>
                    </div>
                  )}

                  {/* Linked Evidence Chips */}
                  {claim.evidence_ids && claim.evidence_ids.length > 0 && (
                    <div className="flex items-center gap-2 pt-1 text-xs text-slate-400">
                      <span className="font-mono text-[11px] text-slate-500">Linked Evidence:</span>
                      {claim.evidence_ids.map((eid) => (
                        <button
                          key={eid}
                          onClick={() => {
                            setSelectedEvidenceId(eid);
                            setActiveTab('evidence');
                          }}
                          className="px-2 py-0.5 rounded text-[11px] font-mono bg-blue-950/80 text-blue-300 border border-blue-800 hover:bg-blue-900 transition-colors"
                        >
                          {eid}
                        </button>
                      ))}
                    </div>
                  )}
                </div>
              );
            })
          )}
        </div>
      )}

      {/* Tab 2: Evidence Intelligence List */}
      {activeTab === 'evidence' && (
        <div className="space-y-4">
          <div className="p-3.5 rounded-xl bg-slate-900/60 border border-slate-800 text-xs text-slate-400 flex items-start gap-2.5">
            <Info className="w-4 h-4 text-blue-400 shrink-0 mt-0.5" />
            <span>
              Independent evidence artifacts collected from trusted public registries (RDAP, DNS-over-HTTPS, structural URL inspection).
              Every item records its specific source, timestamp, and explicit limitations.
            </span>
          </div>

          {evidence.length === 0 ? (
            <div className="p-8 text-center text-slate-500 text-xs bg-slate-900/40 rounded-xl border border-slate-800">
              No evidence artifacts collected.
            </div>
          ) : (
            evidence.map((ev) => {
              const isSelected = selectedEvidenceId === ev.evidence_id;

              return (
                <div
                  key={ev.evidence_id}
                  className={`p-5 rounded-xl bg-slate-900 border transition-all space-y-3 ${
                    isSelected ? 'border-blue-500 shadow-md shadow-blue-500/10' : 'border-slate-800 hover:border-slate-700'
                  }`}
                >
                  <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
                    <div className="flex items-center gap-2 flex-wrap">
                      <span className="font-mono text-xs font-bold text-blue-400 px-2 py-0.5 rounded bg-blue-950 border border-blue-800">
                        {ev.evidence_id}
                      </span>
                      <span className="px-2 py-0.5 text-[11px] font-mono uppercase rounded bg-slate-800 text-slate-300 border border-slate-700">
                        {ev.evidence_type.replace(/_/g, ' ')}
                      </span>
                      <span className={`px-2 py-0.5 text-[11px] font-mono uppercase rounded border ${getEvidenceStatusPill(ev.status)}`}>
                        {ev.status}
                      </span>
                    </div>

                    <div className="text-[11px] font-mono text-slate-500">
                      Retrieved: {new Date(ev.retrieved_at).toLocaleString()}
                    </div>
                  </div>

                  {/* Primary Observation Value */}
                  <div>
                    <h4 className="text-sm font-semibold text-white">
                      {ev.observed_value}
                    </h4>
                    <p className="text-xs text-slate-300 leading-relaxed mt-1">
                      {ev.interpretation}
                    </p>
                  </div>

                  {/* Source details */}
                  <div className="flex items-center gap-4 text-xs font-mono text-slate-400 pt-2 border-t border-slate-800/80">
                    <span>Source: <strong className="text-slate-200">{ev.source_name}</strong></span>
                    {ev.source_url && (
                      <span className="truncate max-w-xs text-slate-500">
                        URL: {ev.source_url}
                      </span>
                    )}
                  </div>

                  {/* Limitations */}
                  {ev.limitations && ev.limitations.length > 0 && (
                    <div className="pt-2 text-[11px] text-slate-400 bg-slate-950/60 p-3 rounded-lg border border-slate-800/80 space-y-1">
                      <span className="font-semibold text-slate-300 block">Check Limitations:</span>
                      {ev.limitations.map((lim, idx) => (
                        <p key={idx} className="flex items-start gap-1.5 text-slate-400">
                          <span className="text-amber-400 shrink-0">&bull;</span>
                          <span>{lim}</span>
                        </p>
                      ))}
                    </div>
                  )}
                </div>
              );
            })
          )}
        </div>
      )}

      {/* Tab 3: Technical Observations */}
      {activeTab === 'observations' && (
        <div className="space-y-4">
          <div className="p-3.5 rounded-xl bg-slate-900/60 border border-slate-800 text-xs text-slate-400 flex items-start gap-2.5">
            <Info className="w-4 h-4 text-blue-400 shrink-0 mt-0.5" />
            <span>
              Categorized technical signals extracted from domain registries, DNS configuration, and email routing.
              Observations highlight objective findings without computing speculative fraud scores.
            </span>
          </div>

          {technical_observations.length === 0 ? (
            <div className="p-8 text-center text-slate-500 text-xs bg-slate-900/40 rounded-xl border border-slate-800">
              No technical observations recorded.
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {technical_observations.map((obs) => {
                const isNotable = obs.severity === 'notable';
                return (
                  <div
                    key={obs.observation_id}
                    className={`p-4 rounded-xl bg-slate-900 border space-y-2 ${
                      isNotable ? 'border-amber-500/40' : 'border-slate-800'
                    }`}
                  >
                    <div className="flex items-center justify-between">
                      <span className="text-[11px] font-mono uppercase tracking-wider text-slate-400">
                        {obs.category}
                      </span>
                      <span className={`text-[10px] font-mono uppercase px-2 py-0.5 rounded font-bold border ${
                        isNotable
                          ? 'bg-amber-950 text-amber-300 border-amber-800'
                          : 'bg-slate-800 text-slate-300 border-slate-700'
                      }`}>
                        {obs.finding}
                      </span>
                    </div>

                    <h4 className="text-sm font-semibold text-white">{obs.label}</h4>
                    <p className="text-xs text-slate-300 leading-relaxed">{obs.detail}</p>
                  </div>
                );
              })}
            </div>
          )}
        </div>
      )}

      {/* Tab 4: Entity Profile */}
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
            </div>
          </div>
        </div>
      )}

      {/* Tab 5: Linguistic Indicators */}
      {activeTab === 'indicators' && (
        <div className="space-y-4">
          <div className="p-4 rounded-xl bg-amber-950/30 border border-amber-500/30 text-xs text-amber-200 flex items-start gap-3">
            <ShieldAlert className="w-5 h-5 text-amber-400 shrink-0 mt-0.5" />
            <div>
              <p className="font-semibold text-amber-300">Phase 3 Observational Standard</p>
              <p className="mt-1 text-slate-300 leading-relaxed">
                Extracted linguistic indicators highlight high-risk phrasing commonly associated with recruitment
                fraud (e.g. upfront fee demands, guaranteed selection, artificial urgency). Per Phase 3 guidelines,
                these indicators are observational evidence and do NOT constitute proof of fraud.
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
          <span>{showJson ? 'Hide' : 'Inspect'} Raw Verification Payload (JSON)</span>
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
