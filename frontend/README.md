# Frontend - VANTAGE

Next.js 14 frontend application for AI-powered patent prior art analysis.

## 🚀 Quick Start

### 1. Install Dependencies

```bash
npm install
# or
yarn install
# or
pnpm install
```

### 2. Configure Environment

```bash
# Copy environment template
cp .env.local.example .env.local

# Edit .env.local with your backend URL
```

Required environment variables:
```bash
# Backend API URL
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

### 3. Run Development Server

```bash
npm run dev
# or
yarn dev
# or
pnpm dev
```

**Application URLs:**
- Development: http://localhost:3000
- Production: https://your-domain.vercel.app

---

## 📁 Project Structure

```
frontend/
├── app/                             # Next.js 14 App Router
│   ├── layout.tsx                   # Root layout with metadata
│   ├── page.tsx                     # Home page (upload interface)
│   ├── globals.css                  # Global styles & Tailwind
│   └── analyses/                    # Analysis routes
│       ├── page.tsx                 # Analyses list page
│       └── [id]/                    # Dynamic analysis route
│           └── page.tsx             # Analysis details page
│
├── components/                      # React Components
│   ├── Header.tsx                   # Navigation header
│   ├── Footer.tsx                   # Footer component
│   ├── FileUpload.tsx               # Drag-and-drop file upload
│   ├── AnalysisCard.tsx             # Analysis summary card
│   ├── PatentCard.tsx               # Patent match card
│   ├── PatentabilityAlert.tsx       # Patentability assessment alert
│   ├── LoadingSpinner.tsx           # Loading indicator
│   └── Button.tsx                   # Reusable button component
│
├── stores/                          # Zustand State Management
│   └── analysisStore.ts             # Global analysis state
│
├── lib/                             # Utilities & Configuration
│   ├── api.ts                       # API client (Axios)
│   ├── types.ts                     # TypeScript type definitions
│   └── utils.ts                     # Utility functions
│
├── public/                          # Static Assets
│   ├── favicon.ico                  # Favicon
│   └── images/                      # Image assets
│
├── tailwind.config.ts               # Tailwind CSS configuration
├── tsconfig.json                    # TypeScript configuration
├── next.config.js                   # Next.js configuration
├── package.json                     # Dependencies
└── .env.local.example               # Environment template
```

---

## ✨ Features

### 🏠 Home Page (`/`)

**Hero Section:**
- Clear value proposition
- Key benefits highlighted
- CTA button for file upload

**File Upload Section:**
- Drag-and-drop interface
- Click to browse files
- Supported formats: PDF, DOCX
- File size limit: 10MB
- Real-time upload progress
- Automatic redirect to analysis page

**How It Works:**
1. Upload disclosure document
2. AI analyzes patentability
3. Search prior art patents
4. Get novelty assessment
5. Download PDF report

### 📊 Analyses List (`/analyses`)

**Features:**
- Paginated list of all analyses
- Filter by status:
  - Processing (in progress)
  - Completed (with results)
  - Failed (with error messages)
- Sort by date (newest first)
- Quick view cards showing:
  - Document title
  - Upload date
  - Status badge
  - Novelty score (if completed)
  - Recommendation badge
- Delete analysis action
- Click card to view details

### 📝 Analysis Details (`/analyses/[id]`)

**Real-time Updates:**
- Auto-polling for processing analyses
- Status updates every 3 seconds
- Progress indicators

**Patentability Assessment Section:**
- Color-coded alert (green/yellow/red)
- Patentable: Green with checkmark
- Borderline: Yellow with warning
- Not Patentable: Red with X
- Confidence score display
- Missing elements list
- Recommendations to improve patentability
- Cost savings tracker

**Extracted Claims Section:**
- Background summary
- Key innovations list
- Technical specifications
- Extracted keywords (chips)
- IPC classifications

**Prior Art Patents Section:**
- Patent cards with:
  - Patent ID with link to Google Patents
  - Title and abstract
  - Similarity score (color-coded)
  - Publication date
  - Inventors
  - Assignee
- Expandable details
- Sorted by similarity score (highest first)

**Overall Assessment:**
- Novelty score gauge (0-100)
- Recommendation badge:
  - 🟢 PURSUE (novelty ≥70%)
  - 🟡 RECONSIDER (40-70%)
  - 🔴 REJECT (novelty <40%)
- Reasoning explanation

**Actions:**
- Generate PDF Report button
- Download report (opens in new tab)
- Delete analysis
- Back to list

---

## 🎨 UI/UX Design

### Color Scheme

```css
/* Primary Colors */
--primary: #3B82F6;        /* Blue - primary actions */
--primary-dark: #2563EB;   /* Darker blue - hover states */

