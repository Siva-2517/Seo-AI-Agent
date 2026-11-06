# SEO Agent - Claude AI Assistant Instructions

This file contains instructions for AI assistants working on the SEO Agent project.

## Project Overview

**SEO Agent** is an autonomous AI-powered blog automation system that uses LangGraph to orchestrate multiple AI agents for researching keywords, planning content, generating SEO-optimized blogs, validating quality, and publishing complete blog pages.

**Technology Stack:**
- Backend: Python, FastAPI, LangGraph, LangChain, SQLAlchemy, Google Gemini API
- Frontend: React, TypeScript, Vite, Tailwind CSS
- Database: SQLite (development), PostgreSQL (production)
- AI: Google Gemini via langchain-google-genai

**Reference Business:** Appin Technology - Digital Marketing Course in Coimbatore

## Architecture

### LangGraph Agent Workflow
```
START → SEO Research → Keyword Selection → Content Planning → 
Duplicate Detection → Blog Writer → SEO Validation → 
(Conditional: Pass → Publisher | Fail → Retry) → END
```

### Key Components
- **7 AI Agents**: Each agent has a specific responsibility in the workflow
- **Shared State**: TypedDict state passed between agents
- **Conditional Routing**: Based on validation results
- **Retry Logic**: Up to 2 retries for failed SEO validation
- **Real-time Progress**: Execution tracking and logging

## Security Guidelines - CRITICAL

### 🔒 Environment Variables & API Keys

**NEVER:**
- ❌ Hardcode API keys in source code
- ❌ Commit `.env` files to version control
- ❌ Expose API keys in frontend code
- ❌ Log API keys or sensitive credentials
- ❌ Store secrets in database without encryption
- ❌ Share `.env` files in chat or documentation

**ALWAYS:**
- ✅ Use `.env` files for local development
- ✅ Add `.env` to `.gitignore`
- ✅ Use environment variables via `os.getenv()` or `Settings`
- ✅ Provide `.env.example` with placeholder values
- ✅ Use secure secret management in production (AWS Secrets Manager, etc.)
- ✅ Validate environment variables on startup
- ✅ Use separate credentials for dev/staging/production

**Required Environment Variables:**
```env
# REQUIRED - Never commit actual values
GEMINI_API_KEY=your_gemini_api_key_here

# Database
DATABASE_URL=sqlite:///./seo_agent.db

# CORS - Adjust for production
ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000

# Business Context
REFERENCE_WEBSITE=https://appincoimbatore.com
BUSINESS_CATEGORY=Digital Marketing Course in Coimbatore
BUSINESS_NAME=Appin Technology
BUSINESS_LOCATION=Coimbatore

# Agent Configuration
MAX_RETRY_ATTEMPTS=2
MIN_VALIDATION_SCORE=70
```

### 🛡️ Security Best Practices

1. **Input Validation**
   - Validate all user inputs
   - Sanitize data before database operations
   - Use Pydantic models for type validation

2. **Database Security**
   - Use parameterized queries (SQLAlchemy ORM handles this)
   - Implement proper indexes
   - Never expose raw SQL errors to users

3. **API Security**
   - Use CORS properly (configure `ALLOWED_ORIGINS`)
   - Implement rate limiting in production
   - Add authentication for admin operations (if needed)
   - Use HTTPS in production

4. **Content Security**
   - AI-generated content is stored as trusted HTML
   - If exposing user-generated content, sanitize with DOMPurify
   - Validate all data before rendering

5. **Error Handling**
   - Never expose stack traces to users
   - Log errors securely
   - Provide user-friendly error messages

## Code Standards

### Python Backend

**File Organization:**
```
app/
├── agents/          # LangGraph agents (one per file)
├── api/routes/      # FastAPI route handlers
├── models/          # SQLAlchemy database models
├── schemas/         # Pydantic request/response models
├── services/        # External service integrations
├── utils/           # Utility functions
├── config.py        # Configuration management
├── database.py      # Database setup
└── main.py          # FastAPI application
```

**Coding Guidelines:**
```python
# Use type hints
async def seo_research_agent(state: AgentState) -> AgentState:
    """Agent docstring explaining purpose"""
    
# Use Pydantic for validation
class KeywordSelection(BaseModel):
    primary_keyword: str = Field(description="...")
    
# Environment variables via Settings
from app.config import settings
api_key = settings.GEMINI_API_KEY

# Proper error handling
try:
    result = await service.call()
except Exception as e:
    logger.error(f"Error: {str(e)}")
    state["error"] = str(e)
    
# Use async/await for I/O operations
async def fetch_data():
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()
```

**LangGraph Best Practices:**
- Define shared state using TypedDict
- One agent per file for maintainability
- Use conditional edges for routing
- Add comprehensive logging to state["logs"]
- Handle errors gracefully and store in state["error"]

