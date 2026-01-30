# backend/main.py
import os
from dotenv import load_dotenv
load_dotenv()
import interview
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta
from schemas import CandidateCreate, AnswerRequest
from interview import initial_difficulty, next_difficulty
from llm import ask_technical_question, evaluate_answer
import threading
import time
import random
from database import engine
from models import Base

app = FastAPI(title="TalentScout Backend")

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

# Add CORS middleware to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

INTERVIEWS = {}
INTERVIEW_ID = 1
OTP_STORE = {}  # Store OTPs with expiration
    
@app.get("/")
def root():
    """Health check endpoint"""
    return {
        "status": "ok", 
        "message": "TalentScout Backend is running",
        "version": "1.0.0",
        "active_interviews": len(INTERVIEWS)
    }

def process_next_question(interview_id: int):
    """Process the next question after evaluating the previous answer"""
    interview = INTERVIEWS.get(interview_id)
    if not interview:
        print(f"❌ process_next_question: Interview {interview_id} not found")
        return

    print(f"🔄 process_next_question: Starting for interview {interview_id}")
    print(f"   Current status: {interview['status']}")
    print(f"   Question count: {interview['question_count']}")
    
    last = interview["answers"][-1]
    # Calculate time taken
    time_taken = int((datetime.utcnow() - last.get("timestamp", datetime.utcnow())).total_seconds())
    time_taken = min(time_taken, 180)  # Cap at 180 seconds

    # Evaluate answer and get score
    evaluation = evaluate_answer(
        last["question"], 
        last["answer"],
        interview["difficulty"],
        time_taken
    )
    passed = evaluation["passed"]
    score = evaluation["score"]

    from database import SessionLocal
    from models import Question

    db = SessionLocal()

    db_question = Question(
        interview_id=interview_id,
        question_text=last["question"],
        answer_text=last["answer"],
        difficulty=interview["difficulty"],
        score=score
    )

    db.add(db_question)
    db.commit()
    db.close()

    print(f"📝 Question scored: {score}/10 (Passed: {passed})")

    interview["difficulty"] = next_difficulty(interview["difficulty"], passed)
    interview["question_count"] += 1
    
    print(f"📊 Question count after increment: {interview['question_count']}")

    if interview["question_count"] > 5:
        interview["status"] = "completed"
        print(f"✅ Interview {interview_id} completed after {interview['question_count']} questions")
        
        # Calculate and save candidate rating
        from llm import rate_candidate
        from database import SessionLocal
        from models import Interview
        
        db = SessionLocal()
        
        questions_data = [
            {
                "question": ans["question"],
                "answer": ans["answer"],
                "score": 0.0,
                "difficulty": interview["difficulty"]
            }
            for ans in interview["answers"]
        ]
        
        db_interview = db.query(Interview).filter(Interview.id == interview_id).first()
        if db_interview and db_interview.questions:
            for i, db_q in enumerate(db_interview.questions):
                if i < len(questions_data):
                    questions_data[i]["score"] = db_q.score if db_q.score else 0.0
                    questions_data[i]["difficulty"] = db_q.difficulty
        
        candidate_rating = rate_candidate(interview["candidate_info"], questions_data)
        
        if db_interview:
            db_interview.candidate_rating = candidate_rating
            db_interview.ended_at = datetime.utcnow()
            db_interview.status = "completed"
            db.commit()
        
        db.close()
        
        print(f"⭐ Candidate rated: {candidate_rating}/5.0")
        return  # EXIT FUNCTION - interview is complete
    
        print(f"➡️ Continuing to generate next question...")
        
        # Calculate candidate rating
        from llm import rate_candidate
        from database import SessionLocal
        from models import Interview
        
        db = SessionLocal()
        
        # Prepare questions data for rating
        questions_data = [
            {
                "question": ans["question"],
                "answer": ans["answer"],
                "score": 0.0,  # Will be fetched from DB
                "difficulty": interview["difficulty"]
            }
            for ans in interview["answers"]
        ]
        
        # Fetch actual scores from database
        db_interview = db.query(Interview).filter(Interview.id == interview_id).first()
        if db_interview and db_interview.questions:
            for i, db_q in enumerate(db_interview.questions):
                if i < len(questions_data):
                    questions_data[i]["score"] = db_q.score if db_q.score else 0.0
                    questions_data[i]["difficulty"] = db_q.difficulty
        
        # Rate candidate
        candidate_rating = rate_candidate(interview["candidate_info"], questions_data)
        
        # Update interview record with rating and end time
        if db_interview:
            db_interview.candidate_rating = candidate_rating
            db_interview.ended_at = datetime.utcnow()
            db_interview.status = "completed"
            db.commit()
        
        db.close()
        
        print(f"⭐ Candidate rated: {candidate_rating}/5.0")
        
        return

    # Determine question type based on context and strategy
    try:
        from llm import ask_followup_question, ask_new_topic_question

        # Check if answer was skipped (PASS) or timed out
        was_skipped = last["answer"].lower().strip() in {
            "pass", "skip", "idk", "i don't know", "don't know",
            "no idea", "not sure", "n/a"
        }
        was_timeout = "[AUTO-SUBMITTED: TIME EXPIRED]" in last["answer"]

        print(f"   Generating next question (skipped={was_skipped}, timeout={was_timeout})")

        # Decide question strategy
        if was_skipped:
            # User skipped - generate from new topic
            next_q = ask_new_topic_question(
                interview["tech_stack"],
                interview["difficulty"],
                interview["candidate_info"]["position"],
                interview["candidate_info"]["experience"],
                interview["covered_topics"],
                interview["question_history"]
            )
            interview["last_question_type"] = "new_topic"
        elif was_timeout:
            # Timeout - 50% chance new topic, 50% followup
            import random
            if random.random() < 0.5 or interview["last_question_type"] == "followup":
                # Generate new topic
                next_q = ask_new_topic_question(
                    interview["tech_stack"],
                    interview["difficulty"],
                    interview["candidate_info"]["position"],
                    interview["candidate_info"]["experience"],
                    interview["covered_topics"],
                    interview["question_history"]
                )
                interview["last_question_type"] = "new_topic"
            else:
                # Continue with followup
                next_q = ask_followup_question(
                    interview["tech_stack"],
                    interview["difficulty"],
                    interview["candidate_info"]["position"],
                    interview["candidate_info"]["experience"],
                    last["question"],
                    last["answer"],
                    interview["covered_topics"]
                )
                interview["last_question_type"] = "followup"
        else:
            # Normal answer - alternate between followup and new topic
            if interview["last_question_type"] == "followup" or interview["question_count"] % 2 == 0:
                # Generate new topic every alternate question
                next_q = ask_new_topic_question(
                    interview["tech_stack"],
                    interview["difficulty"],
                    interview["candidate_info"]["position"],
                    interview["candidate_info"]["experience"],
                    interview["covered_topics"],
                    interview["question_history"]
                )
                interview["last_question_type"] = "new_topic"
            else:
                # Followup question
                next_q = ask_followup_question(
                    interview["tech_stack"],
                    interview["difficulty"],
                    interview["candidate_info"]["position"],
                    interview["candidate_info"]["experience"],
                    last["question"],
                    last["answer"],
                    interview["covered_topics"]
                )
                interview["last_question_type"] = "followup"

        # Store question in history
        interview["question_history"].append(next_q)
        interview["current_question"] = next_q
        interview["status"] = "ready"
        interview["question_started_at"] = datetime.utcnow()
        print(f"✅ Next question ready for interview {interview_id}")
        print(f"   Question text: {next_q[:100]}...")
        print(f"   Status: {interview['status']}")
        print(f"   Question count: {interview['question_count']}")
        print(f"🎉 process_next_question COMPLETED successfully for interview {interview_id}")
        
    except Exception as e:
        print(f"❌ Error generating next question: {e}")
        import traceback
        traceback.print_exc()
        # Mark as completed on error
        interview["status"] = "completed"
        print(f"⚠️ Marking interview {interview_id} as completed due to error")


