'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { SignedIn, SignedOut, SignInButton, UserButton } from '@clerk/nextjs';
import { Zap, Upload, BarChart3, ArrowRight } from 'lucide-react';

export function Header() {
  const pathname = usePathname();
  const isActive = (path: string) => pathname === path;
  const isPublic = pathname === '/';

  return (
    <header className="fixed top-0 left-0 right-0 z-50 border-b border-[var(--border)] bg-[var(--background)]/80 backdrop-blur-xl">
      <div className="container mx-auto px-6">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link href="/" className="flex items-center gap-3 group">
            <div className="relative">
              <div className="absolute inset-0 bg-[var(--primary)] blur-lg opacity-50 group-hover:opacity-75 transition-opacity" />
              <div className="relative flex items-center justify-center w-9 h-9 rounded-xl bg-gradient-to-br from-[var(--primary)] to-[var(--accent)] shadow-lg">
                <Zap className="w-5 h-5 text-white" />
              </div>
            </div>
            <div className="flex flex-col">
              <span className="text-lg font-bold text-[var(--foreground)] tracking-tight">
                VANTAGE
              </span>
              <span className="text-[10px] font-medium text-[var(--foreground-muted)] tracking-wider uppercase">
                TTO Operating System
              </span>
            </div>
          </Link>

          {/* Navigation */}
          <div className="flex items-center gap-1">
            {!isPublic && (
              <nav className="hidden md:flex items-center gap-1 mr-6">
                <SignedIn>
                  <Link
                    href="/dashboard"
                    className={`nav-pill ${isActive('/dashboard') ? 'active' : ''}`}
                  >
                    <Upload className="w-4 h-4" />
                    <span>Upload</span>
                  </Link>

                  <Link
                    href="/analyses"
                    className={`nav-pill ${isActive('/analyses') ? 'active' : ''}`}
                  >
                    <BarChart3 className="w-4 h-4" />
                    <span>Analyses</span>
                  </Link>
                </SignedIn>
              </nav>
            )}

            <SignedOut>
              <SignInButton mode="modal">
                <button className="btn btn-primary btn-sm group">
                  <span>Get Started</span>
                  <ArrowRight className="w-4 h-4 group-hover:translate-x-0.5 transition-transform" />
                </button>
              </SignInButton>
            </SignedOut>

            <SignedIn>
              <UserButton
                afterSignOutUrl="/"
                appearance={{
                  elements: {
                    avatarBox: "w-9 h-9 ring-2 ring-[var(--border)] ring-offset-2 ring-offset-[var(--background)]",
                    userButtonPopoverCard: "bg-[var(--background-secondary)] border border-[var(--border)]",
                    userButtonPopoverActions: "bg-[var(--background-secondary)]",
                    userButtonPopoverActionButton: "hover:bg-[var(--surface)]",
                    userButtonPopoverFooter: "hidden"
                  }
                }}
              />
            </SignedIn>
          </div>
        </div>
      </div>
    </header>
  );
}