### Frontend (React/TypeScript)

**Component Organization:**
```
src/
├── components/      # Reusable UI components
├── pages/           # Page components (routes)
├── services/        # API clients
├── types/           # TypeScript interfaces
├── styles/          # Global styles
├── App.tsx          # Main app component
└── main.tsx         # Entry point
```

**Coding Guidelines:**
```typescript
// Use TypeScript interfaces
interface Blog {
  id: number;
  title: string;
  // ...
}

// Type props
interface BlogCardProps {
  blog: Blog;
}

// Use functional components with hooks
const BlogCard: React.FC<BlogCardProps> = ({ blog }) => {
  const [loading, setLoading] = useState(false);
  
  // API calls with error handling
  try {
    const data = await blogsApi.getAllBlogs();
  } catch (err: any) {
    setError(err.response?.data?.detail || 'Failed');
  }
};

// Environment variables (Vite)
const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';
```

## Working with the Project

### Adding New Features

**Before Starting:**
1. Read this CLAUDE.md file
2. Check existing code structure
3. Follow established patterns
4. Maintain security practices

**Adding a New Agent:**
```python
# 1. Create agent file: app/agents/new_agent.py
async def new_agent(state: AgentState) -> AgentState:
    """New agent description"""
    state["logs"].append({...})
    # Agent logic
    state["current_agent"] = "next_agent"
    return state

# 2. Update state.py if new state fields needed
class AgentState(TypedDict):
    new_field: Optional[str]

# 3. Add to graph.py
workflow.add_node("new_agent", new_agent)
workflow.add_edge("previous_agent", "new_agent")
```

**Adding a New API Endpoint:**
```python
# 1. Create route in app/api/routes/
@router.get("/new-endpoint")
async def new_endpoint(db: Session = Depends(get_db)):
    try:
        # Logic
        return {"data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 2. Include router in main.py
app.include_router(new_router, prefix="/api/new")
```

### Database Changes

**Adding a New Model:**
```python
# 1. Create model in app/models/
class NewModel(Base):
    __tablename__ = "new_table"
    id = Column(Integer, primary_key=True)
    # fields...

# 2. Create schema in app/schemas/
class NewModelSchema(BaseModel):
    # fields...
    class Config:
        from_attributes = True

# 3. Database migration (simple approach)
# Delete seo_agent.db and restart server
# Or use Alembic for production
```

### Testing

**Run Tests:**
```bash
cd backend
pytest tests/ -v
```

**Manual Testing Workflow:**
1. Start backend: `uvicorn app.main:app --reload`
2. Start frontend: `npm run dev`
3. Open http://localhost:5173
4. Click "Create Blog Page"
5. Monitor execution logs
6. Verify blog generation
7. Check database: `backend/seo_agent.db`

### Debugging

**Backend Issues:**
- Check console output for errors
- Verify `.env` file exists and has correct values
- Check database file exists and has correct permissions
- Test API endpoints: http://localhost:8000/docs
- Review execution logs in database

**Frontend Issues:**
- Check browser console (F12)
- Verify API URL in network tab
- Check component state with React DevTools
- Ensure backend is running and accessible

**Agent Issues:**
- Review execution logs in state
- Check Gemini API quota
- Verify prompt formatting
- Test individual agents in isolation

## Content Guidelines

### SEO Blog Generation

**Content Quality Standards:**
- ✅ Original, useful, reader-focused content
- ✅ Natural keyword placement
- ✅ Practical information and examples
- ✅ Honest, factual information
- ❌ No fabricated statistics
- ❌ No unsupported placement guarantees
- ❌ No keyword stuffing
- ❌ No generic filler content

**Data Confidence Labeling:**
- **Verified**: Direct from Google Trends API
- **Estimated**: Internal scoring algorithm
- **Unavailable**: No reliable data source

Always clearly label metrics with their confidence level.

### SEO Validation Checks

1. SEO title length (30-60 chars)
2. Meta description length (120-160 chars)
3. URL slug format
4. H1 uniqueness from title
5. Heading hierarchy (H2, H3)
6. Keyword placement
7. Content length (minimum 1000 chars)
8. FAQ section (minimum 3 questions)
9. Call-to-action presence

## Common Tasks

### Update Business Context
Edit `backend/app/config.py` or `.env`:
```env
REFERENCE_WEBSITE=https://newbusiness.com
BUSINESS_CATEGORY=New Category
BUSINESS_NAME=New Business Name
```

### Adjust SEO Validation Rules
Edit `backend/app/utils/seo_scoring.py`:
```python
self.min_title_length = 30  # Adjust values
self.max_title_length = 60
```

