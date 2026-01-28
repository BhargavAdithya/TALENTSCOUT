# backend/llm.py
import requests
import re
import os
from dotenv import load_dotenv
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = os.getenv("GROQ_API_URL", "https://api.groq.com/openai/v1/chat/completions")
MODEL_NAME = os.getenv("MODEL_NAME", "llama3-8b-8192")

# Headers for Groq API
HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {GROQ_API_KEY}"
}

def call_groq_api(prompt: str, timeout: int = 180) -> str:
    """
    Helper function to call Groq API with proper formatting
    """
    response = requests.post(
        GROQ_API_URL,
        headers=HEADERS,
        json={
            "model": MODEL_NAME,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.7,
            "max_tokens": 2000
        },
        timeout=timeout
    )
    
    if response.status_code != 200:
        raise RuntimeError(f"Groq API error: {response.status_code} - {response.text}")
    
    data = response.json()
    
    if "choices" not in data or len(data["choices"]) == 0:
        raise RuntimeError(f"Groq returned no response: {data}")
    
    return data["choices"][0]["message"]["content"].strip()

def ask_technical_question(tech_stack: str, difficulty: float, position: str = None, experience: float = None) -> str:
    """
    Generates ONE scenario-based technical interview question
    appropriate to the candidate's experience level, position, and tech stack.

    The question focuses on practical reasoning and understanding,
    NOT full system or architecture design.

    Args:
        tech_stack (str): Candidate's technology stack.
        difficulty (float): Candidate's difficulty level (1 to 5).
        position (str): Position the candidate is applying for.
        experience (float): Years of experience the candidate has.
    """

    # Build experience level description
    if experience is not None:
        if experience < 1:
            exp_level = "entry-level with less than 1 year of experience"
        elif experience <= 2:
            exp_level = "junior with 1-2 years of experience"
        elif experience <= 5:
            exp_level = "mid-level with 3-5 years of experience"
        elif experience <= 10:
            exp_level = "senior with 6-10 years of experience"
        else:
            exp_level = "very senior with 10+ years of experience"
    else:
        exp_level = "unknown experience level"

    # Build position context
    position_context = f"\nPosition applying for: {position}" if position else ""
    
    prompt = f"""
You are a technical interviewer conducting a live screening interview.

Candidate profile:
- Tech stack: {tech_stack}
- Experience level: {exp_level}{position_context}
- Interview difficulty (internal): {difficulty} out of 5

Question requirements:
- Ask ONLY ONE question relevant to their tech stack AND position
- The question MUST be scenario-based (realistic workplace situation)
- Tailor the complexity to match their experience level ({exp_level})
- The scenario should be small and focused (not a full system design)
- For junior roles: focus on fundamentals, basic problem-solving, and core concepts
- For mid-level roles: focus on practical application, best practices, and trade-offs
- For senior roles: focus on complex scenarios, architecture decisions, and optimization
- Ask what the candidate would do, explain, or expect to happen
- DO NOT ask full system design or architecture questions
- DO NOT use words like: design an entire system, architect, end-to-end solution
- The question should be answerable verbally in 2–5 minutes
- Make it relevant to the actual work they would do in the {position if position else 'role'}

Return ONLY the question text, nothing else.
"""

    raw = call_groq_api(prompt, timeout=180)

    # If the model adds an intro ending with a colon, strip it
    if ":" in raw.split("\n", 1)[0]:
        raw = raw.split(":", 1)[-1].strip()

    # Remove emojis and non-ASCII symbols
    raw = re.sub(r"[^\x00-\x7F]+", "", raw)

    # Remove wrapping quotes if any
    raw = raw.strip().strip('"')

    return raw

