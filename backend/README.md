# Backend - VANTAGE

FastAPI backend for AI-powered patent prior art analysis with watsonx integration.

## 🚀 Quick Start

### 1. Setup Python Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Unix/MacOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your watsonx credentials
```

Required environment variables:
```bash
# watsonx NLU (for claim extraction)
WATSONX_NLU_API_KEY=your_nlu_api_key
WATSONX_NLU_URL=https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/xxxxx

# watsonx.ai (for patentability & similarity scoring)
WATSONX_API_KEY=your_watsonx_key
WATSONX_PROJECT_ID=your_project_id
WATSONX_URL=https://us-south.ml.cloud.ibm.com

# watsonx Orchestrate (workflow coordination)
WATSONX_ORCHESTRATE_URL=https://api.watsonx-orchestrate.ibm.com
WATSONX_ORCHESTRATE_API_KEY=your_orchestrate_api_key
WATSONX_ORCHESTRATE_TEAM_ID=your_team_id
WATSONX_WORKFLOW_ID=workflow-patent-analysis

# Google Patents API (optional - for patent search)
GOOGLE_PATENTS_API_KEY=your_google_api_key
```

### 3. Initialize Database

```bash
# Database will be created automatically on first run
# Or manually create:
python -c "from app.database import Base, engine; Base.metadata.create_all(bind=engine)"
```

### 4. Run the Server

```bash
# Development mode with auto-reload
uvicorn app.main:app --reload --port 8000

# Production mode
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

**Server URLs:**
- API: http://localhost:8000
- Interactive API Docs: http://localhost:8000/docs
- Alternative Docs: http://localhost:8000/redoc

---

## 📁 Project Structure

```
backend/
├── app/
│   ├── api/v1/                      # API Routes
│   │   ├── analyses.py              # Analysis CRUD operations
│   │   ├── skills.py                # watsonx Orchestrate skill endpoints
│   │   └── health.py                # Health check
│   │
│   ├── models/                      # SQLAlchemy Database Models
│   │   ├── analysis.py              # Analysis model (with patentability fields)
│   │   ├── patent.py                # Patent match model
│   │   └── orchestrate_log.py       # Orchestrate execution logs
│   │
│   ├── schemas/                     # Pydantic Validation Schemas
│   │   ├── analysis.py              # Analysis request/response schemas
│   │   └── patent.py                # Patent schemas
│   │
│   ├── services/                    # Business Logic Layer
│   │   ├── document_parser.py       # PDF/DOCX parsing
│   │   ├── patent_searcher.py       # Google Patents search
│   │   ├── report_generator.py      # PDF report generation
│   │   ├── orchestrate.py           # Legacy conductor (v2.1)
│   │   └── orchestrate_v3_1.py      # watsonx Orchestrate conductor (v3.1)
│   │
│   ├── ml_services/                 # AI/ML Modules (Stub Implementations)
│   │   ├── claim_extractor.py       # Claim extraction + patentability check
│   │   ├── similarity_scorer.py     # Patent similarity scoring
│   │   └── recommender.py           # Recommendation generation
│   │
│   ├── integrations/                # External Service Integrations
│   │   ├── google_patents.py        # Google Patents API client
│   │   ├── watsonx_nlu.py           # watsonx NLU wrapper (stub)
│   │   ├── watsonx_ai.py            # watsonx.ai wrapper (stub)
│   │   └── watsonx_orchestrate.py   # watsonx Orchestrate client
│   │
│   ├── utils/                       # Utility Functions
│   │   ├── file_handler.py          # File operations
│   │   └── logger.py                # Logging configuration
│   │
│   ├── config.py                    # Application configuration
│   ├── database.py                  # Database setup (SQLAlchemy)
│   └── main.py                      # FastAPI application entry point
│
├── training_data/                   # Ground Truth Dataset
│   ├── ground_truth_dataset.json    # Complete dataset (6 IDFs, 60 prior art)
│   ├── test_cases.json              # Pre-built test cases
│   ├── dataset_statistics.json      # Dataset stats
│   ├── pairs/                       # Individual IDF pairs
│   ├── patents/                     # Reference patents
│   ├── Dataset-Documentation.md     # Dataset methodology
│   └── Implementation-Guide.md      # Usage guide
│
├── scripts/                         # Utility Scripts
│   └── load_ground_truth_data.py    # Dataset loader/processor
│
├── uploads/                         # File Storage (auto-created)
│   ├── disclosures/                 # Uploaded disclosure PDFs/DOCX
│   └── reports/                     # Generated PDF reports
│
├── alembic/                         # Database Migrations
│   └── versions/                    # Migration files
│
├── tests/                           # Test Suite
│   ├── test_api.py                  # API endpoint tests
│   ├── test_services.py             # Service layer tests
│   └── validate_with_dataset.py     # ML validation script
│
├── requirements.txt                 # Python dependencies
├── Dockerfile                       # Docker configuration
├── .env.example                     # Environment template
├── README.md                        # This file
├── ORCHESTRATE_SETUP.md             # watsonx Orchestrate setup guide
├── ORCHESTRATE_QUICKSTART.md        # Quick reference
└── ORCHESTRATE_INTEGRATION.md       # Technical integration details
```

