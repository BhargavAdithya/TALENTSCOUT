<div align="center">

# 🚀 TalentScout

### AI-Powered Technical Interview Platform

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Visit%20Now-blue?style=for-the-badge&logo=render)](https://talentscout-frontend.onrender.com)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)](https://postgresql.org)

**An intelligent, AI-driven technical interview platform that conducts adaptive technical screenings with real-time monitoring, automated evaluation, and comprehensive candidate assessment.**

Try it now: **https://talentscout-frontend.onrender.com**

</div>

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

<div align="center">

```mermaid
graph TB
    subgraph "Frontend Layer"
        A[Landing Page<br/>Permissions & Setup]
        B[Interview Flow<br/>Main Interface]
        C[Completion Page<br/>Results]
        A -->|Start Interview| B
        B -->|Complete| C
    end
    
    subgraph "API Layer"
        D[FastAPI Backend<br/>REST Endpoints]
        E[Business Logic<br/>Interview Management]
    end
    
    subgraph "Data Layer"
        F[(PostgreSQL<br/>Database)]
        G[Groq API<br/>LLM Integration]
        H[(Redis Cache<br/>Session Data)]
    end
    
    B <-->|HTTP Requests| D
    D <--> E
    E <-->|Store Data| F
    E <-->|Generate Questions| G
    E <-->|Cache State| H
    
    style A fill:#667eea,stroke:#764ba2,stroke-width:2px,color:#fff
    style B fill:#667eea,stroke:#764ba2,stroke-width:2px,color:#fff
    style C fill:#667eea,stroke:#764ba2,stroke-width:2px,color:#fff
    style D fill:#f093fb,stroke:#f5576c,stroke-width:2px,color:#fff
    style E fill:#f093fb,stroke:#f5576c,stroke-width:2px,color:#fff
    style F fill:#4facfe,stroke:#00f2fe,stroke-width:2px,color:#fff
    style G fill:#43e97b,stroke:#38f9d7,stroke-width:2px,color:#fff
    style H fill:#fa709a,stroke:#fee140,stroke-width:2px,color:#fff
```

</div>

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

### Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/talentscout.git
   cd talentscout
   ```

2. **Configure environment variables**
   - Set up backend `.env` with database and Groq API credentials
   - Set up frontend `.env` with backend URL

3. **Run the application**
   ```bash
   # Backend
   cd backend
   uvicorn main:app --reload
   
   # Frontend (in another terminal)
   cd frontend
   streamlit run app.py
   ```

4. **Access the platform**
   - Frontend: http://localhost:8501
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

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

### Tables
- **Candidates** - Stores candidate profile information
- **Interviews** - Tracks interview sessions and status
- **Questions** - Records questions asked and answers given

### Relationships
- **One-to-Many**: Candidate → Interviews
- **One-to-Many**: Interview → Questions

---

## 🤖 AI Integration

### Question Generation Pipeline
```
User Input → LLM Prompt Engineering → Groq API → Question Extraction → Validation
```

### Groq Configuration
- **Model**: `llama-3.3-70b-versatile`
- **Temperature**: 0.7 (balanced creativity/consistency)
- **Max Tokens**: 2000 per response
- **Timeout**: 180 seconds (3 minutes)

---

## 🤝 Contributing

We welcome contributions from the community! Whether you're fixing bugs, improving documentation, or adding new features, your help is appreciated.

### How to Contribute

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Ideas for Contribution
- Multi-language support
- Code execution environment for programming questions
- Admin dashboard for recruiters
- Resume parsing integration
- Email notifications
- Mobile application

---

## 📄 License

This project is licensed under the **MIT License** - see the LICENSE file for details.

---

## 📞 Contact

### Project Maintainer
- **Name**: Chandu Bhargav Adithya
- **LinkedIn**: [linkedin.com/in/yourprofile](https://www.linkedin.com/in/chandu-bhargav-adithya-5752792a0)
- **GitHub**: [@yourusername](https://github.com/BhargavAdithya)

### Support
- **Issues**: [GitHub Issues](https://github.com/BhargavAdithya/TALENTSCOUT/issues)
- **Discussions**: [GitHub Discussions](https://github.com/BhargavAdithya/TALENTSCOUT/discussions)

---

<div align="center">

### Built with ❤️ for smarter hiring

[⬆ Back to Top](#-talentscout)

</div>