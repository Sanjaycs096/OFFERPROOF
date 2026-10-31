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
  Printer,
  ListChecks,
  Lock,
  ArrowRight,
  X,
} from 'lucide-react';

export default function ExtractionResults({ result, onReset }) {
  const [activeTab, setActiveTab] = useState('assessment');
  const [showJson, setShowJson] = useState(false);
  const [copiedJson, setCopiedJson] = useState(false);
  const [selectedEvidenceId, setSelectedEvidenceId] = useState(null);
  const [showPrintModal, setShowPrintModal] = useState(false);
  const [showLimitations, setShowLimitations] = useState(false);

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
    assessment,
    findings = [],
    recommendations = [],
    verified_facts = [],
    unverified_claims = [],
    next_steps = [],
    errors,
  } = result;

  const {
    organisation = {},
    opportunity = {},
    financial_details = {},
    recruiter = {},
  } = extracted_information;

  // Report Identifier and Analysis Timestamp
  const reportDate = new Date().toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  });
  const reportTime = new Date().toLocaleTimeString('en-US', {
    hour: '2-digit',
    minute: '2-digit',
  });
  const reportId = `OP-RPT-${Math.abs(
    (claims.length * 31 + findings.length * 17 + (organisation?.name?.length || 0)) % 100000
  ).toString().padStart(5, '0')}`;

  const handleCopyJson = () => {
    navigator.clipboard.writeText(JSON.stringify(result, null, 2));
    setCopiedJson(true);
    setTimeout(() => setCopiedJson(false), 2000);
  };

  const handlePrint = () => {
    window.print();
  };

  const getAssessmentTheme = (level) => {
    switch (level?.toLowerCase()) {
      case 'high_caution':
        return {
          bg: 'bg-rose-950/40 border-rose-500/50',
          badgeBg: 'bg-rose-950 border-rose-600 text-rose-300',
          titleColor: 'text-rose-400',
          accentText: 'text-rose-300',
          icon: ShieldAlert,
          label: 'HIGH CAUTION',
        };
      case 'needs_careful_review':
        return {
          bg: 'bg-amber-950/40 border-amber-500/50',
          badgeBg: 'bg-amber-950 border-amber-600 text-amber-300',
          titleColor: 'text-amber-400',
          accentText: 'text-amber-300',
          icon: AlertTriangle,
          label: 'NEEDS CAREFUL REVIEW',
        };
      case 'limited_concerns_detected':
        return {
          bg: 'bg-emerald-950/40 border-emerald-500/50',
          badgeBg: 'bg-emerald-950 border-emerald-600 text-emerald-300',
          titleColor: 'text-emerald-400',
          accentText: 'text-emerald-300',
          icon: ShieldCheck,
          label: 'LIMITED CONCERNS DETECTED',
        };
      case 'insufficient_evidence':
      default:
        return {
          bg: 'bg-slate-900/90 border-slate-700',
          badgeBg: 'bg-slate-800 border-slate-600 text-slate-300',
          titleColor: 'text-slate-300',
          accentText: 'text-slate-400',
          icon: HelpCircle,
          label: 'INSUFFICIENT EVIDENCE',
        };
    }
  };

  const getSeverityBadge = (severity) => {
    switch (severity?.toLowerCase()) {
      case 'high_caution':
        return {
          bg: 'bg-rose-950/90 border-rose-500/60 text-rose-300',
          dot: 'bg-rose-400',
          label: 'HIGH CAUTION',
        };
      case 'caution':
        return {
          bg: 'bg-amber-950/90 border-amber-500/60 text-amber-300',
          dot: 'bg-amber-400',
          label: 'CAUTION',
        };
      case 'informational':
      default:
        return {
          bg: 'bg-blue-950/90 border-blue-500/60 text-blue-300',
          dot: 'bg-blue-400',
          label: 'INFORMATIONAL',
        };
    }
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
      case 'organisation':
        return 'text-blue-400 bg-blue-950/60 border-blue-800/60';
      case 'financial':
        return 'text-emerald-400 bg-emerald-950/60 border-emerald-800/60';
      case 'recruiter':
        return 'text-cyan-400 bg-cyan-950/60 border-cyan-800/60';
      case 'application':
        return 'text-purple-400 bg-purple-950/60 border-purple-800/60';
      case 'opportunity':
        return 'text-indigo-400 bg-indigo-950/60 border-indigo-800/60';
      case 'suspicious_indicator':
        return 'text-rose-400 bg-rose-950/60 border-rose-800/60';
      default:
        return 'text-slate-400 bg-slate-800 border-slate-700';
    }
  };

  const getEvidenceStatusPill = (status) => {
    switch (status?.toLowerCase()) {
      case 'available':
        return 'bg-emerald-950/80 border-emerald-500/40 text-emerald-300';
      case 'unavailable':
        return 'bg-slate-800 border-slate-700 text-slate-400';
      case 'rate_limited':
      case 'error':
        return 'bg-amber-950/80 border-amber-500/40 text-amber-300';
      default:
        return 'bg-slate-800 border-slate-700 text-slate-300';
    }
  };

  const assessmentTheme = getAssessmentTheme(assessment?.assessment_level);
  const AssessmentIcon = assessmentTheme.icon;

  return (
    <div className="space-y-6 animate-fadeIn">
      {/* ------------------------------------------------------------- */}
      {/* PROMINENT OPPORTUNITY ASSESSMENT HERO SECTION                 */}
      {/* ------------------------------------------------------------- */}
      <div className={`p-6 rounded-2xl border ${assessmentTheme.bg} transition-all shadow-lg`}>
        <div className="flex flex-col lg:flex-row lg:items-start justify-between gap-4">
          <div className="space-y-2 max-w-3xl">
            <div className="flex items-center gap-2 flex-wrap">
              <span className={`inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-mono font-bold uppercase tracking-wider border ${assessmentTheme.badgeBg}`}>
                <AssessmentIcon className="w-3.5 h-3.5" />
                <span>{assessment?.assessment_label || assessmentTheme.label}</span>
              </span>

              <span className="text-xs font-mono px-2 py-0.5 rounded bg-slate-800 text-slate-300 uppercase">
                {source_type}
              </span>

              <span className="text-xs font-mono text-slate-500">
                Report ID: <strong className="text-slate-400">{reportId}</strong>
              </span>
            </div>

            <h3 className="text-2xl font-bold text-white tracking-tight">
              {opportunity.title || opportunity.role || 'Evaluated Opportunity Assessment'}
            </h3>

            {organisation.name && (
              <p className="text-xs text-slate-400">
                Stated Organisation: <span className="text-slate-200 font-semibold">{organisation.name}</span>
                {organisation.website && (
                  <span className="ml-2 font-mono text-blue-400">({organisation.website})</span>
                )}
              </p>
            )}

            {/* Assessment Summary */}
            <p className="text-sm text-slate-200 leading-relaxed pt-1">
              {assessment?.summary ||
                'Technical checks were conducted across domain registries, DNS configuration, and recruiter email routing.'}
            </p>
          </div>

          {/* Action buttons */}
          <div className="flex items-center gap-2 shrink-0 pt-2 lg:pt-0">
            <button
              onClick={() => setShowPrintModal(true)}
              className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-blue-600 hover:bg-blue-500 text-white text-xs font-semibold shadow-sm transition-colors"
              title="Print or export clean verification report"
            >
              <Printer className="w-3.5 h-3.5" />
              <span>Print / Save PDF</span>
            </button>

            <button
              onClick={handleCopyJson}
              className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-medium border border-slate-700 transition-colors"
              title="Copy verification response JSON to clipboard"
            >
              {copiedJson ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
              <span>{copiedJson ? 'Copied' : 'JSON'}</span>
            </button>

            <button
              onClick={onReset}
              className="px-3 py-1.5 rounded-lg bg-slate-800/80 hover:bg-slate-700 text-slate-300 text-xs font-medium border border-slate-700 transition-colors"
            >
              New Input
            </button>
          </div>
        </div>

        {/* Metric Overview Counters */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 pt-6 border-t border-slate-800/80 mt-5">
          <div className="p-3 rounded-xl bg-slate-950/70 border border-slate-800/80">
            <span className="text-[11px] font-mono uppercase tracking-wider text-slate-400 block">Assessment Level</span>
            <p className={`text-base font-bold mt-1 uppercase ${assessmentTheme.accentText}`}>
              {assessment?.assessment_label || assessmentTheme.label}
            </p>
          </div>

          <div className="p-3 rounded-xl bg-slate-950/70 border border-slate-800/80">
            <span className="text-[11px] font-mono uppercase tracking-wider text-slate-400 block">Important Findings</span>
            <p className="text-2xl font-bold text-white mt-1">{findings.length}</p>
          </div>

          <div className="p-3 rounded-xl bg-slate-950/70 border border-slate-800/80">
            <span className="text-[11px] font-mono uppercase tracking-wider text-slate-400 block">Unverified Claims</span>
            <p className="text-2xl font-bold text-amber-400 mt-1">{unverified_claims.length || claims.length}</p>
          </div>

          <div className="p-3 rounded-xl bg-slate-950/70 border border-slate-800/80">
            <span className="text-[11px] font-mono uppercase tracking-wider text-slate-400 block">Technical Facts Checked</span>
            <p className="text-2xl font-bold text-blue-400 mt-1">{verified_facts.length || evidence.length}</p>
          </div>
        </div>

        {/* Mandatory Safety Notice */}
        <div className="mt-4 p-3 rounded-xl bg-slate-950/80 border border-slate-800 text-xs text-slate-400 flex items-start gap-2.5">
          <Info className="w-4 h-4 text-blue-400 shrink-0 mt-0.5" />
          <div className="leading-relaxed">
            <strong className="text-slate-300">Evidence Assessment Notice: </strong>
            {assessment?.important_notice ||
              'This is an evidence-based assessment, not a guarantee of legitimacy or fraud. Never make financial payments or share sensitive documents based on unverified announcements.'}
          </div>
        </div>
      </div>

      {/* ------------------------------------------------------------- */}
      {/* NAVIGATION TABS                                               */}
      {/* ------------------------------------------------------------- */}
      <div className="flex items-center gap-2 border-b border-slate-800 pb-2 overflow-x-auto">
        <button
          onClick={() => setActiveTab('assessment')}
          className={`px-4 py-2 text-xs font-semibold rounded-lg transition-all shrink-0 flex items-center gap-1.5 ${
            activeTab === 'assessment'
              ? 'bg-blue-600 text-white shadow-sm shadow-blue-500/20'
              : 'text-slate-400 hover:text-slate-200 hover:bg-slate-900'
          }`}
        >
          <ShieldAlert className="w-3.5 h-3.5" />
          <span>Assessment & Safety ({findings.length})</span>
        </button>

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

      {/* ------------------------------------------------------------- */}
      {/* TAB 1: OPPORTUNITY ASSESSMENT & SAFETY INTELLIGENCE            */}
      {/* ------------------------------------------------------------- */}
      {activeTab === 'assessment' && (
        <div className="space-y-8">
          {/* Section A: Important Findings */}
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <div>
                <h4 className="text-base font-bold text-white flex items-center gap-2">
                  <ShieldAlert className="w-4 h-4 text-blue-400" />
                  <span>Evidence-Based Findings</span>
                </h4>
                <p className="text-xs text-slate-400 mt-0.5">
                  Observable facts and inconsistencies identified through automated extraction and technical checks.
                </p>
              </div>
              <span className="text-xs font-mono text-slate-400 bg-slate-900 px-2 py-0.5 rounded border border-slate-800">
                {findings.length} Finding{findings.length === 1 ? '' : 's'}
              </span>
            </div>

            {findings.length === 0 ? (
              <div className="p-6 rounded-xl bg-slate-900/60 border border-slate-800 text-center text-xs text-slate-400 flex items-center justify-center gap-2">
                <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                <span>No concerning technical inconsistencies or upfront fee patterns were identified.</span>
              </div>
            ) : (
              <div className="space-y-4">
                {findings.map((finding) => {
                  const severityBadge = getSeverityBadge(finding.severity);
                  return (
                    <div
                      key={finding.finding_id}
                      className="p-5 rounded-xl bg-slate-900 border border-slate-800 hover:border-slate-700 transition-colors space-y-3"
                    >
                      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
                        <div className="flex items-center gap-2">
                          <span className="font-mono text-xs font-bold text-blue-400 px-2 py-0.5 rounded bg-blue-950 border border-blue-800/80">
                            {finding.finding_id}
                          </span>
                          <span className={`inline-flex items-center gap-1.5 px-2 py-0.5 rounded text-[10px] font-mono font-bold border ${severityBadge.bg}`}>
                            <span className={`h-1.5 w-1.5 rounded-full ${severityBadge.dot}`}></span>
                            <span>{severityBadge.label}</span>
                          </span>
                        </div>

                        {finding.related_claim_ids?.length > 0 && (
                          <div className="flex items-center gap-1.5 text-xs text-slate-500 font-mono">
                            <span>Claims:</span>
                            {finding.related_claim_ids.map((cid) => (
                              <button
                                key={cid}
                                onClick={() => setActiveTab('claims')}
                                className="px-1.5 py-0.5 rounded bg-slate-950 text-blue-300 border border-slate-800 hover:border-blue-600"
                              >
                                {cid}
                              </button>
                            ))}
                          </div>
                        )}
                      </div>

                      <h5 className="text-sm font-bold text-white">
                        {finding.title}
                      </h5>

                      <p className="text-xs text-slate-300 leading-relaxed">
                        {finding.explanation}
                      </p>

                      <div className="grid grid-cols-1 md:grid-cols-2 gap-3 pt-2 text-xs">
                        <div className="p-3 rounded-lg bg-slate-950/70 border border-slate-800/80 space-y-1">
                          <span className="text-[11px] font-semibold text-slate-300 block">Why this matters:</span>
                          <p className="text-slate-400 leading-relaxed">{finding.why_it_matters}</p>
                        </div>
                        <div className="p-3 rounded-lg bg-slate-950/70 border border-slate-800/80 space-y-1">
                          <span className="text-[11px] font-semibold text-slate-300 block">What this does NOT prove:</span>
                          <p className="text-slate-400 leading-relaxed">{finding.limitations}</p>
                        </div>
                      </div>

                      {/* Recommended action box */}
                      <div className="p-3 rounded-lg bg-blue-950/30 border border-blue-900/50 text-xs text-blue-200 flex items-start gap-2.5">
                        <ArrowRight className="w-4 h-4 text-blue-400 shrink-0 mt-0.5" />
                        <div>
                          <strong className="text-blue-300">Recommended Action: </strong>
                          <span>{finding.recommended_action}</span>
                        </div>
                      </div>
                    </div>
                  );
                })}
              </div>
            )}
          </div>

          {/* Section B: Recommended Next Steps Checklist */}
          <div className="space-y-4">
            <div>
              <h4 className="text-base font-bold text-white flex items-center gap-2">
                <ListChecks className="w-4 h-4 text-emerald-400" />
                <span>Recommended Next Steps Before Applying or Paying</span>
              </h4>
              <p className="text-xs text-slate-400 mt-0.5">
                Prioritized candidate checklist tailored to the observed signals and unverified claims.
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
              {next_steps.map((step) => (
                <div
                  key={step.step_number}
                  className="p-4 rounded-xl bg-slate-900 border border-slate-800 space-y-1.5"
                >
                  <div className="flex items-center gap-2">
                    <span className="w-5 h-5 rounded-full bg-blue-950 border border-blue-800 text-blue-400 text-xs font-mono font-bold flex items-center justify-center shrink-0">
                      {step.step_number}
                    </span>
                    <h5 className="text-xs font-bold text-slate-100">{step.action}</h5>
                  </div>
                  <p className="text-[11px] text-slate-400 pl-7 leading-relaxed">{step.rationale}</p>
                </div>
              ))}
            </div>
          </div>

          {/* Section C: Contextual Safety Recommendations */}
          {recommendations.length > 0 && (
            <div className="space-y-4">
              <div>
                <h4 className="text-base font-bold text-white flex items-center gap-2">
                  <Lock className="w-4 h-4 text-cyan-400" />
                  <span>Targeted Safety Recommendations</span>
                </h4>
                <p className="text-xs text-slate-400 mt-0.5">
                  Protective measures specific to the findings observed in this announcement.
                </p>
              </div>

              <div className="space-y-3">
                {recommendations.map((rec) => (
                  <div
                    key={rec.recommendation_id}
                    className="p-4 rounded-xl bg-slate-900 border border-slate-800 space-y-2"
                  >
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-2">
                        <span className="text-[10px] font-mono font-bold uppercase px-2 py-0.5 rounded bg-slate-800 text-slate-300">
                          {rec.topic.replace(/_/g, ' ')}
                        </span>
                        <span className={`text-[10px] font-mono px-2 py-0.5 rounded ${
                          rec.priority === 1
                            ? 'bg-rose-950 text-rose-300 border border-rose-800'
                            : rec.priority === 2
                            ? 'bg-amber-950 text-amber-300 border border-amber-800'
                            : 'bg-blue-950 text-blue-300 border border-blue-800'
                        }`}>
                          Priority {rec.priority}
                        </span>
                      </div>
                      <span className="font-mono text-xs text-slate-500">{rec.recommendation_id}</span>
                    </div>

                    <h5 className="text-xs font-bold text-white">{rec.title}</h5>
                    <p className="text-xs text-slate-300 leading-relaxed">{rec.advice}</p>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Section D: What We Verified vs What Remains Unverified */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-5 pt-2">
            {/* Column 1: Verified Facts */}
            <div className="p-5 rounded-xl bg-slate-900 border border-slate-800 space-y-3">
              <div className="flex items-center justify-between pb-2 border-b border-slate-800">
                <span className="text-xs font-bold text-emerald-400 uppercase tracking-wider flex items-center gap-1.5">
                  <CheckCircle2 className="w-4 h-4" />
                  <span>What We Independently Verified</span>
                </span>
                <span className="text-xs font-mono text-slate-400">{verified_facts.length} Technical Facts</span>
              </div>

              {verified_facts.length === 0 ? (
                <p className="text-xs text-slate-500 italic py-2">No technical facts were recorded.</p>
              ) : (
                <div className="space-y-2.5 max-h-80 overflow-y-auto pr-1">
                  {verified_facts.map((fact) => (
                    <div
                      key={fact.fact_id}
                      className="p-3 rounded-lg bg-slate-950/70 border border-slate-800/80 text-xs space-y-1"
                    >
                      <p className="text-slate-200 font-medium">{fact.statement}</p>
                      <div className="flex items-center justify-between text-[10px] font-mono text-slate-500 pt-1">
                        <span>Source: <strong className="text-slate-400">{fact.source_name}</strong></span>
                        <span>{new Date(fact.retrieved_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</span>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>

            {/* Column 2: Unverified Claims */}
            <div className="p-5 rounded-xl bg-slate-900 border border-slate-800 space-y-3">
              <div className="flex items-center justify-between pb-2 border-b border-slate-800">
                <span className="text-xs font-bold text-amber-400 uppercase tracking-wider flex items-center gap-1.5">
                  <AlertTriangle className="w-4 h-4" />
                  <span>What Remains Unverified</span>
                </span>
                <span className="text-xs font-mono text-slate-400">{unverified_claims.length} Claims</span>
              </div>

              {unverified_claims.length === 0 ? (
                <p className="text-xs text-slate-500 italic py-2">No unverified claims logged.</p>
              ) : (
                <div className="space-y-2.5 max-h-80 overflow-y-auto pr-1">
                  {unverified_claims.map((claim) => (
                    <div
                      key={claim.claim_id}
                      className="p-3 rounded-lg bg-slate-950/70 border border-slate-800/80 text-xs space-y-1"
                    >
                      <div className="flex items-center justify-between">
                        <span className="text-slate-200 font-medium">{claim.statement}</span>
                        <span className="text-[10px] font-mono uppercase px-1.5 py-0.5 rounded bg-slate-800 text-slate-400 ml-2 shrink-0">
                          {claim.category}
                        </span>
                      </div>
                      <p className="text-[11px] text-slate-400 leading-relaxed italic">
                        {claim.reason_unverified}
                      </p>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>

          {/* Section E: Expandable Methodology & Limitations */}
          <div className="p-4 rounded-xl bg-slate-900/60 border border-slate-800">
            <button
              onClick={() => setShowLimitations(!showLimitations)}
              className="w-full flex items-center justify-between text-xs font-semibold text-slate-300 hover:text-white transition-colors"
            >
              <div className="flex items-center gap-2">
                <Info className="w-4 h-4 text-blue-400" />
                <span>OfferProof Assessment Methodology & System Safeguards</span>
              </div>
              {showLimitations ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
            </button>

            {showLimitations && (
              <div className="mt-3 pt-3 border-t border-slate-800/80 text-xs text-slate-400 space-y-2 leading-relaxed">
                <p>
                  <strong>What OfferProof Checks: </strong> Public RDAP domain registration age, DNS-over-HTTPS routing (A, AAAA, MX, NS),
                  recruiter email domain consistency, and URL protocol security.
                </p>
                <p>
                  <strong>What Cannot Be Checked: </strong> Internal corporate hiring databases, private email authorization, salary/stipend
                  commitments, government corporate registries (SEC, Companies House, MCA), and university credentials.
                </p>
                <p>
                  <strong>Non-Fraud Determination: </strong> OfferProof never produces synthetic scam risk percentages or asserts
                  definitively that an opportunity is legitimate or fraudulent. All assessments are deterministic safety guidance levels.
                </p>
                <p>
                  <strong>SSRF & Privacy Safeguards: </strong> Arbitrary external URLs submitted by users are never downloaded, scraped,
                  or executed by backend systems.
                </p>
              </div>
            )}
          </div>
        </div>
      )}

      {/* ------------------------------------------------------------- */}
      {/* TAB 2: CLAIMS LIST WITH VERIFICATION STATUSES                 */}
      {/* ------------------------------------------------------------- */}
      {activeTab === 'claims' && (
        <div className="space-y-4">
          {claims.length === 0 ? (
            <div className="p-8 text-center text-slate-500 text-xs bg-slate-900/40 rounded-xl border border-slate-800">
              No claims evaluated.
            </div>
          ) : (
            claims.map((claim) => {
              const statusBadge = getVerificationStatusBadge(claim.verification_status);

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

      {/* ------------------------------------------------------------- */}
      {/* TAB 3: EVIDENCE INTELLIGENCE LIST                             */}
      {/* ------------------------------------------------------------- */}
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

                  <div>
                    <h4 className="text-sm font-semibold text-white">
                      {ev.observed_value}
                    </h4>
                    <p className="text-xs text-slate-300 leading-relaxed mt-1">
                      {ev.interpretation}
                    </p>
                  </div>

                  <div className="flex items-center gap-4 text-xs font-mono text-slate-400 pt-2 border-t border-slate-800/80">
                    <span>Source: <strong className="text-slate-200">{ev.source_name}</strong></span>
                    {ev.source_url && (
                      <span className="truncate max-w-xs text-slate-500">
                        URL: {ev.source_url}
                      </span>
                    )}
                  </div>

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

      {/* ------------------------------------------------------------- */}
      {/* TAB 4: TECHNICAL OBSERVATIONS                                 */}
      {/* ------------------------------------------------------------- */}
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

      {/* ------------------------------------------------------------- */}
      {/* TAB 5: ENTITY PROFILE                                         */}
      {/* ------------------------------------------------------------- */}
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

      {/* ------------------------------------------------------------- */}
      {/* TAB 6: LINGUISTIC INDICATORS                                  */}
      {/* ------------------------------------------------------------- */}
      {activeTab === 'indicators' && (
        <div className="space-y-4">
          <div className="p-4 rounded-xl bg-amber-950/30 border border-amber-500/30 text-xs text-amber-200 flex items-start gap-3">
            <ShieldAlert className="w-5 h-5 text-amber-400 shrink-0 mt-0.5" />
            <div>
              <p className="font-semibold text-amber-300">Phase 4 Observational Standard</p>
              <p className="mt-1 text-slate-300 leading-relaxed">
                Extracted linguistic indicators highlight high-risk phrasing commonly associated with recruitment
                fraud (e.g. upfront fee demands, guaranteed selection, artificial urgency). Per OFFERPROOF guidelines,
                these indicators are observational evidence and do NOT constitute definitive proof of fraud.
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

      {/* ------------------------------------------------------------- */}
      {/* EXPANDABLE JSON INSPECTOR                                     */}
      {/* ------------------------------------------------------------- */}
      <div className="pt-2">
        <button
          onClick={() => setShowJson(!showJson)}
          className="flex items-center gap-2 text-xs font-mono text-slate-400 hover:text-slate-200 transition-colors"
        >
          {showJson ? <ChevronUp className="w-3.5 h-3.5" /> : <ChevronDown className="w-3.5 h-3.5" />}
          <span>{showJson ? 'Hide' : 'Inspect'} Raw Assessment Payload (JSON)</span>
        </button>

        {showJson && (
          <div className="mt-3 p-4 rounded-xl bg-slate-950 border border-slate-800 font-mono text-[11px] text-slate-300 overflow-x-auto max-h-96">
            <pre>{JSON.stringify(result, null, 2)}</pre>
          </div>
        )}
      </div>

      {/* ------------------------------------------------------------- */}
      {/* PRINT / EXPORT REPORT MODAL                                   */}
      {/* ------------------------------------------------------------- */}
      {showPrintModal && (
        <div className="fixed inset-0 z-50 bg-slate-950/80 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-slate-900 border border-slate-800 rounded-2xl max-w-3xl w-full max-h-[90vh] overflow-y-auto shadow-2xl p-6 space-y-6">
            {/* Modal Header */}
            <div className="flex items-center justify-between pb-4 border-b border-slate-800">
              <div className="flex items-center gap-2.5">
                <Printer className="w-5 h-5 text-blue-400" />
                <div>
                  <h3 className="text-lg font-bold text-white">Printable Assessment Report</h3>
                  <p className="text-xs text-slate-400">OfferProof Official Opportunity Evidence Summary</p>
                </div>
              </div>
              <button
                onClick={() => setShowPrintModal(false)}
                className="p-1 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition-colors"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            {/* Printable Document Preview Area */}
            <div id="printable-assessment-document" className="bg-white text-slate-900 p-8 rounded-xl space-y-6 text-sm font-sans">
              {/* Header Branding */}
              <div className="flex items-center justify-between border-b pb-4 border-slate-300">
                <div>
                  <h2 className="text-2xl font-black tracking-tight text-blue-900 font-mono">
                    OFFER<span className="text-blue-600">PROOF</span>
                  </h2>
                  <p className="text-xs text-slate-600 italic">Don't trust the offer. Verify the evidence.</p>
                </div>
                <div className="text-right text-xs text-slate-600 font-mono">
                  <p><strong>Report:</strong> {reportId}</p>
                  <p><strong>Date:</strong> {reportDate} {reportTime}</p>
                </div>
              </div>

              {/* Subject Summary */}
              <div className="space-y-1">
                <span className="text-xs uppercase font-bold text-slate-500 font-mono">Target Opportunity</span>
                <h3 className="text-lg font-bold text-slate-900">
                  {opportunity.title || opportunity.role || 'Unspecified Opportunity Title'}
                </h3>
                <p className="text-xs text-slate-700">
                  <strong>Stated Entity:</strong> {organisation.name || 'Not provided'} |{' '}
                  <strong>Website:</strong> {organisation.website || 'Not provided'} |{' '}
                  <strong>Recruiter:</strong> {recruiter.email || recruiter.name || 'Not provided'}
                </p>
              </div>

              {/* Assessment Level Callout */}
              <div className="p-4 rounded-lg bg-slate-100 border border-slate-300 space-y-1">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-mono font-bold uppercase text-slate-700">Assessment Guidance Level</span>
                  <span className="text-xs font-mono font-black uppercase px-2 py-0.5 rounded bg-slate-800 text-white">
                    {assessment?.assessment_label || assessmentTheme.label}
                  </span>
                </div>
                <p className="text-xs text-slate-800 leading-relaxed pt-1">
                  {assessment?.summary}
                </p>
              </div>

              {/* Key Findings */}
              {findings.length > 0 && (
                <div className="space-y-2">
                  <h4 className="text-xs font-bold uppercase tracking-wider text-slate-700 font-mono border-b pb-1 border-slate-200">
                    Key Assessment Findings ({findings.length})
                  </h4>
                  <div className="space-y-2 text-xs">
                    {findings.map((f) => (
                      <div key={f.finding_id} className="p-2.5 rounded bg-slate-50 border border-slate-200 space-y-1">
                        <div className="flex items-center justify-between font-mono text-[11px]">
                          <strong className="text-slate-900">{f.title}</strong>
                          <span className="uppercase text-slate-600 font-semibold">{f.severity}</span>
                        </div>
                        <p className="text-slate-700">{f.explanation}</p>
                        <p className="text-blue-900 text-[11px]">
                          <strong>Action:</strong> {f.recommended_action}
                        </p>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Unverified Claims */}
              {unverified_claims.length > 0 && (
                <div className="space-y-2">
                  <h4 className="text-xs font-bold uppercase tracking-wider text-slate-700 font-mono border-b pb-1 border-slate-200">
                    Claims Remaining Unverified ({unverified_claims.length})
                  </h4>
                  <ul className="list-disc pl-5 text-xs text-slate-700 space-y-1">
                    {unverified_claims.slice(0, 5).map((u) => (
                      <li key={u.claim_id}>
                        <strong>{u.statement}</strong> — <span className="italic">{u.reason_unverified}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {/* Next Steps Checklist */}
              {next_steps.length > 0 && (
                <div className="space-y-2">
                  <h4 className="text-xs font-bold uppercase tracking-wider text-slate-700 font-mono border-b pb-1 border-slate-200">
                    Recommended Next Steps
                  </h4>
                  <ol className="list-decimal pl-5 text-xs text-slate-700 space-y-1">
                    {next_steps.map((s) => (
                      <li key={s.step_number}>
                        <strong>{s.action}</strong>
                      </li>
                    ))}
                  </ol>
                </div>
              )}

              {/* Methodology & Safety Notice */}
              <div className="pt-3 border-t border-slate-200 text-[10px] text-slate-500 leading-relaxed font-mono">
                <p>
                  <strong>DISCLAIMER:</strong> This report is generated through automated public technical intelligence
                  (RDAP, DNS-over-HTTPS, and format analysis). It provides risk guidance and is NOT a legal determination
                  or definitive guarantee of fraud or legitimacy. Financial offers, hiring authority, and internal policies
                  remain unverified. OfferProof never downloads or executes arbitrary user links.
                </p>
              </div>
            </div>

            {/* Modal Actions */}
            <div className="flex items-center justify-end gap-3 pt-2">
              <button
                onClick={() => setShowPrintModal(false)}
                className="px-4 py-2 rounded-lg bg-slate-800 text-slate-300 hover:bg-slate-700 text-xs font-medium transition-colors"
              >
                Close
              </button>
              <button
                onClick={handlePrint}
                className="inline-flex items-center gap-1.5 px-4 py-2 rounded-lg bg-blue-600 hover:bg-blue-500 text-white text-xs font-semibold shadow-md transition-colors"
              >
                <Printer className="w-4 h-4" />
                <span>Print Document / Save as PDF</span>
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
