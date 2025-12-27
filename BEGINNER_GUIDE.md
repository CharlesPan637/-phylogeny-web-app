# 🎓 Complete Beginner's Guide to Your Phylogeny Web App

## Never Used Next.js Before? No Problem!

This guide assumes you know **nothing** about Next.js or web development. Follow along step-by-step!

---

## 📚 Table of Contents

1. [What You Need to Know](#what-you-need-to-know)
2. [Option A: Easy Way (Docker)](#option-a-easy-way-docker)
3. [Option B: Manual Way (Learning)](#option-b-manual-way-learning)
4. [Using the Application](#using-the-application)
5. [Understanding What Happens](#understanding-what-happens)
6. [Simple Customizations](#simple-customizations)
7. [Troubleshooting](#troubleshooting)

---

## 🤔 What You Need to Know

### What is Next.js?

Next.js is a **framework** for building websites. Think of it like this:
- **HTML** = Basic web page structure (boring and static)
- **React** = Makes web pages interactive (like clicking buttons)
- **Next.js** = Makes React easier and adds superpowers (like automatic optimization)

### What is This Application Made Of?

```
Your App = Backend (Python) + Frontend (Next.js)
           ↓                    ↓
     Does the science      Shows nice interface
     (calculations)        (what you see)
```

**Backend (Python/FastAPI):**
- Downloads sequences from UniProt
- Performs alignment
- Builds phylogenetic trees
- Runs on: `http://localhost:8000`

**Frontend (Next.js/React):**
- Shows the beautiful interface
- Lets you input accession numbers
- Displays results nicely
- Runs on: `http://localhost:3000`

---

## 🐳 Option A: Easy Way (Docker)

Docker is like a "virtual box" that runs your application with everything pre-installed.

### Step 1: Check if You Have Docker

**Windows/Mac:**
```bash
docker --version
docker-compose --version
```

**If you see version numbers:** ✅ You're good to go!

**If you see "command not found":**
1. Download Docker Desktop from: https://www.docker.com/products/docker-desktop
2. Install it
3. Restart your computer
4. Open Docker Desktop application

### Step 2: Download Your Application

**On Windows (PowerShell or Command Prompt):**
```bash
# Go to your downloads or desired location
cd C:\Users\YourName\Downloads

# Download from server
scp root@YOUR_SERVER_IP:/root/phylogeny-web-app.tar.gz .

# Extract
tar -xzf phylogeny-web-app.tar.gz

# Go into the folder
cd phylogeny-web-app
```

**On Mac/Linux:**
```bash
# Go to downloads
cd ~/Downloads

# Download
scp root@YOUR_SERVER_IP:/root/phylogeny-web-app.tar.gz .

# Extract
tar -xzf phylogeny-web-app.tar.gz

# Go into the folder
cd phylogeny-web-app
```

### Step 3: Start Everything with One Command!

```bash
docker-compose up -d
```

**What this does:**
- `-d` means "detached" (runs in background)
- Builds your backend (Python)
- Builds your frontend (Next.js)
- Starts both servers
- Connects them together

**You'll see output like:**
```
Creating network "phylogeny-web-app_phylogeny-network"
Creating phylogeny-backend  ... done
Creating phylogeny-frontend ... done
```

### Step 4: Wait and Open!

**Wait:** About 30-60 seconds for everything to start

**Then open your browser:**
```
http://localhost:3000
```

**You should see:** A beautiful blue gradient page with "🧬 Phylogeny Web Analyzer" at the top!

### Step 5: Use It!

Skip to the [Using the Application](#using-the-application) section below!

### Step 6: Stop When Done

```bash
# Stop the application
docker-compose down
```

**Docker is EASIEST for beginners!** ✅ Recommended!

---

## 💻 Option B: Manual Way (Learning)

This teaches you how it actually works. Good for learning!

### Prerequisites Check

**1. Check Node.js (needed for Next.js):**
```bash
node --version
npm --version
```

**You need:** Node.js 18 or higher

**Don't have it?**
- Download from: https://nodejs.org
- Install the "LTS" (Long Term Support) version
- Restart your terminal

**2. Check Python:**
```bash
python --version
# or
python3 --version
```

**You need:** Python 3.9 or higher

### Part 1: Setup Backend (Python/FastAPI)

#### Step 1: Open Terminal and Navigate

**Windows (PowerShell):**
```bash
cd C:\Users\YourName\Downloads\phylogeny-web-app\backend
```

**Mac/Linux:**
```bash
cd ~/Downloads/phylogeny-web-app/backend
```

#### Step 2: Create Virtual Environment

**What is this?** A separate "bubble" for your Python packages so they don't mess up other projects.

**Windows:**
```bash
python -m venv venv
.\venv\Scripts\activate
```

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**You'll see:** `(venv)` appears at the start of your prompt. That means it worked!

#### Step 3: Install Python Packages

```bash
pip install -r requirements.txt
```

**What this does:** Installs all the Python libraries (FastAPI, Biopython, etc.)

**Takes:** About 2-3 minutes

#### Step 4: Start Backend Server

```bash
uvicorn app.main:app --reload --port 8000
```

**What this does:**
- `uvicorn` = Server program
- `app.main:app` = Run the `app` from `main.py` in the `app` folder
- `--reload` = Restart automatically when you change code
- `--port 8000` = Use port 8000

**You'll see:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

**Test it:** Open browser to `http://localhost:8000/api/health`

You should see: `{"status":"healthy","version":"1.0.0","ready":true}`

**✅ Backend is working!**

**IMPORTANT:** Leave this terminal window open! The backend needs to keep running.

### Part 2: Setup Frontend (Next.js)

#### Step 1: Open NEW Terminal Window

**Don't close the backend terminal!** Open a second terminal.

#### Step 2: Navigate to Frontend

**Windows:**
```bash
cd C:\Users\YourName\Downloads\phylogeny-web-app\frontend
```

**Mac/Linux:**
```bash
cd ~/Downloads/phylogeny-web-app/frontend
```

#### Step 3: Install Node Packages

```bash
npm install
```

**What this does:** Downloads all the JavaScript libraries (React, Next.js, etc.)

**Takes:** About 3-5 minutes (downloads lots of files)

**You'll see:** A `node_modules` folder appear (it's huge! ~200MB)

#### Step 4: Start Frontend Server

```bash
npm run dev
```

**What this does:**
- `npm` = Node Package Manager
- `run dev` = Run the "dev" script (development mode)
- Starts Next.js server on port 3000

**You'll see:**
```
  ▲ Next.js 14.1.0
  - Local:        http://localhost:3000
  - Ready in 2.3s
```

**✅ Frontend is working!**

#### Step 5: Open in Browser

Go to: `http://localhost:3000`

**You should see:** The beautiful web interface!

---

## 🎯 Using the Application

Now that it's running (either Docker or manual), here's how to use it:

### Step 1: You See This Page

```
┌────────────────────────────────────────┐
│  🧬 Phylogeny Web Analyzer             │
│  Professional phylogenetic analysis... │
└────────────────────────────────────────┘

┌────────────────────────────────────────┐
│  Enter UniProt Accession Numbers       │
│  ┌──────────────────────────────────┐  │
│  │ P0C6X7                          │  │
│  │ P17763                          │  │
│  │ P29991                          │  │
│  │ P27909                          │  │
│  │ P09866                          │  │
│  └──────────────────────────────────┘  │
│                                        │
│  [ 🚀 Analyze Sequences ]              │
└────────────────────────────────────────┘
```

### Step 2: The Text Box is Pre-Filled!

You'll see example accession numbers already there. These are:
- **P0C6X7** - Reference sequence
- **P17763** - Dengue virus type 1
- **P29991** - Dengue virus type 2
- **P27909** - Dengue virus type 3
- **P09866** - Dengue virus type 4

**You can:**
- ✅ Use these (just click Analyze!)
- ✅ Replace them with your own
- ✅ Add more (one per line)

### Step 3: Click "Analyze Sequences"

The button will show: "Analyzing sequences..." with a spinning icon.

**What's happening behind the scenes:**
1. Frontend sends your accessions to backend
2. Backend downloads sequences from UniProt (5-10 seconds)
3. Backend calculates pairwise identities (5-10 seconds)
4. Backend creates alignment (5-10 seconds)
5. Backend builds phylogenetic tree (5-10 seconds)
6. Frontend receives results and displays them

**Takes:** 30-60 seconds total

### Step 4: See Your Results!

The page will scroll down and show:

#### 📊 Analysis Summary
```
┌─────────────────────────────────────┐
│  5 Sequences                        │
│  3392 Alignment Length              │
│  49.3% Avg Conservation             │
│  10 Comparisons                     │
└─────────────────────────────────────┘
```

#### 📝 Downloaded Sequences
```
┌─────────────────────────────────────┐
│ P0C6X7 - R1AB_SARS                  │
│ Organism: Severe acute respiratory  │
│ 3391 amino acids                    │
├─────────────────────────────────────┤
│ P17763 - POLG_DEN1W                 │
│ Organism: Dengue virus type 1       │
│ 3392 amino acids                    │
└─────────────────────────────────────┘
```

#### 🎯 Pairwise Identity Scores
```
┌────────────────────────────────────────┐
│ Sequence 1 │ Sequence 2 │ Identity    │
├────────────┼────────────┼─────────────┤
│ P17763     │ P27909     │ 97.46% ✅   │
│ P17763     │ P29991     │ 71.62%      │
│ P29991     │ P27909     │ 71.44%      │
└────────────────────────────────────────┘
```

Green badges (>90%) = Very similar
Yellow badges (>70%) = Moderately similar
Red badges (<70%) = Different

#### 🔤 Alignment Preview
```
┌─────────────────────────────────────┐
│ P0C6X7     MESLVLGVNEKTH...         │
│ P17763     MNNQRKKTGRPSF...         │
│ P29991     MNDQRKEAKNTPF...         │
│ Conservation  *:..:......            │
└─────────────────────────────────────┘
```

Legend:
- `*` = Identical in all sequences
- `:` = Highly similar
- `.` = Weakly similar

#### 🌳 Phylogenetic Tree
```
Shows the Newick format tree string
You can copy this to visualize in other tools
```

#### 📄 Summary Report
```
Full text report with:
- All sequence details
- Highest/lowest similarities
- Alignment statistics
- Key findings
```

### Step 5: What Can You Do?

- **Copy text** - Select and copy any results
- **Take screenshots** - For presentations
- **Run again** - Change accessions and click Analyze again
- **Try different sequences** - Any UniProt IDs work!

---

## 🧐 Understanding What Happens

### The Flow of Data

```
You type accessions
        ↓
Frontend (Next.js - port 3000)
        ↓
Sends HTTP request to /api/analyze
        ↓
Backend (FastAPI - port 8000)
        ↓
Downloads from UniProt
        ↓
Performs analysis
        ↓
Sends JSON results back
        ↓
Frontend displays beautifully
        ↓
You see results!
```

### Key Files You Should Know

**Backend:**
```
backend/app/main.py
  └─> Handles /api/analyze request
  └─> Calls functions from phylogeny.py

backend/app/phylogeny.py
  └─> download_uniprot_sequence()
  └─> calculate_identity_matrix()
  └─> create_alignment()
  └─> build_phylogenetic_tree()
```

**Frontend:**
```
frontend/src/app/page.tsx
  └─> The main page you see
  └─> handleAnalyze() function sends request
  └─> Displays all results
```

---

## 🎨 Simple Customizations

### Change the Title

**File:** `frontend/src/app/page.tsx`

**Find (around line 68):**
```tsx
<h1 className="text-5xl font-bold text-gray-900 mb-4">
  🧬 Phylogeny Web Analyzer
</h1>
```

**Change to:**
```tsx
<h1 className="text-5xl font-bold text-gray-900 mb-4">
  🧬 My Lab's Phylogeny Tool
</h1>
```

**Save the file** and the page will auto-reload!

### Change Colors

**File:** `frontend/src/app/globals.css`

**Find:**
```css
--background-start-rgb: 214, 219, 220;
--background-end-rgb: 255, 255, 255;
```

**Change to your colors:**
```css
--background-start-rgb: 200, 255, 200;  /* Light green */
--background-end-rgb: 255, 255, 200;     /* Light yellow */
```

### Add More Example Accessions

**File:** `frontend/src/app/page.tsx`

**Find (around line 8):**
```tsx
const [accessions, setAccessions] = useState('P0C6X7\nP17763\nP29991\nP27909\nP09866')
```

**Change to:**
```tsx
const [accessions, setAccessions] = useState('P0C6X7\nP17763\nP29991\nP27909\nP09866\nQ9YRR4')
```

Now it includes 6 sequences by default!

---

## 🐛 Troubleshooting

### "Page Not Loading" (http://localhost:3000)

**Check 1:** Is the frontend running?
```bash
# You should see this in terminal:
- Local: http://localhost:3000
```

**Check 2:** Is port 3000 already used?
```bash
# Windows
netstat -ano | findstr :3000

# Mac/Linux
lsof -i :3000
```

**Fix:** Kill the process or use different port:
```bash
# Start on different port
npm run dev -- -p 3001

# Then open: http://localhost:3001
```

### "Analysis Failed" Error

**Check 1:** Is backend running?

Open: `http://localhost:8000/api/health`

Should see: `{"status":"healthy",...}`

**Check 2:** Check backend terminal for errors

**Check 3:** Are accession numbers valid?
- Must be real UniProt IDs
- One per line
- No extra spaces

### "npm install" Fails

**Error:** "Cannot find module..."

**Fix:**
```bash
# Delete and reinstall
rm -rf node_modules package-lock.json
npm install
```

### "ModuleNotFoundError" in Backend

**Error:** "No module named 'fastapi'"

**Fix:**
```bash
# Make sure virtual environment is activated
# You should see (venv) in your prompt

# Windows
.\venv\Scripts\activate

# Mac/Linux
source venv/bin/activate

# Then reinstall
pip install -r requirements.txt
```

### Docker "Port Already in Use"

**Error:** "port is already allocated"

**Fix:** Stop whatever is using the port
```bash
# Find what's using port 3000 or 8000
# Windows
netstat -ano | findstr :3000

# Mac/Linux
lsof -i :3000

# Kill it (replace PID with actual number)
kill -9 PID
```

---

## 📖 Learning Resources

### Want to Learn More?

**Next.js:**
- Official Tutorial: https://nextjs.org/learn
- Documentation: https://nextjs.org/docs

**React:**
- Official Tutorial: https://react.dev/learn
- Interactive: https://react-tutorial.app/

**FastAPI:**
- Tutorial: https://fastapi.tiangolo.com/tutorial/
- Full Course: https://testdriven.io/courses/tdd-fastapi/

**General Web Development:**
- FreeCodeCamp: https://www.freecodecamp.org/
- MDN Web Docs: https://developer.mozilla.org/

### Video Tutorials

Search YouTube for:
- "Next.js tutorial for beginners"
- "FastAPI tutorial"
- "React crash course"

---

## ✅ Quick Reference Card

### Start Application (Docker)
```bash
docker-compose up -d
```

### Start Application (Manual)

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate  # Mac/Linux
.\venv\Scripts\activate   # Windows
uvicorn app.main:app --reload
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

### Stop Application

**Docker:**
```bash
docker-compose down
```

**Manual:**
```
Press Ctrl+C in both terminals
```

### Check if Running

**Backend:** http://localhost:8000/api/health
**Frontend:** http://localhost:3000
**API Docs:** http://localhost:8000/api/docs

---

## 🎉 You're Ready!

You now know:
- ✅ How to start the application
- ✅ How to use it
- ✅ What each part does
- ✅ How to make simple changes
- ✅ How to fix common problems

**Next steps:**
1. Try analyzing your own sequences!
2. Share with your lab members
3. Customize the UI to your preferences
4. Learn more about Next.js and React

**Questions?** Check the main README.md or API docs!

---

**Happy analyzing! 🧬🔬**
