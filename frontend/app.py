# frontend/app.py
import streamlit as st
import streamlit.components.v1 as components
import time
import re
import requests
import json
from datetime import datetime

# -------------------------------------------------
# Page config
# -------------------------------------------------
st.set_page_config(
    page_title="TalentScout - Interview",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# UNIVERSAL SIDEBAR TOGGLE HIDER AND MENU HIDER
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

# -------------------------------------------------
# Initialize session state
# -------------------------------------------------
if "app_stage" not in st.session_state:
    st.session_state.app_stage = "permissions"  # permissions -> interview

if "permissions_granted" not in st.session_state:
    st.session_state.permissions_granted = False

if "camera_granted" not in st.session_state:
    st.session_state.camera_granted = False

if "microphone_granted" not in st.session_state:
    st.session_state.microphone_granted = False

if "fullscreen_enabled" not in st.session_state:
    st.session_state.fullscreen_enabled = False

# -------------------------------------------------
# Small style fix
# -------------------------------------------------
components.html(
    """
    <style>
        .main > div {
            padding: 0 !important;
        }
    </style>
    """,
    height=0
)

# -------------------------------------------------
# STAGE 1: PERMISSIONS
# -------------------------------------------------
if st.session_state.app_stage == "permissions":
    
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
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    min-height: 100vh;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    padding: 20px;
                    overflow: auto;
                }
                
                .container {
                    background: white;
                    border-radius: 20px;
                    padding: 40px;
                    max-width: 800px;
                    width: 100%;
                    box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                    max-height: 90vh;
                    overflow-y: auto;
                }
                
                .header {
                    text-align: center;
                    margin-bottom: 40px;
                }
                
                .logo {
                    font-size: 60px;
                    margin-bottom: 10px;
                }
                
                h1 {
                    color: #333;
                    font-size: 28px;
                    margin-bottom: 10px;
                }
                
                .subtitle {
                    color: #666;
                    font-size: 16px;
                }
                
                .permissions {
                    margin: 30px 0;
                }
                
                .permission-item {
                    display: flex;
                    align-items: center;
                    padding: 15px;
                    background: #f8f9fa;
                    border-radius: 10px;
                    margin-bottom: 15px;
                    transition: all 0.3s ease;
                }
                
                .permission-item.granted {
                    background: #d4edda;
                    border-left: 4px solid #28a745;
                }
                
                .permission-icon {
                    font-size: 24px;
                    margin-right: 15px;
                }
                
                .permission-text {
                    flex: 1;
                    font-weight: 500;
                    color: #333;
                }
                
                .permission-status {
                    font-size: 14px;
                    color: #666;
                    font-weight: 600;
                }
                
                .permission-status.granted {
                    color: #28a745;
                }
                
                .preview-section {
                    margin: 30px 0;
                }
                
                .preview-label {
                    font-weight: 600;
                    color: #333;
                    margin-bottom: 10px;
                    display: block;
                    text-transform: uppercase;
                    letter-spacing: 1px;
                    font-size: 12px;
                }
                
                #videoPreview {
                    width: 100%;
                    height: 300px;
                    background: #000;
                    border-radius: 10px;
                    object-fit: cover;
                }
                
                .buttons {
                    display: flex;
                    flex-direction: column;
                    gap: 15px;
                    margin-top: 30px;
                }
                
                button {
                    padding: 15px 30px;
                    border: none;
                    border-radius: 10px;
                    font-size: 16px;
                    font-weight: 600;
                    cursor: pointer;
                    transition: all 0.3s ease;
                }
                
                .btn-camera {
                    background: #007bff;
                    color: white;
                }
                
                .btn-camera:hover:not(:disabled) {
                    background: #0056b3;
                    transform: translateY(-2px);
                }
                
                .btn-microphone {
                    background: #28a745;
                    color: white;
                }
                
                .btn-microphone:hover:not(:disabled) {
                    background: #218838;
                    transform: translateY(-2px);
                }
                
                .btn-start {
                    background: #6c757d;
                    color: white;
                }
                
                .btn-start.enabled {
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                }
                
                .btn-start.enabled:hover:not(:disabled) {
                    transform: translateY(-2px);
                }
                
                button:disabled {
                    opacity: 0.6;
                    cursor: not-allowed;
                }
                
                .privacy-note {
                    text-align: center;
                    color: #666;
                    font-size: 14px;
                    margin-top: 30px;
                    padding-top: 20px;
                    border-top: 1px solid #dee2e6;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <div class="logo">🚀</div>
                    <h1>TalentScout Interview Setup</h1>
                    <p class="subtitle">Grant permissions to begin your journey</p>
                </div>
                
                <div class="permissions">
                    <div class="permission-item" id="cameraStatus">
                        <span class="permission-icon">📹</span>
                        <span class="permission-text">Camera</span>
                        <span class="permission-status">Not granted</span>
                    </div>
                    <div class="permission-item" id="microphoneStatus">
                        <span class="permission-icon">🎤</span>
                        <span class="permission-text">Microphone</span>
                        <span class="permission-status">Not granted</span>
                    </div>
                </div>
                
                <div class="preview-section">
                    <label class="preview-label">Live Preview</label>
                    <video id="videoPreview" autoplay playsinline muted></video>
                </div>
                
                <div class="buttons">
                    <button class="btn-camera" id="cameraBtn" onclick="requestCamera()">
                        📹 Grant Camera Access
                    </button>
                    <button class="btn-microphone" id="microphoneBtn" onclick="requestMicrophone()">
                        🎤 Grant Microphone Access
                    </button>
                    <button class="btn-start" id="startBtn" onclick="startFullscreenInterview()" disabled>
                        🖥️ Start Interview in Fullscreen
                    </button>
                </div>
                
                <div class="privacy-note">
                    🔒 Your privacy matters. Camera and microphone will remain active during the interview.
                </div>
            </div>
            
            <script>
                let cameraGranted = false;
                let microphoneGranted = false;
                let videoStream = null;
                let audioStream = null;
                
                function updateStatus() {
                    const cameraStatus = document.getElementById('cameraStatus');
                    const microphoneStatus = document.getElementById('microphoneStatus');
                    const startBtn = document.getElementById('startBtn');
                    
                    if (cameraGranted) {
                        cameraStatus.classList.add('granted');
                        cameraStatus.querySelector('.permission-status').textContent = 'Granted ✓';
                        cameraStatus.querySelector('.permission-status').classList.add('granted');
                    }
                    
                    if (microphoneGranted) {
                        microphoneStatus.classList.add('granted');
                        microphoneStatus.querySelector('.permission-status').textContent = 'Granted ✓';
                        microphoneStatus.querySelector('.permission-status').classList.add('granted');
                    }
                    
                    if (cameraGranted && microphoneGranted) {
                        startBtn.disabled = false;
                        startBtn.classList.add('enabled');
                    }
                }
                
                async function requestCamera() {
                    try {
                        videoStream = await navigator.mediaDevices.getUserMedia({ 
                            video: { width: { ideal: 1280 }, height: { ideal: 720 } },
                            audio: false
                        });
                        
                        document.getElementById('videoPreview').srcObject = videoStream;
                        cameraGranted = true;
                        document.getElementById('cameraBtn').disabled = true;
                        updateStatus();
                    } catch (error) {
                        console.error('Camera denied:', error);
                        alert('Camera access denied. Please allow camera permissions.');
                    }
                }
                
                async function requestMicrophone() {
                    try {
                        audioStream = await navigator.mediaDevices.getUserMedia({ 
                            audio: true,
                            video: false
                        });
                        
                        microphoneGranted = true;
                        document.getElementById('microphoneBtn').disabled = true;
                        updateStatus();
                    } catch (error) {
                        console.error('Microphone denied:', error);
                        alert('Microphone access denied. Please allow microphone permissions.');
                    }
                }
                
                async function startFullscreenInterview() {
                    if (!cameraGranted || !microphoneGranted) {
                        alert('Please grant both permissions first.');
                        return;
                    }
                    
                    const startBtn = document.getElementById('startBtn');
                    startBtn.textContent = '⏳ Starting...';
                    startBtn.disabled = true;
                    
                    try {
                        // Enter fullscreen
                        const elem = document.documentElement;
                        if (elem.requestFullscreen) {
                            await elem.requestFullscreen();
                        } else if (elem.webkitRequestFullscreen) {
                            await elem.webkitRequestFullscreen();
                        }
                        
                        await new Promise(resolve => setTimeout(resolve, 500));
                        
                        if (document.fullscreenElement || document.webkitFullscreenElement) {
                            // Reload page with interview parameter
                            window.location.href = '/?stage=interview';
                        } else {
                            throw new Error("Fullscreen not activated");
                        }
                    } catch (error) {
                        console.error('Fullscreen failed:', error);
                        startBtn.textContent = '🖥️ Start Interview in Fullscreen';
                        startBtn.disabled = false;
                        alert('Please allow fullscreen to continue.');
                    }
                }
            </script>
        </body>
        </html>
        """,
        height=1000
    )
    
    # Check if we should transition to interview
    query_params = st.query_params
    if "stage" in query_params and query_params["stage"] == "interview":
        st.session_state.app_stage = "interview"
        st.session_state.permissions_granted = True
        st.session_state.camera_granted = True
        st.session_state.microphone_granted = True
        st.session_state.fullscreen_enabled = True
        st.rerun()

# -------------------------------------------------
# STAGE 2: INTERVIEW
# -------------------------------------------------
elif st.session_state.app_stage == "interview":
    # Load the interview directly
    st.switch_page("pages/interview.py")