def monitor_timer(interview_id: int):
    """Background thread that monitors timer and auto-submits on timeout"""
    while True:
        time.sleep(1)
        
        interview = INTERVIEWS.get(interview_id)
        if not interview or interview["status"] != "ready":
            break
        
        elapsed = (datetime.utcnow() - interview["question_started_at"]).total_seconds()
        remaining = max(0, interview["time_limit"] - int(elapsed))
        
        if remaining == 0:
            print(f"⏰ Timer expired for interview {interview_id}")
            print(f"   Current question: {interview['current_question'][:100] if interview.get('current_question') else 'NONE'}...")
            
            # Save the current question BEFORE changing status
            timed_out_question = interview.get("current_question", "")
            
            interview["answers"].append({
                "question": timed_out_question,
                "answer": "[AUTO-SUBMITTED: TIME EXPIRED]",
                "timestamp": datetime.utcnow()
            })
            
            print(f"   Timeout answer appended, starting processing...")
            interview["status"] = "processing"
            
            threading.Thread(
                target=process_next_question,
                args=(interview_id,),
                daemon=True
            ).start()
            break

@app.post("/check-duplicate")
def check_duplicate(data: dict):
    """Check if email or phone already exists in database"""
    email = data.get("email", "").strip().lower()
    phone = data.get("phone", "").strip()
    
    from database import SessionLocal
    from models import Candidate
    
    db = SessionLocal()
    
    duplicates = []
    
    if email:
        existing_email = db.query(Candidate).filter(Candidate.email == email).first()
        if existing_email:
            duplicates.append("email")
    
    if phone:
        existing_phone = db.query(Candidate).filter(Candidate.phone == phone).first()
        if existing_phone:
            duplicates.append("phone")
    
    db.close()
    
    return {
        "duplicates": duplicates,
        "has_duplicates": len(duplicates) > 0
    }

