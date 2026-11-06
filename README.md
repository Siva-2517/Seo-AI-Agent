# SEO Agent - AI-Powered SEO Blog Automation System

An autonomous AI agent system that researches keywords, plans content, generates SEO-optimized blogs, validates them, and publishes complete blog pages automatically.

## 🚀 Features

- **Automated Keyword Research**: Discovers and analyzes keyword opportunities using Google Trends and internal scoring
- **Smart Keyword Selection**: AI-powered selection of optimal keyword clusters
- **Content Planning**: Creates comprehensive SEO-optimized content plans
- **Duplicate Detection**: Prevents keyword cannibalization and duplicate content
- **AI Blog Writing**: Generates complete, human-focused blog content
- **SEO Validation**: Validates content against SEO best practices with automatic retry
- **Automatic Publishing**: Saves blogs to database and generates accessible URLs
- **Real-time Progress Tracking**: Watch agent execution in real-time
- **Modern Dashboard**: Beautiful AI SaaS interface with dark theme

## 📋 Technology Stack

### Backend
- Python 3.9+
- FastAPI
- SQLAlchemy
- LangGraph (Agent Orchestration)
- LangChain
- Google Gemini API
- PyTrends (Google Trends)
- SQLite

### Frontend
- React 18
- TypeScript
- Vite
- Tailwind CSS
- React Router
- Axios
- Lucide React (Icons)

## 📁 Project Structure

```
appin/
├── backend/
│   ├── app/
│   │   ├── agents/
│   │   │   ├── state.py              # Shared agent state
│   │   │   ├── graph.py              # LangGraph workflow
│   │   │   ├── seo_research.py       # SEO Research Agent
│   │   │   ├── keyword_selector.py   # Keyword Selection Agent
│   │   │   ├── content_planner.py    # Content Planning Agent
│   │   │   ├── duplicate_detector.py # Duplicate Detection Agent
│   │   │   ├── blog_writer.py        # Blog Writer Agent
│   │   │   ├── seo_validator.py      # SEO Validation Agent
│   │   │   └── publisher.py          # Publisher Agent
│   │   ├── api/
│   │   │   └── routes/
│   │   │       ├── generation.py     # Generation endpoints
│   │   │       ├── blogs.py          # Blog endpoints
│   │   │       ├── research.py       # Research endpoints
│   │   │       └── health.py         # Health check
│   │   ├── models/
│   │   │   ├── blog.py               # Blog model
│   │   │   ├── keyword.py            # Keyword model
│   │   │   └── execution.py          # Execution model
│   │   ├── schemas/
│   │   │   ├── blog.py               # Blog schemas
│   │   │   ├── execution.py          # Execution schemas
│   │   │   └── research.py           # Research schemas
│   │   ├── services/
│   │   │   ├── gemini_service.py     # Gemini API service
│   │   │   ├── seo_service.py        # SEO research service
│   │   │   └── website_analyzer.py   # Website analysis
│   │   ├── utils/
│   │   │   ├── slug.py               # Slug generation
│   │   │   └── seo_scoring.py        # SEO validation
│   │   ├── config.py                 # Configuration
│   │   ├── database.py               # Database setup
│   │   └── main.py                   # FastAPI app
│   ├── tests/                        # Tests
│   ├── requirements.txt              # Python dependencies
│   └── .env.example                  # Environment variables example
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Header.tsx
│   │   │   ├── StatsOverview.tsx
│   │   │   ├── ExecutionProgress.tsx
│   │   │   └── BlogCard.tsx
│   │   ├── pages/
│   │   │   ├── Dashboard.tsx
│   │   │   ├── Blogs.tsx
│   │   │   └── BlogDetail.tsx
│   │   ├── services/
│   │   │   └── api.ts                # API client
│   │   ├── types/
│   │   │   └── index.ts              # TypeScript types
│   │   ├── styles/
│   │   │   └── index.css             # Global styles
│   │   ├── App.tsx                   # Main app component
│   │   └── main.tsx                  # Entry point
│   ├── index.html
│   ├── package.json
│   ├── vite.config.ts
│   ├── tailwind.config.js
│   └── tsconfig.json
└── README.md
```

## 🛠️ Installation & Setup

### Prerequisites

- Python 3.9 or higher
- Node.js 18 or higher
- Google Gemini API key

### Backend Setup

1. **Navigate to backend directory**:
   ```bash
   cd backend
   ```

2. **Create and activate virtual environment**:
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Create `.env` file**:
   ```bash
   cp .env.example .env
   ```

5. **Edit `.env` and add your Gemini API key**:
   ```env
   GEMINI_API_KEY=your_actual_gemini_api_key_here
   ```

6. **Initialize database** (automatic on first run):
   ```bash
   # Database will be created automatically when you start the server
   ```

