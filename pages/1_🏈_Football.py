import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Stat Cats · Football", page_icon="🏈", layout="wide")

from utils import (
    inject_css, page_header, page_footer, PLAYER_COLORS,
    get_fb_roster, get_fb_player_stats, get_fb_team_season,
    build_fb_radar_values, radar_chart, bar_comparison,
    FB_RADAR_CATS, GOLD, SILVER, PURPLE_DARK,
)

inject_css()
page_header("🏈 FOOTBALL", "K-STATE WILDCATS · PLAYER & TEAM COMPARISONS")

# ─── SIDEBAR ──────────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown('<div class="section-label">📅 Seasons</div>', unsafe_allow_html=True)
    years = list(range(2024, 1988, -1))
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
            roster_a = get_fb_roster(season_a)
            stats_a = get_fb_player_stats(season_a)
        if roster_a.empty:
            st.warning(f"No roster data for {season_a}. Check your CFBD API key.")
            players_a = []
        else:
            names_a = sorted(roster_a["name"].dropna().unique().tolist())
            players_a = st.multiselect(f"Players ({season_a})", names_a, max_selections=4, key="fb_pa")

    with col_b:
        st.markdown(f'<div class="section-label">Season B · {season_b}</div>', unsafe_allow_html=True)
        with st.spinner(f"Loading {season_b} roster..."):
            roster_b = get_fb_roster(season_b)
            stats_b = get_fb_player_stats(season_b)
        if roster_b.empty:
            st.warning(f"No roster data for {season_b}.")
            players_b = []
        else:
            names_b = sorted(roster_b["name"].dropna().unique().tolist())
            players_b = st.multiselect(f"Players ({season_b})", names_b, max_selections=4, key="fb_pb")

    all_sel = [(n, season_a, roster_a, stats_a) for n in players_a] + \
              [(n, season_b, roster_b, stats_b) for n in players_b]

    if not all_sel:
        st.info("👆 Select players from one or both seasons to begin comparing.")
    else:
        st.markdown("---")
        radar_data = []

        for i, (name, season, roster, stats_full) in enumerate(all_sel):
            player_row = roster[roster["name"] == name]
            pos_col = next((c for c in ["position","pos"] if c in roster.columns), None)
            position = player_row.iloc[0][pos_col].upper() if (pos_col and not player_row.empty) else "DEFAULT"
            pos_key = position[:2]
            cats = FB_RADAR_CATS.get(pos_key, FB_RADAR_CATS["DEFAULT"])
            color = PLAYER_COLORS[i % len(PLAYER_COLORS)]

            p_stats = stats_full[stats_full.get("player", pd.Series(dtype=str)) == name] \
                if not stats_full.empty and "player" in stats_full.columns else pd.DataFrame()
            vals = build_fb_radar_values(p_stats, position, cats)
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
            st.plotly_chart(radar_chart(unified, "PLAYER RADAR — K-STATE FOOTBALL"), use_container_width=True)
            st.plotly_chart(bar_comparison(unified, "RAW STAT COMPARISON"), use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# TEAMS
# ══════════════════════════════════════════════════════════════════════════════

with tab_teams:
    st.markdown('<div class="section-label">Select Seasons</div>', unsafe_allow_html=True)
    all_years = list(range(2024, 1988, -1))
    sel_years = st.multiselect("Add seasons", all_years, default=[2024, 2022, 2012, 2003, 1998], max_selections=6, key="fb_ty")

    if not sel_years:
        st.info("Select at least one season.")
    else:
        with st.spinner("Loading team data..."):
            team_data = {yr: get_fb_team_season(yr) for yr in sel_years}

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
                m1.metric("SP+ Rating", d.get("sp_overall", "—"))
                m2.metric("SP+ Off", d.get("sp_offense", "—"))
                m3, m4 = st.columns(2)
                m3.metric("Conf W", d.get("conf_wins", "—"))
                m4.metric("Conf L", d.get("conf_losses", "—"))

        st.markdown("---")
        st.markdown('<div class="section-label">📡 Team Radar</div>', unsafe_allow_html=True)
        team_cats = {"SP+ Off": 45, "SP+ Def": 35, "Conf Wins": 8, "Total Wins": 13}
        team_radar = []
        for i, yr in enumerate(sorted(sel_years, reverse=True)):
            d = team_data[yr]
            vals = {"SP+ Off": d.get("sp_offense",0), "SP+ Def": d.get("sp_defense",0),
                    "Conf Wins": d.get("conf_wins",0), "Total Wins": d.get("wins",0)}
            team_radar.append((str(yr), vals, team_cats, PLAYER_COLORS[i % len(PLAYER_COLORS)]))
        st.plotly_chart(radar_chart(team_radar, "TEAM RADAR — K-STATE FOOTBALL"), use_container_width=True)

        st.markdown("---")
        st.markdown('<div class="section-label">📈 Trend</div>', unsafe_allow_html=True)
        metric = st.selectbox("Metric", ["SP+ Overall","SP+ Offense","SP+ Defense","Total Wins","Conf Wins"], key="fb_trend")
        mmap = {"SP+ Overall":"sp_overall","SP+ Offense":"sp_offense","SP+ Defense":"sp_defense","Total Wins":"wins","Conf Wins":"conf_wins"}
        sorted_yrs = sorted(sel_years)
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=[str(y) for y in sorted_yrs],
            y=[team_data[y].get(mmap[metric], 0) for y in sorted_yrs],
            mode="lines+markers",
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
