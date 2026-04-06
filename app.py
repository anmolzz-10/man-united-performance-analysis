"""
Manchester United 2024-25 | Why We Missed the Top 4
Premium narrative-driven analytics product
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

# ─── PAGE CONFIG ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Man United | Top 4 Diagnosis",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── GLOBAL CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500;600&display=swap');

/* ── Reset & base ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #0a0a0f;
    color: #e8e6df;
}

/* ── Streamlit chrome ── */
.stApp { background: #0a0a0f; }
header[data-testid="stHeader"] { background: transparent; }
.block-container { padding: 0 !important; max-width: 100% !important; }

/* ── Section wrapper ── */
.section {
    padding: 80px 10vw;
    border-bottom: 1px solid rgba(255,255,255,0.06);
}

/* ── Section label ── */
.section-label {
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #DA291C;
    margin-bottom: 10px;
}

/* ── Display type ── */
.display-heading {
    font-family: 'DM Serif Display', serif;
    font-size: clamp(32px, 4vw, 56px);
    font-weight: 400;
    color: #f5f3ed;
    line-height: 1.12;
    margin-bottom: 18px;
}
.display-heading em {
    font-style: italic;
    color: #DA291C;
}

/* ── Body copy ── */
.body-copy {
    font-size: 17px;
    line-height: 1.75;
    color: #a8a49c;
    max-width: 640px;
    margin-bottom: 0;
}

/* ── Insight callout ── */
.insight-callout {
    border-left: 3px solid #DA291C;
    padding: 14px 20px;
    background: rgba(218, 41, 28, 0.07);
    border-radius: 0 8px 8px 0;
    margin: 28px 0;
    font-size: 15px;
    line-height: 1.6;
    color: #c9c5bc;
    font-style: italic;
}

/* ── Stat cards ── */
.stat-grid {
    display: grid;
    gap: 14px;
    margin: 36px 0;
}
.stat-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 12px;
    padding: 22px 24px;
    transition: border-color 0.2s;
}
.stat-card:hover { border-color: rgba(218,41,28,0.4); }
.stat-label {
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #6b6760;
    margin-bottom: 8px;
}
.stat-value {
    font-size: 36px;
    font-weight: 300;
    color: #f5f3ed;
    letter-spacing: -0.02em;
    line-height: 1;
}
.stat-subtext {
    font-size: 12px;
    color: #6b6760;
    margin-top: 4px;
}
.stat-value.danger { color: #DA291C; }
.stat-value.warn   { color: #f59e0b; }
.stat-value.ok     { color: #22c55e; }

/* ── Diagnosis grid ── */
.diag-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px;
    margin: 32px 0;
}
.diag-card {
    border-radius: 12px;
    padding: 24px;
    border: 1px solid rgba(255,255,255,0.08);
}
.diag-card.primary   { background: rgba(218,41,28,0.1);  border-color: rgba(218,41,28,0.3); }
.diag-card.secondary { background: rgba(59,130,246,0.1); border-color: rgba(59,130,246,0.3); }
.diag-title {
    font-size: 13px;
    font-weight: 600;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    margin-bottom: 10px;
}
.diag-card.primary   .diag-title { color: #DA291C; }
.diag-card.secondary .diag-title { color: #3b82f6; }
.diag-number {
    font-family: 'DM Serif Display', serif;
    font-size: 44px;
    font-weight: 400;
    line-height: 1;
    margin-bottom: 4px;
}
.diag-card.primary   .diag-number { color: #ef4444; }
.diag-card.secondary .diag-number { color: #60a5fa; }
.diag-desc {
    font-size: 13px;
    color: #7a7670;
    line-height: 1.5;
}

/* ── Hero band ── */
.hero-band {
    padding: 100px 10vw 80px;
    border-bottom: 1px solid rgba(255,255,255,0.06);
    position: relative;
    overflow: hidden;
}
.hero-band::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    background: radial-gradient(ellipse 60% 60% at 80% 40%, rgba(218,41,28,0.08), transparent);
    pointer-events: none;
}
.hero-eyebrow {
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #DA291C;
    margin-bottom: 20px;
}
.hero-title {
    font-family: 'DM Serif Display', serif;
    font-size: clamp(40px, 6vw, 80px);
    font-weight: 400;
    color: #f5f3ed;
    line-height: 1.05;
    margin-bottom: 24px;
}
.hero-subtitle {
    font-size: 18px;
    color: #7a7670;
    line-height: 1.6;
    max-width: 560px;
    margin-bottom: 48px;
}
.hero-badges {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
}
.hero-badge {
    font-size: 12px;
    font-weight: 500;
    color: #a8a49c;
    padding: 6px 14px;
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 20px;
    letter-spacing: 0.04em;
}

/* ── Section divider ── */
.section-divider {
    width: 40px;
    height: 2px;
    background: #DA291C;
    margin: 20px 0 32px;
}

/* ── Player table ── */
.player-table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 16px;
}
.player-table th {
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #6b6760;
    padding: 10px 0;
    border-bottom: 1px solid rgba(255,255,255,0.08);
    text-align: left;
}
.player-table td {
    padding: 12px 0;
    border-bottom: 1px solid rgba(255,255,255,0.04);
    font-size: 14px;
    color: #c9c5bc;
}
.player-table td.name { color: #f5f3ed; font-weight: 500; }
.player-table td.neg  { color: #ef4444; }
.player-table td.pos  { color: #22c55e; }
.bar-cell {
    display: flex;
    align-items: center;
    gap: 8px;
}
.bar-track {
    flex: 1;
    height: 4px;
    background: rgba(255,255,255,0.06);
    border-radius: 2px;
    overflow: hidden;
}
.bar-fill-red  { height: 4px; background: #DA291C; border-radius: 2px; }
.bar-fill-blue { height: 4px; background: #3b82f6; border-radius: 2px; }

/* ── Simulation controls ── */
.sim-label {
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #6b6760;
    margin-bottom: 6px;
}
.sim-result-card {
    border-radius: 16px;
    padding: 32px;
    border: 1px solid rgba(255,255,255,0.08);
    background: rgba(255,255,255,0.03);
    text-align: center;
}
.sim-projected-pts {
    font-family: 'DM Serif Display', serif;
    font-size: 72px;
    font-weight: 400;
    line-height: 1;
    margin-bottom: 8px;
}
.sim-verdict {
    font-size: 14px;
    font-weight: 500;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    padding: 6px 16px;
    border-radius: 20px;
    display: inline-block;
    margin-bottom: 20px;
}
.verdict-no   { background: rgba(218,41,28,0.15); color: #ef4444; }
.verdict-maybe { background: rgba(245,158,11,0.15); color: #f59e0b; }
.verdict-yes  { background: rgba(34,197,94,0.15);  color: #22c55e; }

/* ── Final section ── */
.diagnosis-pills {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    margin-top: 24px;
}
.pill {
    font-size: 13px;
    font-weight: 500;
    padding: 8px 18px;
    border-radius: 24px;
    border: 1px solid;
}
.pill-red  { border-color: rgba(218,41,28,0.4);  color: #ef4444; background: rgba(218,41,28,0.08); }
.pill-blue { border-color: rgba(59,130,246,0.4); color: #60a5fa; background: rgba(59,130,246,0.08); }
.pill-gray { border-color: rgba(255,255,255,0.1); color: #7a7670; background: rgba(255,255,255,0.03); }

/* ── Plotly override ── */
.js-plotly-plot .plotly .nsewdrag { cursor: default !important; }
</style>
""", unsafe_allow_html=True)