# =========================
# START INTERVIEW
# =========================
@app.post("/start")
def start_interview(candidate: CandidateCreate):
    """Start a new interview session"""
    global INTERVIEW_ID

    print(f"\n{'=' * 60}")
    print(f"🎯 STARTING NEW INTERVIEW")
    print(f"{'=' * 60}")
    print(f"👤 Candidate: {candidate.name}")
    print(f"📧 Email: {candidate.email}")
    print(f"📱 Phone: {candidate.phone}")
    print(f"💼 Experience: {candidate.experience} years")
    print(f"🎯 Position: {candidate.position}")
    print(f"📍 Location: {candidate.location}")
    print(f"🔧 Tech stack: {candidate.tech_stack}")
    
    difficulty = initial_difficulty(candidate.experience)
    print(f"📊 Initial difficulty: {difficulty}")

    from database import SessionLocal
    from models import Candidate, Interview

    db = SessionLocal()

    # Save candidate
    db_candidate = Candidate(
        name=candidate.name,
        email=candidate.email.strip().lower(),
        phone=candidate.phone,
        experience=candidate.experience,
        position=candidate.position,
        location=candidate.location,
        tech_stack=candidate.tech_stack
    )
    db.add(db_candidate)
    db.commit()
    db.refresh(db_candidate)

    # Create interview record
    db_interview = Interview(
        candidate_id=db_candidate.id,
        status="started",
        violations=0
    )
    db.add(db_interview)
    db.commit()
    db.refresh(db_interview)

    db.close()
    
    question = ask_technical_question(
        candidate.tech_stack, 
        difficulty, 
        candidate.position, 
        candidate.experience
    )
    print(f"❓ First question generated: {question[:100]}...")

    INTERVIEWS[INTERVIEW_ID] = {
        "difficulty": difficulty,
        "current_question": question,
        "question_count": 1,
        "tech_stack": candidate.tech_stack,
        "answers": [],
        "status": "ready",
        "question_started_at": datetime.utcnow(),
        "time_limit": 180,  # 3 minutes per question
        "violation_count": 0,
        "is_terminated": False,
        "fullscreen_active": True,  # Track fullscreen status
        "monitor_ready": True,
        "candidate_info": {
            "name": candidate.name,
            "email": candidate.email,
            "phone": candidate.phone,
            "experience": candidate.experience,
            "position": candidate.position,
            "location": candidate.location
        },
        "covered_topics": [],  # Track which tech stack areas have been covered
        "last_question_type": None,  # Track if last question was 'followup' or 'new_topic'
        "question_history": [],  # Store all questions asked to avoid repetition
    }

    # Start timer monitoring
    threading.Thread(
        target=monitor_timer,
        args=(INTERVIEW_ID,),
        daemon=True
    ).start()

    response = {
        "interview_id": INTERVIEW_ID,
        "question": question,
        "message": "Interview started successfully",
        "time_limit": 180
    }
    
    print(f"🆔 Interview ID: {INTERVIEW_ID}")
    print(f"✅ Interview session created successfully")
    print(f"{'=' * 60}\n")

    INTERVIEW_ID += 1
    return response

