# frontend/pages/interview.py
import os
from dotenv import load_dotenv
load_dotenv()
import streamlit as st
import time
import re
import requests
from utils import EXIT_KEYWORDS
from styles import STYLES
import streamlit.components.v1 as components
import json
from datetime import datetime
    
# ============================================
# CHECK PERMISSIONS
# ============================================
if not st.session_state.get("permissions_granted", False):
    st.switch_page("app.py")
    st.stop()

# ============================================
# RE-ACQUIRE MEDIA STREAMS (lost during navigation)
# ============================================
if "media_streams_active" not in st.session_state:
    st.session_state.media_streams_active = False

# Always ensure streams are active on every rerun and stored in parent window
components.html(
    """
    <script>
    (async function() {
        // Store in parent window so streams persist across page navigations
        if (!window.parent.globalCameraStream || !window.parent.globalAudioStream) {
            console.log('🎥 Initializing global media streams...');
            
            try {
                // Request video stream
                const videoStream = await navigator.mediaDevices.getUserMedia({ 
                    video: { width: { ideal: 1280 }, height: { ideal: 720 } },
                    audio: false
                });
                
                // Request audio stream
                const audioStream = await navigator.mediaDevices.getUserMedia({ 
                    audio: true,
                    video: false
                });
                
                // Store in parent window (persists across navigations)
                window.parent.globalCameraStream = videoStream;
                window.parent.globalAudioStream = audioStream;
                
                console.log('✅ Global media streams initialized');
            } catch (error) {
                console.error('❌ Failed to acquire media streams:', error);
            }
        } else {
            console.log('✅ Global media streams already exist');
        }
    })();
    </script>
    """,
    height=0
)

if not st.session_state.media_streams_active:
    st.session_state.media_streams_active = True

