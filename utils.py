import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import requests
from typing import Optional

# ─── BRAND ────────────────────────────────────────────────────────────────────

PURPLE      = "#4B2E83"
PURPLE_DARK = "#1a1625"
GOLD        = "#C9A227"
SILVER      = "#A7A9AC"
BG          = "#0f0d14"
PLAYER_COLORS = ["#C9A227", "#7ec8e3", "#e07070", "#a8e6a8"]

# ─── GLOBAL CSS ───────────────────────────────────────────────────────────────

GLOBAL_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Barlow+Condensed:wght@300;400;600;700&family=Space+Mono:wght@400;700&display=swap');

    html, body, [class*="css"] { font-family: 'Barlow Condensed', sans-serif; }

    .stApp { background-color: #0f0d14; color: #ffffff; }

    [data-testid="stSidebar"] {
        background-color: #1a1625;
        border-right: 2px solid #4B2E83;
    }
    [data-testid="stSidebar"] * { color: #e0e0e0 !important; }

    [data-testid="metric-container"] {
        background: #1a1625;
        border: 1px solid #2a2535;
        border-radius: 8px;
        padding: 12px;
    }
    [data-testid="metric-container"] label {
        color: #A7A9AC !important;
        font-family: 'Space Mono', monospace !important;
        font-size: 10px !important;
        letter-spacing: 1px !important;
    }
    [data-testid="metric-container"] [data-testid="stMetricValue"] {
        color: #ffffff !important;
        font-family: 'Bebas Neue', sans-serif !important;
        font-size: 28px !important;
    }

    [data-testid="stTabs"] button {
        font-family: 'Bebas Neue', sans-serif !important;
        font-size: 20px !important;
        letter-spacing: 2px !important;
        color: #666 !important;
    }
    [data-testid="stTabs"] button[aria-selected="true"] {
        color: #C9A227 !important;
        border-bottom: 3px solid #C9A227 !important;
    }

    [data-testid="stSelectbox"] label,
    [data-testid="stMultiSelect"] label,
    [data-testid="stSlider"] label {
        font-family: 'Space Mono', monospace !important;
        font-size: 11px !important;
        letter-spacing: 1px !important;
        color: #A7A9AC !important;
        text-transform: uppercase;
    }

    .section-label {
        font-family: 'Space Mono', monospace;
        font-size: 11px;
        letter-spacing: 2px;
        color: #A7A9AC;
        text-transform: uppercase;
        margin-bottom: 8px;
        border-bottom: 1px solid #2a2535;
        padding-bottom: 6px;
    }

    .player-card {
        background: #1a1625;
        border-radius: 8px;
        padding: 14px;
        border-left: 4px solid #4B2E83;
        margin-bottom: 10px;
    }
    .player-name {
        font-family: 'Bebas Neue', sans-serif;
        font-size: 22px;
        letter-spacing: 1px;
        color: #C9A227;
    }
    .player-meta {
        font-family: 'Space Mono', monospace;
        font-size: 11px;
        color: #A7A9AC;
    }

    hr { border-color: #2a2535 !important; }

    .footer {
        font-family: 'Space Mono', monospace;
        font-size: 10px;
        color: #333;
        text-align: center;
        margin-top: 40px;
        padding-top: 16px;
        border-top: 1px solid #1a1625;
        letter-spacing: 1px;
    }

    ::-webkit-scrollbar { width: 4px; }
    ::-webkit-scrollbar-track { background: #1a1625; }
    ::-webkit-scrollbar-thumb { background: #4B2E83; border-radius: 2px; }
</style>
"""

def inject_css():
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

def page_footer():
    st.markdown("""
    <div class="footer">
        K-STATE WILDCATS · STAT CATS · MANHATTAN, KS · DATA VIA COLLEGEFOOTBALLDATA.COM & COLLEGEBASKETBALLDATA.COM
    </div>
    """, unsafe_allow_html=True)

def page_header(title: str, subtitle: str = ""):
    st.markdown(f"""
    <div style="background:#4B2E83;border-bottom:3px solid #C9A227;padding:18px 28px;border-radius:8px;margin-bottom:24px;">
        <div style="font-family:'Bebas Neue',sans-serif;font-size:42px;letter-spacing:3px;line-height:1;color:#fff;">{title}</div>
        {f'<div style="font-family:Space Mono,monospace;font-size:11px;color:rgba(255,255,255,0.55);letter-spacing:2px;margin-top:4px;">{subtitle}</div>' if subtitle else ''}
    </div>
    """, unsafe_allow_html=True)

# ─── API ──────────────────────────────────────────────────────────────────────

CFBD_BASE = "https://api.collegefootballdata.com"
CBBD_BASE = "https://api.collegebasketballdata.com"

def cfbd_headers():
    key = st.secrets.get("CFBD_API_KEY", "")
    return {"Authorization": f"Bearer {key}"} if key else {}

def cbbd_headers():
    key = st.secrets.get("CBBD_API_KEY", "")
    return {"Authorization": f"Bearer {key}"} if key else {}

@st.cache_data(ttl=3600, show_spinner=False)
def get_fb_roster(year: int) -> pd.DataFrame:
    try:
        r = requests.get(f"{CFBD_BASE}/roster", params={"team": "Kansas State", "year": year}, headers=cfbd_headers(), timeout=10)
        r.raise_for_status()
        data = r.json()
        if not data:
            return pd.DataFrame()
        df = pd.DataFrame(data)
        keep = ["id","first_name","last_name","position","year","jersey","height","weight","hometown"]
        df = df[[c for c in keep if c in df.columns]].copy()
        df["name"] = (df.get("first_name","") + " " + df.get("last_name","")).str.strip()
        return df
    except Exception as e:
        st.warning(f"Football roster fetch failed: {e}")
        return pd.DataFrame()

@st.cache_data(ttl=3600, show_spinner=False)
def get_fb_player_stats(year: int) -> pd.DataFrame:
    try:
        r = requests.get(f"{CFBD_BASE}/stats/player/season", params={"team": "Kansas State", "year": year, "seasonType": "regular"}, headers=cfbd_headers(), timeout=10)
        r.raise_for_status()
        data = r.json()
        return pd.DataFrame(data) if data else pd.DataFrame()
    except Exception as e:
        st.warning(f"Football stats fetch failed: {e}")
        return pd.DataFrame()

@st.cache_data(ttl=3600, show_spinner=False)
def get_fb_team_season(year: int) -> dict:
    result = {"year": year}
    try:
        r = requests.get(f"{CFBD_BASE}/records", params={"team": "Kansas State", "year": year}, headers=cfbd_headers(), timeout=10)
        r.raise_for_status()
        records = r.json()
        if records:
            rec = records[0]
            result["wins"] = rec.get("total", {}).get("wins", 0)
            result["losses"] = rec.get("total", {}).get("losses", 0)
            result["record"] = f"{result['wins']}-{result['losses']}"
            result["conf_wins"] = rec.get("conferenceGames", {}).get("wins", 0)
            result["conf_losses"] = rec.get("conferenceGames", {}).get("losses", 0)
    except Exception:
        pass
    try:
        r2 = requests.get(f"{CFBD_BASE}/ratings/sp", params={"team": "Kansas State", "year": year}, headers=cfbd_headers(), timeout=10)
        r2.raise_for_status()
        sp = r2.json()
        if sp:
            s = sp[0]
            result["sp_overall"] = round(s.get("rating", 0), 1)
            result["sp_offense"] = round(s.get("offense", {}).get("rating", 0), 1)
            result["sp_defense"] = round(s.get("defense", {}).get("rating", 0), 1)
            result["ranking"] = s.get("ranking")
    except Exception:
        pass
    return result

@st.cache_data(ttl=3600, show_spinner=False)
def get_bb_roster(year: int) -> pd.DataFrame:
    try:
        r = requests.get(f"{CBBD_BASE}/roster", params={"team": "Kansas State", "season": year}, headers=cbbd_headers(), timeout=10)
        r.raise_for_status()
        data = r.json()
        if not data:
            return pd.DataFrame()
        df = pd.DataFrame(data)
        if "name" not in df.columns and "firstName" in df.columns:
            df["name"] = (df["firstName"].fillna("") + " " + df["lastName"].fillna("")).str.strip()
        return df
    except Exception as e:
        st.warning(f"Basketball roster fetch failed: {e}")
        return pd.DataFrame()

@st.cache_data(ttl=3600, show_spinner=False)
def get_bb_player_stats(year: int) -> pd.DataFrame:
    try:
        r = requests.get(f"{CBBD_BASE}/stats/player", params={"team": "Kansas State", "season": year}, headers=cbbd_headers(), timeout=10)
        r.raise_for_status()
        data = r.json()
        return pd.DataFrame(data) if data else pd.DataFrame()
    except Exception as e:
        st.warning(f"Basketball stats fetch failed: {e}")
        return pd.DataFrame()

@st.cache_data(ttl=3600, show_spinner=False)
def get_bb_team_season(year: int) -> dict:
    result = {"year": year}
    try:
        r = requests.get(f"{CBBD_BASE}/stats/team", params={"team": "Kansas State", "season": year}, headers=cbbd_headers(), timeout=10)
        r.raise_for_status()
        data = r.json()
        if data:
            s = data[0] if isinstance(data, list) else data
            result["ppg"] = round(s.get("points", s.get("ppg", 0)), 1)
            result["opp_ppg"] = round(s.get("oppPoints", s.get("opp_ppg", 0)), 1)
            result["fg_pct"] = round(s.get("fgPct", 0) * 100 if s.get("fgPct", 0) < 1 else s.get("fgPct", 0), 1)
            result["rebounds"] = round(s.get("rebounds", 0), 1)
    except Exception:
        pass
    try:
        r2 = requests.get(f"{CBBD_BASE}/records", params={"team": "Kansas State", "season": year}, headers=cbbd_headers(), timeout=10)
        r2.raise_for_status()
        rec_data = r2.json()
        if rec_data:
            rec = rec_data[0] if isinstance(rec_data, list) else rec_data
            result["wins"] = rec.get("wins", rec.get("totalWins", 0))
            result["losses"] = rec.get("losses", rec.get("totalLosses", 0))
            result["record"] = f"{result['wins']}-{result['losses']}"
    except Exception:
        pass
    return result

# ─── CHARTS ───────────────────────────────────────────────────────────────────

FB_RADAR_CATS = {
    "QB":  {"Pass Yds": 4000, "Pass TDs": 40, "Comp %": 70,  "Rush Yds": 800,  "Rush TDs": 15},
    "RB":  {"Rush Yds": 1600, "Rush TDs": 20, "Rec Yds": 600, "YPC": 6.5,      "Rec TDs": 8},
    "WR":  {"Rec Yds": 1400, "Receptions": 90,"Rec TDs": 15,  "YPR": 18,       "Yards/G": 100},
    "LB":  {"Tackles": 120,  "TFLs": 15,      "Sacks": 8,    "INTs": 4,        "FF": 4},
    "DB":  {"Tackles": 80,   "INTs": 6,        "PBUs": 12,    "TFLs": 5,        "FF": 3},
    "DL":  {"Tackles": 60,   "Sacks": 12,      "TFLs": 18,    "FF": 4,          "QBHurries": 20},
    "DEFAULT": {"Tackles": 80,"Sacks": 8,      "TFLs": 12,    "INTs": 4,        "FF": 3},
}
BB_RADAR_CATS = {
    "G":  {"PPG": 22, "APG": 7,  "RPG": 5,  "FG%": 50, "3PT%": 42},
    "F":  {"PPG": 18, "RPG": 9,  "APG": 3,  "FG%": 56, "BPG": 2},
    "C":  {"PPG": 16, "RPG": 10, "APG": 2,  "FG%": 60, "BPG": 3},
    "DEFAULT": {"PPG": 18, "RPG": 7, "APG": 4, "FG%": 52, "BPG": 1.5},
}

def build_fb_radar_values(stats_df: pd.DataFrame, position: str, categories: dict) -> dict:
    vals = {k: 0.0 for k in categories}
    if stats_df.empty:
        return vals
    stat_map = {
        "Pass Yds": ("passing","YDS"), "Pass TDs": ("passing","TD"), "Comp %": ("passing","PCT"),
        "Rush Yds": ("rushing","YDS"), "Rush TDs": ("rushing","TD"), "YPC": ("rushing","AVG"),
        "Rec Yds": ("receiving","YDS"), "Receptions": ("receiving","REC"), "Rec TDs": ("receiving","TD"),
        "YPR": ("receiving","AVG"), "Yards/G": ("receiving","YDS/G"),
        "Tackles": ("defensive","TOT"), "TFLs": ("defensive","TFL"), "Sacks": ("defensive","SACKS"),
        "INTs": ("defensive","INT"), "FF": ("defensive","FF"), "PBUs": ("defensive","PBU"),
        "QBHurries": ("defensive","QB HUR"),
    }
    for cat in categories:
        if cat not in stat_map:
            continue
        cat_type, stat_name = stat_map[cat]
        row = stats_df[
            (stats_df.get("category", pd.Series(dtype=str)).str.lower() == cat_type) &
            (stats_df.get("statType", pd.Series(dtype=str)).str.upper() == stat_name)
        ]
        if not row.empty:
            vals[cat] = float(row.iloc[0].get("stat", 0) or 0)
    return vals

def build_bb_radar_values(stats_row: dict, position: str, categories: dict) -> dict:
    if not stats_row:
        return {k: 0.0 for k in categories}
    field_map = {
        "PPG":  ["points","ppg","pts"],
        "APG":  ["assists","apg","ast"],
        "RPG":  ["rebounds","rpg","reb","totalRebounds"],
        "FG%":  ["fgPct","fg_pct","fieldGoalPct"],
        "3PT%": ["threePct","three_pct","threePointPct"],
        "BPG":  ["blocks","bpg","blk"],
        "SPG":  ["steals","spg","stl"],
    }
    vals = {}
    for cat in categories:
        val = 0.0
        for field in field_map.get(cat, [cat.lower()]):
            if field in stats_row and stats_row[field] is not None:
                raw = float(stats_row[field])
                if "%" in cat and raw < 1:
                    raw *= 100
                val = round(raw, 1)
                break
        vals[cat] = val
    return vals

def radar_chart(players_data: list, title: str = "") -> go.Figure:
    fig = go.Figure()
    for name, vals, maxes, color in players_data:
        cats = list(vals.keys())
        normed = [min(vals[c] / max(maxes[c], 0.01), 1.0) for c in cats]
        fig.add_trace(go.Scatterpolar(
            r=normed + [normed[0]], theta=cats + [cats[0]], fill="toself",
            fillcolor=f"rgba({int(color[1:3],16)},{int(color[3:5],16)},{int(color[5:7],16)},0.12)",
            line=dict(color=color, width=2.5), name=name,
            hovertemplate="<b>%{theta}</b><extra>" + name + "</extra>",
        ))
    fig.update_layout(
        polar=dict(
            bgcolor="#1a1625",
            radialaxis=dict(visible=True, range=[0,1], showticklabels=False, gridcolor="#2a2535", linecolor="#2a2535"),
            angularaxis=dict(gridcolor="#2a2535", linecolor="#3a3545", tickfont=dict(family="Space Mono", size=11, color="#A7A9AC")),
        ),
        paper_bgcolor="#0f0d14", plot_bgcolor="#0f0d14",
        font=dict(family="Barlow Condensed", color="#fff"),
        legend=dict(font=dict(family="Bebas Neue", size=16, color="#fff"), bgcolor="rgba(0,0,0,0)"),
        title=dict(text=title, font=dict(family="Bebas Neue", size=22, color="#C9A227"), x=0.5) if title else None,
        margin=dict(t=60, b=40, l=60, r=60), height=480,
    )
    return fig

def bar_comparison(players_data: list, title: str = "") -> go.Figure:
    if not players_data:
        return go.Figure()
    all_cats = list(players_data[0][1].keys())
    fig = go.Figure()
    for name, vals, _, color in players_data:
        fig.add_trace(go.Bar(name=name, x=all_cats, y=[vals.get(c, 0) for c in all_cats], marker_color=color, opacity=0.85))
    fig.update_layout(
        barmode="group", paper_bgcolor="#0f0d14", plot_bgcolor="#1a1625",
        font=dict(family="Barlow Condensed", color="#fff"),
        legend=dict(font=dict(family="Bebas Neue", size=16, color="#fff"), bgcolor="rgba(0,0,0,0)"),
        title=dict(text=title, font=dict(family="Bebas Neue", size=22, color="#C9A227"), x=0.5) if title else None,
        xaxis=dict(gridcolor="#2a2535", tickfont=dict(family="Space Mono", size=11, color="#A7A9AC")),
        yaxis=dict(gridcolor="#2a2535", tickfont=dict(family="Space Mono", size=11, color="#A7A9AC")),
        margin=dict(t=60, b=40), height=380,
    )
    return fig