def ask_followup_question(tech_stack: str, difficulty: float, position: str, experience: float, 
                         previous_question: str, previous_answer: str, covered_topics: list) -> str:
    """
    Generates a follow-up technical question based on the candidate's previous answer.
    Maintains continuity while respecting tech stack, experience, and difficulty.

    Args:
        tech_stack (str): Candidate's technology stack.
        difficulty (float): Current difficulty level (1 to 5).
        position (str): Position the candidate is applying for.
        experience (float): Years of experience the candidate has.
        previous_question (str): The previous question asked.
        covered_topics (list): List of topics already covered.
        previous_answer (str): The candidate's answer to the previous question.
    """

    # Build experience level description
    if experience is not None:
        if experience < 1:
            exp_level = "entry-level with less than 1 year of experience"
        elif experience <= 2:
            exp_level = "junior with 1-2 years of experience"
        elif experience <= 5:
            exp_level = "mid-level with 3-5 years of experience"
        elif experience <= 10:
            exp_level = "senior with 6-10 years of experience"
        else:
            exp_level = "very senior with 10+ years of experience"
    else:
        exp_level = "unknown experience level"

    # Build position context
    position_context = f"\nPosition applying for: {position}" if position else ""
    
    prompt = f"""
You are a technical interviewer conducting a live screening interview.

Candidate profile:
- Tech stack: {tech_stack}
- Experience level: {exp_level}{position_context}
- Interview difficulty (internal): {difficulty} out of 5

Previous question asked:
{previous_question}

Candidate's answer:
{previous_answer}

Topics already covered in interview: {", ".join(covered_topics) if covered_topics else "None yet"}

Question requirements:
- Generate ONE follow-up question that builds upon or relates to their previous answer
- If they mentioned a specific technology, tool, or concept in their answer, you can ask about it
- If their answer was strong, ask a slightly deeper question on a related topic
- If their answer was weak or they skipped, move to a different but related area
- Maintain the same tech stack focus: {tech_stack}
- Keep the difficulty appropriate for {exp_level}
- The question MUST be scenario-based (realistic workplace situation)
- The scenario should be small and focused (not a full system design)
- For junior roles: focus on fundamentals, basic problem-solving, and core concepts
- For mid-level roles: focus on practical application, best practices, and trade-offs
- For senior roles: focus on complex scenarios, architecture decisions, and optimization
- Ask what the candidate would do, explain, or expect to happen
- DO NOT ask full system design or architecture questions
- The question should be answerable verbally in 2–5 minutes
- Make it relevant to the actual work they would do in the {position if position else 'role'}
- If continuing on the same topic, you may go deeper; otherwise feel free to connect to related areas within their tech stack
- Try to touch upon different aspects of their tech stack over the course of the interview
- Extract the main technology/topic from your question and append it at the end like this: [TOPIC: topic_name]

Return ONLY the question text, nothing else.
"""

    raw = call_groq_api(prompt, timeout=180)

    # If the model adds an intro ending with a colon, strip it
    if ":" in raw.split("\n", 1)[0]:
        raw = raw.split(":", 1)[-1].strip()

    # Remove emojis and non-ASCII symbols
    raw = re.sub(r"[^\x00-\x7F]+", "", raw)

    # Remove wrapping quotes if any
    raw = raw.strip().strip('"')

    # Extract topic if present
    topic_match = re.search(r'\[TOPIC:\s*([^\]]+)\]', raw)
    if topic_match:
        topic = topic_match.group(1).strip()
        if topic not in covered_topics:
            covered_topics.append(topic)
        # Remove the topic tag from the question
        raw = re.sub(r'\[TOPIC:\s*[^\]]+\]', '', raw).strip()

    return raw