/* Status Colors */
--success: #10B981;        /* Green - patentable, pursue */
--warning: #F59E0B;        /* Yellow - borderline, reconsider */
--error: #EF4444;          /* Red - not patentable, reject */
--info: #06B6D4;           /* Cyan - information */

/* Neutrals */
--gray-50: #F9FAFB;
--gray-100: #F3F4F6;
--gray-200: #E5E7EB;
--gray-600: #4B5563;
--gray-900: #111827;
```

### Typography

- **Headings**: Inter font family, bold weights
- **Body**: Inter font family, normal weight
- **Code**: Monospace font for patent IDs

### Components

**Badges:**
- Status badges (processing, completed, failed)
- Recommendation badges (pursue, reconsider, reject)
- Rounded corners, contrasting colors

**Cards:**
- Elevated shadow on hover
- Smooth transitions
- Consistent padding and spacing

**Buttons:**
- Primary: Blue background, white text
- Secondary: White background, gray border
- Danger: Red background, white text
- Disabled state: Grayed out

---

## 🔄 State Management

### Zustand Store (`stores/analysisStore.ts`)

```typescript
interface AnalysisStore {
  // State
  analyses: Analysis[];
  currentAnalysis: Analysis | null;
  isLoading: boolean;
  error: string | null;

  // Actions
  fetchAnalyses: (params?: ListParams) => Promise<void>;
  fetchAnalysis: (id: string) => Promise<void>;
  createAnalysis: (file: File, title?: string) => Promise<Analysis>;
  deleteAnalysis: (id: string) => Promise<void>;
  pollAnalysis: (id: string) => Promise<void>;
  generateReport: (id: string) => Promise<void>;
  clearError: () => void;
}
```

### Usage Example

```typescript
'use client';

import { useAnalysisStore } from '@/stores/analysisStore';

export default function AnalysisPage({ params }: { params: { id: string } }) {
  const { currentAnalysis, isLoading, fetchAnalysis, pollAnalysis } = useAnalysisStore();

  useEffect(() => {
    fetchAnalysis(params.id);

    // Poll for updates if processing
    const interval = setInterval(() => {
      if (currentAnalysis?.status === 'processing') {
        pollAnalysis(params.id);
      }
    }, 3000);

    return () => clearInterval(interval);
  }, [params.id]);

  if (isLoading) return <LoadingSpinner />;

  return (
    <div>
      {/* Render analysis details */}
    </div>
  );
}
```

---

## 🔌 API Integration

### API Client (`lib/api.ts`)

**Base Configuration:**
```typescript
const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1',
  headers: {
    'Content-Type': 'application/json',
  },
});
```

**Available Methods:**

```typescript
// Create analysis (file upload)
createAnalysis(file: File, title?: string): Promise<Analysis>

// Get single analysis
getAnalysis(id: string): Promise<Analysis>

// List all analyses
listAnalyses(params?: {
  skip?: number;
  limit?: number;
  status?: 'processing' | 'completed' | 'failed';
}): Promise<Analysis[]>

// Generate PDF report
generateReport(id: string): Promise<Blob>

// Delete analysis
deleteAnalysis(id: string): Promise<void>

// Health check
healthCheck(): Promise<{ status: string }>
```

---

## 📱 Responsive Design

### Breakpoints

```css
/* Mobile */
@media (max-width: 640px) {
  /* Single column layout */
}

/* Tablet */
@media (min-width: 641px) and (max-width: 1024px) {
  /* Two column layout */
}

/* Desktop */
@media (min-width: 1025px) {
  /* Three column layout */
}
```

### Mobile Optimizations

- Stack cards vertically
- Touch-friendly buttons (min 44px height)
- Simplified navigation
- Bottom sheet for actions
- Reduced animations

---

## 🚀 Deployment

### Vercel (Recommended)

**Automatic Deployment:**

1. Push code to GitHub
2. Connect repository to Vercel
3. Configure:
   - **Framework Preset**: Next.js
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `.next`
4. Set environment variable:
   ```
   NEXT_PUBLIC_API_URL=https://your-backend-url.com/api/v1
   ```
5. Deploy

**Manual Deployment:**

```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
vercel

# Set environment variable
vercel env add NEXT_PUBLIC_API_URL
# Enter: https://your-backend-url.com/api/v1

