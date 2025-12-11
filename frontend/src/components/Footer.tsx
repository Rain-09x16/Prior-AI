'use client';

import { Zap, Github, Twitter, Linkedin, ExternalLink } from 'lucide-react';

export function Footer() {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="relative border-t border-[var(--border)] bg-[var(--background)]">
      {/* Gradient overlay */}
      <div className="absolute inset-0 bg-gradient-to-t from-[var(--primary)]/5 to-transparent pointer-events-none" />

      <div className="relative container mx-auto px-6 py-16">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-12">
          {/* Brand */}
          <div className="lg:col-span-1">
            <div className="flex items-center gap-3 mb-4">
              <div className="flex items-center justify-center w-10 h-10 rounded-xl bg-gradient-to-br from-[var(--primary)] to-[var(--accent)]">
                <Zap className="w-5 h-5 text-white" />
              </div>
              <span className="text-xl font-bold text-[var(--foreground)]">VANTAGE</span>
            </div>
            <p className="text-sm text-[var(--foreground-muted)] leading-relaxed mb-6">
              The TTO Operating System transforming innovation ecosystems
              in emerging markets. From regulatory compliance to commercial success.
            </p>
            <div className="flex items-center gap-3">
              <a
                href="#"
                className="flex items-center justify-center w-9 h-9 rounded-lg bg-[var(--surface)] hover:bg-[var(--surface-hover)] text-[var(--foreground-muted)] hover:text-[var(--foreground)] transition-all"
              >
                <Twitter className="w-4 h-4" />
              </a>
              <a
                href="#"
                className="flex items-center justify-center w-9 h-9 rounded-lg bg-[var(--surface)] hover:bg-[var(--surface-hover)] text-[var(--foreground-muted)] hover:text-[var(--foreground)] transition-all"
              >
                <Github className="w-4 h-4" />
              </a>
              <a
                href="#"
                className="flex items-center justify-center w-9 h-9 rounded-lg bg-[var(--surface)] hover:bg-[var(--surface-hover)] text-[var(--foreground-muted)] hover:text-[var(--foreground)] transition-all"
              >
                <Linkedin className="w-4 h-4" />
              </a>
            </div>
          </div>

          {/* Powered By */}
          <div>
            <h3 className="text-sm font-semibold text-[var(--foreground)] uppercase tracking-wider mb-4">
              Powered By
            </h3>
            <ul className="space-y-3">
              <li>
                <a href="https://www.ibm.com/watsonx" target="_blank" rel="noopener noreferrer" className="flex items-center gap-2 text-sm text-[var(--foreground-muted)] hover:text-[var(--foreground)] transition-colors group">
                  <span className="w-2 h-2 rounded-full bg-[var(--primary)]" />
                  IBM watsonx Orchestrate
                  <ExternalLink className="w-3 h-3 opacity-0 group-hover:opacity-100 transition-opacity" />
                </a>
              </li>
              <li>
                <span className="flex items-center gap-2 text-sm text-[var(--foreground-muted)]">
                  <span className="w-2 h-2 rounded-full bg-[var(--accent)]" />
                  IBM Granite AI Models
                </span>
              </li>
              <li>
                <span className="flex items-center gap-2 text-sm text-[var(--success)]">
                  <span className="w-2 h-2 rounded-full bg-[var(--success)]" />
                  60 Real USPTO Patents Dataset
                </span>
              </li>
              <li>
                <span className="flex items-center gap-2 text-sm text-[var(--success)]">
                  <span className="w-2 h-2 rounded-full bg-[var(--success)]" />
                  85% Validated Accuracy
                </span>
              </li>
            </ul>
          </div>

          {/* Resources */}
          <div>
            <h3 className="text-sm font-semibold text-[var(--foreground)] uppercase tracking-wider mb-4">
              Resources
            </h3>
            <ul className="space-y-3">
              <li>
                <a href="#" className="text-sm text-[var(--foreground-muted)] hover:text-[var(--foreground)] transition-colors">
                  Documentation
                </a>
              </li>
              <li>
                <a href="#" className="text-sm text-[var(--foreground-muted)] hover:text-[var(--foreground)] transition-colors">
                  API Reference
                </a>
              </li>
              <li>
                <a href="#" className="text-sm text-[var(--foreground-muted)] hover:text-[var(--foreground)] transition-colors">
                  Compliance Guide
                </a>
              </li>
              <li>
                <a href="#" className="text-sm text-[var(--foreground-muted)] hover:text-[var(--foreground)] transition-colors">
                  Case Studies
                </a>
              </li>
            </ul>
          </div>

          {/* Built For Impact */}
          <div>
            <h3 className="text-sm font-semibold text-[var(--foreground)] uppercase tracking-wider mb-4">
              Built For Impact
            </h3>
            <div className="p-4 rounded-xl bg-[var(--surface)] border border-[var(--border)]">
              <p className="text-sm text-[var(--foreground-muted)] mb-3">
                An AI-powered platform for technology transfer offices
              </p>
              <div className="flex items-center gap-2">
                <span className="badge badge-primary badge-pill text-xs">
                  Open Source
                </span>
              </div>
            </div>
            <p className="text-xs text-[var(--foreground-muted)] mt-4">
              Addressing the $500B emerging market innovation gap
            </p>
          </div>
        </div>

        {/* Bottom Bar */}
        <div className="mt-12 pt-8 border-t border-[var(--border)]">
          <div className="flex flex-col md:flex-row items-center justify-between gap-4">
            <p className="text-sm text-[var(--foreground-muted)]">
              © {currentYear} VANTAGE
            </p>
            <div className="flex items-center gap-6">
              <a href="#" className="text-xs text-[var(--foreground-muted)] hover:text-[var(--foreground)] transition-colors">
                Privacy Policy
              </a>
              <a href="#" className="text-xs text-[var(--foreground-muted)] hover:text-[var(--foreground)] transition-colors">
                Terms of Service
              </a>
              <a href="#" className="text-xs text-[var(--foreground-muted)] hover:text-[var(--foreground)] transition-colors">
                Cookie Policy
              </a>
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
}
