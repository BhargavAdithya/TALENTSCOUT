# frontend/pages/completion.py
import streamlit as st
import streamlit.components.v1 as components

# ============================================
# SET PAGE CONFIG (MUST BE FIRST)
# ============================================
st.set_page_config(
    page_title="Interview Completed",
    page_icon="✅",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================
# DISABLE PROTECTION ON COMPLETION PAGE
# ============================================
st.markdown(
    """
    <style>
        /* Re-enable text selection */
        * {
            -webkit-user-select: text !important;
            -moz-user-select: text !important;
            -ms-user-select: text !important;
            user-select: text !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)

components.html(
    """
    <script>
    (function() {
        const doc = window.parent.document;
        const win = window.parent;
        
        // Signal completion page
        win.onCompletionPage = true;
        win.onTerminationPage = false;
        win.interviewProtectionAttached = false;
        
        // Remove warnings
        function removeWarnings() {
            const overlay = doc.getElementById('violation-warning-overlay');
            if (overlay) overlay.remove();
        }
        
        removeWarnings();
        setTimeout(removeWarnings, 100);
        setTimeout(removeWarnings, 500);
        
        console.log('✅ Completion page - protection disabled');
    })();
    </script>
    """,
    height=0
)

# ============================================
# CHECK IF INTERVIEW IS ACTUALLY COMPLETED
# ============================================
if not st.session_state.get("interview_completed_id"):
    # Redirect back if accessed directly
    st.switch_page("app.py")
    st.stop()

# Check if interview is terminated due to violations
if st.session_state.get("interview_terminated"):
    components.html(
        """
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                * { margin: 0; padding: 0; box-sizing: border-box; }
                body {
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                    background: #000;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                }
                .termination-card {
                    background: white;
                    padding: 60px 80px;
                    border-radius: 24px;
                    text-align: center;
                    max-width: 700px;
                    box-shadow: 0 20px 60px rgba(0,0,0,0.5);
                }
                h1 { color: #dc2626; font-size: 2.5rem; margin-bottom: 20px; }
                p { font-size: 1.3rem; color: #374151; line-height: 1.6; }
            </style>
        </head>
        <body>
            <div class="termination-card">
                <div style="font-size: 5rem; margin-bottom: 20px;">🚫</div>
                <h1>Interview Terminated!</h1>
                <p>
                    Your interview has been terminated due to<br>
                    multiple fullscreen violations.
                </p>
            </div>
        </body>
        </html>
        """,
        height=800
    )
    st.stop()

# ============================================
# FULLSCREEN EXIT DETECTION & BLUR OVERLAY
# ============================================
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
            
            html, body {
                width: 100%;
                height: 100vh;
                overflow: hidden;
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            }
            
            /* Initial completion message overlay */
            .completion-overlay {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: linear-gradient(135deg, #111111 0%, #667eea 100%);
                z-index: 10000;
                display: flex;
                justify-content: center;
                align-items: center;
                transition: filter 0.8s ease, opacity 0.6s ease;
            }
            
            .completion-overlay.blur-exit {
                filter: blur(20px);
                opacity: 0;
            }
            
            .completion-card {
                background: white;
                padding: 50px 60px;
                border-radius: 24px;
                text-align: center;
                max-width: 600px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.4);
                animation: fadeInScale 0.6s ease;
            }
            
            @keyframes fadeInScale {
                from {
                    opacity: 0;
                    transform: scale(0.9);
                }
                to {
                    opacity: 1;
                    transform: scale(1);
                }
            }
            
            .completion-icon {
                font-size: 4rem;
                margin-bottom: 20px;
                animation: bounce 2s ease-in-out infinite;
            }
            
            @keyframes bounce {
                0%, 100% { transform: translateY(0); }
                50% { transform: translateY(-10px); }
            }
            
            h1 {
                color: #667eea;
                margin-bottom: 20px;
                font-size: 2rem;
            }
            
            p {
                font-size: 1.2rem;
                color: #374151;
                margin-bottom: 20px;
                line-height: 1.6;
            }
            
            .esc-instruction {
                background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
                border: 2px solid #f59e0b;
                padding: 20px 30px;
                border-radius: 12px;
                margin-top: 20px;
                animation: pulse 2s ease-in-out infinite;
            }
            
            .esc-instruction p {
                color: #92400e;
                font-weight: 600;
                font-size: 1.1rem;
                margin: 0;
                line-height: 1.6;
            }
            
            .esc-key {
                display: inline-block;
                background: #374151;
                color: white;
                padding: 8px 16px;
                border-radius: 6px;
                font-weight: bold;
                font-family: monospace;
                font-size: 1.2rem;
                margin: 0 5px;
                box-shadow: 0 4px 8px rgba(0,0,0,0.2);
            }
            
            @keyframes pulse {
                0%, 100% { transform: scale(1); }
                50% { transform: scale(1.02); }
            }
            
            /* Exit confirmation overlay (shown after ESC) */
            .exit-overlay {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0, 0, 0, 0.98);
                backdrop-filter: blur(30px);
                -webkit-backdrop-filter: blur(30px);
                z-index: 10001;
                display: none;
                justify-content: center;
                align-items: center;
                opacity: 0;
                transition: opacity 0.8s ease;
            }
            
            .exit-overlay.show {
                display: flex;
                opacity: 1;
            }
            
            .exit-card {
                background: white;
                padding: 60px 80px;
                border-radius: 24px;
                text-align: center;
                max-width: 700px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.5);
                animation: slideUp 0.6s ease;
            }
            
            @keyframes slideUp {
                from {
                    transform: translateY(50px);
                    opacity: 0;
                }
                to {
                    transform: translateY(0);
                    opacity: 1;
                }
            }
            
            .exit-icon {
                font-size: 5rem;
                margin-bottom: 20px;
            }
            
            .exit-card h1 {
                color: #10b981;
                font-size: 2.5rem;
                margin-bottom: 20px;
            }
            
            .exit-card p {
                font-size: 1.3rem;
                color: #374151;
                margin: 0;
            }
        </style>
    </head>
    <body>
        <!-- Initial completion message -->
        <div class="completion-overlay" id="completionOverlay">
            <div class="completion-card">
                <div class="completion-icon">🎉</div>
                <h1>Interview Completed!</h1>
                <p>
                    Thank you for your time!<br>
                    Your responses have been recorded successfully.
                </p>
                
                <div class="esc-instruction">
                    <p>
                        Press <span class="esc-key">ESC</span> to exit fullscreen<br>
                        and then you may close the browser window.
                    </p>
                </div>
            </div>
        </div>
        
        <!-- Exit confirmation overlay (shown after ESC) -->
        <div class="exit-overlay" id="exitOverlay">
            <div class="exit-card">
                <div class="exit-icon">✅</div>
                <h1>Fullscreen Exited!</h1>
                <p>You can safely close the browser now.</p>
            </div>
        </div>
        
        <script>
        console.log('✅ Interview completion page loaded');
        
        let fullscreenExited = false;
        
        // Listen for fullscreen change events
        document.addEventListener('fullscreenchange', handleFullscreenChange);
        document.addEventListener('webkitfullscreenchange', handleFullscreenChange);
        document.addEventListener('mozfullscreenchange', handleFullscreenChange);
        document.addEventListener('MSFullscreenChange', handleFullscreenChange);
        
        function handleFullscreenChange() {
            const isFullscreen = !!(document.fullscreenElement || 
                                   document.webkitFullscreenElement || 
                                   document.mozFullScreenElement || 
                                   document.msFullscreenElement);
            
            console.log('📺 Fullscreen state changed. Is fullscreen:', isFullscreen);
            
            // If we exited fullscreen and haven't shown the exit message yet
            if (!isFullscreen && !fullscreenExited) {
                fullscreenExited = true;
                console.log('✅ Fullscreen exited - showing blur and exit message');
                showExitConfirmation();
            }
        }
        
        // Show exit confirmation with blur effect
        function showExitConfirmation() {
            console.log('🎬 Starting transition to exit screen');
            
            const completionOverlay = document.getElementById('completionOverlay');
            const exitOverlay = document.getElementById('exitOverlay');
            
            if (!completionOverlay || !exitOverlay) {
                console.error('❌ Overlays not found!');
                return;
            }
            
            // Blur and fade out completion overlay
            completionOverlay.classList.add('blur-exit');
            console.log('👋 Blurring completion overlay');
            
            // Wait for blur animation, then show exit overlay
            setTimeout(function() {
                completionOverlay.style.display = 'none';
                exitOverlay.classList.add('show');
                console.log('✨ Exit overlay visible with blur background');
            }, 800);
        }
        
        console.log('⌨️ Press ESC to exit fullscreen');
        </script>
    </body>
    </html>
    """,
    height=0,
    scrolling=False
)

# Fill the entire viewport and hide sidebar
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
        
        /* Remove all Streamlit default padding and margins */
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
        }
    </style>
    """,
    unsafe_allow_html=True
)