# reworkcv.ai

AI-powered resume tailoring application that customizes resumes for specific job descriptions.

## Features

- **AI-Powered**: Uses Google Gemini to analyze job descriptions and tailor resumes
- **PDF Processing**: Upload existing resumes and generate tailored PDFs
- **Modern UI**: Built with React, TypeScript, and Tailwind CSS
- **FastAPI Backend**: High-performance Python backend with automatic documentation

## Architecture

- **Frontend**: React + Vite + TypeScript + Tailwind CSS
- **Backend**: FastAPI (Python 3.11) 
- **AI**: Google Gemini API for intelligent resume tailoring
- **Deployment**: Google Cloud Run with Docker containerization

## Quick Start

### Local Development

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd reworkcv.ai
   ```

2. **Backend Setup**
   ```bash
   cd backend
   pip install -r requirements.txt
   cp .env.example .env
   # Add your GEMINI_API_KEY to .env
   uvicorn app.main:app --reload --port 8000
   ```

3. **Frontend Setup**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

4. **Access the application**
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

## Deployment

### Google Cloud Run (Recommended)

The application is configured for automatic deployment to Google Cloud Run using GitHub Actions.

**📋 See [DEPLOYMENT.md](./DEPLOYMENT.md) for detailed deployment instructions.**

#### Automatic Deployment

1. Push code to `dev` branch
2. GitHub Actions builds and deploys automatically
3. Application updates without downtime

#### Manual Deployment

```bash
# Build and deploy
gcloud run deploy reworkcv-backend \
  --source . \
  --region us-central1 \
  --allow-unauthenticated
```

### Environment Variables

Required for production:

- `GEMINI_API_KEY`: Google Gemini API key
- `ENVIRONMENT`: Set to `production`
- `CORS_ORIGINS`: Your Cloud Run URL

## API Usage

### Upload and Tailor Resume

```bash
curl -X POST "https://your-app.run.app/api/tailor-resume" \
  -H "Content-Type: multipart/form-data" \
  -F "resume=@resume.pdf" \
  -F "job_description=Senior Software Engineer position requiring Python and cloud experience"
```

### Health Check

```bash
curl "https://your-app.run.app/api/health"
```

## Development

### Project Structure

```
reworkcv.ai/
├── backend/
│   ├── app/
│   │   ├── api/          # API routes
│   │   ├── core/         # Configuration and settings
│   │   └── schemas/      # Pydantic models
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── components/   # React components
│   │   └── lib/          # Utilities
│   └── package.json
├── Dockerfile
├── .github/workflows/    # CI/CD pipelines
└── DEPLOYMENT.md         # Detailed deployment guide
```

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

[Add your license here]

## Support

For deployment issues, check the [DEPLOYMENT.md](./DEPLOYMENT.md) guide or open an issue.