@app.post("/answer")
def submit_answer(data: AnswerRequest):
    """Submit an answer to the current question"""
    interview = INTERVIEWS.get(data.interview_id)

    if not interview:
        raise HTTPException(status_code=404, detail="Invalid interview ID")

    if interview["status"] in ["processing"]:
        print(f"⚠️ Answer submission rejected - already processing")
        return {"status": "already_processing"}

    print(f"\n📝 Answer submitted for interview {data.interview_id}")
    print(f"   Question: {data.question[:80]}...")
    print(f"   Answer: {data.answer[:80]}...")
    print(f"   Current status: {interview['status']}")

    interview["status"] = "processing"

    # Calculate time taken for this question
    question_start_time = interview.get("question_started_at", datetime.utcnow())
    time_taken = int((datetime.utcnow() - question_start_time).total_seconds())

    interview["answers"].append({
        "question": data.question,
        "answer": data.answer,
        "timestamp": datetime.utcnow(),
        "time_taken": time_taken
    })

    print(f"   Starting background processing...")
    
    # Process next question in background
    threading.Thread(
        target=process_next_question,
        args=(data.interview_id,),
        daemon=True
    ).start()

    return {"status": "processing", "message": "Answer submitted successfully"}

@app.get("/next-question/{interview_id}")
def get_next_question(interview_id: int):
    """Get the next question after processing"""
    interview = INTERVIEWS.get(interview_id)

    if not interview:
        raise HTTPException(status_code=404, detail="Invalid interview ID")

    current_status = interview["status"]
    print(f"🔍 /next-question called for {interview_id}, status: {current_status}, count: {interview['question_count']}")

    if current_status == "completed":
        print(f"✅ Interview {interview_id} completed")
        return {"completed": True, "message": "Interview completed successfully"}

    if current_status == "processing":
        print(f"⏳ Still processing interview {interview_id}")
        return {"status": "processing", "message": "Processing your answer..."}

    # Ready to show question - start timer
    if current_status == "ready":
        print(f"✅ Returning question {interview['question_count']} for interview {interview_id}")
        
        threading.Thread(
            target=monitor_timer,
            args=(interview_id,),
            daemon=True
        ).start()

        return {
            "question": interview["current_question"],
            "question_number": interview["question_count"],
            "total_questions": 5
        }
    
    # Unknown/unexpected status
    print(f"⚠️ Unexpected status '{current_status}' for interview {interview_id}")
    return {"status": current_status, "message": "Processing..."}

