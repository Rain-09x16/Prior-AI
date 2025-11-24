# Prior Art Analyst (VANTAGE)

**AI-powered patent prior art analysis platform that reduces analysis time from 10-15 hours to minutes.**

A modern web application built with Next.js and FastAPI for automating patent prior art searches and patentability assessments.

---

## 🎯 Overview

Prior Art Analyst helps Technology Transfer Offices (TTOs) and patent professionals quickly analyze invention disclosures for patentability and prior art. The platform uses AI to:

- **Assess patentability** before expensive prior art searches
- **Extract key claims** and innovations from disclosures
- **Search patent databases** for similar patents
- **Score similarity** between disclosure and prior art
- **Generate recommendations** (pursue, reconsider, or reject)
- **Produce PDF reports** for documentation

---

## ✨ Features

### Core Functionality
- ✅ **Document Upload** - Drag-and-drop PDF/DOCX support with file validation
- ✅ **Patentability Assessment** - AI-powered filter to identify publishable vs patentable research
- ✅ **Claim Extraction** - Automated extraction of background, innovations, and keywords
- ✅ **Patent Search** - Integration with Google Patents API
- ✅ **Similarity Scoring** - Semantic comparison between disclosure and patents
- ✅ **Smart Recommendations** - AI-driven patentability recommendations with reasoning
- ✅ **PDF Report Generation** - Professional reports with ReportLab
- ✅ **Real-time Status Updates** - Live analysis progress with polling

### User Interface
- ✅ **Modern Design** - Clean, responsive UI with Tailwind CSS
- ✅ **Authentication** - Secure user authentication with Clerk
- ✅ **Dashboard** - Upload and manage multiple analyses
- ✅ **Analysis Detail View** - Comprehensive results with patent comparisons
- ✅ **Patentability Alerts** - Color-coded warnings (green/yellow/red)
- ✅ **Skeleton Loading** - Smooth loading states
- ✅ **Dark Mode Ready** - Infrastructure in place (light theme enforced)

### Technical Features
- ✅ **REST API** - FastAPI with automatic OpenAPI documentation
- ✅ **Database Persistence** - SQLite with SQLAlchemy ORM
- ✅ **Type Safety** - Full TypeScript on frontend, Pydantic on backend
- ✅ **State Management** - Zustand for client state
- ✅ **Error Handling** - Comprehensive error handling and validation
- ✅ **API Client** - Centralized API client with interceptors

---

## 🏗️ Architecture

### Tech Stack

**Frontend:**
- Next.js 16.0.3 (App Router)
- React 19.2.0
- TypeScript
- Tailwind CSS 4
- Zustand (State Management)
- Clerk (Authentication)
- Lucide React (Icons)

**Backend:**
- FastAPI
- Python 3.11+
- SQLAlchemy (ORM)
- SQLite (Database)
- Pydantic (Validation)
- PyPDF2 & python-docx (Document Parsing)
- ReportLab (PDF Generation)

**AI/ML Services (Ready for Integration):**
- watsonx NLU - Natural language understanding
- watsonx.ai - Similarity scoring and patentability assessment
- Google Patents API - Patent search

### Project Structure

```
Prior-AI/
├── frontend/                    # Next.js application
│   ├── src/
│   │   ├── app/                # App router pages
│   │   │   ├── page.tsx        # Landing page
│   │   │   ├── dashboard/      # Upload dashboard
│   │   │   │   └── page.tsx
│   │   │   ├── analyses/       # Analysis list & detail
│   │   │   │   ├── page.tsx    # All analyses list
│   │   │   │   └── [id]/       # Individual analysis
│   │   │   │       └── page.tsx
│   │   │   └── layout.tsx      # Root layout
│   │   ├── components/         # React components
│   │   │   ├── Header.tsx
│   │   │   ├── AuthProvider.tsx
│   │   │   ├── FileUpload.tsx
│   │   │   ├── AnalysisCard.tsx
│   │   │   ├── PatentCard.tsx
│   │   │   ├── PatentabilityAlert.tsx
│   │   │   ├── SkeletonCard.tsx
│   │   │   └── ProgressBar.tsx
│   │   ├── lib/                # Utilities
│   │   │   ├── api.ts          # API client
│   │   │   ├── types.ts        # TypeScript types
│   │   │   └── utils.ts        # Helper functions
│   │   └── stores/             # Zustand stores
│   │       └── analysisStore.ts
│   └── package.json
│
├── backend/                     # FastAPI application
│   ├── app/
│   │   ├── main.py             # FastAPI app entry
│   │   ├── config.py           # Configuration
│   │   ├── database.py         # Database config
│   │   ├── models/             # SQLAlchemy models
│   │   │   ├── analysis.py
│   │   │   ├── patent.py
│   │   │   └── orchestrate_log.py
│   │   ├── schemas/            # Pydantic schemas
│   │   │   ├── analysis.py
│   │   │   └── patent.py
│   │   ├── api/v1/             # API endpoints
│   │   │   ├── analyses.py
│   │   │   ├── health.py
│   │   │   └── skills.py
│   │   ├── services/           # Business logic
│   │   │   ├── document_parser.py
│   │   │   ├── patent_searcher.py
│   │   │   ├── report_generator.py
│   │   │   ├── orchestrate.py
│   │   │   ├── orchestrate_new.py
│   │   │   └── orchestrate_v3_1.py
│   │   ├── ml_services/        # AI/ML modules
│   │   │   ├── claim_extractor.py
│   │   │   ├── similarity_scorer.py
│   │   │   └── recommender.py
│   │   ├── integrations/       # External services
│   │   │   ├── watsonx_nlu.py
│   │   │   ├── watsonx_ai.py
│   │   │   ├── watsonx_orchestrate.py
│   │   │   └── google_patents.py
│   │   └── utils/
│   │       ├── logger.py
│   │       ├── clerk_auth.py
│   │       └── file_handler.py
│   ├── requirements.txt
│   └── .env.example
│
└── README.md
```