def ask_new_topic_question(tech_stack: str, difficulty: float, position: str, experience: float,
                          covered_topics: list, question_history: list) -> str:
    """
    Generates a technical question from a NEW topic in the tech stack
    that hasn't been covered yet or is underrepresented.
    
    Args:
        tech_stack (str): Candidate's technology stack.
        difficulty (float): Current difficulty level (1 to 5).
        position (str): Position the candidate is applying for.
        experience (float): Years of experience the candidate has.
        covered_topics (list): List of topics already covered.
        question_history (list): List of all questions asked so far.
    """
    
    # Build experience level description
    if experience is not None:
        if experience < 1:
            exp_level = "entry-level with less than 1 year of experience"
        elif experience <= 2:
            exp_level = "junior with 1-2 years of experience"
        elif experience <= 5:
            exp_level = "mid-level with 3-5 years of experience"
        elif experience <= 10:
            exp_level = "senior with 6-10 years of experience"
        else:
            exp_level = "very senior with 10+ years of experience"
    else:
        exp_level = "unknown experience level"
    
    # Build covered topics context
    covered_str = ", ".join(covered_topics) if covered_topics else "None yet"
    
    position_context = f"\nPosition applying for: {position}" if position else ""
    
    prompt = f"""
You are a technical interviewer conducting a live screening interview.

Candidate profile:
- Tech stack: {tech_stack}
- Experience level: {exp_level}{position_context}
- Interview difficulty (internal): {difficulty} out of 5

Topics already covered: {covered_str}

Question requirements:
- Ask ONE question from a DIFFERENT topic/technology from their tech stack that hasn't been thoroughly explored yet
- Focus on technologies or concepts from their stack that are NOT in the covered topics list
- The question MUST be scenario-based (realistic workplace situation)
- Tailor the complexity to match their experience level ({exp_level})
- The scenario should be small and focused (not a full system design)
- For junior roles: focus on fundamentals, basic problem-solving, and core concepts
- For mid-level roles: focus on practical application, best practices, and trade-offs
- For senior roles: focus on complex scenarios, architecture decisions, and optimization
- Ask what the candidate would do, explain, or expect to happen
- DO NOT ask full system design or architecture questions
- The question should be answerable verbally in 2–5 minutes
- Make it relevant to the actual work they would do in the {position if position else 'role'}
- Extract the main technology/topic from your question and append it at the end like this: [TOPIC: topic_name]

Return ONLY the question text with the topic tag, nothing else.
"""
    
    raw = call_groq_api(prompt, timeout=180)
    
    # Extract topic if present
    topic_match = re.search(r'\[TOPIC:\s*([^\]]+)\]', raw)
    if topic_match:
        topic = topic_match.group(1).strip()
        covered_topics.append(topic)
        # Remove the topic tag from the question
        raw = re.sub(r'\[TOPIC:\s*[^\]]+\]', '', raw).strip()
    
    # If the model adds an intro ending with a colon, strip it
    if ":" in raw.split("\n", 1)[0]:
        raw = raw.split(":", 1)[-1].strip()
    
    # Remove emojis and non-ASCII symbols
    raw = re.sub(r"[^\x00-\x7F]+", "", raw)
    
    # Remove wrapping quotes if any
    raw = raw.strip().strip('"')
    
    return raw

def evaluate_answer(question: str, answer: str, difficulty: float, time_taken: int) -> dict:
    """
    Evaluates the candidate's answer and provides a score out of 10.
    
    Args:
        question (str): The question asked.
        answer (str): The candidate's answer.
        difficulty (float): Difficulty level of the question (1-5).
        time_taken (int): Time taken to answer in seconds.
    
    Returns:
        dict: Contains 'passed' (bool) and 'score' (float out of 10)
    """
    
    # Handle skipped or timeout answers
    if answer.lower().strip() in {"pass", "skip", "idk", "i don't know", "don't know", "no idea", "not sure", "n/a"}:
        return {"passed": False, "score": 0.0}
    
    if "[AUTO-SUBMITTED: TIME EXPIRED]" in answer:
        return {"passed": False, "score": 0.0}
    
    prompt = f"""
You are an expert technical interviewer evaluating a candidate's answer.

Interview Question (Difficulty: {difficulty}/5):
{question}

Candidate's Answer:
{answer}

Time taken to answer: {time_taken} seconds (out of 180 seconds limit)

Evaluation criteria:
1. Technical Accuracy (30%): Is the answer technically correct?
2. Depth of Understanding (25%): Does it show deep understanding or just surface knowledge?
3. Clarity and Communication (20%): Is the explanation clear and well-structured?
4. Practical Application (15%): Does the answer show practical experience?
5. Completeness (10%): Does it address all aspects of the question?

Time efficiency bonus:
- Answered in < 90 seconds: +0.5 points
- Answered in 90-150 seconds: No change
- Answered in > 150 seconds: -0.3 points

Respond with ONLY a JSON object in this exact format (no markdown, no extra text):
{{"score": X.X, "passed": true/false}}

Where:
- score: A decimal number between 0.0 and 10.0
- passed: true if score >= 5.0, false otherwise

Consider the difficulty level when scoring:
- For difficulty 1-2 (junior): Basic understanding is sufficient for passing
- For difficulty 3-4 (mid-level): Expect good practical knowledge
- For difficulty 5 (senior): Expect deep expertise and optimization thinking
"""

    raw = call_groq_api(prompt, timeout=180)
    
    # Clean up response - remove markdown code blocks if present
    raw = re.sub(r'```json\s*|\s*```', '', raw).strip()
    
    try:
        result = eval(raw)  # Using eval for simple dict parsing
        score = float(result.get("score", 0.0))
        passed = result.get("passed", False)
        
        # Ensure score is within bounds
        score = max(0.0, min(10.0, score))
        
        return {"passed": passed, "score": score}
    except Exception as e:
        print(f"⚠️ Error parsing evaluation result: {e}")
        print(f"Raw response: {raw}")
        # Fallback: basic keyword check
        if any(word in answer.lower() for word in ["correct", "yes", "good", "right"]):
            return {"passed": True, "score": 6.0}
        return {"passed": False, "score": 3.0}
    