# ─── DATA ──────────────────────────────────────────────────────────────────────
TEAMS_2024 = {
    "Liverpool":         {"rank": 1, "pts": 84,  "xG": 93.24, "xGA": 42.32, "xPTS": 81.84, "xG_pm": 2.454, "xGA_pm": 1.114},
    "Arsenal":           {"rank": 2, "pts": 74,  "xG": 73.57, "xGA": 39.98, "xPTS": 72.96, "xG_pm": 1.936, "xGA_pm": 1.052},
    "Manchester City":   {"rank": 3, "pts": 71,  "xG": 73.15, "xGA": 52.90, "xPTS": 64.66, "xG_pm": 1.925, "xGA_pm": 1.392},
    "Chelsea":           {"rank": 4, "pts": 69,  "xG": 73.12, "xGA": 54.26, "xPTS": 62.56, "xG_pm": 1.924, "xGA_pm": 1.428},
    "Newcastle United":  {"rank": 5, "pts": 66,  "xG": 71.48, "xGA": 53.98, "xPTS": 62.61, "xG_pm": 1.881, "xGA_pm": 1.421},
    "Manchester United": {"rank": 15,"pts": 42,  "xG": 56.91, "xGA": 60.73, "xPTS": 52.24, "xG_pm": 1.498, "xGA_pm": 1.598},
}

BENCHMARK = {"xG_pm": 2.060, "xGA_pm": 1.246, "pts": 74.5}
MAN_UTD   = TEAMS_2024["Manchester United"]

GAP_XG  = MAN_UTD["xG_pm"]  - BENCHMARK["xG_pm"]   # –0.562
GAP_XGA = MAN_UTD["xGA_pm"] - BENCHMARK["xGA_pm"]   # +0.352

COEF_XG  =  26.57
COEF_XGA = -22.63
INTERCEPT = 46.36

PTS_LOSS_XG  = GAP_XG  * COEF_XG   # ≈ –14.94
PTS_LOSS_XGA = GAP_XGA * COEF_XGA  # ≈ –7.96
TOTAL_LOSS   = PTS_LOSS_XG + PTS_LOSS_XGA  # ≈ –22.9

PLAYERS = [
    {"player": "Bruno Fernandes",    "mins": 3034, "goals": 8,  "assists": 10, "gc": 18, "xG": 9.89, "fin_diff": -1.89, "gc90": 0.534},
    {"player": "Amad Diallo",        "mins": 1887, "goals": 8,  "assists": 6,  "gc": 14, "xG": 4.75, "fin_diff":  3.25, "gc90": 0.668},
    {"player": "Marcus Rashford",    "mins": 1435, "goals": 6,  "assists": 3,  "gc":  9, "xG": 4.99, "fin_diff":  1.01, "gc90": 0.564},
    {"player": "Alejandro Garnacho", "mins": 2176, "goals": 6,  "assists": 2,  "gc":  8, "xG": 9.44, "fin_diff": -3.44, "gc90": 0.331},
    {"player": "Rasmus Højlund",     "mins": 2032, "goals": 4,  "assists": 0,  "gc":  4, "xG": 5.87, "fin_diff": -1.87, "gc90": 0.177},
    {"player": "Joshua Zirkzee",     "mins": 1378, "goals": 3,  "assists": 1,  "gc":  4, "xG": 5.22, "fin_diff": -2.22, "gc90": 0.261},
    {"player": "Diogo Dalot",        "mins": 2821, "goals": 0,  "assists": 3,  "gc":  3, "xG": 1.70, "fin_diff": -1.70, "gc90": 0.096},
    {"player": "Lisandro Martínez",  "mins": 1762, "goals": 2,  "assists": 1,  "gc":  3, "xG": 1.69, "fin_diff":  0.31, "gc90": 0.153},
    {"player": "Manuel Ugarte",      "mins": 1802, "goals": 1,  "assists": 2,  "gc":  3, "xG": 1.09, "fin_diff": -0.09, "gc90": 0.150},
    {"player": "Christian Eriksen",  "mins": 1043, "goals": 1,  "assists": 2,  "gc":  3, "xG": 1.33, "fin_diff": -0.33, "gc90": 0.259},
]