---

## 🌐 Live Demo

- **Frontend**: [https://frontend-8gi274h58-aritra-sahas-projects-af9b1f5c.vercel.app](https://frontend-8gi274h58-aritra-sahas-projects-af9b1f5c.vercel.app)
- **Backend API**: [https://prior-art-analyst-api.onrender.com](https://prior-art-analyst-api.onrender.com)
- **API Documentation**: [https://prior-art-analyst-api.onrender.com/docs](https://prior-art-analyst-api.onrender.com/docs)

---

## 🚀 Quick Start

### Prerequisites

- **Node.js** 18+ and npm
- **Python** 3.11+
- **Clerk Account** (for authentication)
- **IBM watsonx Account** (optional - for AI features)

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/prior-ai.git
cd prior-ai
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env with your credentials

# Initialize database
python -c "from app.database import Base, engine; Base.metadata.create_all(bind=engine)"

# Run backend server
uvicorn app.main:app --reload
```

Backend will be available at: `http://localhost:8000`
API documentation: `http://localhost:8000/docs`

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Configure environment variables
# Create .env.local with:
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=your_clerk_key
CLERK_SECRET_KEY=your_clerk_secret

# Run development server
npm run dev
```

Frontend will be available at: `http://localhost:3000`

---

## 📖 Usage

### Basic Workflow

1. **Sign Up/Sign In** - Create an account or sign in with Clerk
2. **Upload Document** - Drag and drop a PDF or DOCX invention disclosure
3. **View Analysis** - Real-time progress updates as the system analyzes
4. **Review Results**:
   - Patentability assessment with confidence score
   - Novelty score and recommendation
   - Similar patents with similarity scores
   - Extracted claims and keywords
5. **Download Report** - Generate a professional PDF report

### API Endpoints

```bash
# Create new analysis
POST /api/v1/analyses
Content-Type: multipart/form-data
Body: file (PDF/DOCX)

# Get analysis by ID
GET /api/v1/analyses/{id}

# List all analyses
GET /api/v1/analyses?status=completed

# Generate PDF report
POST /api/v1/analyses/{id}/report

# Delete analysis
DELETE /api/v1/analyses/{id}

# Health check
GET /api/v1/health
```

### Response Schema

```typescript
interface Analysis {
  id: string;
  title: string;
  status: 'processing' | 'completed' | 'failed';

  // Disclosure info
  disclosure: {
    filename: string;
    uploadedAt: string;
  };

  // Patentability assessment
  patentabilityAssessment?: {
    isPatentable: boolean;
    confidence: number;
    missingElements?: string[];
    recommendations?: string[];
  };

  // Extracted claims
  extractedClaims?: {
    background: string;
    innovations: string[];
    keywords: string[];
    ipcClassifications?: string[];
  };

  // Similar patents
  patents?: Array<{
    patentId: string;
    title: string;
    abstract: string;
    similarityScore: number;
    overlappingConcepts?: string[];
    keyDifferences?: string[];
  }>;

  // Overall assessment
  noveltyScore?: number;
  recommendation?: 'pursue' | 'reconsider' | 'reject';
  reasoning?: string;

  createdAt: string;
  completedAt?: string;
}
```

---

## 🎨 UI Components

### Key Components

- **`Header`** - Responsive navigation with authentication
- **`FileUpload`** - Drag-and-drop file uploader with validation
- **`AnalysisCard`** - Analysis summary card with status badges
- **`PatentCard`** - Expandable patent information card
- **`PatentabilityAlert`** - Color-coded patentability warnings
- **`SkeletonCard`** - Loading placeholder components
- **`ProgressBar`** - Animated progress indicator

### Design System

- **Colors**: Blue (#3b82f6) primary, semantic colors for states
- **Typography**: System fonts with responsive sizing
- **Spacing**: Consistent 8px grid system
- **Borders**: 2px for emphasis, rounded corners
- **Shadows**: Elevation system (sm, md, lg, xl)
- **Animations**: Smooth transitions and hover effects
- **Accessibility**: WCAG 2.1 AA compliant, 44px touch targets

---

## 🧪 Development

### Running Tests

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

### Code Quality

```bash
# Backend linting
cd backend
flake8 app/
black app/

# Frontend linting
cd frontend
npm run lint
```

### Environment Variables

**Backend (.env):**
```bash
DATABASE_URL=sqlite:///./priorai.db
WATSONX_API_KEY=your_api_key
WATSONX_PROJECT_ID=your_project_id
WATSONX_NLU_URL=https://api.us-south.natural-language-understanding.watson.cloud.ibm.com
```

**Frontend (.env.local):**
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_test_xxx
CLERK_SECRET_KEY=sk_test_xxx
```

---

## 🚢 Deployment

### Backend (Railway/Render)

1. Create new project
2. Connect GitHub repository
3. Set environment variables
4. Deploy from `backend` directory

### Frontend (Vercel/Netlify)

1. Import GitHub repository
2. Set build settings:
   - Build command: `npm run build`
   - Output directory: `.next`
3. Set environment variables
4. Deploy

---

## 🔮 Future Enhancements

### AI/ML Improvements
- **Enhanced NLU Models** - Fine-tuned watsonx models for patent-specific language
- **Multi-language Support** - Analyze patents in multiple languages
- **Image Analysis** - Extract innovation from patent diagrams and figures
- **Citation Network Analysis** - Map patent citation relationships

### Feature Additions
- **Collaborative Workflows** - Team review and approval processes
- **Automated Filing** - Direct integration with patent filing systems
- **Prior Art Watch** - Continuous monitoring for new related patents
- **Competitive Intelligence** - Track competitor patent activities
- **Portfolio Management** - Manage entire patent portfolios
- **Cost Estimator** - Predict patent filing and prosecution costs

### Technical Enhancements
- **Advanced Caching** - Redis for faster repeated queries
- **Microservices Architecture** - Scale individual components independently
- **GraphQL API** - More flexible data querying
- **Real-time Collaboration** - WebSocket-based live updates
- **Enhanced Security** - SOC 2 compliance, data encryption at rest

### Integration Capabilities
- **Patent Office APIs** - Direct USPTO, EPO, WIPO integration
- **Research Databases** - arXiv, IEEE Xplore, PubMed integration
- **CRM Integration** - Salesforce, HubSpot for IP management
- **Slack/Teams Notifications** - Real-time analysis updates
- **Zapier/Make Integration** - Connect with 1000+ apps

### Analytics & Insights
- **Portfolio Analytics** - Dashboard for TTO performance metrics
- **Trend Analysis** - Identify emerging technology trends
- **Success Prediction** - ML-based patent success likelihood
- **ROI Calculator** - Measure IP portfolio value

---

## 📊 Market Opportunity

**Total Addressable Market (TAM)**: $8B
- Global IP management software market
- Patent analytics and prior art search services
- Technology transfer office operations

**Serviceable Addressable Market (SAM)**: $1.2B
- US universities and research institutions (200+ major TTOs)
- Corporate R&D departments (Fortune 500 companies)
- Patent law firms and IP consultancies

**Revenue Model**:
- **Freemium Tier**: 5 analyses/month (free)
- **Professional**: $99/month (50 analyses)
- **Enterprise**: Custom pricing (unlimited, dedicated support)
- **API Access**: $0.10 per analysis for third-party integrations

**Competitive Advantage**:
- ✅ **10x faster** than manual prior art searches (minutes vs 10-15 hours)
- ✅ **AI-powered patentability filter** - saves $5K-$15K on unnecessary searches
- ✅ **Integrated workflow** - from upload to report in one platform
- ✅ **watsonx integration** - enterprise-grade AI with explainability
- ✅ **Modern UX** - designed for non-technical users (TTOs, researchers)

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **IBM watsonx** for AI/ML capabilities
- **Clerk** for authentication services
- **Google Patents** for patent data access
- **Tailwind CSS** for the design system
- **FastAPI** and **Next.js** communities

---

## 📞 Support

For questions or issues:
- Open an issue on GitHub
- Check the API documentation at `/docs`
# Deployment trigger
