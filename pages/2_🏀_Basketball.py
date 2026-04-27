import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Stat Cats · Basketball", page_icon="🏀", layout="wide")

from utils import (
    inject_css, page_header, page_footer, PLAYER_COLORS,
    get_bb_roster, get_bb_player_stats, get_bb_team_season,
    build_bb_radar_values, radar_chart, bar_comparison,
    BB_RADAR_CATS, GOLD, SILVER, PURPLE_DARK,
)

inject_css()
page_header("🏀 BASKETBALL", "K-STATE WILDCATS · PLAYER & TEAM COMPARISONS")

# ─── SIDEBAR ──────────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown('<div class="section-label">📅 Seasons</div>', unsafe_allow_html=True)
    years = list(range(2025, 1990, -1))
    season_a = st.selectbox("Season A", years, index=0)
    season_b = st.selectbox("Season B", years, index=2)
    st.markdown("---")
    st.page_link("Home.py", label="← Back to Home")

# ─── TABS ─────────────────────────────────────────────────────────────────────

tab_players, tab_teams = st.tabs(["PLAYER COMPARISONS", "TEAM COMPARISONS"])

# ══════════════════════════════════════════════════════════════════════════════
# PLAYERS
# ══════════════════════════════════════════════════════════════════════════════

with tab_players:
    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown(f'<div class="section-label">Season A · {season_a}</div>', unsafe_allow_html=True)
        with st.spinner(f"Loading {season_a} roster..."):
            roster_a = get_bb_roster(season_a)
            stats_a = get_bb_player_stats(season_a)
        if roster_a.empty:
            st.warning(f"No roster data for {season_a}. Check your CBBD API key.")
            players_a = []
        else:
            name_col_a = "name" if "name" in roster_a.columns else roster_a.columns[0]
            names_a = sorted(roster_a[name_col_a].dropna().unique().tolist())
            players_a = st.multiselect(f"Players ({season_a})", names_a, max_selections=4, key="bb_pa")

    with col_b:
        st.markdown(f'<div class="section-label">Season B · {season_b}</div>', unsafe_allow_html=True)
        with st.spinner(f"Loading {season_b} roster..."):
            roster_b = get_bb_roster(season_b)
            stats_b = get_bb_player_stats(season_b)
        if roster_b.empty:
            st.warning(f"No roster data for {season_b}.")
            players_b = []
        else:
            name_col_b = "name" if "name" in roster_b.columns else roster_b.columns[0]
            names_b = sorted(roster_b[name_col_b].dropna().unique().tolist())
            players_b = st.multiselect(f"Players ({season_b})", names_b, max_selections=4, key="bb_pb")

    all_sel = [(n, season_a, roster_a, stats_a) for n in players_a] + \
              [(n, season_b, roster_b, stats_b) for n in players_b]

    if not all_sel:
        st.info("👆 Select players from one or both seasons to begin comparing.")
    else:
        st.markdown("---")
        radar_data = []

        for i, (name, season, roster, stats_full) in enumerate(all_sel):
            name_col = "name" if "name" in roster.columns else roster.columns[0]
            player_row = roster[roster[name_col] == name]
            pos_col = next((c for c in ["position","pos"] if c in roster.columns), None)
            position = player_row.iloc[0][pos_col].upper() if (pos_col and not player_row.empty) else "DEFAULT"
            pos_key = position[0] if position else "DEFAULT"
            cats = BB_RADAR_CATS.get(pos_key, BB_RADAR_CATS["DEFAULT"])
            color = PLAYER_COLORS[i % len(PLAYER_COLORS)]

            stats_dict = {}
            if not stats_full.empty:
                name_field = next((c for c in ["name","playerName","player"] if c in stats_full.columns), None)
                if name_field:
                    p_row = stats_full[stats_full[name_field] == name]
                    stats_dict = p_row.iloc[0].to_dict() if not p_row.empty else {}

            vals = build_bb_radar_values(stats_dict, position, cats)
            radar_data.append((f"{name} ({season})", vals, cats, color))

            st.markdown(f"""
            <div class="player-card" style="border-left-color:{color};">
                <div class="player-name" style="color:{color};">{name}</div>
                <div class="player-meta">{position} · {season} SEASON</div>
            </div>
            """, unsafe_allow_html=True)
            metric_cols = st.columns(len(cats))
            for j, (cat, _) in enumerate(cats.items()):
                with metric_cols[j]:
                    st.metric(cat, f"{vals.get(cat, 0):.1f}")

        if radar_data:
            st.markdown("---")
            st.markdown('<div class="section-label">📡 Radar Comparison</div>', unsafe_allow_html=True)
            all_cats = sorted(set(c for _, v, _, _ in radar_data for c in v))
            unified = [(n, {c: v.get(c,0) for c in all_cats}, {c: mx.get(c,100) for c in all_cats}, col)
                       for n, v, mx, col in radar_data]
            st.plotly_chart(radar_chart(unified, "PLAYER RADAR — K-STATE BASKETBALL"), use_container_width=True)
            st.plotly_chart(bar_comparison(unified, "RAW STAT COMPARISON"), use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# TEAMS
# ══════════════════════════════════════════════════════════════════════════════

with tab_teams:
    st.markdown('<div class="section-label">Select Seasons</div>', unsafe_allow_html=True)
    all_years = list(range(2025, 1990, -1))
    sel_years = st.multiselect("Add seasons", all_years, default=[2025, 2023, 2018, 2010, 1988], max_selections=6, key="bb_ty")

    if not sel_years:
        st.info("Select at least one season.")
    else:
        with st.spinner("Loading team data..."):
            team_data = {yr: get_bb_team_season(yr) for yr in sel_years}

        cols = st.columns(min(len(sel_years), 3))
        for i, yr in enumerate(sorted(sel_years, reverse=True)):
            d = team_data[yr]
            color = PLAYER_COLORS[i % len(PLAYER_COLORS)]
            with cols[i % 3]:
                st.markdown(f"""
                <div class="player-card" style="border-left-color:{color};">
                    <div class="player-name" style="color:{color};">{yr}</div>
                    <div class="player-meta">Record: {d.get('record','N/A')}</div>
                </div>
                """, unsafe_allow_html=True)
                m1, m2 = st.columns(2)
                m1.metric("PPG", d.get("ppg","—"))
                m2.metric("Opp PPG", d.get("opp_ppg","—"))
                m3, m4 = st.columns(2)
                m3.metric("FG%", d.get("fg_pct","—"))
                m4.metric("Wins", d.get("wins","—"))

        st.markdown("---")
        st.markdown('<div class="section-label">📡 Team Radar</div>', unsafe_allow_html=True)
        team_cats = {"PPG": 90, "Margin": 25, "FG%": 60, "Wins": 32, "Reb/G": 42}
        team_radar = []
        for i, yr in enumerate(sorted(sel_years, reverse=True)):
            d = team_data[yr]
            ppg = d.get("ppg",0)
            opp = d.get("opp_ppg",0)
            vals = {"PPG": ppg, "Margin": round(ppg - opp,1), "FG%": d.get("fg_pct",0),
                    "Wins": d.get("wins",0), "Reb/G": d.get("rebounds",0)}
            team_radar.append((str(yr), vals, team_cats, PLAYER_COLORS[i % len(PLAYER_COLORS)]))
        st.plotly_chart(radar_chart(team_radar, "TEAM RADAR — K-STATE BASKETBALL"), use_container_width=True)

        st.markdown("---")
        st.markdown('<div class="section-label">📈 Trend</div>', unsafe_allow_html=True)
        metric = st.selectbox("Metric", ["PPG","Opp PPG","FG%","Wins","Scoring Margin"], key="bb_trend")
        mmap = {"PPG":"ppg","Opp PPG":"opp_ppg","FG%":"fg_pct","Wins":"wins"}
        sorted_yrs = sorted(sel_years)
        if metric == "Scoring Margin":
            y_vals = [round(team_data[y].get("ppg",0) - team_data[y].get("opp_ppg",0), 1) for y in sorted_yrs]
        else:
            y_vals = [team_data[y].get(mmap[metric], 0) for y in sorted_yrs]

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=[str(y) for y in sorted_yrs], y=y_vals, mode="lines+markers",
            line=dict(color="#4B2E83", width=3),
            marker=dict(color=GOLD, size=10, line=dict(color="#fff", width=1)),
        ))
        fig.update_layout(
            paper_bgcolor="#0f0d14", plot_bgcolor="#1a1625",
            font=dict(family="Barlow Condensed", color="#fff"),
            xaxis=dict(gridcolor="#2a2535", tickfont=dict(family="Space Mono", size=11, color="#A7A9AC")),
            yaxis=dict(gridcolor="#2a2535", tickfont=dict(family="Space Mono", size=11, color="#A7A9AC"), title=metric),
            margin=dict(t=20, b=40), height=320,
        )
        st.plotly_chart(fig, use_container_width=True)

page_footer()