---

## 🛣️ API Endpoints

### Analysis Operations

#### Create Analysis
```http
POST /api/v1/analyses
Content-Type: multipart/form-data

file: <PDF or DOCX file>
```

**Response:**
```json
{
  "id": "string",
  "title": "Document Title",
  "status": "processing",
  "created_at": "2025-11-23T10:00:00Z"
}
```

#### Get All Analyses
```http
GET /api/v1/analyses?skip=0&limit=10
```

#### Get Analysis by ID
```http
GET /api/v1/analyses/{id}
```

**Response (when completed):**
```json
{
  "id": "string",
  "title": "string",
  "status": "completed",
  "patentabilityAssessment": {
    "isPatentable": true,
    "confidence": 85,
    "missingElements": [],
    "recommendations": []
  },
  "extractedClaims": {
    "background": "string",
    "innovations": ["innovation 1", "innovation 2"],
    "keywords": ["keyword1", "keyword2"],
    "ipcClassifications": ["G06F"]
  },
  "patents": [
    {
      "patentId": "US1234567A",
      "title": "Patent Title",
      "similarityScore": 75.5,
      "publicationDate": "2020-01-01"
    }
  ],
  "noveltyScore": 65,
  "recommendation": "pursue",
  "reasoning": "..."
}
```

#### Generate PDF Report
```http
POST /api/v1/analyses/{id}/report
```

#### Delete Analysis
```http
DELETE /api/v1/analyses/{id}
```

### watsonx Orchestrate Skills

These endpoints are called by watsonx Orchestrate workflow:

```http
POST /api/v1/skills/patentability-checker
POST /api/v1/skills/claim-extractor
POST /api/v1/skills/patent-searcher
POST /api/v1/skills/similarity-scorer
```

### Health Check

```http
GET /api/v1/health
GET /
```

---

## 🗄️ Database Schema

### Analysis Table
```sql
CREATE TABLE analyses (
    id VARCHAR PRIMARY KEY,
    title VARCHAR NOT NULL,
    document_path VARCHAR,
    status VARCHAR,

    -- Patentability Assessment (v2.1)
    is_patentable BOOLEAN,
    patentability_confidence FLOAT,
    missing_elements TEXT,  -- JSON

    -- Extracted Claims
    background TEXT,
    innovations TEXT,  -- JSON
    keywords TEXT,  -- JSON
    ipc_classifications TEXT,  -- JSON

    -- Results
    novelty_score FLOAT,
    recommendation VARCHAR,
    reasoning TEXT,

    -- Metadata
    created_at DATETIME,
    updated_at DATETIME
);
```

### Patent Table
```sql
CREATE TABLE patents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    analysis_id VARCHAR FOREIGN KEY,
    patent_id VARCHAR,
    title VARCHAR,
    abstract TEXT,
    similarity_score FLOAT,
    publication_date DATE,
    inventors TEXT,
    assignee VARCHAR
);
```

### Orchestrate Log Table
```sql
CREATE TABLE orchestrate_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    analysis_id VARCHAR FOREIGN KEY,
    orchestrate_execution_id VARCHAR,
    workflow_name VARCHAR,
    step_name VARCHAR,
    input_data TEXT,  -- JSON
    output_data TEXT,  -- JSON
    status VARCHAR,
    error_message TEXT,
    started_at DATETIME,
    completed_at DATETIME
);
```

---

## 🤖 AI/ML Integration Status

### Current Status: **Stub Implementations**

The following modules need watsonx integration:

| Module | File | Status | watsonx Service |
|--------|------|--------|-----------------|
| **Patentability Check** | `ml_services/claim_extractor.py` | ⚠️ Stub | watsonx.ai |
| **Claim Extraction** | `ml_services/claim_extractor.py` | ⚠️ Stub | watsonx NLU |
| **Similarity Scoring** | `ml_services/similarity_scorer.py` | ⚠️ Stub | watsonx.ai |
| **Recommendations** | `ml_services/recommender.py` | ⚠️ Stub | watsonx.ai |
| **Orchestrate Client** | `integrations/watsonx_orchestrate.py` | ✅ Ready | watsonx Orchestrate |

### Integration Guide

See [AI_ML_INTEGRATION_GUIDE.md](../AI_ML_INTEGRATION_GUIDE.md) for detailed integration instructions.

**Quick Overview:**

1. **Install watsonx SDKs:**
   ```bash
   pip install ibm-watson ibm-watsonx-ai
   ```

2. **Configure credentials in `.env`**

3. **Replace stub implementations:**
   - `claim_extractor.py::assess_patentability()` - Use watsonx.ai prompt
   - `claim_extractor.py::extract()` - Use watsonx NLU
   - `similarity_scorer.py::score_similarity()` - Use watsonx.ai embeddings

