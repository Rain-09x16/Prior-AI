'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { SignedIn, SignedOut, SignInButton, UserButton } from '@clerk/nextjs';
import { FileText, Upload, List, LogIn } from 'lucide-react';

export function Header() {
  const pathname = usePathname();
  const isActive = (path: string) => pathname === path;
  const isPublic = pathname === '/';

  return (
    <header className="border-b-2 border-gray-200 bg-white sticky top-0 z-50 shadow-sm">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16 md:h-18">
          <Link href="/" className="flex items-center space-x-3 hover:opacity-90 transition-all group">
            <div className="p-2 bg-blue-600 rounded-lg group-hover:bg-blue-700 transition-colors">
              <FileText className="h-6 w-6 text-white" />
            </div>
            <div className="flex flex-col">
              <span className="font-bold text-xl text-gray-900 leading-tight">VANTAGE</span>
              <span className="text-xs text-gray-500 font-medium">TTO Operating System</span>
            </div>
          </Link>

          <div className="flex items-center gap-1">
            {!isPublic && (
              <nav className="flex items-center gap-1 mr-4">
                <SignedIn>
                  <Link
                    href="/dashboard"
                    className={`flex items-center gap-2 px-4 py-2.5 rounded-lg transition-all font-medium min-h-10 ${
                      isActive('/dashboard') ? 'bg-blue-100 text-blue-700 shadow-sm' : 'text-gray-600 hover:bg-gray-100'
                    }`}
                  >
                    <Upload className="h-4 w-4" />
                    <span>Upload</span>
                  </Link>

                  <Link
                    href="/analyses"
                    className={`flex items-center gap-2 px-4 py-2.5 rounded-lg transition-all font-medium min-h-10 ${
                      isActive('/analyses') ? 'bg-blue-100 text-blue-700 shadow-sm' : 'text-gray-600 hover:bg-gray-100'
                    }`}
                  >
                    <List className="h-4 w-4" />
                    <span>All Analyses</span>
                  </Link>
                </SignedIn>
              </nav>
            )}

            <SignedOut>
              <SignInButton mode="modal">
                <button className="flex items-center gap-2 px-5 py-2.5 text-gray-700 hover:bg-gray-100 rounded-lg transition-all font-medium min-h-10 border-2 border-transparent hover:border-gray-200">
                  <LogIn className="h-4 w-4" />
                  <span>Sign In</span>
                </button>
              </SignInButton>
            </SignedOut>

            <SignedIn>
              <UserButton
                afterSignOutUrl="/"
                appearance={{
                  elements: {
                    avatarBox: "h-9 w-9"
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