def rate_candidate(candidate_info: dict, questions_data: list) -> float:
    """
    Rates the candidate out of 5 based on overall interview performance.
    
    Args:
        candidate_info (dict): Contains name, experience, position, tech_stack
        questions_data (list): List of dicts with question, answer, score, difficulty
    
    Returns:
        float: Rating out of 5.0
    """
    
    if not questions_data:
        return 0.0
    
    # Calculate statistics
    total_questions = len(questions_data)
    total_score = sum(q["score"] for q in questions_data)
    avg_score = total_score / total_questions if total_questions > 0 else 0
    passed_count = sum(1 for q in questions_data if q["score"] >= 5.0)
    avg_difficulty = sum(q["difficulty"] for q in questions_data) / total_questions
    
    # Build context for LLM
    questions_summary = "\n".join([
        f"Q{i+1} (Difficulty {q['difficulty']}/5): Score {q['score']}/10"
        for i, q in enumerate(questions_data)
    ])
    
    prompt = f"""
You are an expert technical hiring manager evaluating a candidate's overall interview performance.

Candidate Profile:
- Name: {candidate_info.get('name', 'Unknown')}
- Experience: {candidate_info.get('experience', 0)} years
- Position Applied: {candidate_info.get('position', 'Unknown')}
- Tech Stack: {candidate_info.get('tech_stack', 'Unknown')}

Interview Performance Summary:
- Total Questions: {total_questions}
- Questions Passed: {passed_count}/{total_questions}
- Average Score: {avg_score:.1f}/10
- Average Difficulty: {avg_difficulty:.1f}/5

Detailed Scores:
{questions_summary}

Rating criteria:
1. Consistency (25%): Did they perform consistently across questions?
2. Score Quality (30%): Average score relative to difficulty level
3. Pass Rate (20%): Percentage of questions passed
4. Experience Alignment (15%): Performance matches their experience level?
5. Technical Depth (10%): Showed deep understanding vs surface knowledge

Consider:
- For junior candidates (0-2 years): Passing 60%+ is good
- For mid-level (3-5 years): Passing 70%+ is expected
- For senior (6+ years): Passing 80%+ is expected
- Higher difficulty questions should be weighted more positively

Respond with ONLY a JSON object in this exact format (no markdown, no extra text):
{{"rating": X.X, "justification": "brief reason"}}

Where rating is a decimal between 0.0 and 5.0:
- 0.0-1.0: Poor performance, not recommended
- 1.5-2.5: Below average, needs improvement
- 3.0-3.5: Average, meets basic requirements
- 4.0-4.5: Good performance, recommended
- 4.5-5.0: Excellent performance, highly recommended
"""

    raw = call_groq_api(prompt, timeout=180)
    
    # Clean up response
    raw = re.sub(r'```json\s*|\s*```', '', raw).strip()
    
    try:
        result = eval(raw)
        rating = float(result.get("rating", 0.0))
        
        # Ensure rating is within bounds
        rating = max(0.0, min(5.0, rating))
        
        print(f"📊 Candidate Rating: {rating}/5.0")
        print(f"💬 Justification: {result.get('justification', 'N/A')}")
        
        return rating
    except Exception as e:
        print(f"⚠️ Error parsing rating result: {e}")
        print(f"Raw response: {raw}")
        # Fallback calculation
        fallback_rating = (avg_score / 10.0) * 5.0
        return round(min(5.0, max(0.0, fallback_rating)), 1)