4. **Validate with test data:**
   ```bash
   cd backend
   python scripts/load_ground_truth_data.py
   python tests/validate_with_dataset.py
   ```

---

## 🧪 Testing

### Run Tests

```bash
# Install test dependencies
pip install pytest pytest-cov

# Run all tests
pytest

# Run with coverage
pytest --cov=app tests/

# Run specific test file
pytest tests/test_api.py
```

### Validate with Ground Truth Data

```bash
# Load and process dataset
python scripts/load_ground_truth_data.py

# Validate ML implementations (after watsonx integration)
python tests/validate_with_dataset.py
```

Expected validation results:
- **Patentability Accuracy**: ≥83% (5/6 correct classifications)
- **Similarity Precision**: ±15% of expected scores
- **Processing Time**: <2 minutes for 60 patents

---

## 🐳 Docker Deployment

### Build Image

```bash
docker build -t priorai-backend .
```

### Run Container

```bash
docker run -p 8000:8000 \
  -e WATSONX_API_KEY=your_key \
  -e WATSONX_PROJECT_ID=your_project \
  -e WATSONX_NLU_API_KEY=your_nlu_key \
  -e WATSONX_NLU_URL=your_nlu_url \
  priorai-backend
```

### Docker Compose (with frontend)

```yaml
version: '3.8'
services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    env_file:
      - ./backend/.env
    volumes:
      - ./backend/uploads:/app/uploads
      - ./backend/priorai.db:/app/priorai.db
```

---

## 🚀 Deployment

### Railway

1. Create new project: https://railway.app
2. Connect GitHub repository
3. Set root directory: `backend`
4. Add environment variables from `.env.example`
5. Deploy

**Start Command:**
```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

### Render

1. Create new Web Service
2. Connect repository
3. **Build Command:** `pip install -r requirements.txt`
4. **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Add environment variables

### AWS EC2 / VPS

```bash
# Install dependencies
sudo apt update
sudo apt install python3.11 python3-pip nginx

# Clone repository
git clone <your-repo-url>
cd backend

# Setup virtual environment
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configure .env
cp .env.example .env
nano .env

# Run with gunicorn
pip install gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

---

## 🔧 Development

### Database Migrations (Alembic)

```bash
# Create new migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

### Reset Database

```bash
rm priorai.db
python -c "from app.database import Base, engine; Base.metadata.create_all(bind=engine)"
```

### Code Formatting

```bash
# Install formatters
pip install black isort

# Format code
black app/
isort app/
```

### Linting

```bash
pip install pylint flake8
pylint app/
flake8 app/
```

---

## 📊 Monitoring & Logging

### View Logs

```bash
# Application logs
tail -f logs/app.log

# Orchestrate execution logs
tail -f logs/orchestrate.log
```

### Health Check

```bash
curl http://localhost:8000/api/v1/health
```

Expected response:
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "database": "connected"
}
```

---

## 🔒 Security

### Environment Variables

- Never commit `.env` file
- Use environment-specific configuration
- Rotate API keys regularly

### API Security

- CORS configured for frontend origin only
- File upload size limits enforced
- Input validation with Pydantic schemas
- SQL injection prevention via SQLAlchemy ORM

---

## 📚 Additional Documentation

- **[ORCHESTRATE_SETUP.md](ORCHESTRATE_SETUP.md)** - Complete watsonx Orchestrate setup
- **[ORCHESTRATE_QUICKSTART.md](ORCHESTRATE_QUICKSTART.md)** - Quick reference
- **[ORCHESTRATE_INTEGRATION.md](ORCHESTRATE_INTEGRATION.md)** - Technical details
- **[AI_ML_INTEGRATION_GUIDE.md](../AI_ML_INTEGRATION_GUIDE.md)** - watsonx integration guide
- **[training_data/Dataset-Documentation.md](training_data/Dataset-Documentation.md)** - Dataset docs

---

## 🐛 Troubleshooting

### Common Issues

**Issue: ModuleNotFoundError**
```bash
# Ensure virtual environment is activated
source venv/bin/activate  # Unix/Mac
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

**Issue: Database locked**
```bash
# Close all connections and restart server
pkill -f uvicorn
uvicorn app.main:app --reload
```

**Issue: watsonx API authentication failed**
```bash
# Check environment variables
python -c "import os; print(os.getenv('WATSONX_API_KEY'))"

# Verify credentials in IBM Cloud dashboard
```

---

## 📄 License

MIT

---

## 🙏 Support

For issues or questions:
1. Check [AI_ML_INTEGRATION_GUIDE.md](../AI_ML_INTEGRATION_GUIDE.md)
2. Review [ORCHESTRATE_SETUP.md](ORCHESTRATE_SETUP.md)
3. Check API docs at http://localhost:8000/docs
4. Open an issue on GitHub

---

**Last Updated:** November 23, 2025
**Version:** 1.0.0 (Hackathon MVP with watsonx Orchestrate support)
