# 🚀 TalentScout - AI-Powered Technical Interview Platform

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Visit%20Now-blue?style=for-the-badge&logo=render)](https://talentscout-frontend.onrender.com)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)](https://postgresql.org)

> **An intelligent, AI-driven technical interview platform that conducts adaptive technical screenings with real-time monitoring, automated evaluation, and comprehensive candidate assessment.**

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Key Features](#-key-features)
- [Live Demo](#-live-demo)
- [Technology Stack](#-technology-stack)
- [Architecture](#-architecture)
- [Getting Started](#-getting-started)
- [Project Structure](#-project-structure)
- [Environment Variables](#-environment-variables)
- [API Endpoints](#-api-endpoints)
- [Security Features](#-security-features)
- [Database Schema](#-database-schema)
- [AI Integration](#-ai-integration)
- [Deployment](#-deployment)
- [Screenshots](#-screenshots)
- [Contributing](#-contributing)
- [License](#-license)
- [Contact](#-contact)

---

## 🎯 Overview

**TalentScout** is a cutting-edge interview automation platform that leverages AI to conduct technical interviews at scale. It combines adaptive questioning, real-time monitoring, and intelligent evaluation to provide a comprehensive and fair assessment of candidates' technical capabilities.

### Why TalentScout?

- **🤖 AI-Powered**: Uses advanced LLMs (Groq API with Llama 3.3 70B) for dynamic question generation
- **⚡ Adaptive Difficulty**: Questions adjust based on candidate performance
- **📹 Real-time Monitoring**: Live camera and audio monitoring with violation tracking
- **🔒 Secure Environment**: Comprehensive anti-cheating measures and fullscreen enforcement
- **📊 Automated Scoring**: Intelligent answer evaluation with detailed performance metrics
- **🎯 Fair Assessment**: Unbiased, consistent evaluation across all candidates

---

## ✨ Key Features

### 🎤 **Intelligent Interview System**
- **Dynamic Question Generation**: AI generates scenario-based technical questions tailored to:
  - Candidate's tech stack (languages, frameworks, databases, tools)
  - Experience level (0-70 years)
  - Position applied for
  - Previous answer quality
- **Adaptive Difficulty**: Questions become harder/easier based on performance (1-5 scale)
- **Topic Coverage**: Ensures diverse coverage across the candidate's tech stack
- **Time-Limited Questions**: 3-minute countdown timer per question (5 questions total)

### 🔐 **Security & Anti-Cheating**
- **Camera Monitoring**: Live video feed with draggable preview window
- **Fullscreen Enforcement**: Interview must be conducted in fullscreen mode
- **Keyboard Restrictions**: Disabled shortcuts (Ctrl+C, Ctrl+V, F12, Alt+Tab, etc.)
- **Context Menu Blocking**: Right-click and inspect element disabled
- **Violation Tracking**: 10-strike policy - automatic termination on 10th violation
- **Tab Switch Detection**: Monitors and logs any attempt to leave the interview
- **Duplicate Prevention**: Email/phone validation to prevent multiple attempts (3-strike policy)

### 📊 **Evaluation & Analytics**
- **AI-Based Scoring**: Answers evaluated on:
  - Technical accuracy (30%)
  - Depth of understanding (25%)
  - Clarity and communication (20%)
  - Practical application (15%)
  - Completeness (10%)
- **Time Efficiency Bonus**: Rewards quick, accurate responses
- **Overall Rating**: Candidate rated 0-5 stars based on complete interview performance
- **Skip Detection**: Identifies and scores skipped questions appropriately
- **Timeout Handling**: Automatic submission and scoring on timer expiration

### 🎨 **User Experience**
- **Clean, Modern UI**: Gradient backgrounds, smooth animations, responsive design
- **Real-time Feedback**: Live timer, question counter, violation warnings
- **Progress Tracking**: Visual indicators for information gathering and technical assessment
- **Accessibility**: Keyboard navigation in input fields, clear visual hierarchy
- **Mobile Warning**: Alerts users if accessing from non-desktop devices

### 📝 **Candidate Information Collection**
- **Comprehensive Profile**:
  - Full name validation (first + last name required)
  - Email validation (RFC-compliant regex with duplicate checking)
  - Phone number validation (10-15 digits, international format supported)
  - Experience in years (0-70, decimal values accepted)
  - Position/role applying for
  - Preferred job locations (minimum 3 required)
  - Tech stack (languages, frameworks, databases, tools)
- **Validation Feedback**: Real-time validation with helpful error messages

### 🔄 **Interview Flow Management**
- **Question Types**:
  - Initial question based on experience and tech stack
  - Follow-up questions based on previous answers
  - New topic questions for coverage diversity
  - Skip support ("PASS" keyword)
- **State Management**: Robust session handling across page reruns
- **Completion Detection**: Automatic interview conclusion after 5 questions
- **Redirect Flow**: Smooth transition to completion page with 5-second countdown

---

## 🌐 Live Demo

**Try it now:** [https://talentscout-frontend.onrender.com](https://talentscout-frontend.onrender.com)

### Sample Interview Flow:
1. Grant camera and microphone permissions
2. Enter fullscreen mode
3. Provide candidate information (7 questions)
4. Press "OK" to begin technical interview
5. Answer 5 technical questions (3 minutes each)
6. View completion screen and exit

### Test Credentials:
- **No login required** - Direct access to interview
- **Sample Tech Stack**: "Python, Django, PostgreSQL, React, AWS"
- **Sample Position**: "Full Stack Developer"

> **Note**: The demo uses free-tier hosting on Render, so initial load may take 30-60 seconds (cold start).

---

## 🛠️ Technology Stack

### **Frontend**
| Technology | Version | Purpose |
|-----------|---------|---------|
| **Streamlit** | 1.28+ | Interactive web application framework |
| **Python** | 3.11+ | Core programming language |
| **JavaScript** | ES6+ | Browser-level monitoring and protection |
| **HTML5/CSS3** | - | Custom styling and animations |
| **WebRTC** | - | Camera and audio stream handling |

### **Backend**
| Technology | Version | Purpose |
|-----------|---------|---------|
| **FastAPI** | 0.104+ | High-performance REST API framework |
| **SQLAlchemy** | 2.0+ | ORM for database operations |
| **Pydantic** | 2.0+ | Data validation and serialization |
| **Uvicorn** | 0.24+ | ASGI server for FastAPI |
| **Python** | 3.11+ | Core programming language |

### **Database**
| Technology | Version | Purpose |
|-----------|---------|---------|
| **PostgreSQL** | 15+ | Primary relational database |
| **psycopg2** | 2.9+ | PostgreSQL adapter for Python |

### **AI/ML**
| Technology | Version | Purpose |
|-----------|---------|---------|
| **Groq API** | Latest | LLM inference engine |
| **Llama 3.3 70B** | - | Large language model for question generation |
| **Requests** | 2.31+ | HTTP client for API calls |

### **DevOps & Deployment**
| Technology | Version | Purpose |
|-----------|---------|---------|
| **Render** | - | Cloud hosting platform (frontend & backend) |
| **Neon** | - | Serverless PostgreSQL database |
| **Git** | 2.40+ | Version control |
| **python-dotenv** | 1.0+ | Environment variable management |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         Frontend (Streamlit)                 │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  app.py     │  │ interview.py │  │ completion.py│      │
│  │ (Landing)   │→ │ (Main Flow)  │→ │ (End Screen) │      │
│  └─────────────┘  └──────────────┘  └──────────────┘      │
│         │                  │                  │              │
│         └──────────────────┼──────────────────┘              │
│                           │                                  │
└───────────────────────────┼──────────────────────────────────┘
                            │
                    ┌───────▼────────┐
                    │   FastAPI      │
                    │   Backend      │
                    └───────┬────────┘
                            │
            ┌───────────────┼───────────────┐
            │               │               │
    ┌───────▼──────┐ ┌─────▼──────┐ ┌─────▼──────┐
    │  PostgreSQL  │ │  Groq API  │ │   Redis    │
    │  (Database)  │ │    (LLM)   │ │  (Cache)   │
    └──────────────┘ └────────────┘ └────────────┘
```

### Request Flow:
1. **Frontend** → User interacts with Streamlit UI
2. **API Layer** → Streamlit sends HTTP requests to FastAPI backend
3. **Business Logic** → FastAPI processes requests, calls LLM, manages state
4. **Database** → PostgreSQL stores candidate data, interviews, questions
5. **AI Integration** → Groq API generates/evaluates questions
6. **Response** → Backend returns data to frontend for display

---

## 🚀 Getting Started

### Prerequisites

- **Python** 3.11 or higher
- **PostgreSQL** 15 or higher (or Neon serverless database)
- **Groq API Key** (free tier available at [console.groq.com](https://console.groq.com))
- **Git** 2.40 or higher
- **Modern browser** (Chrome 90+, Firefox 88+, Safari 14+)

### Installation

#### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/talentscout.git
cd talentscout
```

#### 2. Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env with your credentials

# Initialize database
python -c "from database import engine; from models import Base; Base.metadata.create_all(bind=engine)"

# Run backend server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### 3. Frontend Setup
```bash
cd ../frontend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env with backend URL

# Run frontend
streamlit run app.py
```

#### 4. Access the Application
- **Frontend**: http://localhost:8501
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

---

## 📁 Project Structure

```
talentscout/
│
├── backend/                    # FastAPI backend
│   ├── __pycache__/           # Python cache
│   ├── venv/                  # Virtual environment
│   ├── .env                   # Environment variables
│   ├── database.py            # Database connection & session
│   ├── interview.py           # Interview logic (difficulty)
│   ├── llm.py                 # LLM integration (Groq API)
│   ├── main.py                # FastAPI app & endpoints
│   ├── models.py              # SQLAlchemy ORM models
│   ├── schemas.py             # Pydantic schemas
│   └── requirements.txt       # Python dependencies
│
├── frontend/                   # Streamlit frontend
│   ├── pages/                 # Streamlit pages
│   │   ├── completion.py      # Interview completion page
│   │   ├── interview.py       # Main interview flow
│   │   └── termination.py     # Termination page (violations)
│   ├── __pycache__/           # Python cache
│   ├── venv/                  # Virtual environment
│   ├── .env                   # Environment variables
│   ├── app.py                 # Landing page (permissions)
│   ├── styles.py              # CSS styles
│   ├── utils.py               # Helper functions
│   └── requirements.txt       # Python dependencies
│
├── .gitignore                 # Git ignore rules
└── README.md                  # This file
```

---

## 🔧 Environment Variables

### Backend (.env)
```env
# Database
DATABASE_URL=postgresql://user:password@host:port/database

# Groq API
GROQ_API_KEY=your_groq_api_key_here
GROQ_API_URL=https://api.groq.com/openai/v1/chat/completions
MODEL_NAME=llama-3.3-70b-versatile

# Server
HOST=0.0.0.0
PORT=8000
```

### Frontend (.env)
```env
# Backend URL
BACKEND_URL=http://localhost:8000
# Or for production: https://your-backend.onrender.com
```

---

## 🔌 API Endpoints

### Health Check
```http
GET /
```
Returns backend status and active interview count.

### Start Interview
```http
POST /start
Content-Type: application/json

{
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "1234567890",
  "experience": 3.5,
  "position": "Full Stack Developer",
  "location": "San Francisco, New York, Remote",
  "tech_stack": "Python, Django, React, PostgreSQL, AWS"
}
```

### Submit Answer
```http
POST /answer
Content-Type: application/json

{
  "interview_id": 1,
  "question": "Explain React hooks",
  "answer": "React hooks are functions that..."
}
```

### Get Next Question
```http
GET /next-question/{interview_id}
```

### Get Timer
```http
GET /timer/{interview_id}
```

### Record Violation
```http
POST /violation/{interview_id}
Content-Type: application/json

{
  "type": "ctrl_c"
}
```

### Check Duplicate
```http
POST /check-duplicate
Content-Type: application/json

{
  "email": "test@example.com",
  "phone": "1234567890"
}
```

### Terminate Interview
```http
POST /terminate/{interview_id}
```

### Get Interview Status
```http
GET /status/{interview_id}
```

---

## 🔒 Security Features

### Authentication & Authorization
- **No user accounts**: Direct interview access (reduces friction)
- **Session-based**: Interview ID tracks state
- **Email/Phone validation**: Prevents duplicate attempts

### Anti-Cheating Measures
| Feature | Implementation | Violation Count |
|---------|---------------|----------------|
| **Copy/Paste** | Disabled via JavaScript + event blocking | ✅ Tracked |
| **Right-click** | Context menu completely disabled | ✅ Tracked |
| **Keyboard Shortcuts** | Ctrl+C/V/X, F12, Ctrl+Shift+I blocked | ✅ Tracked |
| **Tab Switching** | Detected but not blocked (privacy) | ❌ Not tracked |
| **Fullscreen Exit** | 3 exits = automatic termination | ✅ Separate tracking |
| **Text Selection** | Disabled except in input fields | ✅ Tracked |
| **DevTools** | F12, Ctrl+Shift+I/J/U blocked | ✅ Tracked |

### Privacy & Compliance
- **Camera/Audio**: Requested explicitly, used only for monitoring
- **No recording**: Streams are live-only, not saved
- **Data protection**: Candidate info stored securely in PostgreSQL
- **Transparent violations**: Candidates see warning messages

---

## 💾 Database Schema

### Candidates Table
```sql
CREATE TABLE candidates (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    phone VARCHAR(20) UNIQUE NOT NULL,
    experience FLOAT NOT NULL,
    position VARCHAR(100) NOT NULL,
    location VARCHAR(200) NOT NULL,
    tech_stack TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);
```

### Interviews Table
```sql
CREATE TABLE interviews (
    id SERIAL PRIMARY KEY,
    candidate_id INTEGER REFERENCES candidates(id),
    started_at TIMESTAMP DEFAULT NOW(),
    ended_at TIMESTAMP,
    status VARCHAR(50) NOT NULL,
    candidate_rating FLOAT,
    violations INTEGER DEFAULT 0
);
```

### Questions Table
```sql
CREATE TABLE questions (
    id SERIAL PRIMARY KEY,
    interview_id INTEGER REFERENCES interviews(id),
    question_text TEXT NOT NULL,
    answer_text TEXT NOT NULL,
    difficulty FLOAT NOT NULL,
    score FLOAT,
    answered_at TIMESTAMP DEFAULT NOW()
);
```

### Relationships
- **One-to-Many**: Candidate → Interviews
- **One-to-Many**: Interview → Questions

---

## 🤖 AI Integration

### Question Generation Pipeline
```
User Input → LLM Prompt Engineering → Groq API → Question Extraction → Validation
```

### Prompt Strategy
- **Context-aware**: Includes experience, tech stack, position
- **Adaptive**: References previous answers for follow-ups
- **Scenario-based**: Focuses on real-world problems, not theory
- **Difficulty scaling**: Explicit difficulty instructions (1-5)
- **Topic tracking**: Ensures coverage across tech stack

### Evaluation Criteria
```python
{
    "technical_accuracy": 30%,      # Is it correct?
    "depth_of_understanding": 25%,  # Surface vs deep knowledge?
    "clarity": 20%,                 # Well-explained?
    "practical_application": 15%,   # Shows experience?
    "completeness": 10%             # Addresses all aspects?
}
```

### Groq Configuration
- **Model**: `llama-3.3-70b-versatile`
- **Temperature**: 0.7 (balanced creativity/consistency)
- **Max Tokens**: 2000 per response
- **Timeout**: 180 seconds (3 minutes)

---

## 🌍 Deployment

### Frontend (Render)
1. Connect GitHub repository
2. **Build Command**: `pip install -r requirements.txt`
3. **Start Command**: `streamlit run app.py --server.port=$PORT --server.address=0.0.0.0`
4. **Environment Variables**: `BACKEND_URL`

### Backend (Render)
1. Connect GitHub repository
2. **Build Command**: `pip install -r requirements.txt`
3. **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. **Environment Variables**: `DATABASE_URL`, `GROQ_API_KEY`, `GROQ_API_URL`, `MODEL_NAME`

### Database (Neon)
1. Create new project at [neon.tech](https://neon.tech)
2. Copy connection string
3. Add to backend `DATABASE_URL` environment variable

### Environment Setup (Production)
```bash
# Backend
DATABASE_URL=postgresql://user:pass@hostname/dbname?sslmode=require
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxxx
GROQ_API_URL=https://api.groq.com/openai/v1/chat/completions
MODEL_NAME=llama-3.3-70b-versatile

# Frontend
BACKEND_URL=https://your-backend.onrender.com
```

---

## 📸 Screenshots

### Landing Page (Permissions)
![Landing Page](https://via.placeholder.com/800x450/667eea/ffffff?text=Landing+Page+-+Grant+Permissions)

### Candidate Information Collection
![Information Collection](https://via.placeholder.com/800x450/667eea/ffffff?text=Candidate+Information+Form)

### Technical Interview (Question Display)
![Technical Interview](https://via.placeholder.com/800x450/667eea/ffffff?text=Technical+Interview+-+Live+Question)

### Live Monitoring (Camera + Timer)
![Live Monitoring](https://via.placeholder.com/800x450/667eea/ffffff?text=Camera+Monitor+%26+Timer)

### Completion Screen
![Completion](https://via.placeholder.com/800x450/667eea/ffffff?text=Interview+Completed)

---

## 🤝 Contributing

We welcome contributions! Here's how you can help:

### 1. Fork the Repository
```bash
git clone https://github.com/yourusername/talentscout.git
cd talentscout
git checkout -b feature/your-feature-name
```

### 2. Make Changes
- Follow PEP 8 style guide for Python
- Add comments for complex logic
- Update documentation if needed

### 3. Test Thoroughly
```bash
# Backend tests
pytest backend/

# Frontend manual testing
streamlit run frontend/app.py
```

### 4. Submit Pull Request
- Clear title and description
- Reference any related issues
- Include screenshots if UI changes

### Areas for Contribution
- [ ] Add support for multiple languages
- [ ] Implement code execution for programming questions
- [ ] Add video recording option
- [ ] Create admin dashboard for recruiters
- [ ] Add email notifications
- [ ] Implement resume parsing
- [ ] Add support for whiteboard questions
- [ ] Create mobile app version

---

## 📄 License

This project is licensed under the **MIT License**.

```
MIT License

Copyright (c) 2025 TalentScout

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 📞 Contact

### Project Maintainer
- **Name**: Your Name
- **Email**: your.email@example.com
- **LinkedIn**: [linkedin.com/in/yourprofile](https://linkedin.com/in/yourprofile)
- **GitHub**: [@yourusername](https://github.com/yourusername)

### Support
- **Issues**: [GitHub Issues](https://github.com/yourusername/talentscout/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/talentscout/discussions)
- **Email**: support@talentscout.dev

---

## 🙏 Acknowledgments

- **Groq** - For providing fast, reliable LLM inference
- **Streamlit** - For the amazing web framework
- **FastAPI** - For the high-performance backend framework
- **Render** - For seamless deployment
- **Neon** - For serverless PostgreSQL
- **Open Source Community** - For inspiration and support

---

## 🗺️ Roadmap

### Q1 2025
- [x] Core interview functionality
- [x] AI-powered question generation
- [x] Real-time monitoring
- [ ] Admin dashboard
- [ ] Email notifications

### Q2 2025
- [ ] Video recording
- [ ] Code execution environment
- [ ] Multi-language support
- [ ] Resume parsing
- [ ] Interview analytics

### Q3 2025
- [ ] Mobile app (React Native)
- [ ] Integration with ATS systems
- [ ] Advanced proctoring (eye tracking)
- [ ] Team collaboration features

### Q4 2025
- [ ] Enterprise features
- [ ] Custom branding
- [ ] API for third-party integrations
- [ ] Machine learning for candidate matching

---

## 📊 Project Statistics

![GitHub stars](https://img.shields.io/github/stars/yourusername/talentscout?style=social)
![GitHub forks](https://img.shields.io/github/forks/yourusername/talentscout?style=social)
![GitHub issues](https://img.shields.io/github/issues/yourusername/talentscout)
![GitHub pull requests](https://img.shields.io/github/issues-pr/yourusername/talentscout)
![GitHub last commit](https://img.shields.io/github/last-commit/yourusername/talentscout)
![GitHub code size](https://img.shields.io/github/languages/code-size/yourusername/talentscout)

---

<div align="center">

### ⭐ Star this repo if you find it helpful!

**Built with ❤️ by the TalentScout Team**

[🌐 Live Demo](https://talentscout-frontend.onrender.com) • [📖 Documentation](https://docs.talentscout.dev) • [🐛 Report Bug](https://github.com/yourusername/talentscout/issues) • [✨ Request Feature](https://github.com/yourusername/talentscout/issues)

---

© 2025 TalentScout. All rights reserved.

</div>