7. **Start the backend server**:
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

   Backend will be available at: `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend directory** (new terminal):
   ```bash
   cd frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Create `.env` file** (optional, defaults work):
   ```bash
   cp .env.example .env
   ```

4. **Start the development server**:
   ```bash
   npm run dev
   ```

   Frontend will be available at: `http://localhost:5173`

## 🎯 Usage

1. **Open the application** in your browser: `http://localhost:5173`

2. **Click "Create Blog Page"** button on the dashboard

3. **Watch the AI agents work**:
   - SEO Research Agent discovers keywords
   - Keyword Selection Agent picks the best cluster
   - Content Planning Agent creates the structure
   - Duplicate Detection Agent checks for conflicts
   - Blog Writer Agent generates complete content
   - SEO Validation Agent validates quality
   - Publisher Agent saves and publishes

4. **View the generated blog** in the list and click to see the full content

5. **Access the blog page** at `/blogs/{slug}`

## 🔧 API Endpoints

### Generation
- `POST /api/generation/create` - Start blog generation
- `GET /api/generation/{execution_id}` - Get execution status
- `GET /api/generation/{execution_id}/stream` - Stream progress (SSE)

### Blogs
- `GET /api/blogs/` - Get all blogs
- `GET /api/blogs/{slug}` - Get blog by slug
- `GET /api/blogs/id/{blog_id}` - Get blog by ID

### Research
- `GET /api/research/{execution_id}` - Get keyword research data

### Health
- `GET /api/health` - Health check

## 🧪 Testing

### Run Backend Tests
```bash
cd backend
pytest
```

### Manual Testing Workflow
1. Start both backend and frontend servers
2. Open browser to `http://localhost:5173`
3. Click "Create Blog Page"
4. Monitor execution progress
5. Verify blog is generated and accessible
6. Check database: `backend/seo_agent.db`

## 🏗️ LangGraph Workflow

The application uses LangGraph to orchestrate multiple AI agents:

```
START
  ↓
SEO Research Agent
  ↓
Keyword Selection Agent
  ↓
Content Planning Agent
  ↓
Duplicate Detection Agent
  ↓
Blog Writer Agent
  ↓
SEO Validation Agent
  ↓
  ├─ PASS → Publisher Agent → END
  └─ FAIL → Blog Writer Agent (retry up to 2 times)
```

## 📊 Data Confidence Levels

The system clearly labels all metrics:

- **Verified**: Data directly from Google Trends API
- **Estimated**: Internally calculated scores
- **Unavailable**: No reliable data source available

## 🚨 Important Notes

### Content Generation
- No fabricated statistics or unsupported claims
- No salary or placement guarantees
- Focus on genuine value for users
- Natural keyword integration (no stuffing)

### SEO Validation
- Checks title length (30-60 chars)
- Validates meta description (120-160 chars)
- Ensures proper heading structure
- Validates keyword placement
- Requires minimum content length
- Validates FAQ section (minimum 3 questions)
- Checks for call-to-action

### Duplicate Detection
- Prevents duplicate slugs
- Detects keyword cannibalization
- Checks for similar titles

## 🔐 Security Notes

1. **API Keys**: Never commit `.env` files to version control
2. **Content Sanitization**: Blog content is generated by AI and stored as trusted HTML
3. **CORS**: Configure `ALLOWED_ORIGINS` in `.env` for production

## 🚀 Deployment

### Backend (Render)
1. Create new Web Service on Render
2. Connect repository
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Add environment variables from `.env.example`
6. Deploy

### Frontend (Vercel)
1. Import project to Vercel
2. Set framework preset: Vite
3. Set build command: `npm run build`
4. Set output directory: `dist`
5. Add environment variable: `VITE_API_URL=<your-backend-url>/api`
6. Deploy

### Database
- Development: SQLite (included)
- Production: Upgrade to PostgreSQL (update `DATABASE_URL` in `.env`)

## 📝 Configuration

Edit `backend/app/config.py` or use environment variables:

- `GEMINI_API_KEY`: Google Gemini API key (required)
- `DATABASE_URL`: Database connection string
- `REFERENCE_WEBSITE`: Website to analyze for context
- `BUSINESS_CATEGORY`: Business category for targeting
- `MAX_RETRY_ATTEMPTS`: Maximum validation retries (default: 2)
- `MIN_VALIDATION_SCORE`: Minimum SEO score to pass (default: 70)

## 🤝 Contributing

This is a functional engineering project demonstrating AI agent orchestration with LangGraph.

## 📄 License

MIT License

## 🙏 Acknowledgments

- Built with LangGraph for agent orchestration
- Powered by Google Gemini API
- Uses PyTrends for Google Trends data
- Reference business: Appin Technology, Coimbatore

## 📧 Support

For issues or questions, please check the logs in the execution progress panel or backend console output.

---

**Built with ❤️ using LangGraph, FastAPI, and React**
