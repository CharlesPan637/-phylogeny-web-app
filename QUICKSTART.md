# 🚀 Quick Start Guide

Get your phylogeny web application running in minutes!

## 📋 Prerequisites

- Docker and Docker Compose installed
- Or: Python 3.9+ and Node.js 18+

## ⚡ Fastest Method: Docker

```bash
# Navigate to project directory
cd phylogeny-web-app

# Start the application
docker-compose up -d

# Wait 30 seconds for services to start, then open:
# http://localhost:3000
```

That's it! Your application is running.

## 🛠️ Manual Setup (Without Docker)

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start backend server
uvicorn app.main:app --reload --port 8000
```

Backend will run at: http://localhost:8000
API docs at: http://localhost:8000/api/docs

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend will run at: http://localhost:3000

## 🎯 Using the Application

1. **Open your browser** to http://localhost:3000

2. **Enter UniProt Accessions:**
   ```
   P0C6X7
   P17763
   P29991
   P27909
   P09866
   ```

3. **Click "Analyze Sequences"**

4. **Wait 30-60 seconds** for analysis to complete

5. **View Results:**
   - Sequence information
   - Pairwise identity matrix
   - Multiple sequence alignment preview
   - Phylogenetic tree (Newick format)
   - Summary report

## 📊 API Testing

Test the backend API directly:

```bash
# Health check
curl http://localhost:8000/api/health

# Run analysis
curl -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"accessions": ["P0C6X7", "P17763", "P29991"]}'
```

Or visit: http://localhost:8000/api/docs for interactive API documentation

## 🐳 Docker Commands

```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Rebuild after code changes
docker-compose up -d --build

# Stop and remove everything
docker-compose down -v
```

## 🔧 Troubleshooting

### Backend won't start
```bash
# Check Python version
python --version  # Should be 3.9+

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Frontend won't start
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

### Port already in use
```bash
# Change ports in docker-compose.yml:
# Backend: "8001:8000" instead of "8000:8000"
# Frontend: "3001:3000" instead of "3000:3000"
```

### CORS errors
- Make sure backend is running on port 8000
- Check frontend next.config.js proxy settings
- In production, update CORS origins in backend/app/main.py

## 📱 Testing with Sample Data

The application comes pre-loaded with example accessions for Dengue virus serotypes. Just click "Analyze Sequences" to see it in action!

## 🎨 Customization

### Change API endpoint
Edit `frontend/next.config.js`:
```javascript
async rewrites() {
  return [
    {
      source: '/api/:path*',
      destination: 'YOUR_BACKEND_URL/api/:path*',
    },
  ]
}
```

### Add more sequences
Just add more UniProt IDs in the text area, one per line!

### Modify styling
Edit `frontend/src/app/globals.css` for custom styles.

## 📚 Next Steps

- Read the full README.md for detailed documentation
- Explore API docs at http://localhost:8000/api/docs
- Customize the UI in frontend/src/app/page.tsx
- Add authentication, database persistence, etc.

## 💡 Pro Tips

- Use Docker for consistent deployment
- The backend can handle 10+ sequences (may take longer)
- Results are not persisted - download what you need
- API responses include all data for custom visualizations

---

**Need Help?** Check the README.md or API documentation!
