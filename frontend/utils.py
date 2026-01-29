# frontend/utils.py
EXIT_KEYWORDS = ["exit", "quit", "bye", "stop", "end"]

HIDE_MENU_CSS = """
<style>
/* Hide sidebar and all its controls */
[data-testid="collapsedControl"],
section[data-testid="stSidebar"] > div:first-child,
section[data-testid="stSidebar"],
.css-1dp5vir,
button[kind="header"],
[data-testid="stHeader"] button[kind="header"],
[data-testid="stHeader"] > div > div > button,
header button,
#MainMenu,
[data-testid="stToolbar"],
header[data-testid="stHeader"],
[data-testid="stHeaderActionElements"],
button[kind="headerNoPadding"],
[data-testid="baseButton-header"],
.styles_viewerBadge__1yB5_ {
    display: none !important;
}

/* Force hide entire header */
header {
    visibility: hidden !important;
    height: 0 !important;
    padding: 0 !important;
    margin: 0 !important;
}
</style>
"""