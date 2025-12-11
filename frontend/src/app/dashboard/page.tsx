'use client';

import { useRouter } from 'next/navigation';
import { FileUpload } from '@/components/FileUpload';
import { useAnalysisStore } from '@/stores/analysisStore';
import { Sparkles, Clock, Target, Shield, Zap, Bot, ArrowRight } from 'lucide-react';

export default function DashboardPage() {
  const router = useRouter();
  const createAnalysis = useAnalysisStore((state) => state.createAnalysis);

  const handleUpload = async (file: File) => {
    try {
      const analysisId = await createAnalysis(file);
      router.push(`/analyses/${analysisId}`);
    } catch (error) {
      console.error('Upload failed:', error);
      throw error;
    }
  };

  return (
    <div className="min-h-screen bg-background pt-24 pb-16">
      {/* Hero Section */}
      <section className="relative">
        {/* Background gradient */}
        <div className="absolute inset-0 hero-gradient opacity-50" />

        <div className="relative container mx-auto px-6">
          {/* Header */}
          <div className="text-center mb-12">
            <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-surface border border-border mb-6">
              <Bot className="w-4 h-4 text-primary" />
              <span className="text-sm font-medium text-foreground-muted">
                Powered by IBM watsonx Orchestrate
              </span>
            </div>

            <h1 className="text-4xl md:text-5xl font-bold text-foreground mb-4">
              AI-Powered Prior Art Analysis
            </h1>
            <p className="text-lg text-foreground-muted max-w-2xl mx-auto">
              Reduce patent prior art analysis from 10-15 hours to 15 minutes using
              advanced AI and machine learning
            </p>
          </div>

          {/* Upload Section */}
          <div className="max-w-3xl mx-auto mb-16">
            <FileUpload onUpload={handleUpload} />
          </div>

          {/* Features Grid */}
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6 max-w-6xl mx-auto">
            <div className="glass-card p-6 text-center">
              <div className="inline-flex items-center justify-center w-12 h-12 rounded-xl bg-primary/10 mb-4">
                <Sparkles className="w-6 h-6 text-primary" />
              </div>
              <h3 className="font-semibold text-foreground mb-2">AI-Powered</h3>
              <p className="text-sm text-foreground-muted">
                Advanced NLU and ML algorithms for accurate claim extraction
              </p>
            </div>

            <div className="glass-card p-6 text-center">
              <div className="inline-flex items-center justify-center w-12 h-12 rounded-xl bg-success/10 mb-4">
                <Clock className="w-6 h-6 text-success" />
              </div>
              <h3 className="font-semibold text-foreground mb-2">Save Time</h3>
              <p className="text-sm text-foreground-muted">
                Complete analysis in minutes instead of hours
              </p>
            </div>

            <div className="glass-card p-6 text-center">
              <div className="inline-flex items-center justify-center w-12 h-12 rounded-xl bg-accent/10 mb-4">
                <Target className="w-6 h-6 text-accent" />
              </div>
              <h3 className="font-semibold text-foreground mb-2">Smart Recommendations</h3>
              <p className="text-sm text-foreground-muted">
                Get actionable recommendations based on novelty scores
              </p>
            </div>

            <div className="glass-card p-6 text-center">
              <div className="inline-flex items-center justify-center w-12 h-12 rounded-xl bg-warning/10 mb-4">
                <Shield className="w-6 h-6 text-warning" />
              </div>
              <h3 className="font-semibold text-foreground mb-2">Comprehensive</h3>
              <p className="text-sm text-foreground-muted">
                Search multiple patent databases and generate detailed reports
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section className="py-20">
        <div className="container mx-auto px-6">
          <div className="text-center mb-12">
            <span className="badge badge-primary badge-pill mb-4">How It Works</span>
            <h2 className="text-3xl font-bold text-foreground">
              Four Simple Steps
            </h2>
          </div>

          <div className="max-w-4xl mx-auto">
            <div className="space-y-6">
              {[
                {
                  step: 1,
                  title: 'Upload Disclosure',
                  description: 'Upload your invention disclosure document (PDF or DOCX format)',
                  icon: Zap,
                },
                {
                  step: 2,
                  title: 'AI Analysis',
                  description: 'Our AI extracts claims, searches patent databases, and scores similarity',
                  icon: Bot,
                },
                {
                  step: 3,
                  title: 'Review Results',
                  description: 'Get novelty scores, recommendations, and detailed patent comparisons',
                  icon: Target,
                },
                {
                  step: 4,
                  title: 'Generate Report',
                  description: 'Download a comprehensive PDF report for your records',
                  icon: Shield,
                },
              ].map((item, index) => (
                <div
                  key={item.step}
                  className="flex items-start gap-6 p-6 rounded-2xl bg-background-secondary border border-border hover:border-primary/50 transition-all group"
                >
                  <div className="flex-shrink-0">
                    <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-primary to-accent flex items-center justify-center text-white font-bold text-lg shadow-lg shadow-primary/25">
                      {item.step}
                    </div>
                  </div>
                  <div className="flex-1">
                    <h3 className="text-lg font-semibold text-foreground mb-1 group-hover:text-primary transition-colors">
                      {item.title}
                    </h3>
                    <p className="text-foreground-muted">
                      {item.description}
                    </p>
                  </div>
                  <div className="hidden md:flex items-center">
                    <ArrowRight className="w-5 h-5 text-foreground-muted group-hover:text-primary group-hover:translate-x-1 transition-all" />
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}
