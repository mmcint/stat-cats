import streamlit as st

st.set_page_config(
    page_title="Stat Cats",
    page_icon="🐾",
    layout="wide",
    initial_sidebar_state="collapsed",
)

from utils import inject_css, PURPLE, GOLD, SILVER, BG, PURPLE_DARK

inject_css()

# ─── HERO ─────────────────────────────────────────────────────────────────────

st.markdown(f"""
<style>
    /* Hide default sidebar nav on home page */
    [data-testid="stSidebarNav"] {{ display: none; }}

    .hero {{
        background: linear-gradient(135deg, {PURPLE} 0%, #2d1a5e 60%, {BG} 100%);
        border-bottom: 4px solid {GOLD};
        border-radius: 12px;
        padding: 64px 48px 56px;
        text-align: center;
        position: relative;
        overflow: hidden;
        margin-bottom: 40px;
    }}
    .hero::before {{
        content: '';
        position: absolute;
        inset: 0;
        background: repeating-linear-gradient(
            45deg,
            transparent,
            transparent 40px,
            rgba(255,255,255,0.015) 40px,
            rgba(255,255,255,0.015) 80px
        );
        pointer-events: none;
    }}
    .hero-paw {{
        font-size: 72px;
        line-height: 1;
        margin-bottom: 16px;
        filter: drop-shadow(0 0 24px rgba(201,162,39,0.5));
    }}
    .hero-title {{
        font-family: 'Bebas Neue', sans-serif;
        font-size: 96px;
        letter-spacing: 8px;
        line-height: 1;
        color: #ffffff;
        text-shadow: 0 0 60px rgba(201,162,39,0.3);
        margin-bottom: 8px;
    }}
    .hero-subtitle {{
        font-family: 'Space Mono', monospace;
        font-size: 13px;
        color: rgba(255,255,255,0.5);
        letter-spacing: 4px;
        margin-bottom: 32px;
    }}
    .hero-divider {{
        width: 80px;
        height: 3px;
        background: {GOLD};
        margin: 0 auto 32px;
        border-radius: 2px;
    }}
    .hero-tagline {{
        font-family: 'Barlow Condensed', sans-serif;
        font-size: 22px;
        color: rgba(255,255,255,0.75);
        font-weight: 300;
        letter-spacing: 1px;
        max-width: 560px;
        margin: 0 auto;
    }}

    /* Sport cards */
    .sport-grid {{
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 20px;
        margin-bottom: 40px;
    }}
    .sport-card {{
        background: {PURPLE_DARK};
        border: 2px solid #2a2535;
        border-radius: 12px;
        padding: 36px 28px;
        text-align: center;
        transition: all 0.2s ease;
        cursor: pointer;
        text-decoration: none;
        display: block;
    }}
    .sport-card:hover {{
        border-color: {GOLD};
        transform: translateY(-3px);
        box-shadow: 0 12px 40px rgba(75,46,131,0.4);
    }}
    .sport-icon {{
        font-size: 52px;
        margin-bottom: 12px;
        display: block;
    }}
    .sport-name {{
        font-family: 'Bebas Neue', sans-serif;
        font-size: 36px;
        letter-spacing: 3px;
        color: #fff;
        margin-bottom: 6px;
    }}
    .sport-desc {{
        font-family: 'Space Mono', monospace;
        font-size: 10px;
        color: {SILVER};
        letter-spacing: 1px;
        line-height: 1.6;
    }}

    /* Feature pills */
    .features {{
        display: flex;
        gap: 12px;
        justify-content: center;
        flex-wrap: wrap;
        margin-bottom: 40px;
    }}
    .feature-pill {{
        background: rgba(75,46,131,0.25);
        border: 1px solid rgba(75,46,131,0.5);
        border-radius: 20px;
        padding: 8px 18px;
        font-family: 'Space Mono', monospace;
        font-size: 10px;
        color: {SILVER};
        letter-spacing: 1px;
        text-transform: uppercase;
    }}

    /* Stats strip */
    .stats-strip {{
        background: rgba(201,162,39,0.06);
        border: 1px solid rgba(201,162,39,0.2);
        border-radius: 10px;
        padding: 24px 32px;
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 16px;
        text-align: center;
        margin-bottom: 40px;
    }}
    .strip-num {{
        font-family: 'Bebas Neue', sans-serif;
        font-size: 44px;
        color: {GOLD};
        line-height: 1;
        margin-bottom: 4px;
    }}
    .strip-label {{
        font-family: 'Space Mono', monospace;
        font-size: 9px;
        color: {SILVER};
        letter-spacing: 2px;
        text-transform: uppercase;
    }}

    /* Data sources */
    .data-sources {{
        background: {PURPLE_DARK};
        border-radius: 10px;
        padding: 20px 24px;
        display: flex;
        gap: 24px;
        align-items: center;
        justify-content: center;
        margin-bottom: 24px;
    }}
    .ds-label {{
        font-family: 'Space Mono', monospace;
        font-size: 9px;
        color: #444;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-right: 8px;
    }}
    .ds-item {{
        font-family: 'Space Mono', monospace;
        font-size: 10px;
        color: {SILVER};
        letter-spacing: 1px;
    }}
    .ds-dot {{
        color: {GOLD};
        font-size: 8px;
    }}
</style>
""", unsafe_allow_html=True)

