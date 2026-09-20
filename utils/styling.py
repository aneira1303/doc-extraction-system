"""
Custom theme: a "data console" identity for a document-intelligence tool.
Space Grotesk (display) + Inter (UI) + JetBrains Mono (data/labels), on a
cool near-black base with blue as the primary interactive color and red
reserved as a meaningful signal (flags, alerts, destructive actions) rather
than decoration.

Injected once at app startup via st.markdown(..., unsafe_allow_html=True).
Streamlit renders select menus, tooltips, and the header toolbar in portals
outside the .stApp tree, and BaseWeb widgets carry their own high-specificity
inline colors — both are targeted explicitly below rather than relied on
via inheritance.
"""

FONT_IMPORT = """
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
"""

CUSTOM_CSS = """
<style>
:root {
    --ink:        #0a0c11;
    --surface:    #12151d;
    --surface-2:  #191d28;
    --surface-3:  #212635;
    --blue:       #2f6fed;
    --blue-soft:  #5b8bf5;
    --blue-dim:   #1c3f8f;
    --red:        #e2394d;
    --red-soft:   #ef6376;
    --red-dim:    #8f1c2a;
    --text-hi:    #eef0f5;
    --text-lo:    #8a92a8;
    --text-faint: #545c72;
    --line:       #232838;
    --f-display: "Space Grotesk", "Inter", sans-serif;
    --f-body:    "Inter", -apple-system, sans-serif;
    --f-mono:    "JetBrains Mono", ui-monospace, monospace;
}

/* ============ GLOBAL ============ */
html, body, .stApp {
    background: var(--ink) !important;
    color: var(--text-hi) !important;
    font-family: var(--f-body);
}
.stApp { background-image: linear-gradient(180deg, #0d1017 0%, var(--ink) 320px); }

* { scrollbar-width: thin; scrollbar-color: var(--blue-dim) var(--surface); }
::-webkit-scrollbar { width: 9px; height: 9px; }
::-webkit-scrollbar-track { background: var(--surface); }
::-webkit-scrollbar-thumb { background: var(--blue-dim); border-radius: 5px; }
::-webkit-scrollbar-thumb:hover { background: var(--blue); }

header[data-testid="stHeader"] {
    background: var(--ink) !important;
    border-bottom: 1px solid var(--line);
}
header[data-testid="stHeader"] * { color: var(--text-hi) !important; fill: var(--text-hi) !important; }
#MainMenu, footer { visibility: hidden; }

.stApp p, .stApp span, .stApp li, .stApp label,
.stMarkdown, .stMarkdown p, .stText, div[data-testid="stMarkdownContainer"] {
    color: var(--text-hi);
}
.stCaption, [data-testid="stCaptionContainer"], small {
    color: var(--text-lo) !important;
    font-family: var(--f-mono);
    font-size: 0.78rem !important;
    letter-spacing: 0.1px;
}

/* ============ SIDEBAR — control panel ============ */
section[data-testid="stSidebar"] {
    background: var(--surface);
    border-right: 1px solid var(--line);
}
section[data-testid="stSidebar"] * { color: var(--text-hi); }
section[data-testid="stSidebar"] [data-testid="stCaptionContainer"] { color: var(--text-lo) !important; }
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    font-family: var(--f-mono) !important;
    font-size: 0.85rem !important;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: var(--blue-soft) !important;
    border: none !important;
    padding: 0 !important;
    margin-top: 1.4rem !important;
}
section[data-testid="stSidebar"] hr { border-color: var(--line) !important; margin: 1rem 0; }

/* ============ HEADINGS (main content) ============ */
h1, h2, h3, h4 {
    color: var(--text-hi) !important;
    font-family: var(--f-display) !important;
    font-weight: 600 !important;
    letter-spacing: -0.3px;
}
h1 {
    font-size: 2.1rem !important;
    position: relative;
    padding-bottom: 0.6rem;
    margin-bottom: 0.3rem;
}
h1::after {
    content: "";
    position: absolute;
    left: 0; bottom: 0;
    width: 64px; height: 3px;
    background: linear-gradient(90deg, var(--blue) 0%, var(--red) 100%);
    border-radius: 2px;
}
h2, h3 { border-left: 2px solid var(--blue); padding-left: 10px; }

/* ============ WIDGET LABELS ============ */
div[data-testid="stWidgetLabel"] label,
div[data-testid="stWidgetLabel"] p {
    color: var(--text-lo) !important;
    font-family: var(--f-mono) !important;
    font-size: 0.78rem !important;
    text-transform: uppercase;
    letter-spacing: 0.6px;
    font-weight: 500 !important;
}

/* ============ BUTTONS ============ */
.stButton>button {
    background: var(--surface-3);
    color: var(--text-hi) !important;
    border: 1px solid var(--blue-dim);
    border-radius: 6px;
    font-weight: 600;
    font-family: var(--f-body);
    padding: 0.5rem 1.1rem;
    transition: all 0.15s ease;
}
.stButton>button p { color: var(--text-hi) !important; }
.stButton>button:hover {
    background: var(--blue);
    border-color: var(--blue);
    box-shadow: 0 0 0 3px rgba(47,111,237,0.18);
}
.stButton>button:hover p { color: #fff !important; }
.stButton>button:active { transform: translateY(1px); }

/* Primary buttons (st.button(type="primary")) get full blue fill */
.stButton>button[kind="primary"] {
    background: var(--blue);
    border-color: var(--blue);
}
.stButton>button[kind="primary"] p { color: #fff !important; }
.stButton>button[kind="primary"]:hover { background: var(--blue-soft); }

.stDownloadButton>button {
    background: transparent;
    color: var(--blue-soft) !important;
    border: 1px solid var(--blue-dim);
    border-radius: 6px;
    font-weight: 600;
}
.stDownloadButton>button p { color: var(--blue-soft) !important; }
.stDownloadButton>button:hover { background: var(--blue-dim); }
.stDownloadButton>button:hover p { color: #fff !important; }

/* ============ TABS ============ */
.stTabs [data-baseweb="tab-list"] {
    gap: 2px;
    border-bottom: 1px solid var(--line);
    background: transparent;
}
.stTabs [data-baseweb="tab"] {
    background: transparent;
    border-radius: 6px 6px 0 0;
    padding: 10px 18px;
}
.stTabs [data-baseweb="tab"] p {
    color: var(--text-lo) !important;
    font-weight: 600 !important;
    font-size: 0.92rem;
}
.stTabs [aria-selected="true"] { background: var(--surface) !important; }
.stTabs [aria-selected="true"] p { color: var(--text-hi) !important; }
.stTabs [data-baseweb="tab-highlight"] { background: var(--red) !important; height: 2px !important; }
.stTabs [data-baseweb="tab-border"] { background: var(--line) !important; }

/* ============ INPUTS ============ */
.stTextInput input, .stTextArea textarea, .stNumberInput input {
    background: var(--surface) !important;
    color: var(--text-hi) !important;
    border: 1px solid var(--line) !important;
    border-radius: 6px !important;
    font-family: var(--f-mono) !important;
    font-size: 0.9rem !important;
    caret-color: var(--blue-soft);
}
.stTextInput input::placeholder, .stTextArea textarea::placeholder {
    color: var(--text-faint) !important;
    opacity: 1 !important;
    font-family: var(--f-body) !important;
}
.stTextInput input:focus, .stTextArea textarea:focus, .stNumberInput input:focus {
    border-color: var(--blue) !important;
    box-shadow: 0 0 0 1px var(--blue) !important;
}
div[data-baseweb="base-input"] { background: var(--surface) !important; border-color: var(--line) !important; }
.stTextInput button svg { fill: var(--text-lo) !important; }

/* ============ SELECTBOX (BaseWeb) ============ */
div[data-baseweb="select"] > div {
    background: var(--surface) !important;
    border: 1px solid var(--line) !important;
    border-radius: 6px !important;
}
div[data-baseweb="select"] > div:hover { border-color: var(--blue-dim) !important; }
div[data-baseweb="select"] * { color: var(--text-hi) !important; fill: var(--text-lo) !important; }
div[data-baseweb="select"] [class*="placeholder"] { color: var(--text-faint) !important; }

div[data-baseweb="popover"] { z-index: 9999; }
div[data-baseweb="popover"] ul[role="listbox"], div[data-baseweb="menu"] {
    background: var(--surface-2) !important;
    border: 1px solid var(--line) !important;
    box-shadow: 0 12px 28px rgba(0,0,0,0.55);
}
li[role="option"] { background: var(--surface-2) !important; color: var(--text-hi) !important; font-family: var(--f-mono); font-size: 0.88rem; }
li[role="option"]:hover, li[role="option"][aria-selected="true"] {
    background: var(--surface-3) !important;
    color: var(--blue-soft) !important;
}

/* ============ CHECKBOX / RADIO / SLIDER ============ */
.stCheckbox label span, .stRadio label span { color: var(--text-hi) !important; }
.stCheckbox [data-baseweb="checkbox"] svg { fill: var(--blue) !important; }
.stSlider [data-baseweb="slider"] div[role="slider"] { background: var(--blue) !important; }
.stSlider [data-baseweb="slider"] > div > div { background: var(--blue-dim) !important; }

/* ============ EXPANDER ============ */
div[data-testid="stExpander"] {
    background: var(--surface);
    border: 1px solid var(--line);
    border-radius: 8px;
    overflow: hidden;
}
div[data-testid="stExpander"] summary { color: var(--text-hi) !important; font-weight: 500; }
div[data-testid="stExpander"] summary:hover { color: var(--blue-soft) !important; }

/* ============ METRICS ============ */
div[data-testid="stMetric"] {
    background: var(--surface);
    border: 1px solid var(--line);
    border-radius: 8px;
    padding: 14px 16px;
    position: relative;
}
div[data-testid="stMetric"]::before {
    content: "";
    position: absolute; left: 0; top: 12px; bottom: 12px; width: 2px;
    background: var(--blue);
}
div[data-testid="stMetricLabel"] p {
    color: var(--text-lo) !important;
    font-family: var(--f-mono) !important;
    font-size: 0.72rem !important;
    text-transform: uppercase;
    letter-spacing: 0.6px;
}
div[data-testid="stMetricValue"] { color: var(--text-hi) !important; font-family: var(--f-display) !important; font-weight: 600 !important; }
div[data-testid="stMetricDelta"] { color: var(--red-soft) !important; }

/* ============ DATAFRAMES ============ */
div[data-testid="stDataFrame"], div[data-testid="stTable"] {
    border: 1px solid var(--line);
    border-radius: 8px;
    overflow: hidden;
}
div[data-testid="stDataFrame"] * { color: var(--text-hi) !important; font-family: var(--f-mono) !important; font-size: 0.85rem; }

/* ============ ALERTS ============ */
div[data-testid="stAlert"] { border-radius: 6px; border: 1px solid var(--line); background: var(--surface) !important; }
div[data-testid="stAlertContentInfo"] { color: var(--blue-soft) !important; }
div[data-testid="stAlertContentError"] { color: var(--red-soft) !important; }
div[data-testid="stAlertContentSuccess"] { color: #34d399 !important; }
div[data-testid="stAlertContentWarning"] { color: #f5b642 !important; }

/* ============ FILE UPLOADER ============ */
section[data-testid="stFileUploaderDropzone"] {
    background: var(--surface) !important;
    border: 1px dashed var(--line) !important;
    border-radius: 8px;
    transition: border-color 0.15s ease;
}
section[data-testid="stFileUploaderDropzone"] * { color: var(--text-hi) !important; }
section[data-testid="stFileUploaderDropzone"]:hover { border-color: var(--blue) !important; }
div[data-testid="stFileUploaderFile"] { background: var(--surface-2); border-radius: 6px; }

/* ============ PROGRESS ============ */
div[data-testid="stProgress"] > div > div { background: var(--line) !important; }
div[data-testid="stProgress"] > div > div > div { background: var(--blue) !important; }

/* ============ SPINNER ============ */
div[data-testid="stSpinner"] p { color: var(--blue-soft) !important; font-family: var(--f-mono); }

/* ============ CHAT ============ */
div[data-testid="stChatMessage"] {
    background: var(--surface);
    border: 1px solid var(--line);
    border-radius: 8px;
}
div[data-testid="stChatMessage"] p { color: var(--text-hi) !important; }
div[data-testid="stChatMessageAvatarUser"] { background: var(--blue) !important; }
div[data-testid="stChatMessageAvatarAssistant"] { background: var(--surface-3) !important; border: 1px solid var(--red) !important; }
div[data-testid="stChatInput"] textarea {
    background: var(--surface) !important;
    color: var(--text-hi) !important;
    border: 1px solid var(--line) !important;
    font-family: var(--f-body) !important;
}
div[data-testid="stChatInput"] textarea:focus { border-color: var(--blue) !important; }
div[data-testid="stChatInput"] textarea::placeholder { color: var(--text-faint) !important; }
div[data-testid="stChatInput"] button svg { fill: var(--blue) !important; }

/* ============ JSON VIEWER ============ */
div[data-testid="stJson"] {
    background: var(--surface) !important;
    border: 1px solid var(--line);
    border-radius: 8px;
    font-family: var(--f-mono) !important;
}

/* ============ SIGNAL BADGES (confidence tags, used in app.py) ============ */
.badge {
    display: inline-block;
    padding: 2px 8px;
    border-radius: 4px;
    font-family: var(--f-mono);
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 0.4px;
    margin-right: 6px;
}
.badge-high   { background: rgba(47,111,237,0.14); color: var(--blue-soft); border: 1px solid var(--blue-dim); }
.badge-medium { background: rgba(255,255,255,0.05); color: var(--text-lo); border: 1px solid var(--line); }
.badge-low    { background: rgba(226,57,77,0.14); color: var(--red-soft); border: 1px solid var(--red-dim); }

.doc-card {
    background: var(--surface);
    border: 1px solid var(--line);
    border-left: 2px solid var(--blue);
    border-radius: 6px;
    padding: 14px 16px;
    margin-bottom: 10px;
}
.doc-card.flagged { border-left-color: var(--red); }
.doc-card b { color: var(--text-hi); font-family: var(--f-display); font-weight: 600; }

mark.hl {
    background: var(--red);
    color: #fff;
    padding: 0 3px;
    border-radius: 3px;
    font-weight: 600;
}

/* ============ TOOLTIPS ============ */
div[data-baseweb="tooltip"] {
    background: var(--surface-2) !important;
    color: var(--text-hi) !important;
    border: 1px solid var(--line) !important;
    font-family: var(--f-mono) !important;
    font-size: 0.78rem !important;
}

hr { border-color: var(--line) !important; }
</style>
"""


def inject_custom_css(st):
    """Call once near the top of app.py: inject_custom_css(st)"""
    st.markdown(FONT_IMPORT, unsafe_allow_html=True)
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
