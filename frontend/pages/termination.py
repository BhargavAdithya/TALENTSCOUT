# frontend/pages/termination.py
import streamlit as st
import streamlit.components.v1 as components
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import HIDE_MENU_CSS

# ============================================
# SET PAGE CONFIG (MUST BE FIRST)
# ============================================
st.set_page_config(
    page_title="Access Denied",
    page_icon="🚫",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================
# DISABLE PROTECTION AND REMOVE WARNINGS ON TERMINATION PAGE
# ============================================
st.markdown(
    """
    <style>
        /* Re-enable text selection on termination page */
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
    <!DOCTYPE html>
    <html>
    <body>
        <script>
        (function() {
            console.log('🚫 Termination page - disabling all protection');
            
            const doc = window.parent.document;
            const win = window.parent;
            
            // Signal termination page
            win.onTerminationPage = true;
            
            // Disable protection flag
            win.interviewProtectionAttached = false;
            
            // Function to remove all warnings
            function removeAllWarnings() {
                const overlays = doc.querySelectorAll('#violation-warning-overlay');
                overlays.forEach(overlay => {
                    if (overlay && overlay.parentNode) {
                        overlay.remove();
                        console.log('✅ Warning removed');
                    }
                });
                
                // Also try removing by class
                const warningElements = doc.querySelectorAll('[id*="warning"]');
                warningElements.forEach(el => {
                    if (el.id.includes('violation')) {
                        el.remove();
                    }
                });
            }
            
            // Remove warnings multiple times
            removeAllWarnings();
            setTimeout(removeAllWarnings, 50);
            setTimeout(removeAllWarnings, 100);
            setTimeout(removeAllWarnings, 200);
            setTimeout(removeAllWarnings, 500);
            setTimeout(removeAllWarnings, 1000);
            setTimeout(removeAllWarnings, 2000);
            
            // Override the showWarning functions to prevent new warnings
            win.showWarning = function() {
                console.log('⚠️ Warning blocked on termination page');
            };
            win.showInfoWarning = function() {
                console.log('⚠️ Info warning blocked on termination page');
            };
            
            // Set up observer to auto-remove any warnings that appear
            const observer = new MutationObserver(function(mutations) {
                mutations.forEach(function(mutation) {
                    mutation.addedNodes.forEach(function(node) {
                        if (node.id === 'violation-warning-overlay') {
                            node.remove();
                            console.log('✅ Auto-removed new warning');
                        }
                    });
                });
            });
            
            observer.observe(doc.body, {
                childList: true,
                subtree: true
            });
            
            console.log('✅ Termination page protection fully disabled');
        })();
        </script>
    </body>
    </html>
    """,
    height=0
)

st.markdown(HIDE_MENU_CSS, unsafe_allow_html=True)

# ============================================
# CHECK TERMINATION REASON
# ============================================
termination_reason = st.session_state.get("termination_reason", "duplicate")  # default to duplicate

# Check if it's a policy violation termination from interview
if st.session_state.get("interview_id"):
    try:
        import requests
        status_response = requests.get(
            f"https://talentscout-backend-c504.onrender.com/status/{st.session_state.interview_id}",
            timeout=5
        ).json()
        
        if status_response.get("is_terminated") and status_response.get("violation_count", 0) >= 3:
            termination_reason = "policy_violation"
    except Exception as e:
        pass

# ============================================
# DISPLAY APPROPRIATE TERMINATION MESSAGE
# ============================================
if termination_reason == "policy_violation":
    # Policy violation during interview
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
                
                .termination-card {
                    background: white;
                    padding: 60px 80px;
                    border-radius: 24px;
                    text-align: center;
                    max-width: 700px;
                    box-shadow: 0 20px 60px rgba(0,0,0,0.5);
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
                    animation: shake 0.5s ease-in-out;
                }
                
                @keyframes shake {
                    0%, 100% { transform: rotate(0deg); }
                    25% { transform: rotate(-10deg); }
                    75% { transform: rotate(10deg); }
                }
                
                h1 {
                    color: #dc2626;
                    font-size: 2.5rem;
                    margin-bottom: 20px;
                    font-weight: 700;
                }
                
                p {
                    font-size: 1.3rem;
                    color: #374151;
                    line-height: 1.8;
                    margin-bottom: 15px;
                }
                
                .reason {
                    background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
                    color: #991b1b;
                    padding: 20px;
                    border-radius: 12px;
                    margin-top: 30px;
                    border-left: 4px solid #dc2626;
                }
                
                .reason strong {
                    display: block;
                    font-size: 1.1rem;
                    margin-bottom: 10px;
                }
                
                .footer {
                    margin-top: 30px;
                    color: #6b7280;
                    font-size: 1rem;
                }
            </style>
        </head>
        <body>
            <div class="termination-card">
                <div class="icon">🚫</div>
                <h1>Interview Terminated</h1>
                <p>
                    Your interview has been terminated due to policy violations.
                </p>
                
                <div class="reason">
                    <strong>Reason:</strong>
                    Multiple attempts to use disabled functionality during the interview.<br>
                    This includes using prohibited keyboard shortcuts, copy/paste operations, or other restricted actions.
                </div>
                
                <p class="footer">
                    If you believe this is an error, please contact our support team.
                </p>
            </div>
        </body>
        </html>
        """,
        height=800
    )
else:
    # Duplicate email/phone termination (original message)
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
                
                .termination-card {
                    background: white;
                    padding: 60px 80px;
                    border-radius: 24px;
                    text-align: center;
                    max-width: 700px;
                    box-shadow: 0 20px 60px rgba(0,0,0,0.5);
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
                    animation: shake 0.5s ease-in-out;
                }
                
                @keyframes shake {
                    0%, 100% { transform: rotate(0deg); }
                    25% { transform: rotate(-10deg); }
                    75% { transform: rotate(10deg); }
                }
                
                h1 {
                    color: #dc2626;
                    font-size: 2.5rem;
                    margin-bottom: 20px;
                    font-weight: 700;
                }
                
                p {
                    font-size: 1.3rem;
                    color: #374151;
                    line-height: 1.8;
                    margin-bottom: 15px;
                }
                
                .reason {
                    background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
                    color: #991b1b;
                    padding: 20px;
                    border-radius: 12px;
                    margin-top: 30px;
                    border-left: 4px solid #dc2626;
                }
                
                .reason strong {
                    display: block;
                    font-size: 1.1rem;
                    margin-bottom: 10px;
                }
                
                .footer {
                    margin-top: 30px;
                    color: #6b7280;
                    font-size: 1rem;
                }
            </style>
        </head>
        <body>
            <div class="termination-card">
                <div class="icon">🚫</div>
                <h1>Access Denied</h1>
                <p>
                    You have been blocked from continuing the interview process.
                </p>
                
                <div class="reason">
                    <strong>Reason:</strong>
                    Multiple attempts to use duplicate email or phone number.<br>
                    This indicates fraudulent activity or system abuse.
                </div>
                
                <p class="footer">
                    If you believe this is an error, please contact our support team.
                </p>
            </div>
        </body>
        </html>
        """,
        height=800
    )

# Fill the entire viewport
st.markdown(
    """
    <style>
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