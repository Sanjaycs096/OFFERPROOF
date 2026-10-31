import React, { useState, useRef } from 'react';
import {
  FileText,
  Link2,
  UploadCloud,
  Search,
  CheckCircle2,
  AlertCircle,
  Info,
  X,
  FileCheck2,
  Sparkles,
  FileUp,
  Trash2,
  Loader2,
  Cpu,
} from 'lucide-react';
import { ingestPdf, ingestText, extractClaims, verifyClaims } from '../services/api';
import ExtractionResults from './ExtractionResults';

const MAX_PDF_SIZE_BYTES = 5 * 1024 * 1024; // 5 MB

export default function SubmissionForm({ isOnline }) {
  const [description, setDescription] = useState('');
  const [opportunityUrl, setOpportunityUrl] = useState('');
  const [opportunityType, setOpportunityType] = useState('job');
  const [selectedFile, setSelectedFile] = useState(null);
  const [fileError, setFileError] = useState('');
  const [isDragging, setIsDragging] = useState(false);

  // Execution states
  const [isLoading, setIsLoading] = useState(false);
  const [loadingStep, setLoadingStep] = useState('');
  const [errorMessage, setErrorMessage] = useState('');
  const [extractionResult, setExtractionResult] = useState(null);

  const fileInputRef = useRef(null);
  const resultsRef = useRef(null);

  const sampleDescriptions = {
    job: "Congratulations! You have been selected for a Remote Data Analyst position at Apex Technologies LLC. Salary offered: $65/hr without interview. Pay $150 as a registration fee before November 15. Guaranteed selection. Contact hr@apextechnologies.example.com.",
    internship: "Congratulations! You have been selected for a Data Science Internship at ABC Technologies. Earn ₹45,000 per month. Pay ₹1,500 as a registration fee before October 31. Guaranteed selection.",
    scholarship: "Global STEM Leadership Fellowship claiming $10,000 grant. Non-refundable $75 application processing fee required before December 1.",
  };

  const handleApplySample = (type) => {
    setOpportunityType(type);
    setDescription(sampleDescriptions[type]);
    setSelectedFile(null);
    setFileError('');
    setErrorMessage('');
    if (type === 'job') setOpportunityUrl('https://apextechnologies.example.com/apply/9843');
    if (type === 'internship') setOpportunityUrl('https://abctech.example.com/apply');
    if (type === 'scholarship') setOpportunityUrl('https://stem-fellowship.example.org/apply');
  };

  const validateAndSetFile = (file) => {
    if (!file) return;

    if (!file.name.toLowerCase().endsWith('.pdf') && file.type !== 'application/pdf') {
      setFileError('Invalid file type: Please select a text-based PDF document (.pdf).');
      setSelectedFile(null);
      return;
    }

    if (file.size > MAX_PDF_SIZE_BYTES) {
      setFileError('File size exceeds the 5 MB limit. Please upload a smaller PDF document.');
      setSelectedFile(null);
      return;
    }

    setFileError('');
    setSelectedFile(file);
    setErrorMessage('');
  };

  const handleFileChange = (e) => {
    const file = e.target.files?.[0];
    validateAndSetFile(file);
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    setIsDragging(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);
    const file = e.dataTransfer.files?.[0];
    validateAndSetFile(file);
  };

  const handleRemoveFile = () => {
    setSelectedFile(null);
    setFileError('');
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErrorMessage('');

    if (!description.trim() && !selectedFile && !opportunityUrl.trim()) {
      setErrorMessage('Please provide opportunity text, a PDF document, or an application URL.');
      return;
    }

    setIsLoading(true);
    setExtractionResult(null);

    try {
      let contentToExtract = description.trim();
      let sourceType = 'text';

      // 1. If PDF is attached, ingest PDF first
      if (selectedFile) {
        setLoadingStep('Uploading & parsing PDF via PyMuPDF in memory...');
        const pdfRes = await ingestPdf(selectedFile, opportunityUrl.trim() || undefined);
        if (!pdfRes.success) {
          throw new Error(pdfRes.error || 'Failed to parse PDF document.');
        }

        sourceType = 'pdf';
        contentToExtract = pdfRes.data.content;

        // If user also added descriptive text notes, combine them
        if (description.trim()) {
          contentToExtract = `${description.trim()}\n\n--- Document Text ---\n${pdfRes.data.content}`;
          sourceType = 'combined';
        }
      } else if (!contentToExtract && opportunityUrl.trim()) {
        // Only URL was provided without text
        contentToExtract = `Application opportunity link referenced: ${opportunityUrl.trim()}`;
        sourceType = 'url_reference';
      }

      // 2. Perform Extraction
      setLoadingStep('Extracting structured entities, claims, and linguistic indicators...');
      const extractRes = await extractClaims({
        content: contentToExtract,
        source_type: sourceType,
        application_url: opportunityUrl.trim() || undefined,
      });

      if (!extractRes.success) {
        throw new Error(extractRes.error || 'Claim extraction failed.');
      }

      // 3. Perform Evidence Verification (Phase 3)
      setLoadingStep('Collecting independent technical evidence & cross-referencing...');
      const verifyRes = await verifyClaims({
        extracted_information: extractRes.data.extracted_information,
        claims: extractRes.data.claims,
        source_type: sourceType,
        application_url: opportunityUrl.trim() || undefined,
      });

      if (verifyRes.success) {
        setExtractionResult({
          ...extractRes.data,
          verification_summary: verifyRes.data.verification_summary,
          claims: verifyRes.data.claims,
          evidence: verifyRes.data.evidence,
          technical_observations: verifyRes.data.technical_observations,
          limitations: verifyRes.data.limitations,
        });
      } else {
        // Fallback to extraction output if verification encountered non-fatal issues
        setExtractionResult(extractRes.data);
      }

      // Scroll smoothly to results
      setTimeout(() => {
        resultsRef.current?.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }, 100);
    } catch (err) {
      setErrorMessage(err instanceof Error ? err.message : 'An unexpected error occurred during analysis.');
    } finally {
      setIsLoading(false);
      setLoadingStep('');
    }
  };

  const handleResetAll = () => {
    setDescription('');
    setOpportunityUrl('');
    setSelectedFile(null);
    setFileError('');
    setErrorMessage('');
    setExtractionResult(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  return (
    <section id="submit" className="py-16 bg-slate-900/40">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Section Header */}
        <div className="mb-8 text-center sm:text-left sm:flex sm:items-end sm:justify-between">
          <div>
            <div className="flex items-center gap-2">
              <span className="text-xs font-mono uppercase tracking-wider text-blue-400 font-semibold">
                Opportunity Ingestion
              </span>
              <span className="px-2 py-0.5 rounded text-[10px] uppercase font-mono font-bold bg-blue-950 border border-blue-800 text-blue-300">
                Phase 3 Evidence Engine
              </span>
            </div>
            <h2 className="text-2xl sm:text-3xl font-bold text-white mt-1">
              Ingest & Extract Opportunity Claims
            </h2>
            <p className="text-sm text-slate-400 mt-1">
              Paste offer text, upload offer PDFs, or provide links for structured entity and claim extraction.
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
                Opportunity / Application Link (Reference Only)
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
              <p className="text-[11px] text-slate-500 mt-1">
                For security against SSRF, external URLs are not auto-fetched; hostnames are extracted as input references.
              </p>
            </div>

            {/* Document Upload (PDF) */}
            <div>
              <div className="flex items-center justify-between mb-2">
                <label className="block text-xs font-mono uppercase tracking-wider text-slate-300">
                  Offer Document / Contract (PDF Upload)
                </label>
                <span className="text-[10px] uppercase font-mono px-2 py-0.5 rounded bg-blue-950 text-blue-300 border border-blue-800">
                  PyMuPDF Enabled
                </span>
              </div>

              {!selectedFile ? (
                <div
                  onDragOver={handleDragOver}
                  onDragLeave={handleDragLeave}
                  onDrop={handleDrop}
                  onClick={() => fileInputRef.current?.click()}
                  className={`rounded-xl border border-dashed p-6 text-center transition-all cursor-pointer ${
                    isDragging
                      ? 'border-blue-400 bg-blue-950/20'
                      : 'border-slate-700 bg-slate-950/40 hover:border-slate-500 hover:bg-slate-950/60'
                  }`}
                >
                  <input
                    ref={fileInputRef}
                    type="file"
                    accept=".pdf,application/pdf"
                    onChange={handleFileChange}
                    className="hidden"
                  />
                  <div className="mx-auto w-10 h-10 rounded-full bg-slate-800/80 border border-slate-700 flex items-center justify-center text-slate-300 mb-2">
                    <UploadCloud className="w-5 h-5 text-blue-400" />
                  </div>
                  <p className="text-xs font-medium text-slate-200">
                    Click to browse or drag and drop a PDF offer letter
                  </p>
                  <p className="text-[11px] text-slate-500 mt-1">
                    Text-based PDF documents up to 5 MB (max 15 pages).
                  </p>
                </div>
              ) : (
                <div className="p-3.5 rounded-xl bg-slate-950 border border-slate-700 flex items-center justify-between gap-3">
                  <div className="flex items-center gap-3 overflow-hidden">
                    <div className="w-9 h-9 rounded-lg bg-blue-500/10 border border-blue-500/20 flex items-center justify-center text-blue-400 shrink-0">
                      <FileUp className="w-4 h-4" />
                    </div>
                    <div className="overflow-hidden">
                      <p className="text-xs font-medium text-white truncate">{selectedFile.name}</p>
                      <p className="text-[10px] font-mono text-slate-400">
                        {(selectedFile.size / 1024).toFixed(1)} KB &bull; PDF Document
                      </p>
                    </div>
                  </div>

                  <button
                    type="button"
                    onClick={handleRemoveFile}
                    className="p-1.5 text-slate-400 hover:text-rose-400 hover:bg-rose-950/30 rounded-lg transition-colors"
                    title="Remove file"
                  >
                    <Trash2 className="w-4 h-4" />
                  </button>
                </div>
              )}

              {fileError && (
                <p className="text-xs text-rose-400 mt-2 flex items-center gap-1.5">
                  <AlertCircle className="w-3.5 h-3.5" />
                  <span>{fileError}</span>
                </p>
              )}
            </div>

            {/* Validation / error alert */}
            {errorMessage && (
              <div className="p-3.5 rounded-xl bg-rose-950/50 border border-rose-500/40 text-rose-300 text-xs flex items-center gap-2">
                <AlertCircle className="w-4 h-4 shrink-0" />
                <span>{errorMessage}</span>
              </div>
            )}

            {/* Submit & Reset actions */}
            <div className="pt-2 flex flex-col sm:flex-row items-center gap-3">
              <button
                type="submit"
                disabled={isLoading}
                className="w-full sm:w-auto flex-1 inline-flex items-center justify-center gap-2 px-6 py-3 rounded-xl bg-blue-600 hover:bg-blue-500 active:bg-blue-700 disabled:opacity-50 text-white font-semibold text-sm transition-all shadow-md shadow-blue-600/25"
              >
                {isLoading ? (
                  <>
                    <Loader2 className="w-4 h-4 animate-spin text-white" />
                    <span>{loadingStep || 'Processing Ingestion...'}</span>
                  </>
                ) : (
                  <>
                    <Search className="w-4 h-4" />
                    <span>Extract Claims & Entities</span>
                  </>
                )}
              </button>

              {(description || opportunityUrl || selectedFile) && !isLoading && (
                <button
                  type="button"
                  onClick={handleResetAll}
                  className="w-full sm:w-auto px-4 py-3 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 text-sm font-medium border border-slate-700 transition-colors"
                >
                  Clear Fields
                </button>
              )}
            </div>
          </form>
        </div>

        {/* Extraction Results View */}
        <div ref={resultsRef}>
          {extractionResult && (
            <ExtractionResults result={extractionResult} onReset={handleResetAll} />
          )}
        </div>
      </div>
    </section>
  );
}