### Change Retry Logic
Edit `backend/.env`:
```env
MAX_RETRY_ATTEMPTS=3  # Change from 2 to 3
MIN_VALIDATION_SCORE=80  # Raise threshold
```

### Add New Keywords to Research
Edit `backend/app/agents/seo_research.py`:
```python
manual_suggestions = [
    "digital marketing course in coimbatore",
    "new keyword here",  # Add more
]
```

## Deployment

### Environment-Specific Configuration

**Development (.env):**
```env
DEBUG=True
DATABASE_URL=sqlite:///./seo_agent.db
ALLOWED_ORIGINS=http://localhost:5173
```

**Production (.env.production):**
```env
DEBUG=False
DATABASE_URL=postgresql://user:pass@host:5432/dbname
ALLOWED_ORIGINS=https://yourdomain.com
GEMINI_API_KEY=prod_key_here  # Use secret manager!
```

**Security for Production:**
1. Use environment variables from hosting platform
2. Enable HTTPS only
3. Use PostgreSQL instead of SQLite
4. Add rate limiting
5. Implement authentication if needed
6. Set up monitoring and logging
7. Use CDN for frontend assets

### Deployment Checklist

Backend (Render/Railway):
- [ ] Set environment variables (never commit)
- [ ] Use production database
- [ ] Configure CORS properly
- [ ] Set DEBUG=False
- [ ] Enable logging

Frontend (Vercel/Netlify):
- [ ] Set VITE_API_URL to backend URL
- [ ] Build command: `npm run build`
- [ ] Output directory: `dist`
- [ ] Enable HTTPS

## Error Handling Patterns

### Backend
```python
try:
    result = await dangerous_operation()
    state["logs"].append({
        "timestamp": datetime.utcnow().isoformat(),
        "agent": "agent_name",
        "message": "Success message",
        "level": "info"
    })
except Exception as e:
    error_msg = f"Agent error: {str(e)}"
    logger.error(error_msg)  # Server-side only
    state["logs"].append({
        "timestamp": datetime.utcnow().isoformat(),
        "agent": "agent_name",
        "message": error_msg,
        "level": "error"
    })
    state["error"] = error_msg  # User-friendly message
```

### Frontend
```typescript
const [error, setError] = useState<string | null>(null);

try {
  const data = await api.call();
  setError(null);
} catch (err: any) {
  const message = err.response?.data?.detail || 'Operation failed';
  setError(message);
  console.error('Error details:', err);  // Dev only
}
```

## Important Reminders

### When Modifying Agents
- ✅ Update state type definitions
- ✅ Add comprehensive logging
- ✅ Handle errors gracefully
- ✅ Update graph edges if flow changes
- ✅ Test entire workflow end-to-end

### When Adding Dependencies
```bash
# Backend: Update requirements.txt
pip freeze > requirements.txt

# Frontend: Use exact versions
npm install --save-exact package-name
```

### When Changing Database Schema
- Document migration steps
- Test with fresh database
- Provide rollback instructions
- Update schemas and models

### When Working with Gemini API
- Handle rate limits gracefully
- Add retries with exponential backoff
- Validate API responses
- Never expose API keys
- Monitor API usage/quota

## Git Guidelines

**Files to NEVER commit:**
- `.env` (contains secrets)
- `*.db` (database files)
- `__pycache__/` (Python cache)
- `node_modules/` (Node packages)
- `venv/` (Python virtual environment)
- `.DS_Store` (macOS)

**Always commit:**
- `.env.example` (with placeholders)
- `.gitignore` (properly configured)
- `requirements.txt` / `package.json`
- Documentation updates
- Code with tests

## Support Resources

**Documentation:**
- FastAPI: https://fastapi.tiangolo.com/
- LangGraph: https://langchain-ai.github.io/langgraph/
- React: https://react.dev/
- Tailwind: https://tailwindcss.com/

**APIs:**
- Gemini API: https://ai.google.dev/docs
- PyTrends: https://pypi.org/project/pytrends/

**Project Files:**
- README.md: Comprehensive guide
- QUICKSTART.md: Quick start instructions
- This file (CLAUDE.md): AI assistant instructions

## Final Notes

This is a production-quality demonstration project showing:
- Real AI agent orchestration with LangGraph
- Proper separation of concerns
- Security best practices
- Clean, maintainable code
- Modern UI/UX patterns

When working on this project, prioritize:
1. **Security**: Never expose secrets
2. **Quality**: Write clean, tested code
3. **Documentation**: Keep docs updated
4. **User Experience**: Real functionality, not mocks
5. **Reliability**: Handle errors gracefully

---

**Version:** 1.0.0  
**Last Updated:** 2026-11-06  
**Project:** SEO Agent - AI-Powered Blog Automation System
