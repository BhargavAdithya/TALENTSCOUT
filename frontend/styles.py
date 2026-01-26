# frontend/styles.py
"""
CSS styles for TalentScout Hiring Assistant
"""

STYLES = """
<style>
/* Global Styles */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

/* Force dark background everywhere - comprehensive */
html,
body,
.main,
.stApp,
[data-testid="stAppViewContainer"],
[data-testid="stHeader"],
[data-testid="stBottom"],
footer,
section,
.stChatFloatingInputContainer,
[data-testid="stChatFloatingInputContainer"] {
    background: linear-gradient(135deg, #111111 0%, #667eea 100%) !important;
    background-attachment: fixed !important;
}

/* Target the sticky bottom container */
.main > div:last-child,
.stBottom > div,
[class*="bottom"],
[class*="Bottom"],
[class*="floating"] {
    background: linear-gradient(135deg, #111111 0%, #667eea 100%) !important;
}

.main {
    font-family: 'Inter', sans-serif;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 900px;
}

/* Animated Background */
@keyframes gradient {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* Header Styles */
h1 {
    color: white !important;
    text-align: center;
    font-weight: 700 !important;
    font-size: 2.5rem !important;
    margin-bottom: 0.5rem !important;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    animation: fadeInDown 0.8s ease-out;
}

h2 {
    color: white !important;
    text-align: center;
    font-weight: 500 !important;
    font-size: 1.3rem !important;
    opacity: 0.95;
    margin-bottom: 2rem !important;
    animation: fadeInDown 0.8s ease-out 0.2s both;
}

h3 {
    color: white !important;
    text-align: center;
    font-weight: 600 !important;
    font-size: 1.5rem !important;
    margin-top: 2rem !important;
    margin-bottom: 1.5rem !important;
    animation: fadeInUp 0.6s ease-out;
}

/* Chat Message Styles */
.stChatMessage {
    background: white !important;
    border-radius: 16px !important;
    padding: 1.2rem !important;
    margin-bottom: 1rem !important;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1) !important;
    animation: slideIn 0.4s ease-out;
}

.stChatMessage,
.stChatMessage *,
.stChatMessage p,
.stChatMessage div,
.stChatMessage span {
    color: #1e293b !important;
}

/* Ensure user messages are also visible */
[data-testid="stChatMessageContent"],
[data-testid="stChatMessageContent"] *,
[data-testid="stChatMessageContent"] p,
[data-testid="stChatMessageContent"] div {
    color: #1e293b !important;
}

/* Assistant Message Box */
.assistant-box {
    background: linear-gradient(135deg, #f5f7fa 0%, #e8ecf1 100%);
    color: #1e293b;
    padding: 16px 20px;
    border-radius: 14px;
    margin-bottom: 12px;
    border-left: 4px solid #667eea;
    box-shadow: 0 2px 8px rgba(102, 126, 234, 0.15);
    animation: slideInLeft 0.5s ease-out;
    line-height: 1.6;
}

/* Question Box */
.question-box {
    background: linear-gradient(135deg, #eef2ff 0%, #e0e7ff 100%);
    color: #1e293b;
    padding: 18px 60px 18px 22px;
    border-radius: 14px;
    font-weight: 600;
    margin-top: 12px;
    border: 2px solid #818cf8;
    box-shadow: 0 4px 12px rgba(129, 140, 248, 0.25);
    position: relative;
}

/* Timer Styles - Integrated with question */
.timer-display {
    position: absolute;
    top: 10px;
    right: 10px;
    font-size: 1.1rem;
    font-weight: 700;
    display: inline-block;
    z-index: 10;
    background: rgba(255, 255, 255, 0.9);
    padding: 4px 8px;
    border-radius: 6px;
}

.timer-normal {
    color: #10b981;
    animation: fadeIn 0.5s ease-out;
}

.timer-warning {
    color: #f59e0b;
    animation: pulse-zoom 1.5s ease-in-out infinite;
}

.timer-critical {
    color: #ef4444;
    animation: pulse-zoom-fast 0.8s ease-in-out infinite;
}

@keyframes pulse-zoom {
    0%, 100% {
        transform: scale(1);
    }
    50% {
        transform: scale(1.15);
    }
}

@keyframes pulse-zoom-fast {
    0%, 100% {
        transform: scale(1);
    }
    50% {
        transform: scale(1.25);
    }
}

/* Rule Box */
.rule-box {
    background: linear-gradient(135deg, #fff7ed 0%, #ffedd5 100%);
    color: #7c2d12;
    padding: 16px 20px;
    border-left: 5px solid #f97316;
    border-radius: 12px;
    margin-top: 12px;
    box-shadow: 0 4px 10px rgba(249, 115, 22, 0.15);
    animation: fadeIn 0.8s ease-out;
    line-height: 1.7;
}

.rule-box b {
    color: #ea580c;
    font-size: 1.1em;
}

/* Chat Input */
.stChatInputContainer {
    background: transparent !important;
    border-radius: 16px;
    padding: 0.5rem;
    box-shadow: none !important;
}

.stChatInputContainer,
.stChatInputContainer > div,
.stChatInputContainer textarea,
[data-testid="stChatInput"],
[data-testid="stChatInput"] > div {
    max-width: 700px !important;
    width: 700px !important;
    margin-left: auto !important;
    margin-right: auto !important;
}

.stChatInputContainer textarea {
    max-height: 40px !important;
    min-height: 40px !important;
    background: rgba(255, 255, 255, 0.95) !important;
    border-radius: 12px !important;
    border: 2px solid rgba(255, 255, 255, 0.3) !important;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15) !important;
}

/* Spinner */
.stSpinner > div {
    border-top-color: #000000 !important;
}

.stSpinner > div > div {
color: #000000 !important;
font-weight: 600 !important;
}

/* Timer Styles */
.timer-box {
    background: linear-gradient(135deg, #dcfce7 0%, #bbf7d0 100%);
    color: #166534;
    padding: 12px 20px;
    border-radius: 12px;
    text-align: center;
    font-weight: 700;
    font-size: 1.2rem;
    margin: 15px 0;
    box-shadow: 0 4px 10px rgba(34, 197, 94, 0.2);
    animation: fadeIn 0.5s ease-out;
}

.timer-box.warning {
    background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
    color: #92400e;
    animation: pulse 1s ease-in-out infinite;
}

.timer-box.critical {
    background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
    color: #991b1b;
    animation: pulse-red 0.8s ease-in-out infinite;
}

/* Animations */
@keyframes fadeIn {
    from {
        opacity: 0;
    }
    to {
        opacity: 1;
    }
}

@keyframes fadeInDown {
    from {
        opacity: 0;
        transform: translateY(-20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes slideIn {
    from {
        opacity: 0;
        transform: translateX(-30px);
    }
    to {
        opacity: 1;
        transform: translateX(0);
    }
}

@keyframes slideInLeft {
    from {
        opacity: 0;
        transform: translateX(-20px);
    }
    to {
        opacity: 1;
        transform: translateX(0);
    }
}

@keyframes pulse {
    0%, 100% {
        transform: scale(1);
    }
    50% {
        transform: scale(1.02);
    }
}

@keyframes pulse-red {
    0% { transform: scale(1); }
    50% { transform: scale(1.05); }
    100% { transform: scale(1); }
}

/* Progress Indicator */
.progress-container {
    background: rgba(255, 255, 255, 0.2);
    border-radius: 10px;
    padding: 10px 20px;
    margin: 20px auto;
    text-align: center;
    backdrop-filter: blur(10px);
    animation: fadeIn 0.6s ease-out;
}

.progress-text {
    color: white;
    font-weight: 600;
    font-size: 0.9rem;
}

/* Emoji Enhancement */
.emoji {
    display: inline-block;
    animation: bounce 2s ease-in-out infinite;
}

@keyframes bounce {
    0%, 100% {
        transform: translateY(0);
    }
    50% {
        transform: translateY(-5px);
    }
}

/* Completion Modal Overlay */
.completion-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.85);
    backdrop-filter: blur(10px);
    z-index: 9999;
    display: flex;
    justify-content: center;
    align-items: center;
    animation: fadeIn 0.5s ease-out;
}

.completion-modal {
    background: linear-gradient(135deg, #ffffff 0%, #f0f9ff 100%);
    padding: 50px 60px;
    border-radius: 24px;
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.4);
    text-align: center;
    max-width: 600px;
    animation: slideInUp 0.6s ease-out;
    border: 3px solid #667eea;
}

.completion-modal h2 {
    color: #667eea !important;
    font-size: 2.5rem !important;
    margin-bottom: 1.5rem !important;
    font-weight: 700 !important;
}

.completion-modal p {
    color: #1e293b !important;
    font-size: 1.3rem !important;
    line-height: 1.8 !important;
    margin-bottom: 1rem !important;
}

.completion-icon {
    font-size: 4rem;
    margin-bottom: 1rem;
    animation: bounce 2s ease-in-out infinite;
}

@keyframes slideInUp {
    from {
        opacity: 0;
        transform: translateY(50px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}
</style>
"""