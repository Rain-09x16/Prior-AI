import Link from 'next/link';
import { SignedIn, SignedOut, SignUpButton } from '@clerk/nextjs';
import {
  ArrowRight,
  Zap,
  Clock,
  Target,
  FileCheck,
  Bot,
  Search,
  BarChart3,
  Shield,
  CheckCircle2,
  Sparkles,
  Play,
} from 'lucide-react';

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-[var(--background)]">
      {/* Hero Section */}
      <section className="relative min-h-screen flex items-center justify-center overflow-hidden pt-16">
        {/* Background Effects */}
        <div className="absolute inset-0 hero-gradient" />
        <div className="absolute inset-0 hero-grid opacity-30" />

        {/* Floating Orbs */}
        <div className="glow-orb -top-20 -left-20 animate-float" />
        <div className="glow-orb -bottom-40 -right-20 animate-float delay-300" style={{ background: 'var(--accent)' }} />

        <div className="relative container mx-auto px-6 py-24 text-center">
          {/* Badge */}
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-[var(--surface)] border border-[var(--border)] mb-8 animate-fade-in">
            <span className="flex h-2 w-2">
              <span className="animate-ping absolute inline-flex h-2 w-2 rounded-full bg-[var(--success)] opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2 w-2 bg-[var(--success)]"></span>
            </span>
            <span className="text-sm font-medium text-[var(--foreground-muted)]">
              Powered by IBM watsonx AI
            </span>
          </div>

          {/* Main Title */}
          <h1 className="text-5xl md:text-7xl lg:text-8xl font-black mb-6 animate-fade-in-up tracking-tight">
            <span className="text-[var(--foreground)]">From Lab to</span>
            <br />
            <span className="gradient-text">Market</span>
          </h1>

          {/* Subtitle */}
          <p className="text-xl md:text-2xl text-[var(--foreground-muted)] max-w-3xl mx-auto mb-8 animate-fade-in-up delay-100 leading-relaxed">
            The Operating System for Emerging Innovation. Transform 12-month bureaucratic cycles
            into <span className="text-[var(--foreground)] font-semibold">3-week automated workflows</span>.
          </p>

          {/* Trust Badges */}
          <div className="flex flex-wrap items-center justify-center gap-3 mb-12 animate-fade-in-up delay-200">
            <span className="badge badge-neutral badge-pill">
              Philippine IMPACT Network (34 Universities)
            </span>
            <span className="badge badge-primary badge-pill">
              <Bot className="w-3 h-3" />
              IBM watsonx Orchestrate
            </span>
            <span className="badge badge-success badge-pill">
              <CheckCircle2 className="w-3 h-3" />
              85% Validated Accuracy
            </span>
          </div>

          {/* CTA Buttons */}
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4 animate-fade-in-up delay-300">
            <SignedOut>
              <SignUpButton mode="modal">
                <button className="btn btn-gradient btn-lg group">
                  <Sparkles className="w-5 h-5" />
                  <span>Start Free Analysis</span>
                  <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
                </button>
              </SignUpButton>
            </SignedOut>
            <SignedIn>
              <Link href="/dashboard" className="btn btn-gradient btn-lg group">
                <Sparkles className="w-5 h-5" />
                <span>Go to Dashboard</span>
                <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
              </Link>
            </SignedIn>
            <button className="btn btn-secondary btn-lg group">
              <Play className="w-5 h-5" />
              <span>Watch Demo</span>
            </button>
          </div>
        </div>
      </section>

      {/* Metrics Section */}
      <section className="relative py-24 border-t border-[var(--border)]">
        <div className="container mx-auto px-6">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="metric-card text-center group">
              <div className="metric-value gradient-text">98%</div>
              <h3 className="text-lg font-semibold text-[var(--foreground)] mt-4">Time Reduction</h3>
              <p className="text-sm text-[var(--foreground-muted)] mt-2">
                From 15 hours to 15 minutes per analysis
              </p>
            </div>

            <div className="metric-card text-center border-[var(--success-border)] group">
              <div className="metric-value text-[var(--success)]">85%</div>
              <h3 className="text-lg font-semibold text-[var(--foreground)] mt-4">Validated Accuracy</h3>
              <p className="text-sm text-[var(--foreground-muted)] mt-2">
                Ground truth testing on 60 USPTO patents
              </p>
            </div>

            <div className="metric-card text-center group">
              <div className="metric-value gradient-text">3-Week</div>
              <h3 className="text-lg font-semibold text-[var(--foreground)] mt-4">Compliance Timeline</h3>
              <p className="text-sm text-[var(--foreground-muted)] mt-2">
                vs. 12-month traditional process
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section className="relative py-24 bg-[var(--background-secondary)]">
        <div className="container mx-auto px-6">
          <div className="text-center mb-16">
            <span className="badge badge-primary badge-pill mb-4">How It Works</span>
            <h2 className="text-4xl md:text-5xl font-bold text-[var(--foreground)] mb-4">
              Powered by IBM watsonx Orchestrate
            </h2>
            <p className="text-lg text-[var(--foreground-muted)] max-w-2xl mx-auto">
              Multi-agent AI coordination that makes autonomous decisions at every step
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {/* Step 1 */}
            <div className="step-card">
              <div className="step-number">1</div>
              <div className="w-12 h-12 rounded-xl bg-[var(--primary)]/10 flex items-center justify-center mb-4">
                <FileCheck className="w-6 h-6 text-[var(--primary)]" />
              </div>
              <h3 className="text-lg font-bold text-[var(--foreground)] mb-2">Upload Disclosure</h3>
              <p className="text-sm text-[var(--foreground-muted)]">
                Submit invention disclosure form (PDF/DOCX). VANTAGE ingests into secure processing pipeline.
              </p>
            </div>

            {/* Step 2 */}
            <div className="step-card">
              <div className="step-number">2</div>
              <div className="w-12 h-12 rounded-xl bg-[var(--accent)]/10 flex items-center justify-center mb-4">
                <Bot className="w-6 h-6 text-[var(--accent)]" />
              </div>
              <h3 className="text-lg font-bold text-[var(--foreground)] mb-2">Orchestrate Analysis</h3>
              <p className="text-sm text-[var(--foreground-muted)]">
                IBM watsonx Orchestrate coordinates multiple AI agents: Claim Extraction → Patent Search → Novelty Scoring
              </p>
            </div>

            {/* Step 3 */}
            <div className="step-card">
              <div className="step-number">3</div>
              <div className="w-12 h-12 rounded-xl bg-[var(--success)]/10 flex items-center justify-center mb-4">
                <Search className="w-6 h-6 text-[var(--success)]" />
              </div>
              <h3 className="text-lg font-bold text-[var(--foreground)] mb-2">Multi-Agent Workflow</h3>
              <p className="text-sm text-[var(--foreground-muted)]">
                Each agent makes autonomous decisions. IBM Granite models analyze claims. Search agents query global databases.
              </p>
            </div>

            {/* Step 4 */}
            <div className="step-card">
              <div className="step-number">4</div>
              <div className="w-12 h-12 rounded-xl bg-[var(--warning)]/10 flex items-center justify-center mb-4">
                <BarChart3 className="w-6 h-6 text-[var(--warning)]" />
              </div>
              <h3 className="text-lg font-bold text-[var(--foreground)] mb-2">Compliance Report</h3>
              <p className="text-sm text-[var(--foreground-muted)]">
                Generate audit-ready documentation with patentability scores, prior art citations, and FOB-compliant recommendations.
              </p>
            </div>
          </div>

          {/* Validation Banner */}
          <div className="mt-16 p-8 rounded-2xl bg-[var(--surface)] border border-[var(--border)] text-center">
            <div className="flex items-center justify-center gap-3 mb-4">
              <Shield className="w-6 h-6 text-[var(--success)]" />
              <span className="text-lg font-semibold text-[var(--foreground)]">Production-Ready Validation</span>
            </div>
            <p className="text-[var(--foreground-muted)] max-w-2xl mx-auto">
              VANTAGE is validated against <span className="text-[var(--foreground)] font-semibold">60 real USPTO patents</span> with ground truth labels,
              not mock data. We achieve <span className="text-[var(--success)] font-semibold">85% accuracy</span> in patentability assessment —
              this isn't a demo, it's production-ready technology.
            </p>
          </div>
        </div>
      </section>

      {/* Features Grid */}
      <section className="relative py-24 border-t border-[var(--border)]">
        <div className="container mx-auto px-6">
          <div className="text-center mb-16">
            <span className="badge badge-primary badge-pill mb-4">Features</span>
            <h2 className="text-4xl md:text-5xl font-bold text-[var(--foreground)] mb-4">
              Why Technology Transfer Offices Choose VANTAGE
            </h2>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div className="glass-card p-6">
              <div className="w-12 h-12 rounded-xl bg-[var(--primary)]/10 flex items-center justify-center mb-4">
                <Zap className="w-6 h-6 text-[var(--primary)]" />
              </div>
              <h3 className="text-lg font-bold text-[var(--foreground)] mb-2">AI-Powered Analysis</h3>
              <p className="text-sm text-[var(--foreground-muted)]">
                Advanced NLU and ML algorithms for accurate claim extraction powered by IBM Granite models
              </p>
            </div>

            <div className="glass-card p-6">
              <div className="w-12 h-12 rounded-xl bg-[var(--accent)]/10 flex items-center justify-center mb-4">
                <Clock className="w-6 h-6 text-[var(--accent)]" />
              </div>
              <h3 className="text-lg font-bold text-[var(--foreground)] mb-2">Save Time</h3>
              <p className="text-sm text-[var(--foreground-muted)]">
                Complete analysis in 15 minutes instead of 15 hours with intelligent automation
              </p>
            </div>

            <div className="glass-card p-6">
              <div className="w-12 h-12 rounded-xl bg-[var(--success)]/10 flex items-center justify-center mb-4">
                <Target className="w-6 h-6 text-[var(--success)]" />
              </div>
              <h3 className="text-lg font-bold text-[var(--foreground)] mb-2">Smart Recommendations</h3>
              <p className="text-sm text-[var(--foreground-muted)]">
                Get actionable recommendations based on novelty scores and prior art analysis
              </p>
            </div>

            <div className="glass-card p-6">
              <div className="w-12 h-12 rounded-xl bg-[var(--warning)]/10 flex items-center justify-center mb-4">
                <Shield className="w-6 h-6 text-[var(--warning)]" />
              </div>
              <h3 className="text-lg font-bold text-[var(--foreground)] mb-2">Compliance Ready</h3>
              <p className="text-sm text-[var(--foreground-muted)]">
                Generate FOB-compliant documentation with audit trails for regulatory requirements
              </p>
            </div>

            <div className="glass-card p-6">
              <div className="w-12 h-12 rounded-xl bg-[var(--error)]/10 flex items-center justify-center mb-4">
                <Search className="w-6 h-6 text-[var(--error)]" />
              </div>
              <h3 className="text-lg font-bold text-[var(--foreground)] mb-2">Global Database Search</h3>
              <p className="text-sm text-[var(--foreground-muted)]">
                Search multiple patent databases including USPTO, EPO, and WIPO simultaneously
              </p>
            </div>

            <div className="glass-card p-6">
              <div className="w-12 h-12 rounded-xl bg-[var(--info)]/10 flex items-center justify-center mb-4">
                <Bot className="w-6 h-6 text-[var(--info)]" />
              </div>
              <h3 className="text-lg font-bold text-[var(--foreground)] mb-2">Multi-Agent AI</h3>
              <p className="text-sm text-[var(--foreground-muted)]">
                Specialized AI agents working in coordination through IBM watsonx Orchestrate
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="relative py-24 border-t border-[var(--border)] overflow-hidden">
        {/* Background */}
        <div className="absolute inset-0 bg-gradient-to-b from-[var(--primary)]/5 to-transparent" />
        <div className="glow-orb top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2" />

        <div className="relative container mx-auto px-6 text-center">
          <h2 className="text-4xl md:text-5xl font-bold text-[var(--foreground)] mb-6">
            Ready to Transform Your Innovation Pipeline?
          </h2>
          <p className="text-lg text-[var(--foreground-muted)] max-w-2xl mx-auto mb-10">
            Join the Philippine IMPACT Network in revolutionizing technology transfer
            with AI-powered orchestration.
          </p>
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
            <SignedOut>
              <SignUpButton mode="modal">
                <button className="btn btn-gradient btn-lg group">
                  <span>Start Analyzing Now</span>
                  <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
                </button>
              </SignUpButton>
            </SignedOut>
            <SignedIn>
              <Link href="/dashboard" className="btn btn-gradient btn-lg group">
                <span>Go to Dashboard</span>
                <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
              </Link>
            </SignedIn>
          </div>
        </div>
      </section>
    </div>
  );
}