# ============================================
# SET PAGE CONFIG (MUST BE FIRST)
# ============================================
st.set_page_config(
    page_title="TalentScout Hiring Assistant",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================
# INITIALIZE SESSION STATE
# ============================================
if "messages" not in st.session_state:
    st.session_state.messages = []

if "current_q" not in st.session_state:
    st.session_state.current_q = 0

if "answers" not in st.session_state:
    st.session_state.answers = {}

if "stage" not in st.session_state:
    st.session_state.stage = "info"

if "interview_id" not in st.session_state:
    st.session_state.interview_id = None

if "tech_q_count" not in st.session_state:
    st.session_state.tech_q_count = 0

if "current_tech_question" not in st.session_state:
    st.session_state.current_tech_question = None

if "collected_locations" not in st.session_state:
    st.session_state.collected_locations = []

if "timer_placeholder" not in st.session_state:
    st.session_state.timer_placeholder = None

if "input_locked" not in st.session_state:
    st.session_state.input_locked = False

if "pending_user_input" not in st.session_state:
    st.session_state.pending_user_input = None

if "timeout_detected" not in st.session_state:
    st.session_state.timeout_detected = False

if "email_verified" not in st.session_state:
    st.session_state.email_verified = False

if "otp_sent_email" not in st.session_state:
    st.session_state.otp_sent_email = False

if "waiting_for_otp_email" not in st.session_state:
    st.session_state.waiting_for_otp_email = False

if "violation_count" not in st.session_state:
    st.session_state.violation_count = 0

if "interview_completed_id" not in st.session_state:
    st.session_state.interview_completed_id = None

if "otp_email_boxes" not in st.session_state:
    st.session_state.otp_email_boxes = ["", "", "", "", "", ""]

if "otp_email_timestamp" not in st.session_state:
    st.session_state.otp_email_timestamp = None

if "temp_email" not in st.session_state:
    st.session_state.temp_email = None

if "otp_email_expired" not in st.session_state:
    st.session_state.otp_email_expired = False

if "email_duplicate_attempts" not in st.session_state:
    st.session_state.email_duplicate_attempts = 0

if "phone_duplicate_attempts" not in st.session_state:
    st.session_state.phone_duplicate_attempts = 0

if "show_duplicate_modal" not in st.session_state:
    st.session_state.show_duplicate_modal = False

if "duplicate_field" not in st.session_state:
    st.session_state.duplicate_field = None

if "terminated_duplicate" not in st.session_state:
    st.session_state.terminated_duplicate = False

# ============================================
# BACKEND CONFIGURATION
# ============================================
BACKEND_URL = os.getenv("BACKEND_URL", "https://talentscout-backend-c504.onrender.com")
QUESTION_TIME_LIMIT = 180

# ============================================
# CHECK IF INTERVIEW IS TERMINATED
# ============================================
if st.session_state.get("interview_id"):
    try:
        status_response = requests.get(
            f"{BACKEND_URL}/status/{st.session_state.interview_id}",
            timeout=5
        ).json()
        
        if status_response.get("is_terminated") or status_response.get("status") == "terminated":
            st.switch_page("pages/termination.py")
            st.stop()
    except Exception as e:
        pass

def get_remaining_time(interview_id):
    res = requests.get(f"{BACKEND_URL}/timer/{interview_id}", timeout=5)
    return res.json()["remaining"]

def backend_start_interview(candidate_data):
    try:
        response = requests.post(f"{BACKEND_URL}/start", json=candidate_data, timeout=180)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout:
        st.error("⏰ The server is taking longer than expected. Please try again.")
        st.stop()
    except requests.exceptions.RequestException as e:
        st.error(f"❌ Connection error: {str(e)}")
        st.stop()

def backend_submit_answer(interview_id, question, answer):
    try:
        response = requests.post(
            f"{BACKEND_URL}/answer",
            json={"interview_id": interview_id, "question": question, "answer": answer},
            timeout=180
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout:
        st.error("⏰ The server is taking longer than expected. Please try again.")
        st.stop()
    except requests.exceptions.RequestException as e:
        st.error(f"❌ Connection error: {str(e)}")
        st.stop()

# Apply CSS styles
st.markdown(STYLES, unsafe_allow_html=True)

# Hide sidebar toggle button and three-dot menu
st.markdown(
    """
    <style>
        /* Hide sidebar and all its controls */
        [data-testid="collapsedControl"] {
            display: none !important;
        }
        
        section[data-testid="stSidebar"] > div:first-child {
            display: none !important;
        }
        
        section[data-testid="stSidebar"] {
            display: none !important;
        }
        
        .css-1dp5vir {
            display: none !important;
        }
        
        button[kind="header"] {
            display: none !important;
        }
        
        /* Hide the three-dot menu (hamburger menu) */
        [data-testid="stHeader"] button[kind="header"] {
            display: none !important;
        }
        
        [data-testid="stHeader"] > div > div > button {
            display: none !important;
        }
        
        /* Hide all header buttons */
        header button {
            display: none !important;
        }
        
        /* Hide streamlit menu */
        #MainMenu {
            display: none !important;
        }
        
        /* Hide the entire header toolbar */
        [data-testid="stToolbar"] {
            display: none !important;
        }
        
        header[data-testid="stHeader"] {
            display: none !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# ============================================
# CHECK IF INTERVIEW IS ALREADY COMPLETED (MUST BE EARLY)
# ============================================
if st.session_state.get("interview_completed_id"):
    # Hide all Streamlit UI elements
    st.markdown(
        """
        <style>
            /* Hide ALL Streamlit elements */
            .main > div {
                padding: 0 !important;
            }
            
            .block-container {
                padding: 0 !important;
                max-width: 100% !important;
            }
            
            header, footer {
                display: none !important;
            }
            
            /* Make iframe fill entire screen */
            iframe {
                position: fixed !important;
                top: 0 !important;
                left: 0 !important;
                width: 100vw !important;
                height: 100vh !important;
                border: none !important;
                z-index: 999999 !important;
            }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    components.html(
        """
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                * {
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                }
                
                body {
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                    background: linear-gradient(135deg, #1f2937 0%, #111827 100%);
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    overflow: hidden;
                }
                
                .completion-card {
                    background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
                    padding: 60px 80px;
                    border-radius: 24px;
                    text-align: center;
                    max-width: 700px;
                    box-shadow: 0 20px 60px rgba(0,0,0,0.5);
                    border: 3px solid #dc2626;
                    animation: slideDown 0.6s ease-out;
                }
                
                @keyframes slideDown {
                    from {
                        opacity: 0;
                        transform: translateY(-50px);
                    }
                    to {
                        opacity: 1;
                        transform: translateY(0);
                    }
                }
                
                .icon {
                    font-size: 5rem;
                    margin-bottom: 20px;
                    animation: bounce 2s ease-in-out infinite;
                }
                
                @keyframes bounce {
                    0%, 100% {
                        transform: translateY(0);
                    }
                    50% {
                        transform: translateY(-10px);
                    }
                }
                
                h1 {
                    color: #dc2626;
                    font-size: 2.5rem;
                    margin-bottom: 20px;
                    font-weight: 700;
                    text-shadow: 0 2px 4px rgba(220, 38, 38, 0.1);
                }
                
                p {
                    font-size: 1.3rem;
                    color: #1e293b;
                    line-height: 1.8;
                    margin-bottom: 15px;
                }
                
                .message-box {
                    background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
                    color: #92400e;
                    padding: 20px;
                    border-radius: 12px;
                    margin-top: 25px;
                    border-left: 4px solid #f59e0b;
                    font-size: 1.1rem;
                    font-weight: 600;
                }
                
                .footer {
                    margin-top: 20px;
                    color: #64748b;
                    font-size: 1rem;
                }
            </style>
        </head>
        <body>
            <div class="completion-card">
                <div class="icon">🚫</div>
                <h1>Interview Already Completed</h1>
                <p>
                    You have already completed this interview.<br>
                    You cannot re-enter.
                </p>
                
                <div class="message-box">
                    ⚠️ Multiple attempts to access a completed interview are not allowed.
                </div>
                
                <p class="footer">
                    Thank you for participating!
                </p>
            </div>
        </body>
        </html>
        """,
        height=800
    )
    st.stop()

# Show live camera monitor throughout the interview
if st.session_state.get("permissions_granted"):
    # ALWAYS create camera HTML on every rerun (so it's visible)
    st.markdown(
        """
        <div id="cameraMonitor" style="
            position: fixed;
            top: 80px;
            right: 30px;
            width: 240px;
            height: 180px;
            background: #000;
            border: 4px solid #667eea;
            border-radius: 16px;
            z-index: 999999;
            overflow: hidden;
            box-shadow: 0 8px 32px rgba(0,0,0,0.4);
            cursor: move;
            user-select: none;
        ">
            <video id="camVideo" autoplay muted playsinline style="
                width: 100%;
                height: 100%;
                object-fit: cover;
                pointer-events: none;
            "></video>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # JavaScript to connect to existing stream (runs every rerun but doesn't re-request camera)
    components.html(
        """
        <script>
        (async function() {
            await new Promise(r => setTimeout(r, 10));
            
            const video = window.parent.document.getElementById('camVideo');
            const monitor = window.parent.document.getElementById('cameraMonitor');
            
            if (!video || !monitor) {
                console.error('Elements not found');
                return;
            }
            
            // ===== SETUP DRAGGABLE (safe to re-attach) =====
            if (!monitor.draggableAttached) {
                let isDragging = false;
                let currentX, currentY, initialX, initialY;
                let xOffset = 0, yOffset = 0;
                
                monitor.addEventListener('mousedown', function dragStart(e) {
                    initialX = e.clientX;
                    initialY = e.clientY;
                    const rect = monitor.getBoundingClientRect();
                    xOffset = rect.left;
                    yOffset = rect.top;
                    isDragging = true;
                    monitor.style.cursor = 'grabbing';
                });
                
                window.parent.document.addEventListener('mousemove', function drag(e) {
                    if (isDragging) {
                        e.preventDefault();
                        currentX = e.clientX - initialX;
                        currentY = e.clientY - initialY;
                        const newX = xOffset + currentX;
                        const newY = yOffset + currentY;
                        monitor.style.left = newX + 'px';
                        monitor.style.top = newY + 'px';
                        monitor.style.right = 'auto';
                    }
                });
                
                window.parent.document.addEventListener('mouseup', function dragEnd(e) {
                    isDragging = false;
                    monitor.style.cursor = 'move';
                    const rect = monitor.getBoundingClientRect();
                    xOffset = rect.left;
                    yOffset = rect.top;
                });
                
                monitor.draggableAttached = true;
            }
            
            // ===== RECONNECT TO EXISTING STREAM (NO FLICKER) =====
            if (window.parent.globalCameraStream) {
                // Stream already exists, just reconnect
                const tracks = window.parent.globalCameraStream.getVideoTracks();
                if (tracks.length > 0 && tracks[0].readyState === 'live') {
                    video.srcObject = window.parent.globalCameraStream;
                    if (video.paused) {
                        video.play().catch(e => console.log('Play retry:', e));
                    }
                    console.log('✅ Reconnected to existing stream');
                    return;
                }
            }
            
            // ===== INITIALIZE CAMERA (ONLY FIRST TIME) =====
            if (!window.parent.cameraStreamInitialized) {
                console.log('🎥 Initializing camera for first time');
                window.parent.cameraStreamInitialized = true;
                
                try {
                    const stream = await navigator.mediaDevices.getUserMedia({
                        video: { 
                            facingMode: "user",
                            width: { ideal: 1280 },
                            height: { ideal: 720 }
                        },
                        audio: true
                    });
                    
                    video.srcObject = stream;
                    window.parent.globalCameraStream = stream;
                    console.log('✅ Camera stream created');
                } catch (error) {
                    console.error('❌ Camera error:', error);
                    monitor.innerHTML = '<div style="color:white;padding:20px;text-align:center;font-size:14px;">Camera Error</div>';
                }
            }
        })();
        </script>
        """,
        height=0
    )

# ============================================
# COMPREHENSIVE INTERVIEW PROTECTION
# ============================================
if st.session_state.get("permissions_granted"):
    # Add CSS protection via Streamlit markdown
    st.markdown(
        """
        <style>
        /* DISABLE TEXT SELECTION GLOBALLY */
        * {
            -webkit-user-select: none !important;
            -moz-user-select: none !important;
            -ms-user-select: none !important;
            user-select: none !important;
            -webkit-touch-callout: none !important;
        }
        
        /* Allow selection ONLY in input fields */
        input, textarea, [contenteditable="true"] {
            -webkit-user-select: text !important;
            -moz-user-select: text !important;
            -ms-user-select: text !important;
            user-select: text !important;
        }
        
        /* Disable pointer cursor on text */
        p, span, div, h1, h2, h3, h4, h5, h6, label, b, strong, i, em {
            cursor: default !important;
        }
        
        /* Keep pointer on interactive elements */
        button, a, input, textarea, select {
            cursor: pointer !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    # Determine if we should track violations
    track_violations = st.session_state.get('interview_id') is not None
    interview_id_value = st.session_state.get('interview_id', 'null')
    
    components.html(
        f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                @keyframes slideUp {{
                    from {{ transform: translate(-50%, 100px); opacity: 0; }}
                    to {{ transform: translate(-50%, 0); opacity: 1; }}
                }}
                
                @keyframes slideDown {{
                    from {{ transform: translate(-50%, 0); opacity: 1; }}
                    to {{ transform: translate(-50%, 100px); opacity: 0; }}
                }}
                
                .warning-close-btn {{
                    position: absolute;
                    top: -15px;
                    right: -15px;
                    width: 36px;
                    height: 36px;
                    background: #dc2626;
                    color: white;
                    border-radius: 50%;
                    border: 3px solid white;
                    cursor: pointer;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 20px;
                    font-weight: bold;
                    box-shadow: 0 4px 12px rgba(0,0,0,0.4);
                    transition: all 0.2s;
                    z-index: 999999;
                    line-height: 1;
                    user-select: none;
                    -webkit-user-select: none;
                    pointer-events: auto !important;
                }}
                
                .warning-close-btn:hover {{
                    background: #b91c1c;
                    transform: scale(1.15);
                    box-shadow: 0 6px 16px rgba(0,0,0,0.5);
                }}
                
                .warning-close-btn:active {{
                    transform: scale(1.05);
                }}
            </style>
        </head>
        <body>
            <script>
            (function() {{
                const INTERVIEW_ID = {interview_id_value};
                const TRACK_VIOLATIONS = {str(track_violations).lower()};
                
                // Access parent document
                const doc = window.parent.document;
                const win = window.parent;
                
                // CRITICAL: Check if on termination page - exit immediately
                if (win.onTerminationPage === true) {{
                    console.log('🚫 On termination page, protection completely disabled');

                    // Remove any existing warnings
                    const overlay = doc.getElementById('violation-warning-overlay');
                    if (overlay) overlay.remove();

                    return; // Exit completely
                }}
                
                console.log('🔒 Initializing protection...');
                
                // =====================================
                // HELPER: Check if element should be protected
                // =====================================
                function shouldProtect(element) {{
                    if (!element) return true;
                    
                    // Don't protect camera monitor elements
                    if (element.id === 'cameraMonitor' || element.id === 'camVideo') {{
                        return false;
                    }}
                    
                    // Don't protect close button
                    if (element.className && element.className.includes('warning-close-btn')) {{
                        return false;
                    }}
                    
                    // Don't protect warning overlay itself
                    if (element.id === 'violation-warning-overlay') {{
                        return false;
                    }}
                    
                    // Check if element is inside camera monitor or warning
                    let parent = element.parentElement;
                    while (parent) {{
                        if (parent.id === 'cameraMonitor' || 
                            parent.id === 'violation-warning-overlay' ||
                            (parent.className && parent.className.includes('warning-close-btn'))) {{
                            return false;
                        }}
                        parent = parent.parentElement;
                    }}
                    
                    // Don't protect input fields
                    const tag = element.tagName;
                    if (tag === 'INPUT' || tag === 'TEXTAREA') {{
                        return false;
                    }}
                    
                    return true;
                }}
                
                // =====================================
                // PROTECTION FUNCTIONS
                // =====================================
                
                // Block text selection
                function blockSelection(e) {{
                    if (!shouldProtect(e.target)) return;
                    
                    e.preventDefault();
                    e.stopPropagation();
                    e.stopImmediatePropagation();
                    
                    if (TRACK_VIOLATIONS) {{
                        recordViolation('text_selection');
                    }} else {{
                        showInfoWarning('Text selection is disabled during the interview');
                    }}
                    return false;
                }}
                
                // Block clipboard
                function blockClipboard(e) {{
                    if (!shouldProtect(e.target)) return;
                    
                    e.preventDefault();
                    e.stopPropagation();
                    e.stopImmediatePropagation();
                    
                    if (TRACK_VIOLATIONS) {{
                        recordViolation('clipboard_' + e.type);
                    }} else {{
                        showInfoWarning('Copy/Paste is disabled during the interview');
                    }}
                    return false;
                }}
                
                // Block context menu
                function blockContextMenu(e) {{
                    if (!shouldProtect(e.target)) return;
                    
                    e.preventDefault();
                    e.stopPropagation();
                    
                    if (TRACK_VIOLATIONS) {{
                        recordViolation('right_click');
                    }} else {{
                        showInfoWarning('Right-click is disabled during the interview');
                    }}
                    return false;
                }}
                
                // Block keyboard
                function blockKeyboard(e) {{
                    const key = e.key;
                    const ctrl = e.ctrlKey || e.metaKey;
                    const shift = e.shiftKey;
                    const alt = e.altKey;
                    const tag = e.target.tagName;
                    const isInput = tag === 'INPUT' || tag === 'TEXTAREA';
                    
                    let blocked = false;
                    let type = '';
                    
                    // Windows/Meta key
                    if (key === 'Meta' || key === 'OS') {{
                        blocked = true;
                        type = 'windows_key';
                    }}
                    // Function keys
                    else if (/^F\d+$/.test(key)) {{
                        blocked = true;
                        type = 'function_key';
                    }}
                    // Alt combos
                    else if (alt && key !== 'Alt') {{
                        blocked = true;
                        type = 'alt_combo';
                    }}
                    // Tab outside inputs
                    else if (key === 'Tab' && !isInput) {{
                        blocked = true;
                        type = 'tab_key';
                    }}
                    // Clipboard shortcuts
                    else if (ctrl && ['c', 'v', 'x'].includes(key.toLowerCase())) {{
                        blocked = true;
                        type = 'ctrl_' + key.toLowerCase();
                    }}
                    // Select all outside inputs
                    else if (ctrl && key.toLowerCase() === 'a' && !isInput) {{
                        blocked = true;
                        type = 'ctrl_a';
                    }}
                    // DevTools
                    else if (ctrl && ['i', 'j', 'u'].includes(key.toLowerCase())) {{
                        blocked = true;
                        type = 'devtools';
                    }}
                    // Ctrl+Shift
                    else if (ctrl && shift) {{
                        blocked = true;
                        type = 'ctrl_shift';
                    }}
                    // Escape
                    else if (key === 'Escape') {{
                        blocked = true;
                        type = 'escape';
                    }}
                    // PrintScreen
                    else if (key === 'PrintScreen') {{
                        blocked = true;
                        type = 'printscreen';
                    }}
                    
                    if (blocked) {{
                        e.preventDefault();
                        e.stopPropagation();
                        e.stopImmediatePropagation();
                        
                        if (TRACK_VIOLATIONS) {{
                            recordViolation(type);
                        }} else {{
                            showInfoWarning('Functionality you are trying to access is disabled');
                        }}
                        return false;
                    }}
                }}
                
                // =====================================
                // ATTACH LISTENERS (with removal first)
                // =====================================
                
                // Check if already attached
                if (win.interviewProtectionAttached) {{
                    console.log('⚠️ Protection already attached');
                    return;
                }}
                
                // Selection
                doc.addEventListener('selectstart', blockSelection, true);
                doc.addEventListener('mousedown', blockSelection, true);
                
                // Clipboard
                doc.addEventListener('copy', blockClipboard, true);
                doc.addEventListener('cut', blockClipboard, true);
                doc.addEventListener('paste', blockClipboard, true);
                
                // Context menu
                doc.addEventListener('contextmenu', blockContextMenu, true);
                
                // Drag
                doc.addEventListener('dragstart', function(e) {{ 
                    if (shouldProtect(e.target)) {{
                        e.preventDefault(); 
                        return false; 
                    }}
                }}, true);
                
                // Keyboard
                doc.addEventListener('keydown', blockKeyboard, true);
                win.addEventListener('keydown', blockKeyboard, true);
                
                // Mark as attached
                win.interviewProtectionAttached = true;
                
                console.log('✅ Protection active');
                
                // =====================================
                // VIOLATION HANDLING
                // =====================================
                
                async function recordViolation(type) {{
                    if (!INTERVIEW_ID) {{
                        showInfoWarning('Functionality you are trying to access is disabled');
                        return;
                    }}
                    
                    try {{
                        const response = await fetch(`https://talentscout-backend-c504.onrender.com/violation/${{INTERVIEW_ID}}`, {{
                            method: 'POST',
                            headers: {{'Content-Type': 'application/json'}},
                            body: JSON.stringify({{type: type}})
                        }});
                        
                        const data = await response.json();
                        showWarning(data.message, data.violation_count, data.terminated);
                        
                        if (data.terminated) {{
                            setTimeout(() => win.location.reload(), 2000);
                        }}
                    }} catch (error) {{
                        showInfoWarning('Functionality you are trying to access is disabled');
                    }}
                }}
                
                // Close warning manually
                function closeWarning(e) {{
                    if (e) {{
                        e.preventDefault();
                        e.stopPropagation();
                    }}
                    
                    const overlay = doc.getElementById('violation-warning-overlay');
                    if (overlay) {{
                        overlay.style.animation = 'slideDown 0.3s ease-out';
                        setTimeout(() => {{
                            if (overlay.parentNode) {{
                                overlay.remove();
                            }}
                        }}, 300);
                    }}
                }}
                
                function showInfoWarning(message) {{
                    // Don't show warnings on termination page
                    if (win.onTerminationPage === true) {{
                        console.log('⚠️ Warning blocked - on termination page');
                        return;
                    }}

                    let overlay = doc.getElementById('violation-warning-overlay');
                    if (overlay) overlay.remove();
                    
                    overlay = doc.createElement('div');
                    overlay.id = 'violation-warning-overlay';
                    overlay.style.cssText = `
                        position: fixed;
                        bottom: 20px;
                        left: 50%;
                        transform: translateX(-50%);
                        background: #fef3c7;
                        color: #92400e;
                        padding: 16px 32px 16px 32px;
                        border-radius: 12px;
                        border: 2px solid #f59e0b;
                        box-shadow: 0 8px 24px rgba(0,0,0,0.3);
                        z-index: 999998;
                        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                        font-weight: 600;
                        font-size: 1.1rem;
                        animation: slideUp 0.3s ease-out;
                        max-width: 600px;
                        text-align: center;
                        pointer-events: auto;
                    `;
                    
                    overlay.innerHTML = `⚠️ ${{message}}`;
                    
                    // Create close button separately
                    const closeBtn = doc.createElement('button');
                    closeBtn.className = 'warning-close-btn';
                    closeBtn.innerHTML = '×';
                    closeBtn.style.cssText = `
                        position: absolute;
                        top: -15px;
                        right: -15px;
                        width: 36px;
                        height: 36px;
                        background: #dc2626;
                        color: white;
                        border-radius: 50%;
                        border: 3px solid white;
                        cursor: pointer;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        font-size: 22px;
                        font-weight: bold;
                        box-shadow: 0 4px 12px rgba(0,0,0,0.4);
                        transition: all 0.2s;
                        z-index: 999999;
                        line-height: 1;
                        padding: 0;
                        user-select: none;
                        -webkit-user-select: none;
                        pointer-events: auto;
                    `;
                    
                    closeBtn.onmouseover = function() {{
                        this.style.background = '#b91c1c';
                        this.style.transform = 'scale(1.15)';
                    }};
                    
                    closeBtn.onmouseout = function() {{
                        this.style.background = '#dc2626';
                        this.style.transform = 'scale(1)';
                    }};
                    
                    closeBtn.onclick = function(e) {{
                        e.preventDefault();
                        e.stopPropagation();
                        closeWarning();
                    }};
                    
                    overlay.appendChild(closeBtn);
                    doc.body.appendChild(overlay);
                    
                    // Auto-close after 5 seconds
                    setTimeout(() => {{
                        if (overlay && overlay.parentNode) {{
                            closeWarning();
                        }}
                    }}, 5000);
                }}
                
                function showWarning(message, count, terminated) {{
                    // Don't show warnings on termination page
                    if (win.onTerminationPage === true) {{
                        console.log('⚠️ Warning blocked - on termination page');
                        return;
                    }}

                    let overlay = doc.getElementById('violation-warning-overlay');
                    if (overlay) overlay.remove();
                    
                    overlay = doc.createElement('div');
                    overlay.id = 'violation-warning-overlay';
                    overlay.style.cssText = `
                        position: fixed;
                        bottom: 20px;
                        left: 50%;
                        transform: translateX(-50%);
                        background: ${{terminated ? '#fee2e2' : '#fef3c7'}};
                        color: ${{terminated ? '#991b1b' : '#92400e'}};
                        padding: 16px 32px 16px 32px;
                        border-radius: 12px;
                        border: 2px solid ${{terminated ? '#dc2626' : '#f59e0b'}};
                        box-shadow: 0 8px 24px rgba(0,0,0,0.3);
                        z-index: 999998;
                        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                        font-weight: 600;
                        font-size: 1.1rem;
                        animation: slideUp 0.3s ease-out;
                        max-width: 600px;
                        text-align: center;
                        pointer-events: auto;
                    `;
                    
                    overlay.innerHTML = `
                        <div style="margin-bottom: 8px;">⚠️ ${{message}}</div>
                        <div style="font-size: 0.9rem; opacity: 0.9;">
                            Violations: ${{count}}/10 | Remaining: ${{Math.max(0, 10 - count)}}
                            ${{count >= 9 ? '<br><strong>Next violation terminates interview!</strong>' : ''}}
                        </div>
                    `;
                    
                    // Create close button separately
                    const closeBtn = doc.createElement('button');
                    closeBtn.className = 'warning-close-btn';
                    closeBtn.innerHTML = '×';
                    closeBtn.style.cssText = `
                        position: absolute;
                        top: -15px;
                        right: -15px;
                        width: 36px;
                        height: 36px;
                        background: #dc2626;
                        color: white;
                        border-radius: 50%;
                        border: 3px solid white;
                        cursor: pointer;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        font-size: 22px;
                        font-weight: bold;
                        box-shadow: 0 4px 12px rgba(0,0,0,0.4);
                        transition: all 0.2s;
                        z-index: 999999;
                        line-height: 1;
                        padding: 0;
                        user-select: none;
                        -webkit-user-select: none;
                        pointer-events: auto;
                    `;
                    
                    closeBtn.onmouseover = function() {{
                        this.style.background = '#b91c1c';
                        this.style.transform = 'scale(1.15)';
                    }};
                    
                    closeBtn.onmouseout = function() {{
                        this.style.background = '#dc2626';
                        this.style.transform = 'scale(1)';
                    }};
                    
                    closeBtn.onclick = function(e) {{
                        e.preventDefault();
                        e.stopPropagation();
                        closeWarning();
                    }};
                    
                    overlay.appendChild(closeBtn);
                    doc.body.appendChild(overlay);
                    
                    // Don't auto-close if terminated
                    if (!terminated) {{
                        setTimeout(() => {{
                            if (overlay && overlay.parentNode) {{
                                closeWarning();
                            }}
                        }}, 5000);
                    }}
                }}
                
                // =====================================
                // ATTACH LISTENERS
                // =====================================
                
                if (win.interviewProtectionAttached) {{
                    console.log('⚠️ Protection already attached');
                    return;
                }}
                
                // Selection
                doc.addEventListener('selectstart', blockSelection, true);
                doc.addEventListener('mousedown', blockSelection, true);
                
                // Clipboard
                doc.addEventListener('copy', blockClipboard, true);
                doc.addEventListener('cut', blockClipboard, true);
                doc.addEventListener('paste', blockClipboard, true);
                
                // Context menu
                doc.addEventListener('contextmenu', blockContextMenu, true);
                
                // Drag
                doc.addEventListener('dragstart', function(e) {{ 
                    if (shouldProtect(e.target)) {{
                        e.preventDefault(); 
                        return false; 
                    }}
                }}, true);
                
                // Keyboard
                doc.addEventListener('keydown', blockKeyboard, true);
                win.addEventListener('keydown', blockKeyboard, true);
                
                // Mark as attached
                win.interviewProtectionAttached = true;
                
                console.log('✅ Protection active');
            }})();
            </script>
        </body>
        </html>
        """,
        height=0
    )

# Check if terminated due to duplicate attempts
if st.session_state.terminated_duplicate:
    st.switch_page("pages/termination.py")
    st.stop()

QUESTIONS = [
    "Please enter your <b>full name</b> exactly as it appears on your official ID.",
    "Please provide your <b>personal email address</b>.",
    "Please enter your <b>phone number</b>.",
    "How many year(s) of experience do you have? (Enter a number, e.g., 1, 3.5, 5)",
    "Which position are you applying for?",
    "What are your preferred job locations? (Enter at least 3, separated by commas)",
    "Please list your tech stack (languages, frameworks, databases, tools)."
]

st.markdown("<h1><span class='emoji'>🚀</span> TalentScout Hiring Assistant</h1>", unsafe_allow_html=True)

# Scroll to bottom for new messages
components.html(
    """
    <script>
    setTimeout(() => {
        window.parent.scrollTo({
            top: window.parent.document.body.scrollHeight,
            behavior: 'smooth'
        });
    }, 100);
    </script>
    """,
    height=0
)

# Progress Indicator
if st.session_state.stage == "info":
    progress = (st.session_state.current_q / len(QUESTIONS)) * 100
    st.markdown(
        f"""
        <div class='progress-container'>
            <div class='progress-text'>📋 Candidate Information: Question {min(st.session_state.current_q + 1, len(QUESTIONS))} of {len(QUESTIONS)}</div>
        </div>
        """,
        unsafe_allow_html=True
    )
elif st.session_state.stage == "tech":
    st.markdown(
        f"""
        <div class='progress-container'>
            <div class='progress-text'>🧪 Technical Interview: Question {min(st.session_state.tech_q_count + 1, 5)} of 5</div>
        </div>
        """,
        unsafe_allow_html=True
    )

# Display chat messages
for i, msg in enumerate(st.session_state.messages):
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"], unsafe_allow_html=True)

# EMAIL OTP Display
if (st.session_state.waiting_for_otp_email and 
    st.session_state.otp_sent_email and 
    not st.session_state.email_verified and
    st.session_state.pending_user_input is None):
    
    if st.session_state.otp_email_timestamp:
        elapsed = (datetime.now() - st.session_state.otp_email_timestamp).total_seconds()
        remaining_time = max(0, 120 - int(elapsed))
        
        if remaining_time == 0 and not st.session_state.otp_email_expired:
            st.session_state.otp_email_expired = True
            st.session_state.waiting_for_otp_email = False
            st.session_state.otp_sent_email = False
            st.session_state.otp_email_timestamp = None
            st.session_state.temp_email = None
            msg = "⏰ <b>OTP Expired!</b><br><br>The time for entering the OTP has expired. Please re-enter your email address to send a new verification code. 📧"
            st.session_state.messages.append({"role": "assistant", "content": msg})
            st.rerun()
    else:
        remaining_time = 120
    
    if st.session_state.otp_email_expired:
        st.stop()
    
    if remaining_time > 0:
        temp_email_display = st.session_state.temp_email if st.session_state.temp_email else ""
        components.html(
            f"""
            <!DOCTYPE html>
            <html>
            <head>
                <style>
                    * {{
                        margin: 0;
                        padding: 0;
                        box-sizing: border-box;
                    }}
                    
                    body {{
                        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                        padding: 20px;
                    }}
                    
                    .otp-container {{
                        background: white;
                        padding: 30px;
                        border-radius: 16px;
                        max-width: 500px;
                        margin: 0 auto;
                        box-shadow: 0 8px 24px rgba(0,0,0,0.15);
                    }}
                    
                    h3 {{
                        color: #667eea;
                        text-align: center;
                        margin-bottom: 20px;
                        font-size: 1.5rem;
                    }}
                    
                    .email-text {{
                        text-align: center;
                        color: #64748b;
                        margin-bottom: 10px;
                        font-size: 0.95rem;
                    }}
                    
                    .email-text strong {{
                        color: #334155;
                    }}
                    
                    #timer-display {{
                        text-align: center;
                        margin-bottom: 20px;
                    }}
                    
                    #timer-text {{
                        font-size: 1.5rem;
                        font-weight: bold;
                        color: #667eea;
                    }}
                    
                    .instruction-text {{
                        text-align: center;
                        color: #9333ea;
                        font-size: 0.95rem;
                        margin-bottom: 15px;
                        font-weight: 600;
                    }}
                </style>
            </head>
            <body>
                <div class="otp-container">
                    <h3>📧 Email Verification</h3>
                    <p class="email-text">
                        Enter the 6-digit OTP sent to <strong>{temp_email_display}</strong>
                    </p>
                    <div id="timer-display">
                        <span id="timer-text">⏱️ {remaining_time // 60}:{remaining_time % 60:02d}</span>
                    </div>
                    <p class="instruction-text">
                        👇 Enter OTP below in the chat input box to verify
                    </p>
                </div>
                
                <script>
                let startTime = {remaining_time};
                let timerInterval;
                let expired = false;
                
                function updateTimer() {{
                    if (expired) return;
                    startTime--;
                    const minutes = Math.floor(startTime / 60);
                    const seconds = startTime % 60;
                    const timerText = document.getElementById('timer-text');
                    
                    if (startTime < 30) {{
                        timerText.style.color = '#dc2626';
                    }}
                    
                    timerText.textContent = `⏱️ ${{minutes}}:${{seconds.toString().padStart(2, '0')}}`;
                    
                    if (startTime <= 0) {{
                        clearInterval(timerInterval);
                        expired = true;
                        window.parent.postMessage({{type: 'otp_expired'}}, '*');
                    }}
                }}
                
                timerInterval = setInterval(updateTimer, 1000);
                </script>
            </body>
            </html>
            """,
            height=250
        )
        st.markdown("⬇️ **Please enter the 6-digit OTP in the chat input box below to verify your email.**", unsafe_allow_html=True)

# Display timer for technical questions
if (st.session_state.stage == "tech" and 
    st.session_state.interview_id and 
    st.session_state.current_tech_question and
    st.session_state.messages and
    not st.session_state.input_locked):
    
    last_msg = st.session_state.messages[-1]
    if last_msg["role"] == "assistant" and "question-box" in last_msg["content"]:
        if st.session_state.timer_placeholder is None:
            st.session_state.timer_placeholder = st.empty()
        
        try:
            timer_response = requests.get(f"{BACKEND_URL}/timer/{st.session_state.interview_id}", timeout=5).json()
            remaining = timer_response.get("remaining", 0)
            timeout = timer_response.get("timeout", False)
            
            if timeout:
                st.session_state.timer_placeholder = None
                st.session_state.input_locked = True
                st.session_state.timeout_detected = True
                st.rerun()
            
            if remaining > 0:
                minutes = remaining // 60
                seconds = remaining % 60
                
                if remaining > 60:
                    timer_class = "timer-normal"
                elif remaining > 30:
                    timer_class = "timer-warning"
                else:
                    timer_class = "timer-critical"
                
                with st.session_state.timer_placeholder.container():
                    st.markdown(
                        f"""
                        <div style="position: relative; margin-top: -50px; text-align: right; padding-right: 40px;">
                            <span class="timer-display {timer_class}">⏱️ {minutes:02d}:{seconds:02d}</span>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
        except Exception as e:
            pass

# Initial greeting
if st.session_state.current_q == 0 and not st.session_state.messages:
    greeting = (
        "Hello! I'm TalentScout's AI Hiring Assistant.\n\n"
        "I'll ask you a few questions to understand your profile, "
        "followed by a technical interview.\n\n"
        f"<b>{QUESTIONS[0]}</b>"
    )
    st.session_state.messages.append({"role": "assistant", "content": greeting})
    with st.chat_message("assistant"):
        st.markdown(f"<div class='assistant-box'>{greeting}</div>", unsafe_allow_html=True)

# Chat input handling
if st.session_state.stage == "completed":
    # Show completion message with countdown
    if "completion_message_shown_at" not in st.session_state:
        st.session_state.completion_message_shown_at = time.time()
        st.session_state.countdown_placeholder = st.empty()
    
    elapsed = time.time() - st.session_state.completion_message_shown_at
    remaining = max(0, int(5 - elapsed))
    
    if remaining <= 0:
        # Countdown finished, now redirect
        st.session_state.interview_completed_id = st.session_state.interview_id
        st.switch_page("pages/completion.py")
        st.stop()
    else:
        # Show continuous countdown using HTML
        with st.session_state.countdown_placeholder:
            st.markdown(
                f"""
                <div style="
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    padding: 20px;
                    background: rgba(255, 255, 255, 0.15);
                    border-radius: 12px;
                    margin: 20px auto;
                    max-width: 400px;
                    backdrop-filter: blur(10px);
                ">
                    <div class="stSpinner" style="
                        width: 24px;
                        height: 24px;
                        border: 3px solid rgba(255, 255, 255, 0.3);
                        border-top-color: white;
                        border-radius: 50%;
                        animation: spin 1s linear infinite;
                        margin-right: 15px;
                    "></div>
                    <span style="
                        color: white;
                        font-size: 1.2rem;
                        font-weight: 600;
                    ">
                        ⏳ Redirecting in {remaining} second{'s' if remaining != 1 else ''}...
                    </span>
                </div>
                <style>
                    @keyframes spin {{
                        0% {{ transform: rotate(0deg); }}
                        100% {{ transform: rotate(360deg); }}
                    }}
                </style>
                """,
                unsafe_allow_html=True
            )
        
        time.sleep(1)
        st.rerun()

elif not st.session_state.get("input_locked", False):
    user_input = st.chat_input("Type your response here...")
else:
    st.chat_input("Processing... Please wait", disabled=True, key="disabled_input")
    user_input = None

# Auto-refresh timer
if (st.session_state.stage == "tech" and 
    st.session_state.interview_id and 
    st.session_state.current_tech_question and
    not user_input and
    not st.session_state.input_locked and
    not st.session_state.get("timeout_detected", False) and
    st.session_state.stage != "completed"):
    time.sleep(1)
    st.rerun()

# HANDLE TIMEOUT
if st.session_state.get("timeout_detected", False):
    st.session_state.timeout_detected = False
    
    st.session_state.tech_q_count += 1
    
    # Check if this was the last question
    if st.session_state.tech_q_count >= 5:
        with st.spinner("⏳ Processing your response..."):
            # Submit timeout to backend
            backend_submit_answer(
                st.session_state.interview_id,
                st.session_state.current_tech_question,
                "[AUTO-SUBMITTED: TIME EXPIRED]"
            )
            
            # Wait for backend to process
            time.sleep(3)
            
            # Check completion status
            while True:
                time.sleep(1)
                res = requests.get(
                    f"{BACKEND_URL}/next-question/{st.session_state.interview_id}",
                    timeout=120
                ).json()
                
                if res.get("completed"):
                    break
        
        end_msg = (
            "<div class='assistant-box'>"
            "Thank you. This concludes the technical interview. ✅<br><br>"
            "Our team will review your responses and get back to you. 📧"
            "</div>"
        )
        st.session_state.messages.append({"role": "assistant", "content": end_msg})
        st.session_state.input_locked = False
        st.session_state.stage = "completed"
        st.rerun()
    
    # Not the last question - get next question
    with st.spinner("⏳ Time's up! Loading next question..."):
        # Submit timeout to backend
        backend_submit_answer(
            st.session_state.interview_id,
            st.session_state.current_tech_question,
            "[AUTO-SUBMITTED: TIME EXPIRED]"
        )
        
        # Wait for next question
        while True:
            time.sleep(2)
            res = requests.get(
                f"{BACKEND_URL}/next-question/{st.session_state.interview_id}",
                timeout=120
            ).json()
            
            if "question" in res:
                st.session_state.current_tech_question = res["question"]
                break
    
    timeout_msg = (
        "<div class='assistant-box' style='background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%); color: #991b1b;'>"
        "⏰ Previous question was skipped as response was not submitted within the time limit. "
        "Please answer the question before the timer ends to save the response."
        "</div>\n\n"
        f"<div class='question-box'>{st.session_state.current_tech_question}</div>"
    )
    
    st.session_state.messages.append({"role": "assistant", "content": timeout_msg})
    st.session_state.input_locked = False
    st.rerun()

# INPUT HANDLING
if user_input:
    if st.session_state.pending_user_input is None:
        st.session_state.pending_user_input = user_input
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        if st.session_state.stage == "tech" and st.session_state.current_tech_question:
            st.session_state.input_locked = True
            st.session_state.timer_placeholder = None
        
        st.rerun()

if st.session_state.pending_user_input is not None:
    user_input = st.session_state.pending_user_input
    st.session_state.pending_user_input = None
    
    if user_input.lower() in EXIT_KEYWORDS:
        farewell = "Thank you for your time. This concludes the interview. 👋"
        st.session_state.messages.append({"role": "assistant", "content": farewell})
        st.rerun()

    # INFO STAGE
    if st.session_state.stage == "info":
        question = QUESTIONS[st.session_state.current_q]

        # NAME VALIDATION
        if st.session_state.current_q == 0:
            name = user_input.strip()
            name_valid = (
                len(name.split()) >= 2
                and all(part.isalpha() for part in name.split())
                and len(name) >= 3
            )
            if not name_valid:
                msg = (
                    "Please enter your full name (first and last name) using only letters. "
                    "Example: John Doe"
                )
                st.session_state.messages.append({"role": "assistant", "content": msg})
                st.rerun()

        # EMAIL VALIDATION
        if st.session_state.current_q == 1:
            if st.session_state.waiting_for_otp_email:
                otp = user_input.strip()
                if len(otp) != 6 or not otp.isdigit():
                    msg = "Please enter a valid 6-digit OTP. 🔢"
                    st.session_state.messages.append({"role": "assistant", "content": msg})
                    st.rerun()
                
                with st.spinner("🔐 Validating OTP, please wait..."):
                    time.sleep(5.0)
                    try:
                        verify_response = requests.post(
                            f"{BACKEND_URL}/verify-otp/email/{st.session_state.temp_email}/{otp}",
                            timeout=10
                        ).json()
                        
                        if verify_response["verified"]:
                            time.sleep(0.8)
                            st.session_state.email_verified = True
                            st.session_state.waiting_for_otp_email = False
                            st.session_state.otp_sent_email = False
                            st.session_state.otp_email_expired = False
                            st.session_state.otp_email_timestamp = None
                            st.session_state.answers[QUESTIONS[1]] = st.session_state.temp_email
                        else:
                            msg = f"❌ {verify_response['message']}"
                            st.session_state.messages.append({"role": "assistant", "content": msg})
                            st.rerun()
                    except Exception as e:
                        msg = f"❌ Error verifying OTP: {str(e)}"
                        st.session_state.messages.append({"role": "assistant", "content": msg})
                        st.rerun()
            else:
                email = user_input.strip()
                email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[A-Za-z]{2,}$'
                if not re.match(email_pattern, email):
                    msg = "Please enter a valid email address. Example: john.doe@example.com 📧"
                    st.session_state.messages.append({"role": "assistant", "content": msg})
                    st.rerun()
                
                # Check for duplicate email
                try:
                    duplicate_check = requests.post(
                        f"{BACKEND_URL}/check-duplicate",
                        json={"email": email},
                        timeout=5
                    ).json()
                    
                    if duplicate_check.get("has_duplicates") and "email" in duplicate_check.get("duplicates", []):
                        st.session_state.email_duplicate_attempts += 1
                        
                        if st.session_state.email_duplicate_attempts >= 3:
                            # Terminate on 3rd attempt
                            st.session_state.terminated_duplicate = True
                            st.switch_page("pages/termination.py")
                            st.stop()
                        else:
                            # Show warning modal and ask again
                            st.session_state.show_duplicate_modal = True
                            st.session_state.duplicate_field = "email"
                            
                            attempts = st.session_state.email_duplicate_attempts
                            remaining = 3 - attempts
                            
                            msg = (
                                f"<div class='assistant-box' style='background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%); color: #991b1b; border-left: 4px solid #dc2626;'>"
                                f"⚠️ <b>Email Already Used!</b><br><br>"
                                f"This email is already registered in our system. Please enter a valid email address.<br><br>"
                                f"<b>Attempts: {attempts}/3 | Remaining warnings: {remaining}</b><br>"
                                f"After 3 attempts, you will be blocked from continuing."
                                f"</div>"
                            )
                            st.session_state.messages.append({"role": "assistant", "content": msg})
                            st.rerun()
                except Exception as e:
                    print(f"⚠️ Duplicate check failed: {e}")

                # If we reach here, email is unique - proceed with OTP  
                st.session_state.temp_email = email
                
                with st.spinner("📧 Sending OTP to your email..."):
                    time.sleep(2.5)
                    try:
                        otp_response = requests.post(
                            f"{BACKEND_URL}/send-otp/email/{email}",
                            timeout=10
                        ).json()
                        
                        if otp_response["success"]:
                            st.session_state.otp_sent_email = True
                            st.session_state.waiting_for_otp_email = True
                            st.session_state.otp_email_expired = False
                            st.session_state.otp_email_timestamp = datetime.now()
                            msg = f"📧 A 6-digit OTP has been sent to <b>{email}</b>.<br>Please enter the OTP within 2 minutes to verify your email."
                            st.session_state.messages.append({"role": "assistant", "content": msg})
                            st.rerun()
                        else:
                            msg = "❌ Failed to send OTP. Please try again."
                            st.session_state.messages.append({"role": "assistant", "content": msg})
                            st.rerun()
                    except Exception as e:
                        msg = f"❌ Error sending OTP: {str(e)}"
                        st.session_state.messages.append({"role": "assistant", "content": msg})
                        st.rerun()

        # PHONE VALIDATION
        if st.session_state.current_q == 2:
            phone = user_input.strip()
            phone_clean = re.sub(r'[\s\-\(\)\+]', '', phone)
            if not (phone_clean.isdigit() and 10 <= len(phone_clean) <= 15):
                msg = "Please enter a valid phone number (10-15 digits). Example: +1234567890 or 1234567890 📱"
                st.session_state.messages.append({"role": "assistant", "content": msg})
                st.rerun()
            
            # Check for duplicate phone
            try:
                duplicate_check = requests.post(
                    f"{BACKEND_URL}/check-duplicate",
                    json={"phone": phone_clean},
                    timeout=5
                ).json()
                
                if duplicate_check.get("has_duplicates") and "phone" in duplicate_check.get("duplicates", []):
                    st.session_state.phone_duplicate_attempts += 1
                    
                    if st.session_state.phone_duplicate_attempts >= 3:
                        # Terminate on 3rd attempt
                        st.session_state.terminated_duplicate = True
                        st.switch_page("pages/termination.py")
                        st.stop()
                    else:
                        # Show warning and ask again
                        attempts = st.session_state.phone_duplicate_attempts
                        remaining = 3 - attempts
                        
                        msg = (
                            f"<div class='assistant-box' style='background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%); color: #991b1b; border-left: 4px solid #dc2626;'>"
                            f"⚠️ <b>Phone Number Already Used!</b><br><br>"
                            f"This phone number is already registered in our system. Please enter a valid phone number.<br><br>"
                            f"<b>Attempts: {attempts}/3 | Remaining warnings: {remaining}</b><br>"
                            f"After 3 attempts, you will be blocked from continuing."
                            f"</div>"
                        )
                        st.session_state.messages.append({"role": "assistant", "content": msg})
                        st.rerun()
            except Exception as e:
                print(f"⚠️ Duplicate check failed: {e}")

            # If we reach here, phone is unique - proceed
            st.session_state.answers[QUESTIONS[2]] = phone_clean

        # EXPERIENCE VALIDATION
        if st.session_state.current_q == 3:
            try:
                exp = float(user_input)
                if exp < 0 or exp > 70:
                    raise ValueError
            except ValueError:
                msg = (
                    "I don't really understand that. "
                    "Please enter your experience as a valid number (e.g., 0, 1, 2.5)."
                )
                st.session_state.messages.append({"role": "assistant", "content": msg})
                st.rerun()

        # LOCATION VALIDATION
        if st.session_state.current_q == 5:
            locations = [loc.strip() for loc in user_input.split(',') if loc.strip()]
            
            valid_locations = []
            invalid_locations = []
            for loc in locations:
                is_valid = (
                    len(loc) >= 3
                    and re.search(r"[a-zA-Z]", loc)
                    and re.search(r"[aeiouAEIOU]", loc)
                    and re.fullmatch(r"[A-Za-z ,.-]+", loc)
                    and len(loc.split()) <= 4
                    and not re.search(r"(.)\1{3,}", loc)
                    and sum(c.isalpha() for c in loc) >= len(loc) * 0.6
                )
                if is_valid:
                    valid_locations.append(loc)
                else:
                    invalid_locations.append(loc)
            
            if invalid_locations:
                msg = (
                    f"The following locations appear invalid: <b>{', '.join(invalid_locations)}</b><br><br>"
                    "Please enter valid city or place names (e.g., Bangalore, New York, San Francisco). 📍"
                )
                st.session_state.messages.append({"role": "assistant", "content": msg})
                st.rerun()
            
            st.session_state.collected_locations.extend(valid_locations)
            st.session_state.collected_locations = list(dict.fromkeys(st.session_state.collected_locations))
            
            total_locations = len(st.session_state.collected_locations)
            
            if total_locations < 3:
                remaining = 3 - total_locations
                current_list = ", ".join(st.session_state.collected_locations) if st.session_state.collected_locations else "None yet"
                msg = (
                    f"Thanks! I've saved your location(s): <b>{current_list}</b><br><br>"
                    f"You need to enter <b>{remaining} more location(s)</b> to proceed. "
                    "Please provide additional preferred work locations separated by commas. 📍"
                )
                st.session_state.messages.append({"role": "assistant", "content": msg})
                st.rerun()

        skip_save = (st.session_state.current_q == 1 and not st.session_state.email_verified)
        
        if not skip_save and not st.session_state.waiting_for_otp_email:
            if st.session_state.current_q != 1:
                st.session_state.answers[question] = user_input

        time.sleep(0.2)

        ACK_MAP = {
            0: lambda val: f"Nice to meet you, <b>{val}</b>! Let's continue. ✨",
            1: lambda val: f"Your email <b>{val}</b> is verified and saved successfully. ✅",
            2: lambda val: f"Your phone number <b>{val}</b> is saved successfully. 📱",
            3: lambda _: "Thanks for sharing your experience. 💼",
            4: lambda _: "Great! Your specified role is saved. 🎯",
            5: lambda _: f"Perfect! I've saved all your preferred locations: <b>{', '.join(st.session_state.collected_locations)}</b>. 📍",
            6: lambda _: "Great, that gives me a good overview of your technical expertise. 🔧" 
        }

        if st.session_state.current_q == 1:
            if st.session_state.email_verified:
                ack_value = st.session_state.temp_email
            elif st.session_state.waiting_for_otp_email:
                st.rerun()
            else:
                st.rerun()
        else:
            ack_value = user_input
        
        ack = ACK_MAP[st.session_state.current_q](ack_value)
        st.session_state.current_q += 1

        if st.session_state.current_q < len(QUESTIONS):
            response = f"<div class='assistant-box'>{ack}</div>\n\n<div class='assistant-box'><b>{QUESTIONS[st.session_state.current_q]}</b></div>"
        else:
            st.session_state.stage = "tech"
            response = (
                f"<div class='assistant-box'>{ack}</div>\n\n"
                "<div class='rule-box'>"
                "<b>⚠️ Before we begin:</b><br><br>"
                "• <b>Read every question thoroughly before answering</b><br>"
                "• <b>Each question has a time limit of 3 minutes</b> ⏱️<br>"
                "• <b>The question must be answered within the time limit to proceed</b><br>"
                "• <b>If the timer runs out, the question will be automatically skipped</b><br>"
                "• <b>Answers must be written in your own words, Any form of plagiarism will result in disqualification</b><br>"
                "• <b>If you are unsure of an answer or wish to skip a question</b>, type <b>PASS</b> to proceed<br>"
                "• <b>Even if a question is skipped or times out, it is counted toward the total number of questions</b><br>"
                "• <b>During the interview, do not SWITCH TABS or EXIT FULLSCREEN</b><br><br>"
                "Press <b>OK</b> when you're ready to begin the technical interview. 🚀"
                "</div>"
            )

        with st.spinner("✨ TalentScout is reviewing your response..."):
            time.sleep(2.0)

        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()

    # TECHNICAL STAGE
    else:
        if (
            st.session_state.current_tech_question is None
            and user_input.strip().lower() == "ok"
        ):
            with st.spinner("⏳ Starting interview..."):
                payload = {
                    "name": st.session_state.answers[QUESTIONS[0]],
                    "email": st.session_state.answers[QUESTIONS[1]],
                    "phone": st.session_state.answers[QUESTIONS[2]],
                    "experience": float(st.session_state.answers[QUESTIONS[3]]),
                    "position": st.session_state.answers[QUESTIONS[4]],
                    "location": ", ".join(st.session_state.collected_locations),
                    "tech_stack": st.session_state.answers[QUESTIONS[-1]],
                }
                
                data = backend_start_interview(payload)
                st.session_state.interview_id = data["interview_id"]
                st.session_state.current_tech_question = data["question"]

            formatted_q = f"<div class='question-box'>{st.session_state.current_tech_question}</div>"
            st.session_state.messages.append({"role": "assistant", "content": formatted_q})
            st.session_state.input_locked = False
            st.rerun()

        skip_inputs = {
            "pass", "skip", "idk", "i don't know", "don't know",
            "no idea", "not sure", "n/a"
        }

        if user_input.strip().lower() in skip_inputs:
            st.session_state.tech_q_count += 1
            
            # Check if this was the last question
            if st.session_state.tech_q_count >= 5:
                with st.spinner("⏳ Processing your response..."):
                    backend_submit_answer(
                        st.session_state.interview_id,
                        st.session_state.current_tech_question,
                        user_input
                    )
                    
                    # Wait for completion
                    while True:
                        time.sleep(1)
                        res = requests.get(
                            f"{BACKEND_URL}/next-question/{st.session_state.interview_id}",
                            timeout=120
                        ).json()
                        
                        if res.get("completed"):
                            break
                
                end_msg = (
                    "<div class='assistant-box'>"
                    "Thank you. This concludes the technical interview. ✅<br><br>"
                    "Our team will review your responses and get back to you. 📧"
                    "</div>"
                )
                st.session_state.messages.append({"role": "assistant", "content": end_msg})
                st.session_state.input_locked = False
                st.session_state.stage = "completed"
                st.rerun()
            
            # Not the last question - get next question
            with st.spinner("⏳ Loading next question..."):
                backend_submit_answer(
                    st.session_state.interview_id,
                    st.session_state.current_tech_question,
                    user_input
                )
                
                while True:
                    time.sleep(2)
                    res = requests.get(
                        f"{BACKEND_URL}/next-question/{st.session_state.interview_id}",
                        timeout=120
                    ).json()
                    
                    if "question" in res:
                        st.session_state.current_tech_question = res["question"]
                        break

            # Varied skip acknowledgements
            import random
            skip_acknowledgements = [
                "It's ok! Let's move on to the next question. ⏭️",
                "No problem! Let's explore a different area. 🔄",
                "That's alright! Moving forward to the next one. ➡️",
                "Understood! Let's try a different question. 🎯",
                "No worries! Let me ask you something else. 💫",
                "That's fine! Let's continue with another topic. 📋"
            ]
            
            skip_msg = random.choice(skip_acknowledgements)

            msg = (
                f"<div class='assistant-box'>{skip_msg}</div>\n\n"
                f"<div class='question-box'>{st.session_state.current_tech_question}</div>"
            )

            st.session_state.messages.append({"role": "assistant", "content": msg})
            st.session_state.input_locked = False
            st.rerun()

        # EVALUATE ANSWER
        st.session_state.tech_q_count += 1
        
        # Check if this was the last question
        if st.session_state.tech_q_count >= 5:
            with st.spinner("⏳ Please wait, your answer is being saved..."):
                backend_submit_answer(
                    st.session_state.interview_id,
                    st.session_state.current_tech_question,
                    user_input
                )
                time.sleep(3)
                
                # Wait for completion confirmation
                while True:
                    time.sleep(1)
                    res = requests.get(
                        f"{BACKEND_URL}/next-question/{st.session_state.interview_id}",
                        timeout=120
                    ).json()
                    
                    if res.get("completed"):
                        break
            
            end_msg = (
                "<div class='assistant-box'>"
                "Thank you. This concludes the technical interview. ✅<br><br>"
                "Our team will review your responses and get back to you. 📧"
                "</div>"
            )
            st.session_state.messages.append({"role": "assistant", "content": end_msg})
            st.session_state.input_locked = False
            st.session_state.stage = "completed"
            st.rerun()
        
        # Not the last question - get next question
        with st.spinner("⏳ Please wait, your answer is being saved..."):
            backend_submit_answer(
                st.session_state.interview_id,
                st.session_state.current_tech_question,
                user_input
            )
            time.sleep(6.0)

        with st.spinner("✅ Answer saved, next question is being loaded..."):
            while True:
                time.sleep(2)
                res = requests.get(
                    f"{BACKEND_URL}/next-question/{st.session_state.interview_id}",
                    timeout=120
                ).json()
                
                if "question" in res:
                    st.session_state.current_tech_question = res["question"]
                    
                    # Varied acknowledgements - randomly selected
                    import random
                    acknowledgements = [
                        "Thanks for sharing your thoughts. I appreciate you walking me through your reasoning. 🤔",
                        "That's an interesting approach! Let me ask you something related to what you just mentioned. 💡",
                        "I see where you're going with that. Building on your answer, let's explore this further. 🔍",
                        "Great! Your explanation gives me a good sense of your understanding. Let's continue. ✨",
                        "Thank you for that detailed response. Let me follow up with another question. 📝",
                        "I appreciate your perspective on this. Now, let's move to the next scenario. 🎯",
                        "Interesting! Based on what you shared, here's a related question. 🚀",
                        "Thanks for walking me through that. Let's explore another aspect of your expertise. 💼",
                        "That makes sense. Let me ask you about something connected to your answer. 🔗",
                        "Good! I can see your thought process. Let's continue with the next question. ⚡"
                    ]
                    
                    feedback = random.choice(acknowledgements)

                    combined = (
                        f"<div class='assistant-box'>{feedback}</div>\n\n"
                        f"<div class='question-box'>{st.session_state.current_tech_question}</div>"
                    )

                    st.session_state.messages.append({"role": "assistant", "content": combined})
                    st.session_state.input_locked = False
                    break
        st.rerun()