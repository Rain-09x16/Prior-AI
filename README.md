# VANTAGE: Prior Art Analyst

> **AI-powered patent prior art analysis platform that reduces analysis time from 10-15 hours to minutes.**

A modern **Hybrid Architecture** web application (Next.js + FastAPI) designed to automate patentability assessments using RAG and Semantic Search.

![Status](https://img.shields.io/badge/Status-Production-success?style=for-the-badge)
![Stack](https://img.shields.io/badge/Stack-Next.js_16_|_FastAPI_|_Python-blue?style=for-the-badge)
![AI](https://img.shields.io/badge/AI-Watsonx_|_OpenAI-purple?style=for-the-badge)

---

## 🎯 Overview

**VANTAGE** helps Technology Transfer Offices (TTOs) and patent professionals accelerate the invention disclosure process. By combining **FastAPI's** data processing capabilities with **Next.js's** interactive UI, the platform uses AI to:

- **Assess Patentability:** Pre-screen disclosures before incurring expensive legal fees.
- **Extract Claims:** NLP-driven extraction of innovations and background context.
- **Semantic Search:** Utilize Vector Embeddings to find conceptually similar patents (not just keywords).
- **Generate Reports:** Automated PDF generation via ReportLab.

---

## ✨ Features

### Core Functionality
- ✅ **Document Ingestion** - Drag-and-drop PDF/DOCX support with binary parsing validation.
- ✅ **Patentability Assessment** - AI-powered filtering to identify "Publishable" vs "Patentable" research.
- ✅ **Automated Claim Extraction** - NLP extraction of background, core innovations, and keywords.
- ✅ **Global Patent Search** - Integrated Google Patents API with semantic reranking.
- ✅ **Similarity Scoring** - Vector-based comparison scoring between disclosure and prior art.
- ✅ **Smart Recommendations** - AI-generated reasoning (Pursue / Reconsider / Reject).
- ✅ **Real-time Status** - WebSocket/Polling architecture for live analysis updates.

### User Interface
- ✅ **Modern Design** - Responsive UI built with Tailwind CSS 4.
- ✅ **Authentication** - Secure RBAC authentication via Clerk.
- ✅ **Dashboard** - Multi-tenant management of analysis history.
- ✅ **Visual Analytics** - Color-coded patentability alerts (Green/Yellow/Red).
- ✅ **Optimistic UI** - Skeleton loading and smooth state transitions.

### Technical Architecture
- ✅ **REST API** - Strongly typed FastAPI endpoints with auto-generated OpenAPI docs.
- ✅ **Relational Persistence** - SQLAlchemy ORM with SQLite (Dev) / PostgreSQL (Prod).
- ✅ **End-to-End Type Safety** - TypeScript (Frontend) ↔ Pydantic (Backend) sync.
- ✅ **State Management** - Zustand for high-performance client state.
- ✅ **Centralized API Layer** - Axios client with request/response interceptors.

---

## 🏗️ Architecture

### Tech Stack

| Domain | Technology | Reason for Choice |
| :--- | :--- | :--- |
| **Frontend** | **Next.js 16 (App Router)** | Server Components for performance & SEO. |
| **UI Library** | **React 19** | Utilizing latest hooks and transition APIs. |
| **Backend** | **FastAPI (Python 3.11+)** | Selected for superior PDF parsing (`PyPDF2`) and AI library support. |
| **Database** | **SQLite / SQLAlchemy** | Relational data integrity for Analyses and Patents. |
| **Validation** | **Pydantic V2** | Strict data validation sharing logic with OpenAPI. |
| **Auth** | **Clerk** | Secure, managed authentication middleware. |

**AI/ML Integrations:**
- **IBM watsonx.ai** - Similarity scoring and patentability assessment.
- **IBM watsonx NLU** - Natural Language Understanding.
- **Google Patents API** - External patent corpus search.

### Project Structure

```bash
Prior-AI/
├── frontend/                 # Next.js 16 application
│   ├── src/
│   │   ├── app/              # App Router (Page Logic)
│   │   ├── components/       # Atomic React Components
│   │   ├── lib/              # API Client & Utils
│   │   └── stores/           # Zustand State Stores
│
├── backend/                  # FastAPI application
│   ├── app/
│   │   ├── main.py           # Application Entry Point
│   │   ├── models/           # SQLAlchemy Database Models
│   │   ├── schemas/          # Pydantic Response/Request Models
│   │   ├── services/         # Business Logic (Orchestrators)
│   │   ├── ml_services/      # AI Modules (Scoring, Extraction)
│   │   └── integrations/     # External APIs (Watsonx, Google)
```

---

## 🚀 Quick Start

### Prerequisites

- Node.js 18+
- Python 3.11+
- Clerk Account (Auth)
- IBM watsonx Account (AI Features)

### 1. Clone & Install

```bash
git clone https://github.com/yourusername/prior-ai.git
cd prior-ai
```

### 2. Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Configure Environment
cp .env.example .env

# Initialize DB & Run
uvicorn app.main:app --reload
```
API available at: http://localhost:8000/docs

### 3. Frontend Setup

```bash
cd frontend
npm install

# Configure Environment
# Create .env.local with:
# NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
# NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=...
# CLERK_SECRET_KEY=...

npm run dev
```
UI available at: http://localhost:3000

---

## 📖 API Documentation

### Core Endpoints

```bash
# Upload & Start Analysis
POST /api/v1/analyses
Content-Type: multipart/form-data
Body: file (PDF/DOCX)

# Get Analysis Results
GET /api/v1/analyses/{id}

# Generate PDF Report
POST /api/v1/analyses/{id}/report
```

#### Data Schema (Analysis)

```typescript
interface Analysis {
  id: string;
  status: 'processing' | 'completed' | 'failed';
  patentabilityAssessment: {
    isPatentable: boolean;
    confidence: number; // 0.0 to 1.0
    recommendations: string[];
  };
  noveltyScore: number;
  recommendation: 'pursue' | 'reconsider' | 'reject';
}
```

---

## 📊 Market Opportunity

Total Addressable Market (TAM): $8B (Global IP management, Patent Analytics, and TTO operations)

**Competitive Advantage:**

✅ **10x Faster:** AI reduction of analysis time (Minutes vs Hours).

✅ **Cost Saving:** Pre-screen patentability to save $5K-$15K on failed filings.

✅ **Explainable AI:** Integrated reasoning for every recommendation.

✅ **Hybrid Workflow:** Seamless document-to-report pipeline.

---

## 🔮 Roadmap

- [ ] Multi-Modal Analysis: Extract innovation from patent diagrams/images.
- [ ] Citation Network: Graph-based mapping of patent citations.
- [ ] Collaborative Workflows: Team-based review and approval queues.
- [ ] Integration: Direct filing connectors for USPTO/EPO APIs.

---

## 📄 License & Credits

Built by Aritra using IBM watsonx, Clerk, and FastAPI. Licensed under the MIT License.