THEME = {
    "attack":    "#DA291C",
    "defense":   "#3b82f6",
    "benchmark": "#a8a49c",
    "surface":   "rgba(255,255,255,0.03)",
    "border":    "rgba(255,255,255,0.08)",
    "text":      "#f5f3ed",
    "muted":     "#6b6760",
    "bg":        "#0a0a0f",
    "bg2":       "#111116",
}

CHART_LAYOUT = dict(
    plot_bgcolor  = "rgba(0,0,0,0)",
    paper_bgcolor = "rgba(0,0,0,0)",
    font          = dict(family="DM Sans", color="#a8a49c", size=12),
    margin        = dict(l=0, r=0, t=16, b=0),
    showlegend    = False,
    hoverlabel    = dict(bgcolor="#1a1a22", font_color="#f5f3ed", font_size=13, bordercolor="rgba(255,255,255,0.1)"),
)


# ─── HELPERS ───────────────────────────────────────────────────────────────────
def section(html): st.markdown(f'<div class="section">{html}</div>', unsafe_allow_html=True)
def raw(html):     st.markdown(html, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# HERO
# ═══════════════════════════════════════════════════════════════════════════════
raw("""
<div class="hero-band">
    <div class="hero-eyebrow">Manchester United · 2024–25 Premier League · Post-Season Analysis</div>
    <h1 class="hero-title">Why Manchester United<br>missed the Top 4</h1>
    <p class="hero-subtitle">
        A data-led diagnosis of the 32-point gap between Manchester United
        and a Champions League place — built on xG, xGA, player efficiency,
        and a regression model that explains 70% of the underperformance.
    </p>
    <div class="hero-badges">
        <span class="hero-badge">xG / xGA Analysis</span>
        <span class="hero-badge">Player Contribution</span>
        <span class="hero-badge">Finishing Efficiency</span>
        <span class="hero-badge">Regression Model</span>
        <span class="hero-badge">Interactive Simulation</span>
    </div>
</div>
""")


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 1 — BENCHMARK
# ═══════════════════════════════════════════════════════════════════════════════
raw('<div class="section">')
raw("""
<div class="section-label">01 — The Standard</div>
<h2 class="display-heading">What does a Top 4 team<br>actually look like?</h2>
<div class="section-divider"></div>
<p class="body-copy">
    Before diagnosing failure, we need to define success.
    The 2024–25 Top 4 — Liverpool, Arsenal, Manchester City, Chelsea —
    averaged <strong style="color:#f5f3ed">2.06 xG per match</strong> attacking
    and conceded just <strong style="color:#f5f3ed">1.25 xGA</strong> defensively.
    That translated to <strong style="color:#f5f3ed">74.5 points</strong> — the entry ticket.
</p>
""")

raw('<div class="insight-callout">'
    '"An elite attack can compensate for a leaky defense. City and Chelsea both '
    'conceded 1.39–1.43 xGA per game — yet still finished Top 4. '
    'Attack is the primary driver of qualification."'
    '</div>')

# Benchmark quadrant scatter
teams_df = pd.DataFrame([
    {"team": k, **v} for k, v in TEAMS_2024.items()
])

fig_bench = go.Figure()

# background quadrant shading
fig_bench.add_shape(type="rect", x0=1.4, x1=2.6, y0=0.8, y1=1.26,
    fillcolor="rgba(34,197,94,0.04)", line_color="rgba(34,197,94,0.08)")
fig_bench.add_annotation(x=2.53, y=0.83, text="TOP 4 ZONE", showarrow=False,
    font=dict(size=9, color="rgba(34,197,94,0.5)", family="DM Sans"), xanchor="right")

# benchmark crosshairs
fig_bench.add_shape(type="line", x0=BENCHMARK["xG_pm"], x1=BENCHMARK["xG_pm"],
    y0=0.8, y1=1.9, line=dict(color="rgba(168,164,156,0.25)", dash="dot", width=1))
fig_bench.add_shape(type="line", x0=1.3, x1=2.6, y0=BENCHMARK["xGA_pm"], y1=BENCHMARK["xGA_pm"],
    line=dict(color="rgba(168,164,156,0.25)", dash="dot", width=1))
fig_bench.add_annotation(x=BENCHMARK["xG_pm"]+0.02, y=1.86, text="Top 4 avg xG",
    showarrow=False, font=dict(size=10, color="rgba(168,164,156,0.5)", family="DM Sans"), xanchor="left")
fig_bench.add_annotation(x=1.32, y=BENCHMARK["xGA_pm"]-0.03, text="Top 4 avg xGA",
    showarrow=False, font=dict(size=10, color="rgba(168,164,156,0.5)", family="DM Sans"), xanchor="left")

# teams
for _, row in teams_df.iterrows():
    is_utd = row["team"] == "Manchester United"
    color  = THEME["attack"] if is_utd else (THEME["benchmark"] if row["rank"] <= 4 else "rgba(168,164,156,0.3)")
    size   = 14 if is_utd else (10 if row["rank"] <= 4 else 7)
    label  = "Man Utd" if is_utd else (row["team"] if row["rank"] <= 5 else "")

    fig_bench.add_trace(go.Scatter(
        x=[row["xG_pm"]], y=[row["xGA_pm"]],
        mode="markers+text",
        marker=dict(size=size, color=color, line=dict(width=1, color="rgba(255,255,255,0.2)")),
        text=[label],
        textposition="top right" if not is_utd else "bottom left",
        textfont=dict(size=11, color=color, family="DM Sans"),
        hovertemplate=(
            f"<b>{row['team']}</b><br>"
            f"xG/match: {row['xG_pm']:.2f}<br>"
            f"xGA/match: {row['xGA_pm']:.2f}<br>"
            f"Points: {row['pts']}<extra></extra>"
        ),
    ))

fig_bench.update_xaxes(
    title="xG per match (attack →)", title_font=dict(size=11, color=THEME["muted"]),
    range=[1.3, 2.6], showgrid=True, gridcolor="rgba(255,255,255,0.04)",
    zeroline=False, tickfont=dict(size=10), tickcolor=THEME["muted"],
    linecolor="rgba(255,255,255,0.08)",
)
fig_bench.update_yaxes(
    title="xGA per match (← better defense)", title_font=dict(size=11, color=THEME["muted"]),
    range=[0.8, 1.9], autorange="reversed", showgrid=True,
    gridcolor="rgba(255,255,255,0.04)", zeroline=False,
    tickfont=dict(size=10), tickcolor=THEME["muted"],
    linecolor="rgba(255,255,255,0.08)",
)
fig_bench.update_layout(**CHART_LAYOUT, height=400)

st.plotly_chart(fig_bench, use_container_width=True, config={"displayModeBar": False})
raw('</div>')  # /section


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 2 — THE GAP
# ═══════════════════════════════════════════════════════════════════════════════
raw('<div class="section">')
raw("""
<div class="section-label">02 — The Gap</div>
<h2 class="display-heading">United were <em>structurally</em><br>off the pace</h2>
<div class="section-divider"></div>
<p class="body-copy">
    Strip away results, form runs, injuries. When you look at the underlying
    data, United underperformed the Top 4 benchmark on <em>both</em> sides of the ball —
    but attack was the bigger problem by a wide margin.
</p>
""")

raw("""
<div class="diag-grid">
    <div class="diag-card primary">
        <div class="diag-title">⚡ Attack deficit</div>
        <div class="diag-number">−0.56</div>
        <div style="font-size:13px; color:#DA291C; margin-bottom:8px;">xG per match below benchmark</div>
        <div class="diag-desc">Creating 27% fewer expected goals than the Top 4 average. Fewer shots, lower-quality chances, or both.</div>
    </div>
    <div class="diag-card secondary">
        <div class="diag-title">🛡 Defense gap</div>
        <div class="diag-number">+0.35</div>
        <div style="font-size:13px; color:#3b82f6; margin-bottom:8px;">xGA per match above benchmark</div>
        <div class="diag-desc">Conceding higher-quality chances than the top teams — but the structural exposure is smaller than the attacking hole.</div>
    </div>
</div>
""")

# Horizontal gap bar chart
categories   = ["xG per match", "xGA per match"]
utd_vals     = [MAN_UTD["xG_pm"], MAN_UTD["xGA_pm"]]
bench_vals   = [BENCHMARK["xG_pm"], BENCHMARK["xGA_pm"]]

fig_gap = go.Figure()

fig_gap.add_trace(go.Bar(
    name="Top 4 Benchmark", x=bench_vals, y=categories,
    orientation="h",
    marker=dict(color=THEME["benchmark"], opacity=0.35),
    hovertemplate="%{y}: %{x:.2f}<extra>Benchmark</extra>",
    width=0.35,
))
fig_gap.add_trace(go.Bar(
    name="Manchester United", x=utd_vals, y=categories,
    orientation="h",
    marker_color=[THEME["attack"], THEME["defense"]],
    hovertemplate="%{y}: %{x:.2f}<extra>Man Utd</extra>",
    width=0.35,
))

# Gap annotations
for i, (u, b, cat) in enumerate(zip(utd_vals, bench_vals, categories)):
    diff = u - b
    sign = "+" if diff > 0 else ""
    color = THEME["defense"] if diff > 0 and i == 1 else THEME["attack"]
    fig_gap.add_annotation(
        x=max(u, b)+0.04, y=cat,
        text=f"{sign}{diff:.2f}",
        showarrow=False,
        font=dict(size=12, color=color, family="DM Sans"),
        xanchor="left",
    )

fig_gap.update_xaxes(range=[0, 2.9], showgrid=True, gridcolor="rgba(255,255,255,0.04)",
    zeroline=False, tickfont=dict(size=11), linecolor="rgba(255,255,255,0.08)")
fig_gap.update_yaxes(tickfont=dict(size=12))
gap_layout = {**CHART_LAYOUT, "showlegend": True}
fig_gap.update_layout(
    **gap_layout, barmode="group", height=200,
    legend=dict(orientation="h", x=0, y=-0.3, font=dict(size=11)),
)
st.plotly_chart(fig_gap, use_container_width=True, config={"displayModeBar": False})
raw('</div>')


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 3 — IMPACT (MODEL)
# ═══════════════════════════════════════════════════════════════════════════════
raw('<div class="section">')
raw("""
<div class="section-label">03 — Quantifying the Cost</div>
<h2 class="display-heading">How many points did each<br>gap actually cost?</h2>
<div class="section-divider"></div>
<p class="body-copy">
    A linear regression across all 20 PL clubs quantifies the marginal value
    of attacking and defensive performance. Every +0.1 xG per match adds 2.66 points.
    Every −0.1 xGA conceded adds 2.26 points. Applied to United's gap, the model
    explains the majority of the 32.5-point deficit.
</p>
""")

raw('<div class="insight-callout">'
    '"United\'s attacking shortfall cost an estimated 15 points — nearly double '
    'the 8 points lost through defensive exposure. Attack is not just a problem; '
    'it is <em>the</em> problem."'
    '</div>')

# Waterfall chart
labels    = ["Benchmark points (Top 4 avg)", "Attack penalty (low xG)", "Defense penalty (high xGA)", "Projected points"]
values    = [BENCHMARK["pts"], PTS_LOSS_XG, PTS_LOSS_XGA, 0]
cumulative = [BENCHMARK["pts"], BENCHMARK["pts"] + PTS_LOSS_XG,
              BENCHMARK["pts"] + PTS_LOSS_XG + PTS_LOSS_XGA, 0]
projected  = round(BENCHMARK["pts"] + TOTAL_LOSS, 1)

colors_wf = [THEME["benchmark"], THEME["attack"], THEME["defense"], THEME["benchmark"]]
opacities  = [0.7, 1.0, 1.0, 0.4]

fig_wf = go.Figure(go.Waterfall(
    name="Points", orientation="v",
    measure=["absolute", "relative", "relative", "total"],
    x=labels,
    y=[BENCHMARK["pts"], PTS_LOSS_XG, PTS_LOSS_XGA, 0],
    text=[f"{BENCHMARK['pts']:.0f}", f"{PTS_LOSS_XG:.1f}", f"{PTS_LOSS_XGA:.1f}", f"{projected:.0f}"],
    textposition="outside",
    textfont=dict(size=12, color="#f5f3ed"),
    connector=dict(line=dict(color="rgba(255,255,255,0.08)", width=1, dash="dot")),
    decreasing=dict(marker=dict(color=THEME["attack"])),
    increasing=dict(marker=dict(color=THEME["defense"])),
    totals=dict(marker=dict(color="rgba(168,164,156,0.3)", line=dict(color=THEME["benchmark"], width=1.5))),
))

fig_wf.update_xaxes(tickfont=dict(size=11), linecolor="rgba(255,255,255,0.08)")
fig_wf.update_yaxes(range=[30, 90], showgrid=True, gridcolor="rgba(255,255,255,0.04)",
    zeroline=False, tickfont=dict(size=11))
fig_wf.add_hline(y=MAN_UTD["pts"], line_dash="dot",
    line_color=THEME["attack"], line_width=1, opacity=0.6,
    annotation_text=f"Actual: {MAN_UTD['pts']} pts",
    annotation_font=dict(size=11, color=THEME["attack"]))
fig_wf.update_layout(**CHART_LAYOUT, height=360)
st.plotly_chart(fig_wf, use_container_width=True, config={"displayModeBar": False})
raw('</div>')


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 4 — VALIDATION (Performance vs Expectation)
# ═══════════════════════════════════════════════════════════════════════════════
raw('<div class="section">')
raw("""
<div class="section-label">04 — The Hidden Layer</div>
<h2 class="display-heading">The model doesn't explain<br>everything — and that matters</h2>
<div class="section-divider"></div>
<p class="body-copy">
    The structural model accounts for 22.9 of the 32.5-point gap. 
    The remaining ~10 points come from <em>execution</em> — how well the team
    converted the chances they created, and how results aligned with underlying performance.
</p>
""")

col1, col2, col3 = st.columns(3)

with col1:
    raw("""
    <div class="stat-card">
        <div class="stat-label">Goals vs xG</div>
        <div class="stat-value danger">−12.9</div>
        <div class="stat-subtext">goals below expectation · poor finishing</div>
    </div>""")

with col2:
    raw("""
    <div class="stat-card">
        <div class="stat-label">GA vs xGA</div>
        <div class="stat-value ok">−6.7</div>
        <div class="stat-subtext">goals conceded below expectation · strong goalkeeping</div>
    </div>""")

with col3:
    raw("""
    <div class="stat-card">
        <div class="stat-label">Points vs xPTS</div>
        <div class="stat-value warn">−10.2</div>
        <div class="stat-subtext">points below model expectation</div>
    </div>""")

raw("""
<div style="margin-top:32px;">
    <p class="body-copy">
        The <span style="color:#22c55e">defensive execution is genuinely strong</span> — 
        Onana and the backline conceded 6.7 fewer goals than expected. 
        But the attack wasted its opportunities. 
        United generated chances worth 56.9 goals — and scored just 44.
        That 12.9-goal gap is an execution crisis on top of a structural one.
    </p>
</div>
""")

# Variance breakdown bar
fig_var = go.Figure()
items   = ["Structural: Attack", "Structural: Defense", "Efficiency: Finishing", "Efficiency: Points"]
values_ = [abs(PTS_LOSS_XG), abs(PTS_LOSS_XGA), 10.2, 10.2]
colors_ = [THEME["attack"], THEME["defense"], "rgba(218,41,28,0.5)", "rgba(245,158,11,0.6)"]
labels_ = [f"−{abs(PTS_LOSS_XG):.1f} pts", f"−{abs(PTS_LOSS_XGA):.1f} pts", "−10.2 pts", "~70%/30% split"]

fig_var.add_trace(go.Bar(
    x=items, y=values_,
    marker_color=colors_,
    text=[f"{v:.1f}" for v in values_],
    textposition="outside",
    textfont=dict(size=12, color="#f5f3ed"),
    hovertemplate="%{x}: %{y:.1f} pts<extra></extra>",
    width=0.55,
))
fig_var.update_xaxes(tickfont=dict(size=11), linecolor="rgba(255,255,255,0.08)")
fig_var.update_yaxes(range=[0, 20], showgrid=True, gridcolor="rgba(255,255,255,0.04)",
    zeroline=False, tickfont=dict(size=11), title="Points impact",
    title_font=dict(size=11, color=THEME["muted"]))
fig_var.update_layout(**CHART_LAYOUT, height=280)
st.plotly_chart(fig_var, use_container_width=True, config={"displayModeBar": False})
raw('</div>')


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 5 — PLAYER CAUSE
# ═══════════════════════════════════════════════════════════════════════════════
raw('<div class="section">')
raw("""
<div class="section-label">05 — Inside the Squad</div>
<h2 class="display-heading">The attack relies on<br>too few players</h2>
<div class="section-divider"></div>
<p class="body-copy">
    We know attack is the primary problem. Now we need to know <em>why</em>.
    The squad data reveals a concentration problem — 65% of all goal contributions
    came from just four players. Crucially, the designated striker delivered at
    less than a third of their xG rate.
</p>
""")

# Player contribution chart (sorted horizontal bars)
df_players = pd.DataFrame(PLAYERS)
df_top     = df_players.sort_values("gc", ascending=True).tail(8)

fig_players = go.Figure()
colors_p = [THEME["attack"] if r == "Bruno Fernandes" else
            ("rgba(218,41,28,0.6)" if r in ["Amad Diallo", "Marcus Rashford", "Alejandro Garnacho"]
             else "rgba(168,164,156,0.25)") for r in df_top["player"]]

fig_players.add_trace(go.Bar(
    x=df_top["gc"], y=df_top["player"],
    orientation="h",
    marker_color=colors_p,
    text=df_top["gc"].astype(str),
    textposition="outside",
    textfont=dict(size=11, color="#a8a49c"),
    hovertemplate="%{y}<br>Goal contributions: %{x}<extra></extra>",
    width=0.6,
))
fig_players.add_vline(x=10, line_dash="dot", line_color="rgba(255,255,255,0.1)", line_width=1)
fig_players.update_xaxes(range=[0, 25], showgrid=True, gridcolor="rgba(255,255,255,0.04)",
    zeroline=False, tickfont=dict(size=11), title="Goal contributions (G+A)",
    title_font=dict(size=11, color=THEME["muted"]))
fig_players.update_yaxes(tickfont=dict(size=11))
fig_players.update_layout(**CHART_LAYOUT, height=320)
st.plotly_chart(fig_players, use_container_width=True, config={"displayModeBar": False})

# Finishing efficiency table
raw("<h3 style='font-size:15px; font-weight:500; color:#f5f3ed; margin: 32px 0 16px;'>Finishing efficiency — goals vs expectation</h3>")
raw("<p class='body-copy' style='margin-bottom:16px; font-size:14px;'>Positive = overperforming xG. Negative = goals left behind.</p>")

rows_html = ""
max_xg = max(p["xG"] for p in PLAYERS)
for p in sorted(PLAYERS, key=lambda x: x["fin_diff"]):
    diff  = p["fin_diff"]
    color = "#ef4444" if diff < 0 else "#22c55e"
    sign  = "+" if diff >= 0 else ""
    bar_w = int(abs(p["xG"]) / max_xg * 100)
    bar_color = THEME["attack"] if diff < 0 else "#22c55e"
    rows_html += f"""
    <tr>
        <td class="name">{p['player']}</td>
        <td>{p['goals']}</td>
        <td style="color:#a8a49c">{p['xG']:.2f}</td>
        <td class="{'neg' if diff < 0 else 'pos'}">{sign}{diff:.2f}</td>
        <td>
            <div class="bar-cell">
                <div class="bar-track"><div class="{'bar-fill-red' if diff < 0 else 'bar-fill-blue'}" style="width:{bar_w}%"></div></div>
            </div>
        </td>
    </tr>"""

raw(f"""
<table class="player-table">
    <thead><tr>
        <th>Player</th><th>Goals</th><th>xG</th><th>Diff</th><th>Efficiency</th>
    </tr></thead>
    <tbody>{rows_html}</tbody>
</table>
""")
raw('</div>')


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 6 — DIAGNOSIS
# ═══════════════════════════════════════════════════════════════════════════════
raw('<div class="section">')
raw("""
<div class="section-label">06 — The Verdict</div>
<h2 class="display-heading">Three problems.<br>One root cause.</h2>
<div class="section-divider"></div>
<p class="body-copy">
    Bringing all stages together, United's 32.5-point deficit has a clear
    structure: a dominant structural attacking failure, amplified by poor
    finishing efficiency, cushioned only by surprisingly strong defensive execution.
</p>
""")

col_a, col_b = st.columns([2, 1], gap="large")

with col_a:
    # Donut: 70/30 structure vs variance
    fig_donut = go.Figure(go.Pie(
        values=[22.9, 10.2],
        labels=["Structural (xG / xGA gap)", "Efficiency (finishing / results)"],
        hole=0.65,
        marker=dict(colors=[THEME["attack"], "rgba(245,158,11,0.7)"],
                    line=dict(color=THEME["bg"], width=3)),
        textfont=dict(size=11, color="#f5f3ed"),
        hovertemplate="%{label}<br>%{value:.1f} pts<extra></extra>",
    ))
    fig_donut.add_annotation(text="32.5 pts<br>explained",
        showarrow=False, font=dict(size=13, color="#a8a49c", family="DM Sans"),
        x=0.5, y=0.5)
    fig_donut.update_layout(**CHART_LAYOUT, height=280,
        legend=dict(orientation="h", x=-0.05, y=-0.12, font=dict(size=11)))
    fig_donut.update_traces(showlegend=True)
    st.plotly_chart(fig_donut, use_container_width=True, config={"displayModeBar": False})

with col_b:
    raw("""
    <div style="padding-top:12px;">
    <div class="stat-card" style="margin-bottom:12px;">
        <div class="stat-label">Structural loss</div>
        <div class="stat-value danger" style="font-size:28px;">−22.9 pts</div>
        <div class="stat-subtext">70% of the deficit · xG + xGA gap</div>
    </div>
    <div class="stat-card" style="margin-bottom:12px;">
        <div class="stat-label">Efficiency loss</div>
        <div class="stat-value warn" style="font-size:28px;">−10.2 pts</div>
        <div class="stat-subtext">30% of the deficit · poor finishing</div>
    </div>
    <div class="stat-card">
        <div class="stat-label">Actual deficit</div>
        <div class="stat-value danger" style="font-size:28px;">−32.5 pts</div>
        <div class="stat-subtext">vs Top 4 threshold (74.5 pts)</div>
    </div>
    </div>
    """)

raw("""
<div style="margin-top:36px;">
    <p class="body-copy" style="margin-bottom:18px;">Root causes, in order of impact:</p>
    <div class="diagnosis-pills">
        <span class="pill pill-red">Weak chance creation (−15 pts)</span>
        <span class="pill pill-red">Poor finishing (−13 goals wasted)</span>
        <span class="pill pill-blue">Defensive exposure (−8 pts)</span>
        <span class="pill pill-gray">Concentration in top contributors</span>
        <span class="pill pill-gray">Højlund / Garnacho xG underperformance</span>
        <span class="pill pill-gray">Dalot 0 goals from 1.70 xG</span>
    </div>
</div>
""")
raw('</div>')


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 7 — SIMULATION
# ═══════════════════════════════════════════════════════════════════════════════
raw('<div class="section">')
raw("""
<div class="section-label">07 — What Would It Take?</div>
<h2 class="display-heading">Simulate the path<br>back to Top 4</h2>
<div class="section-divider"></div>
<p class="body-copy">
    The model gives us a decision-support tool. Drag the sliders to project
    how improving attack or defense would translate into points — and whether
    it's enough to reach the 69-point threshold for a Top 4 finish.
</p>
""")

col_sl1, col_sl2 = st.columns(2)
with col_sl1:
    raw('<div class="sim-label">⚡ Attack improvement — xG per match</div>')
    delta_xg = st.slider("Improve xG per match", min_value=0.0, max_value=0.80, value=0.20, step=0.05,
                          format="+%.2f", label_visibility="collapsed")

with col_sl2:
    raw('<div class="sim-label">Defense improvement &mdash; reduce xGA per match</div>')
    delta_xga = st.slider("Reduce xGA per match", min_value=0.0, max_value=0.60, value=0.15, step=0.05,
                           format="-%0.2f", label_visibility="collapsed")

new_xg  = MAN_UTD["xG_pm"]  + delta_xg
new_xga = MAN_UTD["xGA_pm"] - delta_xga
pts_gain_xg  = delta_xg  * COEF_XG
pts_gain_xga = delta_xga * abs(COEF_XGA)
projected_pts = round(MAN_UTD["pts"] + pts_gain_xg + pts_gain_xga)

top4_threshold = 69
if projected_pts >= 74:
    verdict, verdict_class, verdict_text = "TOP 4 ACHIEVED", "verdict-yes", "Projected to finish in the Top 4"
elif projected_pts >= 69:
    verdict, verdict_class, verdict_text = "BORDERLINE", "verdict-maybe", "On the margin — needs everything to go right"
else:
    verdict, verdict_class, verdict_text = "STILL SHORT", "verdict-no", f"Would need {69 - projected_pts}+ more points to challenge"

pts_color = "#22c55e" if projected_pts >= 74 else ("#f59e0b" if projected_pts >= 69 else "#ef4444")

raw(f"""
<div class="sim-result-card">
    <div class="sim-projected-pts" style="color:{pts_color}">{projected_pts}</div>
    <div style="font-size:13px; color:#6b6760; margin-bottom:10px;">projected points</div>
    <div class="sim-verdict {verdict_class}">{verdict}</div>
    <div style="font-size:13px; color:#7a7670;">{verdict_text}</div>
</div>
""")

# Simulation breakdown chart
sim_labels = ["Current", f"+{delta_xg:.2f} xG", f"−{delta_xga:.2f} xGA", "Projected"]
sim_vals   = [MAN_UTD["pts"], pts_gain_xg, pts_gain_xga, 0]

fig_sim = go.Figure(go.Waterfall(
    orientation="v",
    measure=["absolute", "relative", "relative", "total"],
    x=sim_labels,
    y=sim_vals,
    text=[f"{MAN_UTD['pts']}", f"+{pts_gain_xg:.1f}", f"+{pts_gain_xga:.1f}", f"{projected_pts}"],
    textposition="outside",
    textfont=dict(size=12, color="#f5f3ed"),
    connector=dict(line=dict(color="rgba(255,255,255,0.06)", width=1, dash="dot")),
    decreasing=dict(marker=dict(color=THEME["attack"])),
    increasing=dict(marker=dict(color="#22c55e")),
    totals=dict(marker=dict(color=pts_color)),
))

fig_sim.add_hline(y=69, line_dash="dot", line_color="rgba(245,158,11,0.5)",
    annotation_text="Top 4 minimum (69 pts)", annotation_font=dict(size=10, color="rgba(245,158,11,0.7)"))
fig_sim.add_hline(y=74.5, line_dash="dot", line_color="rgba(168,164,156,0.4)",
    annotation_text="Top 4 avg (74.5 pts)", annotation_font=dict(size=10, color="rgba(168,164,156,0.6)"))

fig_sim.update_xaxes(tickfont=dict(size=12), linecolor="rgba(255,255,255,0.08)")
fig_sim.update_yaxes(range=[30, 90], showgrid=True, gridcolor="rgba(255,255,255,0.04)",
    zeroline=False, tickfont=dict(size=11))
fig_sim.update_layout(**CHART_LAYOUT, height=320)
st.plotly_chart(fig_sim, use_container_width=True, config={"displayModeBar": False})
raw('</div>')


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 8 — CONCLUSION
# ═══════════════════════════════════════════════════════════════════════════════
raw('<div class="section">')
raw("""
<div class="section-label">08 — What Needs to Change</div>
<h2 class="display-heading">The diagnosis is clear.<br>The fix is attacking.</h2>
<div class="section-divider"></div>
<p class="body-copy">
    Defensive structure is not the priority — United over-performed their xGA by 6.7 goals.
    The investment case is entirely on the attacking side: a prolific striker
    (Højlund returned 4 goals from 5.87 xG), a consistent wide creator, and squad
    depth that reduces the over-reliance on Bruno Fernandes.
</p>
<div class="insight-callout">
    "Attack is the lever. A +0.3 xG improvement per match alone projects United
    to 50 points. Add defensive consolidation of −0.2 xGA and the model reaches
    59 points — still short, but within range of a strong-form run. Only a combined
    structural overhaul gets United back to 69+."
</div>
""")

col_r1, col_r2, col_r3 = st.columns(3)

with col_r1:
    raw("""
    <div class="stat-card">
        <div class="stat-label">Priority 1</div>
        <div style="font-size:16px; font-weight:500; color:#f5f3ed; margin:8px 0;">Prolific striker</div>
        <div class="stat-subtext">Højlund scored 4 goals from 5.87 xG. 
        A top-9 converting at xG-rate adds ~8 goals and 5+ points per season.</div>
    </div>""")

with col_r2:
    raw("""
    <div class="stat-card">
        <div class="stat-label">Priority 2</div>
        <div style="font-size:16px; font-weight:500; color:#f5f3ed; margin:8px 0;">Wide creator depth</div>
        <div class="stat-subtext">Garnacho wasted 3.44 xG. A consistent
        wide threat adds volume — the team created the chances, they just weren't converted.</div>
    </div>""")

with col_r3:
    raw("""
    <div class="stat-card">
        <div class="stat-label">Priority 3</div>
        <div style="font-size:16px; font-weight:500; color:#f5f3ed; margin:8px 0;">Reduce dependency on #8</div>
        <div class="stat-subtext">Bruno Fernandes alone contributed 18 goal actions.
        One injury or dip in form removes 37% of total goal involvement.</div>
    </div>""")

raw('</div>')

# ─── FOOTER ────────────────────────────────────────────────────────────────────
raw("""
<div style="padding:40px 10vw; border-top:1px solid rgba(255,255,255,0.06); 
     display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:16px;">
    <div>
        <div style="font-size:13px; font-weight:600; color:#f5f3ed; margin-bottom:4px;">Manchester United · 2024–25 Diagnosis</div>
        <div style="font-size:12px; color:#4a4845;">Data: FBref / Understat · Model: Linear Regression (R²~0.85) · Season: 2024–25 PL</div>
    </div>
    <div style="font-size:12px; color:#4a4845;">Built with Streamlit + Plotly</div>
</div>
""")