# ── Hero section ──

st.markdown("""
<div class="hero">
    <div class="hero-paw">🐾</div>
    <div class="hero-title">STAT CATS</div>
    <div class="hero-subtitle">K-STATE WILDCATS · ANALYTICS DASHBOARD</div>
    <div class="hero-divider"></div>
    <div class="hero-tagline">
        Compare players and teams across every era of Wildcat history —
        from Bill Snyder's rebuild to today.
    </div>
</div>
""", unsafe_allow_html=True)

# ── Feature pills ──

st.markdown("""
<div class="features">
    <div class="feature-pill">📡 Live API Data</div>
    <div class="feature-pill">🕰️ Era-to-Era Comparison</div>
    <div class="feature-pill">📊 Radar Charts</div>
    <div class="feature-pill">🏆 Team Season Analysis</div>
    <div class="feature-pill">📈 Multi-Season Trends</div>
</div>
""", unsafe_allow_html=True)

# ── Sport cards — use st.page_link for navigation ──

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="sport-card" style="border-color: rgba(75,46,131,0.6);">
        <span class="sport-icon">🏈</span>
        <div class="sport-name">FOOTBALL</div>
        <div class="sport-desc">
            PLAYER COMPARISONS · TEAM SEASONS<br>
            RADAR ANALYSIS · TREND LINES<br>
            DATA VIA COLLEGEFOOTBALLDATA.COM
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.page_link("pages/1_🏈_Football.py", label="Open Football Dashboard →", use_container_width=True)

with col2:
    st.markdown("""
    <div class="sport-card" style="border-color: rgba(75,46,131,0.6);">
        <span class="sport-icon">🏀</span>
        <div class="sport-name">BASKETBALL</div>
        <div class="sport-desc">
            PLAYER COMPARISONS · TEAM SEASONS<br>
            RADAR ANALYSIS · TREND LINES<br>
            DATA VIA COLLEGEBASKETBALLDATA.COM
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.page_link("pages/2_🏀_Basketball.py", label="Open Basketball Dashboard →", use_container_width=True)

# ── K-State by the numbers ──

st.markdown("""
<div class="stats-strip">
    <div>
        <div class="strip-num">16</div>
        <div class="strip-label">Big 12 / Big 8<br>Championships</div>
    </div>
    <div>
        <div class="strip-num">215+</div>
        <div class="strip-label">Football<br>Seasons Available</div>
    </div>
    <div>
        <div class="strip-num">4</div>
        <div class="strip-label">Elite 8<br>Basketball Runs</div>
    </div>
    <div>
        <div class="strip-num">1863</div>
        <div class="strip-label">K-State<br>Founded</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Data sources strip ──

st.markdown("""
<div class="data-sources">
    <span class="ds-label">Data Sources</span>
    <span class="ds-item">CollegeFootballData.com</span>
    <span class="ds-dot">◆</span>
    <span class="ds-item">CollegeBasketballData.com</span>
    <span class="ds-dot">◆</span>
    <span class="ds-item">Live API · Updated Each Season</span>
</div>
""", unsafe_allow_html=True)

# ── Footer ──

st.markdown("""
<div style="font-family:'Space Mono',monospace;font-size:10px;color:#333;text-align:center;letter-spacing:1px;padding-top:8px;">
    K-STATE WILDCATS · STAT CATS · MANHATTAN, KS
</div>
""", unsafe_allow_html=True)