# Deploy to production
vercel --prod
```

### Netlify

1. Connect GitHub repository
2. **Build Command**: `npm run build`
3. **Publish Directory**: `.next`
4. Add environment variable:
   ```
   NEXT_PUBLIC_API_URL=https://your-backend-url.com/api/v1
   ```
5. Deploy

### Manual/Self-Hosted

```bash
# Build for production
npm run build

# Start production server
npm start

# Or use PM2 for process management
npm install -g pm2
pm2 start npm --name "priorai-frontend" -- start
pm2 save
pm2 startup
```

---

## 🔧 Development

### Type Checking

```bash
# Run TypeScript compiler (no emit)
npx tsc --noEmit

# Watch mode
npx tsc --noEmit --watch
```

### Linting

```bash
# Run ESLint
npm run lint

# Fix auto-fixable issues
npm run lint --fix
```

### Code Formatting

```bash
# Install Prettier
npm install --save-dev prettier

# Format code
npx prettier --write "**/*.{ts,tsx,js,jsx,json,css,md}"
```

### Build Analysis

```bash
# Analyze bundle size
npm run build
# Check .next/analyze/ for bundle analysis
```

---

## 🧪 Testing

### Setup Testing (Optional)

```bash
# Install testing libraries
npm install --save-dev @testing-library/react @testing-library/jest-dom jest jest-environment-jsdom
```

### Example Test

```typescript
// components/__tests__/Button.test.tsx
import { render, screen } from '@testing-library/react';
import Button from '../Button';

describe('Button', () => {
  it('renders button with text', () => {
    render(<Button>Click me</Button>);
    expect(screen.getByText('Click me')).toBeInTheDocument();
  });
});
```

---

## 📊 Performance Optimization

### Image Optimization

```typescript
import Image from 'next/image';

<Image
  src="/logo.png"
  alt="Logo"
  width={200}
  height={50}
  priority  // For above-the-fold images
/>
```

### Code Splitting

```typescript
// Dynamic imports for large components
import dynamic from 'next/dynamic';

const HeavyComponent = dynamic(() => import('./HeavyComponent'), {
  loading: () => <LoadingSpinner />,
  ssr: false,  // Disable server-side rendering if needed
});
```

### Font Optimization

```typescript
// app/layout.tsx
import { Inter } from 'next/font/google';

const inter = Inter({
  subsets: ['latin'],
  display: 'swap',  // Prevent FOUT
});
```

---

## 🔒 Security

### Environment Variables

- Never commit `.env.local` to version control
- Use `.env.local.example` as template
- Validate environment variables on build

### API Security

- All API calls use HTTPS in production
- CORS configured on backend
- No sensitive data in localStorage
- XSS protection via React's built-in escaping

---

## 🐛 Troubleshooting

### Common Issues

**Issue: "API connection failed"**
```bash
# Check backend is running
curl http://localhost:8000/api/v1/health

# Verify NEXT_PUBLIC_API_URL in .env.local
cat .env.local
```

**Issue: "Module not found"**
```bash
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

**Issue: "Build failed"**
```bash
# Check TypeScript errors
npx tsc --noEmit

# Check for missing dependencies
npm install
```

**Issue: "Styles not loading"**
```bash
# Rebuild Tailwind CSS
npm run dev  # Restart dev server
```

---

## 📚 Additional Resources

- **Next.js Documentation**: https://nextjs.org/docs
- **Tailwind CSS**: https://tailwindcss.com/docs
- **Zustand**: https://github.com/pmndrs/zustand
- **TypeScript**: https://www.typescriptlang.org/docs

---

## 🔄 Future Enhancements

Potential improvements for future iterations:

- [ ] Add unit tests with Jest
- [ ] Implement E2E tests with Playwright
- [ ] Add accessibility (a11y) improvements
- [ ] Implement dark mode toggle
- [ ] Add internationalization (i18n)
- [ ] Implement Progressive Web App (PWA) features
- [ ] Add analytics tracking
- [ ] Implement error boundary components
- [ ] Add skeleton loaders for better UX
- [ ] Implement infinite scroll for analyses list

---

## 📄 License

MIT

---

## 🙏 Support

For issues or questions:
1. Check [main README](../README.md) for project overview
2. Review [backend documentation](../backend/README.md) for API details
3. Check Next.js documentation for framework-specific issues
4. Open an issue on GitHub

---

**Last Updated:** November 23, 2025
**Version:** 1.0.0 (Hackathon MVP)
**Framework:** Next.js 14 with App Router
**Styling:** Tailwind CSS
**State Management:** Zustand