@app.get("/timer/{interview_id}")
def get_timer(interview_id: int):
    """Get remaining time for current question"""
    interview = INTERVIEWS.get(interview_id)

    if not interview:
        raise HTTPException(status_code=404, detail="Invalid interview ID")

    if interview["status"] != "ready":
        return {"remaining": 0, "timeout": interview["status"] == "timeout"}

    elapsed = (datetime.utcnow() - interview["question_started_at"]).total_seconds()
    remaining = max(0, interview["time_limit"] - int(elapsed))

    return {
        "remaining": remaining, 
        "timeout": False,
        "elapsed": int(elapsed)
    }

@app.post("/violation/{interview_id}")
def record_violation(interview_id: int, data: dict = None):
    """Record a policy violation (keyboard/interaction violations)"""
    interview = INTERVIEWS.get(interview_id)

    if not interview:
        raise HTTPException(status_code=404, detail="Invalid interview ID")

    # Only count violations during technical interview
    if interview.get("status") not in ["ready", "processing"]:
        return {
            "violation_count": interview["violation_count"],
            "terminated": False,
            "remaining_warnings": max(0, 10 - interview["violation_count"])
        }

    # Record the violation
    interview["violation_count"] += 1
    
    violation_type = data.get("type", "unknown") if data else "unknown"
    print(f"⚠️ Policy violation: {violation_type}")
    print(f"Total violations: {interview['violation_count']}/10")

    # Terminate on 10th violation
    terminated = interview["violation_count"] >= 10

    if terminated:
        interview["is_terminated"] = True
        interview["status"] = "terminated"
        print(f"❌ Interview {interview_id} TERMINATED due to violations")
    
    # Update database with violation count and termination details
    from database import SessionLocal
    from models import Interview
    from datetime import datetime
    
    db = SessionLocal()
    try:
        db_interview = db.query(Interview).filter(Interview.id == interview_id).first()
        if db_interview:
            # Update violation count
            db_interview.violations = interview["violation_count"]
            
            # If terminated, update database accordingly
            if terminated:
                db_interview.status = "terminated"
                db_interview.ended_at = datetime.utcnow()
                db_interview.candidate_rating = None  # Set rating to NULL for terminated interviews
                print(f"📝 Database updated - Status: terminated, Ended at: {db_interview.ended_at}, Rating: NULL, Violations: {db_interview.violations}")
            
            db.commit()
            db.refresh(db_interview)
    except Exception as e:
        print(f"❌ Failed to update database: {e}")
        db.rollback()
    finally:
        db.close()

    return {
        "violation_count": interview["violation_count"],
        "terminated": terminated,
        "remaining_warnings": max(0, 10 - interview["violation_count"]),
        "message": "Functionality you are trying to access is disabled during the interview."
    }

@app.get("/violation/{interview_id}")
def get_violations(interview_id: int):
    """Get current violation count"""
    interview = INTERVIEWS.get(interview_id)

    if not interview:
        raise HTTPException(status_code=404, detail="Invalid interview ID")

    return {
        "violation_count": interview["violation_count"],
        "max_violations": 4,
        "remaining_warnings": max(0, 4 - interview["violation_count"])
    }

# Global fullscreen tracking
FULLSCREEN_EXIT_COUNTS = {}

@app.post("/fullscreen-exit")
def handle_fullscreen_exit(data: dict):
    """Track fullscreen exits during interview"""
    exit_count = data.get("exit_count", 0)
    
    print(f"⚠️ Fullscreen exit detected. Count: {exit_count}")
    
    # Terminate on 3rd exit
    if exit_count >= 3:
        print(f"❌ Interview terminated due to fullscreen violations")
        return {
            "terminated": True,
            "message": "Interview terminated due to multiple fullscreen exits",
            "exit_count": exit_count
        }
    
    return {
        "terminated": False,
        "remaining_warnings": 2 - exit_count,
        "exit_count": exit_count
    }

@app.get("/fullscreen-status")
def get_fullscreen_status():
    """Get current fullscreen violation status"""
    # Check session storage for termination
    return {
        "terminated": False
    }

@app.post("/terminate/{interview_id}")
def terminate_interview(interview_id: int):
    """Terminate an interview due to policy violations"""
    interview = INTERVIEWS.get(interview_id)

    if not interview:
        raise HTTPException(status_code=404, detail="Invalid interview ID")

    interview["is_terminated"] = True
    interview["status"] = "terminated"
    
    # Update database
    from database import SessionLocal
    from models import Interview
    from datetime import datetime
    
    db = SessionLocal()
    try:
        db_interview = db.query(Interview).filter(Interview.id == interview_id).first()
        if db_interview:
            db_interview.status = "terminated"
            db_interview.ended_at = datetime.utcnow()
            db_interview.candidate_rating = None  # NULL rating for terminated interviews
            db_interview.violations = interview.get("violation_count", 0)
            db.commit()
            print(f"✅ Interview {interview_id} terminated and database updated")
            print(f"   Status: terminated")
            print(f"   Ended at: {db_interview.ended_at}")
            print(f"   Rating: NULL")
            print(f"   Violations: {db_interview.violations}")
    except Exception as e:
        print(f"❌ Failed to update database on termination: {e}")
        db.rollback()
    finally:
        db.close()
    
    print(f"❌ Interview {interview_id} terminated")
    
    return {
        "message": "Interview terminated due to policy violations",
        "reason": "Multiple violations detected"
    }

@app.get("/status/{interview_id}")
def check_status(interview_id: int):
    """Check the current status of an interview"""
    interview = INTERVIEWS.get(interview_id)

    if not interview:
        raise HTTPException(status_code=404, detail="Invalid interview ID")

    return {
        "status": interview["status"],
        "is_terminated": interview.get("is_terminated", False),
        "completed": interview["status"] in ["completed", "terminated"],
        "question_count": interview["question_count"],
        "violation_count": interview["violation_count"]
    }


@app.get("/check-interview/{interview_id}")
def check_interview_exists(interview_id: int):
    """Check if an interview exists and its completion status"""
    interview = INTERVIEWS.get(interview_id)
    
    if not interview:
        return {
            "exists": False,
            "message": "Interview not found"
        }
    
    if interview["status"] in ["completed", "terminated"] or interview.get("is_terminated", False):
        return {
            "exists": True,
            "completed": True,
            "status": interview["status"],
            "message": "Your interview is already completed. Thank you!"
        }
    
    return {
        "exists": True, 
        "completed": False,
        "status": interview["status"],
        "question_count": interview["question_count"]
    }


@app.get("/interview-summary/{interview_id}")
def get_interview_summary(interview_id: int):
    """Get a summary of the interview (for admin/review purposes)"""
    interview = INTERVIEWS.get(interview_id)
    
    if not interview:
        raise HTTPException(status_code=404, detail="Invalid interview ID")
    
    return {
        "interview_id": interview_id,
        "candidate": interview["candidate_info"],
        "status": interview["status"],
        "questions_answered": len(interview["answers"]),
        "total_questions": interview["question_count"],
        "violations": interview["violation_count"],
        "terminated": interview.get("is_terminated", False),
        "difficulty_level": interview["difficulty"]
    }


@app.post("/fullscreen-status/{interview_id}")
def update_fullscreen_status(interview_id: int, is_fullscreen: bool):
    """Update fullscreen status for an interview"""
    interview = INTERVIEWS.get(interview_id)
    
    if not interview:
        raise HTTPException(status_code=404, detail="Invalid interview ID")
    
    interview["fullscreen_active"] = is_fullscreen
    
    if not is_fullscreen:
        print(f"⚠️ Fullscreen exited for interview {interview_id}")
    
    return {
        "fullscreen_active": is_fullscreen,
        "message": "Fullscreen status updated"
    }