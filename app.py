
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import math
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib
from io import BytesIO

from hx_simulator.fluids import (
    get_properties, make_custom_fluid, FLUID_TABLES, FluidProperties,
)
from hx_simulator.hx_solver import (
    FluidInput, GeometryInput, SolverResult, BaffleResult,
    solve_rating, solve_design, compute_baffles,
)
from hx_simulator.heat_transfer import FOULING_FACTORS as FF, FOULING_DESCRIPTIONS
from hx_simulator.utils import (
    epsilon_NTU_counterflow, epsilon_NTU_parallel,
)
from hx_simulator.bell_delaware import SHELL_TYPES, TEMA_FRONT, TEMA_REAR, get_tema_code
from hx_simulator.materials import MATERIAL_DB, list_materials
from hx_simulator.two_phase import (
    nusselt_condensation, shah_condensation, kern_condensation,
    rohsenow_pool_boiling, mostinski_convective_boiling, lockhart_martinelli_multiplier,
)

matplotlib.rcParams["mathtext.fontset"] = "cm"

st.set_page_config(
    page_title="HX Simulator — Industrial Heat Exchanger Design",
    page_icon="favicon.ico",
    layout="wide",
    initial_sidebar_state="expanded",
)


DARK_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root {
    --bg-primary: #0a0e17;
    --bg-secondary: #111827;
    --bg-card: rgba(17,24,39,0.7);
    --bg-card-hover: rgba(30,41,59,0.8);
    --bg-glass: rgba(255,255,255,0.03);
    --border: rgba(255,255,255,0.06);
    --border-accent: rgba(99,102,241,0.3);
    --text-primary: #f1f5f9;
    --text-secondary: #94a3b8;
    --text-muted: #64748b;
    --accent: #6366f1;
    --accent-glow: rgba(99,102,241,0.15);
    --hot: #f43f5e;
    --hot-glow: rgba(244,63,94,0.12);
    --cold: #3b82f6;
    --cold-glow: rgba(59,130,246,0.12);
    --success: #10b981;
    --warning: #f59e0b;
    --purple: #a78bfa;
    --radius: 12px;
    --radius-sm: 8px;
    --shadow: 0 4px 24px rgba(0,0,0,0.3);
    --shadow-lg: 0 8px 40px rgba(0,0,0,0.4);
}

/* ── Global ── */
.stApp, .main .block-container {
    background: var(--bg-primary) !important;
    color: var(--text-primary) !important;
    font-family: 'Inter', system-ui, sans-serif !important;
}
section[data-testid="stSidebar"] > div {
    background: var(--bg-secondary) !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] .stMarkdown p,
[data-testid="stSidebar"] .stMarkdown li,
[data-testid="stSidebar"] .stCaption,
[data-testid="stSidebar"] label {
    color: var(--text-secondary) !important;
}

/* ── Typography ── */
h1, h2, h3, h4, h5, h6, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
    color: var(--text-primary) !important;
    font-weight: 700 !important;
    letter-spacing: -0.02em !important;
}

/* ── Metric Cards (Glassmorphism) ── */
div[data-testid="stMetric"] {
    background: var(--bg-glass) !important;
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    padding: 16px 18px !important;
    transition: all 0.25s cubic-bezier(0.4,0,0.2,1) !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.2) !important;
}
div[data-testid="stMetric"]:hover {
    border-color: var(--border-accent) !important;
    box-shadow: 0 4px 20px rgba(99,102,241,0.1) !important;
    transform: translateY(-2px) !important;
}
div[data-testid="stMetricValue"] {
    font-size: 1.2rem !important;
    font-weight: 700 !important;
    color: var(--text-primary) !important;
    letter-spacing: -0.01em !important;
}
div[data-testid="stMetricLabel"] {
    font-size: 0.75rem !important;
    font-weight: 500 !important;
    color: var(--text-muted) !important;
    text-transform: uppercase !important;
    letter-spacing: 0.05em !important;
}

/* ── Badges ── */
.hx-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 0.72rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.06em;
}
.hx-hot {
    background: var(--hot-glow);
    color: var(--hot);
    border: 1px solid rgba(244,63,94,0.2);
}
.hx-cold {
    background: var(--cold-glow);
    color: var(--cold);
    border: 1px solid rgba(59,130,246,0.2);
}
.hx-ok {
    background: rgba(16,185,129,0.1);
    color: var(--success);
    border: 1px solid rgba(16,185,129,0.2);
}
.hx-warn {
    background: rgba(245,158,11,0.1);
    color: var(--warning);
    border: 1px solid rgba(245,158,11,0.2);
}
.hx-info {
    background: rgba(167,139,250,0.1);
    color: var(--purple);
    border: 1px solid rgba(167,139,250,0.2);
}

/* ── SVG Viz Box ── */
.hx-viz-box {
    background: var(--bg-glass);
    backdrop-filter: blur(12px);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 12px;
    overflow: hidden;
    box-shadow: var(--shadow);
}

/* ── Tabs ── */
button[role="tab"] {
    font-size: 0.82rem !important;
    font-weight: 500 !important;
    border-radius: var(--radius-sm) var(--radius-sm) 0 0 !important;
    padding: 8px 16px !important;
    transition: all 0.2s ease !important;
}
button[role="tab"][aria-selected="true"] {
    border-bottom: 2px solid var(--accent) !important;
    color: var(--text-primary) !important;
}

/* ── Code blocks ── */
.stCode code {
    border-radius: var(--radius-sm) !important;
    font-size: 0.8rem !important;
    background: rgba(0,0,0,0.3) !important;
    border: 1px solid var(--border) !important;
}

/* ── Dividers ── */
hr {
    border: none !important;
    border-top: 1px solid var(--border) !important;
    margin: 1rem 0 !important;
}

/* ── Alerts ── */
.stAlert {
    border-radius: var(--radius) !important;
    border: 1px solid var(--border) !important;
    backdrop-filter: blur(8px);
}

/* ── Buttons ── */
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%) !important;
    border: none !important;
    border-radius: var(--radius-sm) !important;
    font-weight: 600 !important;
    letter-spacing: 0.02em !important;
    box-shadow: 0 4px 16px rgba(99,102,241,0.3) !important;
    transition: all 0.25s ease !important;
}
.stButton > button[kind="primary"]:hover {
    box-shadow: 0 6px 24px rgba(99,102,241,0.4) !important;
    transform: translateY(-1px) !important;
}

/* ── Select boxes / Inputs ── */
.stSelectbox, .stNumberInput, .stRadio, .stToggle {
    font-size: 0.88rem !important;
}

/* ── Expander ── */
details {
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    overflow: hidden;
}
details summary {
    font-weight: 600 !important;
    color: var(--text-secondary) !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.1); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: rgba(255,255,255,0.2); }

/* ── Hero Header ── */
.hx-hero {
    background: linear-gradient(135deg, rgba(99,102,241,0.08) 0%, rgba(139,92,246,0.05) 50%, rgba(59,130,246,0.08) 100%);
    border: 1px solid var(--border-accent);
    border-radius: var(--radius);
    padding: 24px 32px;
    margin-bottom: 24px;
    position: relative;
    overflow: hidden;
}
.hx-hero::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -20%;
    width: 300px;
    height: 300px;
    background: radial-gradient(circle, rgba(99,102,241,0.08) 0%, transparent 70%);
    pointer-events: none;
}
.hx-hero h1 {
    font-size: 1.8rem !important;
    font-weight: 800 !important;
    background: linear-gradient(135deg, #f1f5f9, #94a3b8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 4px !important;
}
.hx-hero p {
    color: var(--text-muted) !important;
    font-size: 0.88rem !important;
    margin: 0 !important;
}

/* ── Section Headers ── */
.hx-section {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 16px;
    padding-bottom: 8px;
    border-bottom: 1px solid var(--border);
}
.hx-section h3 {
    margin: 0 !important;
    font-size: 1rem !important;
}

/* ── Status Pill ── */
.hx-status {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 6px 14px;
    border-radius: 20px;
    font-size: 0.78rem;
    font-weight: 600;
}
.hx-status-ok {
    background: rgba(16,185,129,0.1);
    color: var(--success);
    border: 1px solid rgba(16,185,129,0.2);
}
.hx-status-warn {
    background: rgba(245,158,11,0.1);
    color: var(--warning);
    border: 1px solid rgba(245,158,11,0.2);
}
.hx-status-err {
    background: rgba(244,63,94,0.1);
    color: var(--hot);
    border: 1px solid rgba(244,63,94,0.2);
}
</style>
"""
st.markdown(DARK_CSS, unsafe_allow_html=True)

def get_tc():
    return dict(bg="none", text="#e0e0e0", grid="#333", hot="#ff6b6b",
                cold="#42a5f5", accent="#ffa502", fill="#ffa502",
                line2="#00c853", dot="#ffffff")

def styled_fig(figsize=(7, 4)):
    tc = get_tc()
    fig, ax = plt.subplots(figsize=figsize, facecolor=tc["bg"])
    ax.set_facecolor(tc["bg"])
    ax.tick_params(colors=tc["text"])
    ax.xaxis.label.set_color(tc["text"])
    ax.yaxis.label.set_color(tc["text"])
    ax.title.set_color(tc["text"])
    for s in ax.spines.values():
        s.set_color(tc["grid"])
    return fig, ax, tc


def render_hx_svg(hx_type, arr_key, Th_in, Th_out, Tc_in, Tc_out,
                  D_i, D_o, L, N_tubes, D_shell, baffle, q, h_i, h_o,
                  dp_tube, dp_shell):
    def temp_color(T, T_lo, T_hi):
        if T_hi <= T_lo:
            return "#999"
        t = max(0.0, min(1.0, (T - T_lo) / (T_hi - T_lo)))
        r = int(66 + (255 - 66) * t)
        g = int(165 + (107 - 165) * t * 0.6)
        b = int(245 + (107 - 245) * t)
        return f"#{r:02x}{g:02x}{b:02x}"

    T_lo = min(Tc_in, Tc_out, Th_in, Th_out)
    T_hi = max(Tc_in, Tc_out, Th_in, Th_out)

    h_ic  = temp_color(Th_in, T_lo, T_hi)
    h_oc  = temp_color(Th_out, T_lo, T_hi)
    c_ic  = temp_color(Tc_in, T_lo, T_hi)
    c_oc  = temp_color(Tc_out, T_lo, T_hi)

    W, H = 820, 340
    TL, TR = 150, 670
    CY = 170
    ST, SB = CY - 75, CY + 75

    s = []
    s.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
             f'style="max-width:100%;height:auto;font-family:system-ui,sans-serif;">')

    # Dark theme SVG colors
    svg_text_dim = "#999"
    svg_shell_stroke = "#888"
    svg_baffle_stroke = "#666"
    svg_arrow_color = "white"
    svg_title_color = "#ccc"
    svg_box_fill = "rgba(0,0,0,0.35)"
    svg_box_text = "#ddd"
    svg_box_stroke = "rgba(255,255,255,0.1)"

    # Gradient defs
    s.append(f"""
    <defs>
      <linearGradient id="gHot" x1="0%" y1="0%" x2="100%" y2="0%">
        <stop offset="0%" stop-color="{h_ic}"/>
        <stop offset="100%" stop-color="{h_oc}"/>
      </linearGradient>
      <linearGradient id="gCold" x1="0%" y1="0%" x2="100%" y2="0%">
        <stop offset="0%" stop-color="{c_oc}"/>
        <stop offset="100%" stop-color="{c_ic}"/>
      </linearGradient>
      <marker id="ahHot" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto">
        <path d="M0,0 L8,3 L0,6" fill="{h_ic}" opacity="0.9"/>
      </marker>
      <marker id="ahCold" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto">
        <path d="M0,0 L8,3 L0,6" fill="{c_ic}" opacity="0.9"/>
      </marker>
    </defs>
    """)

    # Shell body
    s.append(f'<rect x="{TL-5}" y="{ST-5}" width="{TR-TL+10}" height="{SB-ST+10}" '
             f'rx="14" fill="none" stroke="{svg_shell_stroke}" stroke-width="2.5" opacity="0.7"/>')

    # Tube(s)
    if hx_type == "Shell-and-tube" and N_tubes > 1:
        n_show = min(N_tubes, 7)
        gap = (SB - ST - 20) / max(n_show - 1, 1)
        for i in range(n_show):
            ty = ST + 10 + i * gap
            s.append(f'<line x1="{TL}" y1="{ty}" x2="{TR}" y2="{ty}" '
                     f'stroke="url(#gHot)" stroke-width="4" stroke-linecap="round" opacity="0.85"/>')
            s.append(f'<line x1="{TL}" y1="{ty}" x2="{TR}" y2="{ty}" '
                     f'stroke="url(#gHot)" stroke-width="1.5" stroke-dasharray="8,12" opacity="0.5"/>')
    else:
        s.append(f'<line x1="{TL}" y1="{CY}" x2="{TR}" y2="{CY}" '
                 f'stroke="url(#gHot)" stroke-width="6" stroke-linecap="round"/>')
        s.append(f'<line x1="{TL}" y1="{CY}" x2="{TR}" y2="{CY}" '
                 f'stroke="url(#gHot)" stroke-width="2" stroke-dasharray="10,14" opacity="0.6"/>')

    # Flow arrows on tube
    s.append(f'<line x1="{TL+30}" y1="{CY}" x2="{TR-30}" y2="{CY}" '
             f'stroke="{svg_arrow_color}" stroke-width="1.5" stroke-dasharray="6,8" opacity="0.4" '
             f'marker-end="url(#ahHot)"/>')

    # Baffles
    if baffle and hx_type == "Shell-and-tube":
        n_b = min(baffle.N_baffles, 20)
        baffle_spacing_px = (TR - TL) / (n_b + 1)
        for i in range(1, n_b + 1):
            bx = TL + i * baffle_spacing_px
            cut = baffle.cut_pct / 100.0
            btop = ST + (SB - ST) * cut * 0.5
            bbot = SB - (SB - ST) * cut * 0.5
            s.append(f'<line x1="{bx}" y1="{btop}" x2="{bx}" y2="{bbot}" '
                     f'stroke="{svg_baffle_stroke}" stroke-width="2" opacity="0.5" stroke-dasharray="4,3"/>')

    # Shell-side flow (cold) — U-turn arrows
    arrow_y_top = ST + 15
    arrow_y_bot = SB - 15
    if arr_key == "counter":
        s.append(f'<line x1="{TR+5}" y1="{CY+25}" x2="{TL-5}" y2="{CY+25}" '
                 f'stroke="{c_ic}" stroke-width="2" stroke-dasharray="7,5" opacity="0.6" '
                 f'marker-end="url(#ahCold)"/>')
        s.append(f'<line x1="{TL-5}" y1="{CY-25}" x2="{TR+5}" y2="{CY-25}" '
                 f'stroke="{c_oc}" stroke-width="2" stroke-dasharray="7,5" opacity="0.6"/>')
    else:
        s.append(f'<line x1="{TL-5}" y1="{CY+25}" x2="{TR+5}" y2="{CY+25}" '
                 f'stroke="{c_ic}" stroke-width="2" stroke-dasharray="7,5" opacity="0.6" '
                 f'marker-end="url(#ahCold)"/>')
        s.append(f'<line x1="{TR+5}" y1="{CY-25}" x2="{TL-5}" y2="{CY-25}" '
                 f'stroke="{c_oc}" stroke-width="2" stroke-dasharray="7,5" opacity="0.6"/>')

    # Inlet / Outlet labels
    fs = 11
    # Hot in (left)
    s.append(f'<text x="{TL-8}" y="{CY-3}" text-anchor="end" font-size="{fs}" '
             f'font-weight="600" fill="{h_ic}">{Th_in-273.15:.1f}</text>')
    s.append(f'<text x="{TL-8}" y="{CY+10}" text-anchor="end" font-size="9" fill="{svg_text_dim}">Hot In</text>')
    # Hot out (right)
    s.append(f'<text x="{TR+8}" y="{CY-3}" text-anchor="start" font-size="{fs}" '
             f'font-weight="600" fill="{h_oc}">{Th_out-273.15:.1f}</text>')
    s.append(f'<text x="{TR+8}" y="{CY+10}" text-anchor="start" font-size="9" fill="{svg_text_dim}">Hot Out</text>')
    # Cold in (right, for counter)
    if arr_key == "counter":
        s.append(f'<text x="{TR+8}" y="{CY+29}" text-anchor="start" font-size="{fs}" '
                 f'font-weight="600" fill="{c_ic}">{Tc_in-273.15:.1f}</text>')
        s.append(f'<text x="{TR+8}" y="{CY+42}" text-anchor="start" font-size="9" fill="{svg_text_dim}">Cold In</text>')
        s.append(f'<text x="{TL-8}" y="{CY+29}" text-anchor="end" font-size="{fs}" '
                 f'font-weight="600" fill="{c_oc}">{Tc_out-273.15:.1f}</text>')
        s.append(f'<text x="{TL-8}" y="{CY+42}" text-anchor="end" font-size="9" fill="{svg_text_dim}">Cold Out</text>')
    else:
        s.append(f'<text x="{TL-8}" y="{CY+29}" text-anchor="end" font-size="{fs}" '
                 f'font-weight="600" fill="{c_ic}">{Tc_in-273.15:.1f}</text>')
        s.append(f'<text x="{TL-8}" y="{CY+42}" text-anchor="end" font-size="9" fill="{svg_text_dim}">Cold In</text>')
        s.append(f'<text x="{TR+8}" y="{CY+29}" text-anchor="start" font-size="{fs}" '
                 f'font-weight="600" fill="{c_oc}">{Tc_out-273.15:.1f}</text>')
        s.append(f'<text x="{TR+8}" y="{CY+42}" text-anchor="start" font-size="9" fill="{svg_text_dim}">Cold Out</text>')

    # Title
    s.append(f'<text x="{(TL+TR)//2}" y="22" text-anchor="middle" font-size="13" '
             f'font-weight="700" fill="{svg_title_color}">{hx_type} ({arr_key}-flow)</text>')

    # Parameter box (bottom right)
    bx, by = TL + 10, SB + 20
    s.append(f'<rect x="{bx}" y="{by}" width="195" height="82" rx="6" '
             f'fill="{svg_box_fill}" stroke="{svg_box_stroke}" stroke-width="1"/>')
    info_lines = [
        f"q = {q:,.0f} W",
        f"h_i = {h_i:.0f} W/m\u00b2K",
        f"h_o = {h_o:.0f} W/m\u00b2K",
        f"\u0394P_tube = {dp_tube:.0f} Pa",
        f"\u0394P_shell = {dp_shell:.0f} Pa",
    ]
    for i, line in enumerate(info_lines):
        s.append(f'<text x="{bx+8}" y="{by+15+i*14}" font-size="10" fill="{svg_box_text}">{line}</text>')

    # Geometry box (bottom left)
    if baffle:
        gx = (TL+TR)//2 + 30
        s.append(f'<rect x="{gx}" y="{by}" width="195" height="82" rx="6" '
                 f'fill="{svg_box_fill}" stroke="{svg_box_stroke}" stroke-width="1"/>')
        g_lines = [
            f"D_i={D_i*1000:.1f}mm  D_o={D_o*1000:.1f}mm",
            f"L={L:.1f}m  N_tubes={N_tubes}",
            f"Baffles: {baffle.N_baffles} @ {baffle.spacing*1000:.0f}mm spacing",
            f"Baffle cut: {baffle.cut_pct:.0f}%",
            f"D_shell={D_shell*1000:.0f}mm",
        ]
        for i, line in enumerate(g_lines):
            s.append(f'<text x="{gx+8}" y="{by+15+i*14}" font-size="10" fill="{svg_box_text}">{line}</text>')
    else:
        gx = (TL+TR)//2 - 90
        s.append(f'<rect x="{gx}" y="{by}" width="180" height="68" rx="6" '
                 f'fill="{svg_box_fill}" stroke="{svg_box_stroke}" stroke-width="1"/>')
        g_lines = [
            f"D_i={D_i*1000:.1f}mm  D_o={D_o*1000:.1f}mm",
            f"L={L:.1f}m",
            f"k_wall = wall conductivity",
            f"Double-pipe configuration",
        ]
        for i, line in enumerate(g_lines):
            s.append(f'<text x="{gx+8}" y="{by+15+i*14}" font-size="10" fill="{svg_box_text}">{line}</text>')

    # Temperature color bar
    bar_x, bar_y, bar_w, bar_h = TR + 35, ST, 18, SB - ST
    s.append(f'<defs><linearGradient id="gBar" x1="0" y1="1" x2="0" y2="0">'
             f'<stop offset="0%" stop-color="{c_ic}"/>'
             f'<stop offset="50%" stop-color="#ffa502"/>'
             f'<stop offset="100%" stop-color="{h_ic}"/>'
             f'</linearGradient></defs>')
    s.append(f'<rect x="{bar_x}" y="{bar_y}" width="{bar_w}" height="{bar_h}" '
             f'rx="3" fill="url(#gBar)" opacity="0.8"/>')
    s.append(f'<text x="{bar_x+bar_w+4}" y="{bar_y+8}" font-size="8" fill="#999">'
             f'{T_hi-273.15:.0f}C</text>')
    s.append(f'<text x="{bar_x+bar_w+4}" y="{bar_y+bar_h}" font-size="8" fill="#999">'
             f'{T_lo-273.15:.0f}C</text>')

    # Flow animation circles
    n_dots = 8
    for i in range(n_dots):
        cx = TL + 20 + i * ((TR - TL - 40) / n_dots)
        dur = 2.5 + i * 0.3
        s.append(f'<circle cx="{cx}" cy="{CY}" r="2.5" fill="white" opacity="0.7">'
                 f'<animate attributeName="cx" from="{cx}" to="{TR}" dur="{dur}s" repeatCount="indefinite"/>'
                 f'<animate attributeName="opacity" values="0.7;0.2;0.7" dur="{dur}s" repeatCount="indefinite"/>'
                 f'</circle>')

    s.append("</svg>")
    return "\n".join(s)


def build_fluid(prefix, key_suffix):
    label = "Hot" if prefix == "hot" else "Cold"
    badge = "hx-hot" if prefix == "hot" else "hx-cold"
    st.markdown(f'<span class="hx-badge {badge}">{label} Fluid</span>', unsafe_allow_html=True)

    fluid_opts = ["water", "air", "oil", "custom"]
    c1, c2, c3 = st.columns(3)
    with c1:
        name = st.selectbox(f"{label} fluid", fluid_opts, key=f"fluid_{key_suffix}")
    with c2:
        T_inlet = st.number_input(
            f"T_inlet [K]", min_value=273.0, max_value=800.0,
            value=353.15 if prefix == "hot" else 293.15,
            step=1.0, key=f"T_{key_suffix}",
        )
    with c3:
        m_dot = st.number_input(
            f"m_dot [kg/s]", min_value=0.001, max_value=100.0,
            value=0.5, step=0.01, format="%.3f", key=f"mdot_{key_suffix}",
        )

    if name != "custom":
        props = get_properties(name, T_inlet)
        c1, c2, c3, c4, c5 = st.columns(5)
        c1.metric("rho", f"{props.rho:.1f}")
        c2.metric("mu", f"{props.mu:.4e}")
        c3.metric("Cp", f"{props.Cp:.1f}")
        c4.metric("k", f"{props.k:.4f}")
        c5.metric("Pr", f"{props.Pr:.3f}")
        return FluidInput(name=name, T_inlet=T_inlet, m_dot=m_dot)
    else:
        st.caption("Custom fluid properties:")
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            rho = st.number_input("rho [kg/m3]", value=997.0, key=f"rho_{key_suffix}")
        with c2:
            mu = st.number_input("mu [Pa.s]", value=8.55e-4, format="%.2e", key=f"mu_{key_suffix}")
        with c3:
            Cp = st.number_input("Cp [J/kgK]", value=4179.0, key=f"Cp_{key_suffix}")
        with c4:
            k = st.number_input("k [W/mK]", value=0.606, format="%.4f", key=f"k_{key_suffix}")
        return FluidInput(name="custom", T_inlet=T_inlet, m_dot=m_dot,
                          properties=make_custom_fluid(rho, mu, Cp, k),
                          rho=rho, mu=mu, Cp=Cp, k=k)


with st.sidebar:
    st.markdown("""
    <div style="padding:4px 0 8px 0;">
        <div style="font-size:1.4rem;font-weight:800;letter-spacing:-0.03em;
                     background:linear-gradient(135deg,#6366f1,#a78bfa);
                     -webkit-background-clip:text;-webkit-text-fill-color:transparent;">
            🔥 HX Simulator
        </div>
        <div style="font-size:0.78rem;color:#64748b;margin-top:2px;">
            Industrial Heat Exchanger Design Tool
        </div>
    </div>
    """, unsafe_allow_html=True)

    # How to Use button
    if st.button("📖 How to Use", use_container_width=True, key="how_to_use"):
        st.session_state.show_howto = True

    st.divider()

    mode = st.radio(
        "⚙️ Operating Mode",
        ["Rating (Analysis)", "Design (Sizing)"],
        help="Rating: given geometry → find performance. Design: given temps → find required area.",
    )
    mode_key = "rating" if "Rating" in mode else "design"

    arrangement = st.radio(
        "🔄 Flow Arrangement", ["Counter-flow", "Parallel-flow"], horizontal=True
    )
    arr_key = "counter" if "Counter" in arrangement else "parallel"

    st.divider()
    hx_type = st.radio(
        "🏗️ HX Type", ["Double-pipe", "Shell-and-tube"], horizontal=True
    )

    fouling_key = st.selectbox("🧪 Fouling Condition", list(FF.keys()), index=0)

    with st.expander("Fouling Info", expanded=False):
        for key, desc in FOULING_DESCRIPTIONS.items():
            if key == fouling_key:
                st.markdown(f"**{key}:** {desc}")
                break

    use_custom_rf = st.checkbox("Use custom fouling factors", value=False)
    custom_rfi = 0.0
    custom_rfo = 0.0
    if use_custom_rf:
        cf1, cf2 = st.columns(2)
        with cf1:
            custom_rfi = st.number_input(
                "R_f,inner (m²·K/W)",
                min_value=0.0, value=FF[fouling_key][0], format="%.6f",
                help="Inner (tube-side) fouling resistance. Typical range: 0–0.001 m²·K/W.",
            )
        with cf2:
            custom_rfo = st.number_input(
                "R_f,outer (m²·K/W)",
                min_value=0.0, value=FF[fouling_key][1], format="%.6f",
                help="Outer (shell-side) fouling resistance. Typical range: 0–0.001 m²·K/W.",
            )
        st.caption("TEMA Table RGP-T-2.4-2 typical values: seawater 1.0e-4, river water 3.0e-4, fuel oil 9.0e-4 m²·K/W.")

    st.divider()
    with st.expander("References & Sources", expanded=False):
        st.markdown("""
**Heat Transfer Correlations:**
- **Dittus-Boelter** — Nu = 0.023 Re⁰·⁸ Prⁿ
  Dittus & Boelter (1930), *Int. Comm. Heat Mass Transfer*
  [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S0735193315000553)
- **Bell-Delaware** — Shell-side h with correction factors
  Bell (1990), *Handbook of Heat Exchanger Design*, Hemisphere
- **LMTD & ε-NTU** — Incropera & DeWitt, *Fundamentals of Heat and Mass Transfer*, 7th Ed., Wiley
  [LMTD (Wikipedia)](https://en.wikipedia.org/wiki/Logarithmic_mean_temperature_difference)
- **Overall U** — 1/U = 1/h_i + R_wall + 1/h_o + R_f
  Kern & Seaton (1959), *British Chemical Engineering*

**Pressure Drop:**
- **Darcy-Weisbach** — ΔP = f·(L/D)·ρ·V²/2
  [Engineering Toolbox](https://www.engineeringtoolbox.com/darcy-weisbach-equation-d_787.html)
- **Blasius** — f = 0.316 Re⁻⁰·²⁵
  Blasius (1913), *Forsch. Ingenieurwes.* [DOI:10.1007/BF02769807](https://doi.org/10.1007/BF02769807)
- **Minor losses** — K = 2.5 (return bend), K_inlet = 0.5, K_exit = 1.0
  Kern, *Process Heat Transfer*, McGraw-Hill, 1950

**Flow-Induced Vibration (FIV):**
- **Connors criterion** — V_crit = K_c·f_n·d_o·√(m_L·δ / ρ·d_o²), K_c = 9.9
  Connors (1970), *ASME FIV Symposium*
  [ASME Digital](https://www.asmedigitalcollection.asme.org/ebooks/ebook-chapter/2723)
- **Vortex shedding** — f_vs = St·V/d_o, St ≈ 0.2
  Blevins, *Flow-Induced Vibration*, 2nd Ed., Van Nostrand, 1990
- **Acoustic resonance** — f_ac = m·c/(2·W_e)
  Eisinger (1998), *ASME J. Pressure Vessel Tech.*
  [Springer](https://link.springer.com/article/10.1007/s11319-024-01816-4)

**Two-Phase Flow:**
- **Shah condensation** — h_tp = h_l·(1 + 3.8/ε⁰·⁸⁵)
  Shah (1979), *Int. J. Heat Mass Transfer*
  [ScienceDirect](https://www.sciencedirect.com/science/article/pii/0017931079900574)
- **Rohsenow boiling** — pool boiling correlation
  Rohsenow (1952), *Trans. ASME*
  [ResearchGate](https://www.researchgate.net/publication/230007610)
- **Forster-Zuber** — nucleate boiling
  Forster & Zuber (1955), *AIChE J.*
  [DOI:10.1007/BF02769807](https://aiche.onlinelibrary.wiley.com/doi/abs/10.1002/aic.690010417)
- **Lockhart-Martinelli** — two-phase multiplier
  Lockhart & Martinelli (1949), *Chem. Eng. Progress*
  [Wikipedia](https://en.wikipedia.org/wiki/Lockhart%E2%80%93Martinelli_correlation)

**Fouling Model:**
- **Kern-Seaton** — Rf(t) = Rf*·(1 − e^(−t/τ))
  Kern & Seaton (1959), *British Chemical Engineering*
- **TEMA fouling data** — Table RGP-T-2.4-2
  TEMA Standards, 10th Ed. (2019)

**Cost Model:**
- **Lang factor** = 3.5 (shell-and-tube)
  Kern, *Process Heat Transfer*, 1950; Ulrich, *A Guide to Chemical Eng. Process Design*, 1984
- **Maintenance** = 3% CAPEX/yr
  Couper et al., *Chemical Process Equipment*, 3rd Ed., Elsevier, 2012

**Materials & Standards:**
- **ASME Section II Part D** — Material properties
  [ASME.org](https://www.asme.org/codes-standards/find-codes-standards/bpvc-section-ii-materials-part-d-properties-(metric))
- **TEMA Standards** — 10th Ed. (2019), shell types, nomenclature
  [TEMA.org](https://tema.org/standards)
  [Nomenclature PDF](http://support.tema.org/images/HeatExchangerNomenclature.pdf)
- **API RP 14E** — Nozzle erosion velocity (V = C/√ρ, C = 122)
- **ASME B16.5** — Standard nozzle/flange sizes
  [Engineering Toolbox](https://www.engineeringtoolbox.com/asme-b16-dimensions-piping-d_2985.html)

**Textbooks:**
- Incropera & DeWitt, *Fundamentals of Heat and Mass Transfer*, 7th Ed., Wiley, 2011
- Holman, *Heat Transfer*, 10th Ed., McGraw-Hill, 2010
- Kern, *Process Heat Transfer*, McGraw-Hill, 1950
- Blevins, *Flow-Induced Vibration*, 2nd Ed., Van Nostrand, 1990
- Turton et al., *Analysis, Synthesis & Design of Chemical Processes*, 4th Ed., Prentice Hall, 2012
- Peters & Timmerhaus, *Plant Design for Chemical Engineers*, 4th Ed., McGraw-Hill, 1991
""")


# ── How to Use Popup (on first load) ──
if "show_howto" not in st.session_state:
    st.session_state.show_howto = True  # show on first visit

if st.session_state.get("show_howto", False):
    HOWTO_CSS = """
    <style>
    .howto-overlay {
        position: fixed; top: 0; left: 0; right: 0; bottom: 0;
        background: rgba(0,0,0,0.6); backdrop-filter: blur(4px);
        z-index: 9998; display: flex; align-items: center; justify-content: center;
    }
    .howto-card {
        background: #111827; border: 1px solid rgba(99,102,241,0.3);
        border-radius: 16px; padding: 32px; max-width: 620px; width: 90%;
        box-shadow: 0 24px 80px rgba(0,0,0,0.5);
        font-family: 'Inter', system-ui, sans-serif; color: #f1f5f9;
    }
    .howto-card h2 { margin: 0 0 16px 0; font-size: 1.3rem; font-weight: 800;
        background: linear-gradient(135deg,#6366f1,#a78bfa);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    .howto-card ol { padding-left: 20px; line-height: 1.9; font-size: 0.88rem; color: #94a3b8; }
    .howto-card li { margin-bottom: 6px; }
    .howto-card li strong { color: #f1f5f9; }
    .howto-card .step-num {
        display: inline-flex; align-items: center; justify-content: center;
        width: 22px; height: 22px; border-radius: 50%;
        background: rgba(99,102,241,0.15); color: #a78bfa;
        font-size: 0.72rem; font-weight: 700; margin-right: 6px;
    }
    .howto-card a { color: #818cf8; text-decoration: none; }
    .howto-card a:hover { text-decoration: underline; }
    </style>
    """
    st.markdown(HOWTO_CSS, unsafe_allow_html=True)

    hx_close, hx_title = st.columns([1, 10])
    with hx_close:
        if st.button("✕", key="close_howto", help="Close"):
            st.session_state.show_howto = False
            st.rerun()
    with hx_title:
        st.markdown("")
        st.markdown("""
        <div style="padding:4px 0;">
            <h2 style="margin:0;font-size:1.3rem;font-weight:800;
                background:linear-gradient(135deg,#6366f1,#a78bfa);
                -webkit-background-clip:text;-webkit-text-fill-color:transparent;">
                📖 How to Use HX Simulator
            </h2>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div style="font-family:'Inter',system-ui,sans-serif;color:#f1f5f9;">
    <ol style="padding-left:20px;line-height:1.9;font-size:0.88rem;color:#94a3b8;">
        <li style="margin-bottom:6px;"><span style="display:inline-flex;align-items:center;justify-content:center;width:22px;height:22px;border-radius:50%;background:rgba(99,102,241,0.15);color:#a78bfa;font-size:0.72rem;font-weight:700;margin-right:6px;">1</span> <strong style="color:#f1f5f9;">Choose mode</strong> in the sidebar — <em>Rating</em> (analyze existing HX) or <em>Design</em> (size a new HX)</li>
        <li style="margin-bottom:6px;"><span style="display:inline-flex;align-items:center;justify-content:center;width:22px;height:22px;border-radius:50%;background:rgba(99,102,241,0.15);color:#a78bfa;font-size:0.72rem;font-weight:700;margin-right:6px;">2</span> <strong style="color:#f1f5f9;">Select HX type</strong> — Double-pipe or Shell-and-tube</li>
        <li style="margin-bottom:6px;"><span style="display:inline-flex;align-items:center;justify-content:center;width:22px;height:22px;border-radius:50%;background:rgba(99,102,241,0.15);color:#a78bfa;font-size:0.72rem;font-weight:700;margin-right:6px;">3</span> <strong style="color:#f1f5f9;">Set hot & cold fluids</strong> — pick from built-in fluids (water, air, oil) or define custom properties</li>
        <li style="margin-bottom:6px;"><span style="display:inline-flex;align-items:center;justify-content:center;width:22px;height:22px;border-radius:50%;background:rgba(99,102,241,0.15);color:#a78bfa;font-size:0.72rem;font-weight:700;margin-right:6px;">4</span> <strong style="color:#f1f5f9;">Enter geometry</strong> — tube diameters, length, number of tubes, baffle settings (shell-and-tube)</li>
        <li style="margin-bottom:6px;"><span style="display:inline-flex;align-items:center;justify-content:center;width:22px;height:22px;border-radius:50%;background:rgba(99,102,241,0.15);color:#a78bfa;font-size:0.72rem;font-weight:700;margin-right:6px;">5</span> <strong style="color:#f1f5f9;">Click "Run Simulation"</strong> — results appear instantly with animated HX visualization</li>
        <li style="margin-bottom:6px;"><span style="display:inline-flex;align-items:center;justify-content:center;width:22px;height:22px;border-radius:50%;background:rgba(99,102,241,0.15);color:#a78bfa;font-size:0.72rem;font-weight:700;margin-right:6px;">6</span> <strong style="color:#f1f5f9;">Explore tabs</strong> — Temperatures, Heat Transfer, Pressure Drop, FIV, Cost, Fouling, Nozzles, Charts, Export</li>
    </ol>
    <p style="font-size:0.8rem;color:#64748b;margin-top:12px;">
        Full source verification and references available in the sidebar →
        <a href="https://github.com/dadhichmohak/hxsimulator" target="_blank" style="color:#818cf8;">GitHub Repo</a>
    </p>
    </div>
    """, unsafe_allow_html=True)

# ── Hero Header ──
st.markdown("""
<div class="hx-hero">
    <h1>Heat Exchanger Simulator</h1>
    <p>Double-pipe & Shell-and-tube &nbsp;|&nbsp; Rating & Design &nbsp;|&nbsp; Bell-Delaware &nbsp;|&nbsp; FIV &nbsp;|&nbsp; Two-Phase &nbsp;|&nbsp; Cost Analysis</p>
</div>
""", unsafe_allow_html=True)

col_hot, col_cold = st.columns(2)
with col_hot:
    hot = build_fluid("hot", "hot")
with col_cold:
    cold = build_fluid("cold", "cold")

st.markdown("---")
st.markdown("### Geometry")

if hx_type == "Double-pipe":
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        D_i = st.number_input("D_i [m]", value=0.0254, format="%.4f", min_value=0.001)
    with c2:
        D_o = st.number_input("D_o [m]", value=0.0318, format="%.4f", min_value=0.002)
    with c3:
        L = st.number_input("Tube length L [m]", value=3.0, min_value=0.1, step=0.5)
    with c4:
        k_wall = st.number_input("k_wall [W/mK]", value=50.0, min_value=1.0)
    N_tubes = 1
    N_passes = 1
    D_shell = max(D_o * 3, 0.05)
    pitch_ratio = 1.25
    baffle_spacing_ratio = 0.3
    baffle_cut_pct = 25.0
    shell_type = "E"
    tube_layout = "triangular"
    baffle_type_sel = "segmental"
    material_sel = "SA-249-304"
    tube_thickness = 0.002
else:
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        D_i = st.number_input("D_i [m]", value=0.0254, format="%.4f", min_value=0.001)
    with c2:
        D_o = st.number_input("D_o [m]", value=0.0318, format="%.4f", min_value=0.002)
    with c3:
        L = st.number_input("Tube length L [m]", value=3.0, min_value=0.1, step=0.5)
    with c4:
        N_tubes = st.number_input("N_tubes", value=10, min_value=1, step=1)
    with c5:
        D_shell = st.number_input("D_shell [m]", value=0.1, format="%.3f", min_value=0.01)

    st.markdown("**TEMA & Shell Configuration**")
    tc1, tc2, tc3, tc4, tc5 = st.columns(5)
    with tc1:
        shell_type = st.selectbox("Shell type (TEMA)", list(SHELL_TYPES.keys()), index=0,
                                   help="E=1-pass, F=2-pass, G=split, etc.")
    with tc2:
        tube_layout = st.selectbox("Tube layout", ["triangular", "square"], index=0,
                                    help="Triangular: better h, higher dP. Square: easier cleaning.")
    with tc3:
        N_passes = st.number_input("Tube passes", value=1, min_value=1, max_value=16, step=1,
                                    help="Multi-pass increases tube velocity and h_i.")
    with tc4:
        baffle_type_sel = st.selectbox("Baffle type", ["segmental", "double-segmental", "rod-baffle"],
                                        index=0)
    with tc5:
        material_sel = st.selectbox("Tube material", list_materials(), index=3,
                                     help="SA-249-304 is common stainless steel.")

    st.markdown("**Baffle & Pitch**")
    bp1, bp2, bp3, bp4, bp5 = st.columns(5)
    with bp1:
        pitch_ratio = st.number_input("Pitch ratio (pitch/D_o)", value=1.25, min_value=1.0, max_value=3.0, step=0.05)
    with bp2:
        baffle_spacing_ratio = st.number_input("Baffle spacing / D_shell", value=0.30, min_value=0.05, max_value=1.0, step=0.05)
    with bp3:
        baffle_cut_pct = st.number_input("Baffle cut [%]", value=25.0, min_value=10.0, max_value=50.0, step=1.0)
    with bp4:
        k_wall = st.number_input("k_wall [W/mK]", value=50.0, min_value=1.0)
    with bp5:
        tube_thickness = st.number_input("Tube wall [mm]", value=2.0, min_value=0.5, max_value=10.0, step=0.5)
        tube_thickness_m = tube_thickness / 1000.0

# Design-mode inputs
q_duty = None
Tc_o_desired = None
if mode_key == "design":
    st.markdown("---")
    st.markdown("### Design Target")
    dt1, dt2 = st.columns(2)
    with dt1:
        design_target = st.radio(
            "Target type", ["Cold outlet temperature", "Heat duty (W)"],
            horizontal=True, key="dt",
        )
    with dt2:
        if "outlet" in design_target:
            Tc_o_desired = st.number_input(
                "T_c,out desired [K]", value=333.15, min_value=273.0, max_value=800.0, step=1.0,
            )
        else:
            q_duty = st.number_input(
                "q required [W]", value=50000.0, min_value=100.0, step=1000.0,
            )


geom = GeometryInput(
    D_i=D_i, D_o=D_o, L=L, N_tubes=N_tubes, N_passes=N_passes if hx_type == "Shell-and-tube" else 1,
    D_shell=D_shell, shell_type=shell_type if hx_type == "Shell-and-tube" else "E",
    pitch_ratio=pitch_ratio, tube_layout=tube_layout if hx_type == "Shell-and-tube" else "triangular",
    k_wall=k_wall, fouling=fouling_key, arrangement=arr_key,
    baffle_spacing_ratio=baffle_spacing_ratio if hx_type == "Shell-and-tube" else 0.3,
    baffle_cut_pct=baffle_cut_pct if hx_type == "Shell-and-tube" else 25.0,
    baffle_type=baffle_type_sel if hx_type == "Shell-and-tube" else "segmental",
    material=material_sel if hx_type == "Shell-and-tube" else "SA-249-304",
    tube_thickness=tube_thickness_m if hx_type == "Shell-and-tube" else 0.002,
    custom_Rf=custom_rfi if use_custom_rf else None,
)

st.markdown("---")
col_btn, col_sp = st.columns([1, 3])
with col_btn:
    solve_btn = st.button("Run Simulation", type="primary", use_container_width=True)

if solve_btn:
    try:
        with st.spinner("Solving..."):
            if mode_key == "rating":
                result = solve_rating(hot, cold, geom)
            else:
                result = solve_design(hot, cold, geom,
                                      Tc_o_desired=Tc_o_desired, q_duty=q_duty)
    except Exception as e:
        st.error(f"Solver error: {e}")
        st.stop()

    # Convergence banner
    if result.converged:
        st.success(f"Converged in {result.iterations} iterations")
    else:
        st.warning(f"Did not converge after {result.iterations} iterations")
    for w in result.warnings:
        st.warning(w)

    # ── HX Animation ──
    svg = render_hx_svg(
        hx_type, arr_key,
        hot.T_inlet, result.Th_o, cold.T_inlet, result.Tc_o,
        D_i, D_o, L, N_tubes, D_shell,
        result.baffle, result.q,
        result.ht.h_i, result.ht.h_o,
        result.dp_tube.delta_P, result.dp_shell.delta_P,
    )
    st.markdown(f'<div class="hx-viz-box">{svg}</div>', unsafe_allow_html=True)
    st.markdown("")

    # Key metrics
    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("Heat Duty q", f"{result.q:,.0f} W")
    m2.metric("Effectiveness", f"{result.epsilon:.4f}")
    m3.metric("NTU", f"{result.NTU:.3f}")
    m4.metric("LMTD", f"{result.LMTD:.2f} K")
    m5.metric("Iterations", f"{result.iterations}")

    # Tabs
    tab_temps, tab_ht, tab_dp, tab_baffle, tab_tema, tab_fiv, tab_cost, tab_foul, tab_nozzle, tab_charts, tab_export = st.tabs(
        ["Temperatures", "Heat Transfer", "Pressure Drop",
         "Baffles", "TEMA & Shell", "FIV Check",
         "Cost Analysis", "Fouling", "Nozzle Sizing",
         "Charts", "Export"]
    )


    with tab_temps:
        st.markdown("#### Fluid Temperatures")
        tc1, tc2 = st.columns(2)
        with tc1:
            st.markdown('<span class="hx-badge hx-hot">Hot side</span>', unsafe_allow_html=True)
            st.metric("T_in", f"{hot.T_inlet:.2f} K ({hot.T_inlet-273.15:.1f} C)")
            st.metric("T_out", f"{result.Th_o:.2f} K ({result.Th_o-273.15:.1f} C)",
                       delta=f"{result.Th_o - hot.T_inlet:.2f} K")
        with tc2:
            st.markdown('<span class="hx-badge hx-cold">Cold side</span>', unsafe_allow_html=True)
            st.metric("T_in", f"{cold.T_inlet:.2f} K ({cold.T_inlet-273.15:.1f} C)")
            st.metric("T_out", f"{result.Tc_o:.2f} K ({result.Tc_o-273.15:.1f} C)",
                       delta=f"{result.Tc_o - cold.T_inlet:.2f} K")

        st.markdown("---")
        st.markdown("#### Capacity Rates")
        cr1, cr2, cr3, cr4 = st.columns(4)
        cr1.metric("C_h", f"{result.C_h:.2f} W/K")
        cr2.metric("C_c", f"{result.C_c:.2f} W/K")
        cr3.metric("C_min", f"{result.C_min:.2f} W/K")
        cr4.metric("C_r = C_min/C_max", f"{result.Cr:.4f}")


    with tab_ht:
        st.markdown("#### Heat Transfer Coefficients")
        ht1, ht2, ht3 = st.columns(3)
        with ht1:
            st.markdown("**Tube-side (internal)**")
            st.metric("h_i", f"{result.ht.h_i:.2f} W/m2K")
            st.metric("Re_i", f"{result.ht.Re_i:.0f}")
            st.metric("Pr_i", f"{result.ht.Pr_i:.3f}")
            st.metric("Nu_i", f"{result.ht.Nu_i:.2f}")
        with ht2:
            st.markdown("**Shell-side (external)**")
            st.metric("h_o", f"{result.ht.h_o:.2f} W/m2K")
            st.metric("Re_o", f"{result.ht.Re_o:.0f}")
            st.metric("Pr_o", f"{result.ht.Pr_o:.3f}")
            st.metric("Nu_o", f"{result.ht.Nu_o:.2f}")
        with ht3:
            st.markdown("**Overall U**")
            st.metric("U_o clean", f"{result.ht.U_o:.2f} W/m2K")
            st.metric("U_o fouled", f"{result.ht.U_o_fouled:.2f} W/m2K")
            red = (1 - result.ht.U_o_fouled / result.ht.U_o) * 100 if result.ht.U_o > 0 else 0
            st.metric("Fouling penalty", f"-{red:.1f}%")

        st.markdown("---")
        st.code(
            "Tube:   Nu = 0.023 * Re^0.8 * Pr^n   (Dittus-Boelter)\n"
            "Shell:  Nu = 0.2  * Re^0.6 * Pr^0.33  (Donohue)\n"
            "1/U_o = (D_o/D_i)/h_i + D_o*ln(D_o/D_i)/(2*k) + 1/h_o",
            language=None,
        )


    with tab_dp:
        st.markdown("#### Pressure Drop")
        dp1, dp2 = st.columns(2)
        with dp1:
            st.markdown("**Tube-side**")
            st.metric("dP total", f"{result.dp_tube.delta_P:.1f} Pa")
            st.metric("dP friction", f"{result.dp_tube.delta_P_friction:.1f} Pa")
            st.metric("dP minor", f"{result.dp_tube.delta_P_minor:.1f} Pa")
            st.metric("Velocity", f"{result.dp_tube.velocity:.3f} m/s")
            st.metric("Re", f"{result.dp_tube.Re:.0f}")
            st.metric("f_D", f"{result.dp_tube.f_D:.5f}")
            st.metric("Regime", result.dp_tube.regime)
        with dp2:
            st.markdown("**Shell-side**")
            st.metric("dP total", f"{result.dp_shell.delta_P:.1f} Pa")
            st.metric("Velocity", f"{result.dp_shell.velocity:.3f} m/s")
            st.metric("Re", f"{result.dp_shell.Re:.0f}")
            st.metric("f_D", f"{result.dp_shell.f_D:.4f}")
            st.metric("Regime", result.dp_shell.regime)

        st.code(
            "Tube:  dP = f*(L/D_i)*(rho*v^2/2) + (K_ent+K_exit)*(rho*v^2/2)\n"
            "Shell: dP = f_shell*(N_baffles+1)*(rho*v_shell^2/2)",
            language=None,
        )


    with tab_baffle:
        if result.baffle:
            st.markdown("#### Baffle Geometry (Shell-and-Tube)")
            b = result.baffle
            b1, b2, b3, b4 = st.columns(4)
            with b1:
                st.metric("Baffles", f"{b.N_baffles}")
                st.metric("Spacing", f"{b.spacing*1000:.1f} mm")
            with b2:
                st.metric("Cut %", f"{b.cut_pct:.0f}%")
                st.metric("Cut height", f"{b.cut_height*1000:.1f} mm")
            with b3:
                st.metric("A_baffle", f"{b.A_baffle:.6f} m2")
                st.metric("A_flow_shell", f"{b.A_flow_shell:.6f} m2")
            with b4:
                st.metric("D_eq", f"{b.D_eq*1000:.2f} mm")

            st.markdown("---")
            st.markdown("**Baffle design rules:**")
            st.code(
                f"B = baffle_spacing_ratio * D_shell\n"
                f"  = {geom.baffle_spacing_ratio:.2f} * {D_shell*1000:.0f} mm = {b.spacing*1000:.1f} mm\n"
                f"N_baffles = round(L/B) - 1 = {b.N_baffles}\n"
                f"Baffle cut = {b.cut_pct:.0f}% of D_shell = {b.cut_height*1000:.1f} mm\n"
                f"A_flow = D_shell * B * (pitch - D_o) / pitch = {b.A_flow_shell:.6f} m2",
                language=None,
            )
        else:
            st.markdown("#### Double-Pipe HX")
            st.info("Baffles are used only in shell-and-tube configurations.")
            st.markdown("**Geometry summary:**")
            g1, g2, g3 = st.columns(3)
            with g1:
                st.metric("D_i", f"{D_i*1000:.2f} mm")
                st.metric("D_o", f"{D_o*1000:.2f} mm")
            with g2:
                st.metric("L", f"{L:.2f} m")
                A_total = math.pi * D_o * L * N_tubes
                st.metric("A_total", f"{A_total:.4f} m2")
            with g3:
                st.metric("k_wall", f"{k_wall:.1f} W/mK")
                st.metric("Fouling", fouling_key)

        if mode_key == "design":
            st.markdown("---")
            st.markdown("#### Design Sizing")
            sd1, sd2, sd3 = st.columns(3)
            with sd1:
                st.metric("Required area", f"{result.area_required:.4f} m2")
            with sd2:
                A_per_tube = math.pi * D_o * L
                N_req = math.ceil(result.area_required / A_per_tube) if A_per_tube > 0 else 1
                st.metric("Tubes required", f"{N_req}")
            with sd3:
                st.metric("Heat duty achieved", f"{result.q:,.0f} W")

    with tab_tema:
        st.markdown("#### TEMA Designation & Shell Configuration")
        if result.tema_code:
            st.markdown(f'<span class="hx-badge hx-info">TEMA: {result.tema_code}</span>', unsafe_allow_html=True)
            st.markdown("")
            tc1, tc2, tc3 = st.columns(3)
            with tc1:
                front_letter = result.tema_code[0]
                shell_letter = result.tema_code[1]
                rear_letter = result.tema_code[2]
                st.metric("Front Head", f"{front_letter} — {TEMA_FRONT.get(front_letter, '')}")
                st.metric("Shell", f"{shell_letter} — {SHELL_TYPES.get(shell_letter, '')}")
            with tc2:
                st.metric("Rear Head", f"{rear_letter} — {TEMA_REAR.get(rear_letter, '')}")
                st.metric("Tube passes", f"{geom.N_passes}")
            with tc3:
                st.metric("Tube layout", f"{geom.tube_layout}")
                st.metric("Baffle type", f"{geom.baffle_type}")

            st.markdown("---")
            st.markdown("**Shell types reference:**")
            for code, desc in SHELL_TYPES.items():
                st.markdown(f"  **{code}**: {desc}")
        else:
            st.info("TEMA codes apply to shell-and-tube exchangers only.")

    with tab_fiv:
        st.markdown("#### Flow-Induced Vibration Analysis")
        if result.fiv:
            fiv = result.fiv
            if fiv.safe:
                st.success("FIV check PASSED — no vibration concerns detected")
            else:
                st.error("FIV check FAILED — vibration risk detected")

            fv1, fv2, fv3 = st.columns(3)
            with fv1:
                st.metric("Tube natural freq", f"{fiv.f_natural:.1f} Hz")
                st.metric("Vortex shedding freq", f"{fiv.f_vortex:.1f} Hz")
                st.metric("f_v / f_n", f"{fiv.f_ratio:.3f}")
            with fv2:
                st.metric("Crossflow velocity", f"{fiv.v_crossflow:.3f} m/s")
                st.metric("Critical velocity (elastic)", f"{fiv.v_critical_elastic:.2f} m/s")
                st.metric("v / v_cr", f"{fiv.v_ratio_elastic:.3f}")
            with fv3:
                st.metric("Amplitude (total)", f"{fiv.total_amplitude*1000:.4f} mm")
                st.metric("Min clearance", f"{fiv.min_clearance*1000:.2f} mm")
                st.metric("Acoustic freq", f"{fiv.f_acoustic:.0f} Hz")

            if fiv.warnings:
                st.markdown("---")
                for w in fiv.warnings:
                    st.warning(w)

            st.markdown("---")
            st.code(
                "Connors criterion:  v_cr = K * f_n * D_o\n"
                f"  K = 3.0 (conservative)\n"
                f"  f_n = {fiv.f_natural:.1f} Hz\n"
                f"  D_o = {D_o*1000:.1f} mm\n"
                f"  v_cr = {fiv.v_critical_elastic:.2f} m/s\n"
                f"  Actual v = {fiv.v_crossflow:.3f} m/s\n"
                f"  Ratio = {fiv.v_ratio_elastic:.3f} (< 1.0 = SAFE)",
                language=None,
            )
        else:
            st.info("FIV analysis is available for shell-and-tube exchangers only.")

    with tab_cost:
        st.markdown("#### Cost Analysis (CAPEX + OPEX)")
        if result.cost:
            cost = result.cost
            cc1, cc2 = st.columns(2)
            with cc1:
                st.markdown("**Capital Costs (CAPEX)**")
                st.metric("Tube material", f"${cost.tube_cost:,.0f}")
                st.metric("Shell & fabrication", f"${cost.shell_cost:,.0f}")
                st.metric("Baffles", f"${cost.baffle_cost:,.0f}")
                st.metric("Nozzles", f"${cost.nozzle_cost:,.0f}")
                st.metric("Total CAPEX", f"${cost.total_capex:,.0f}")
                st.metric("Cost per m2", f"${cost.cost_per_m2:,.0f}")
                st.metric("Cost per kW", f"${cost.cost_per_kw:,.0f}")
            with cc2:
                st.markdown("**Operating Costs (OPEX)**")
                st.metric("Tube pumping", f"{cost.pumping_power_tube:.0f} W")
                st.metric("Shell pumping", f"{cost.pumping_power_shell:.0f} W")
                st.metric("Total pumping", f"{cost.total_pumping_power:.0f} W")
                st.metric("Annual energy", f"${cost.annual_energy_cost:,.0f}/yr")
                st.metric("Annual maintenance", f"${cost.annual_maintenance:,.0f}/yr")
                st.metric("Annual OPEX", f"${cost.total_annual_opex:,.0f}/yr")
                st.metric("Lifecycle cost", f"${cost.total_lifecycle_cost:,.0f}")
        else:
            st.info("Cost analysis is available for shell-and-tube exchangers only.")

    with tab_foul:
        st.markdown("#### Fouling Trend Prediction")
        if result.fouling_pred:
            fp = result.fouling_pred
            st.markdown(f"**Fluid:** {fp.description}")
            ff1, ff2, ff3, ff4 = st.columns(4)
            with ff1:
                st.metric("Design Rf", f"{fp.Rf_design:.2e} m²·K/W")
                st.metric("Predicted Rf (5yr)", f"{fp.Rf_predicted:.2e} m²·K/W")
            with ff2:
                st.metric("U clean", f"{fp.U_clean:.0f} W/m²K")
                st.metric("U fouled", f"{fp.U_fouled:.0f} W/m²K")
            with ff3:
                st.metric("U minimum", f"{fp.U_minimum:.0f} W/m²K")
                margin = fp.U_fouled - fp.U_minimum
                st.metric("Fouling margin", f"{margin:.0f} W/m²K")
            with ff4:
                st.metric("Cleaning interval", f"{fp.cleaning_interval:.1f} years")
                st.metric("Evaluation time", f"{fp.time_years:.0f} years")
            st.caption("Based on Kern-Seaton asymptotic model. Cleaning interval = time for U to drop to U_min.")
        else:
            st.info("Fouling prediction could not be computed. Check inputs.")

    with tab_nozzle:
        st.markdown("#### Nozzle Sizing")
        if result.nozzle_hot_in:
            st.markdown("**Hot Side**")
            ni1, ni2 = st.columns(2)
            with ni1:
                st.metric("Hot In — NPS", f'{result.nozzle_hot_in.NPS}"')
                st.metric("Hot In — Velocity", f"{result.nozzle_hot_in.velocity:.2f} m/s")
                st.metric("Hot In — dP", f"{result.nozzle_hot_in.dP_nozzle:.0f} Pa")
                st.metric("Hot In — Flange class", f"ANSI {result.nozzle_hot_in.flange_class}")
            with ni2:
                st.metric("Hot Out — NPS", f'{result.nozzle_hot_out.NPS}"')
                st.metric("Hot Out — Velocity", f"{result.nozzle_hot_out.velocity:.2f} m/s")
                st.metric("Hot Out — dP", f"{result.nozzle_hot_out.dP_nozzle:.0f} Pa")

            st.markdown("**Cold Side**")
            nc1, nc2 = st.columns(2)
            with nc1:
                st.metric("Cold In — NPS", f'{result.nozzle_cold_in.NPS}"')
                st.metric("Cold In — Velocity", f"{result.nozzle_cold_in.velocity:.2f} m/s")
                st.metric("Cold In — dP", f"{result.nozzle_cold_in.dP_nozzle:.0f} Pa")
            with nc2:
                st.metric("Cold Out — NPS", f'{result.nozzle_cold_out.NPS}"')
                st.metric("Cold Out — Velocity", f"{result.nozzle_cold_out.velocity:.2f} m/s")
                st.metric("Cold Out — dP", f"{result.nozzle_cold_out.dP_nozzle:.0f} Pa")

            for nozzle, label in [
                (result.nozzle_hot_in, "Hot In"),
                (result.nozzle_hot_out, "Hot Out"),
                (result.nozzle_cold_in, "Cold In"),
                (result.nozzle_cold_out, "Cold Out"),
            ]:
                if nozzle.warnings:
                    for w in nozzle.warnings:
                        st.warning(f"{label}: {w}")
        else:
            st.info("Nozzle sizing is available for shell-and-tube exchangers only.")


    with tab_charts:
        c1, c2 = st.columns(2)

        # Temperature profile
        with c1:
            st.markdown("#### Temperature Profile")
            x = np.linspace(0, L, 200)
            if arr_key == "counter":
                Th = hot.T_inlet + (result.Th_o - hot.T_inlet) * (x / L)
                Tc = result.Tc_o + (cold.T_inlet - result.Tc_o) * (x / L)
            else:
                Th = hot.T_inlet + (result.Th_o - hot.T_inlet) * (x / L)
                Tc = cold.T_inlet + (result.Tc_o - cold.T_inlet) * (x / L)

            fig, ax, tc = styled_fig()
            ax.plot(x, Th - 273.15, color=tc["hot"], linewidth=2.2, label="Hot fluid")
            ax.plot(x, Tc - 273.15, color=tc["cold"], linewidth=2.2, label="Cold fluid")
            ax.fill_between(x, Tc - 273.15, Th - 273.15, alpha=0.08, color=tc["fill"])
            ax.set_xlabel("Length [m]")
            ax.set_ylabel("Temperature [C]")
            ax.set_title(f"{arrangement} - Temperature Profile")
            ax.legend(facecolor="none", edgecolor="none", labelcolor=tc["text"])
            ax.grid(True, alpha=0.15, color=tc["grid"])
            st.pyplot(fig)
            plt.close(fig)

        # epsilon-NTU
        with c2:
            st.markdown("#### Effectiveness vs NTU")
            ntu_arr = np.linspace(0.01, 5, 200)
            if arr_key == "counter":
                eps_arr = [epsilon_NTU_counterflow(n, result.Cr) for n in ntu_arr]
            else:
                eps_arr = [epsilon_NTU_parallel(n, result.Cr) for n in ntu_arr]

            fig2, ax2, tc2 = styled_fig()
            ax2.plot(ntu_arr, eps_arr, color=tc2["line2"], linewidth=2.2, label=f"C_r = {result.Cr:.3f}")
            ax2.axvline(result.NTU, color=tc2["hot"], linestyle="--", alpha=0.7, label=f"NTU = {result.NTU:.3f}")
            ax2.axhline(result.epsilon, color=tc2["cold"], linestyle=":", alpha=0.7, label=f"e = {result.epsilon:.4f}")
            ax2.plot(result.NTU, result.epsilon, color=tc2["dot"], markersize=9, zorder=5)
            ax2.plot(result.NTU, result.epsilon, color=tc2["hot"], markersize=5, zorder=6)
            ax2.set_xlabel("NTU")
            ax2.set_ylabel("Effectiveness")
            ax2.set_title("epsilon-NTU Relation")
            ax2.legend(facecolor="none", edgecolor="none", labelcolor=tc2["text"])
            ax2.grid(True, alpha=0.15, color=tc2["grid"])
            ax2.set_xlim(0, 5)
            ax2.set_ylim(0, 1)
            st.pyplot(fig2)
            plt.close(fig2)

        # Thermal resistance breakdown
        st.markdown("#### Thermal Resistance Breakdown")
        r_tube = (D_o / D_i) / result.ht.h_i
        r_wall = D_o * math.log(D_o / D_i) / (2 * k_wall)
        r_shell = 1.0 / result.ht.h_o
        r_fi = FF[fouling_key][0] * (D_o / D_i)
        r_fo = FF[fouling_key][1]

        labels = ["Tube-side conv.", "Wall conduction", "Shell-side conv."]
        sizes = [r_tube, r_wall, r_shell]
        colors_pie = ["#ff6b6b", "#ffa502", "#42a5f5"]
        if r_fi + r_fo > 0:
            labels.append("Fouling (i+o)")
            sizes.append(r_fi + r_fo)
            colors_pie.append("#7bed9f")

        fig3, ax3, tc3 = styled_fig()
        wedges, texts, autotexts = ax3.pie(
            sizes, labels=labels, autopct="%1.1f%%",
            colors=colors_pie, startangle=90,
            textprops={"color": tc3["text"], "fontsize": 10},
        )
        for at in autotexts:
            at.set_color("white")
            at.set_fontweight("bold")
        ax3.set_title("Thermal Resistance Distribution")
        st.pyplot(fig3)
        plt.close(fig3)

        rc1, rc2, rc3, rc4 = st.columns(4)
        rc1.metric("R_tube", f"{r_tube:.6f}")
        rc2.metric("R_wall", f"{r_wall:.6f}")
        rc3.metric("R_shell", f"{r_shell:.6f}")
        if r_fi + r_fo > 0:
            rc4.metric("R_fouling", f"{r_fi+r_fo:.6f}")

        # Friction factor chart
        st.markdown("#### Friction Factor vs Re")
        from hx_simulator.pressure_drop import friction_factor as ff_fn
        Re_range = np.logspace(1, 6, 300)
        f_arr = [ff_fn(r) for r in Re_range]

        fig4, ax4, tc4 = styled_fig()
        ax4.loglog(Re_range, f_arr, color=tc4["accent"], linewidth=2)
        ax4.axvline(2300, color=tc4["hot"], linestyle="--", alpha=0.5, label="Re=2300")
        ax4.axvline(10000, color=tc4["cold"], linestyle="--", alpha=0.5, label="Re=10000")
        ax4.loglog(result.dp_tube.Re, result.dp_tube.f_D, "o", color=tc4["dot"],
                   markersize=10, zorder=5)
        ax4.loglog(result.dp_tube.Re, result.dp_tube.f_D, "o", color=tc4["hot"],
                   markersize=6, zorder=6, label=f"Operating (Re={result.dp_tube.Re:.0f})")
        ax4.set_xlabel("Reynolds Number")
        ax4.set_ylabel("Darcy Friction Factor")
        ax4.set_title("Tube-side Friction")
        ax4.legend(facecolor="none", edgecolor="none", labelcolor=tc4["text"])
        ax4.grid(True, alpha=0.15, color=tc4["grid"])
        st.pyplot(fig4)
        plt.close(fig4)


    with tab_export:
        st.markdown("#### Export Results")

        report = [
            "=" * 60,
            "  HEAT EXCHANGER SIMULATION REPORT",
            "=" * 60, "",
            f"Mode: {mode}",
            f"HX Type: {hx_type}",
            f"Arrangement: {arrangement}",
            f"Fouling: {fouling_key}", "",
            "--- INPUTS ---",
            f"Hot:   {hot.name}, T_in={hot.T_inlet:.2f}K, m={hot.m_dot:.4f}kg/s",
            f"Cold:  {cold.name}, T_in={cold.T_inlet:.2f}K, m={cold.m_dot:.4f}kg/s",
            f"Geom:  D_i={D_i:.4f}m, D_o={D_o:.4f}m, L={L:.2f}m, N={N_tubes}",
            f"       D_shell={D_shell:.4f}m, k_wall={k_wall:.1f}W/mK", "",
            "--- RESULTS ---",
            f"q = {result.q:.2f} W",
            f"epsilon = {result.epsilon:.4f}",
            f"NTU = {result.NTU:.4f}",
            f"LMTD = {result.LMTD:.2f} K",
            f"Th_o = {result.Th_o:.2f} K  |  Tc_o = {result.Tc_o:.2f} K", "",
            f"h_i = {result.ht.h_i:.2f} W/m2K",
            f"h_o = {result.ht.h_o:.2f} W/m2K",
            f"U_clean = {result.ht.U_o:.2f}  |  U_fouled = {result.ht.U_o_fouled:.2f}", "",
            f"dP_tube = {result.dp_tube.delta_P:.1f} Pa ({result.dp_tube.regime})",
            f"dP_shell = {result.dp_shell.delta_P:.1f} Pa ({result.dp_shell.regime})",
        ]
        if result.baffle:
            b = result.baffle
            report += [
                "", "--- BAFFLES ---",
                f"N = {b.N_baffles}, spacing = {b.spacing*1000:.1f}mm",
                f"cut = {b.cut_pct:.0f}%, A_flow = {b.A_flow_shell:.6f} m2",
            ]
        if mode_key == "design":
            report.append(f"\nRequired area = {result.area_required:.4f} m2")

        st.code("\n".join(report), language=None)

        st.download_button("Download report (.txt)", "\n".join(report),
                           file_name="hx_report.txt", mime="text/plain",
                           use_container_width=True)

        import csv
        from io import StringIO
        csv_buf = StringIO()
        w = csv.writer(csv_buf)
        w.writerow(["Parameter", "Value", "Unit"])
        w.writerow(["q", f"{result.q:.2f}", "W"])
        w.writerow(["epsilon", f"{result.epsilon:.4f}", "-"])
        w.writerow(["NTU", f"{result.NTU:.4f}", "-"])
        w.writerow(["LMTD", f"{result.LMTD:.2f}", "K"])
        w.writerow(["Th_o", f"{result.Th_o:.2f}", "K"])
        w.writerow(["Tc_o", f"{result.Tc_o:.2f}", "K"])
        w.writerow(["h_i", f"{result.ht.h_i:.2f}", "W/m2K"])
        w.writerow(["h_o", f"{result.ht.h_o:.2f}", "W/m2K"])
        w.writerow(["U_fouled", f"{result.ht.U_o_fouled:.2f}", "W/m2K"])
        w.writerow(["dP_tube", f"{result.dp_tube.delta_P:.1f}", "Pa"])
        w.writerow(["dP_shell", f"{result.dp_shell.delta_P:.1f}", "Pa"])

        st.download_button("Download CSV", csv_buf.getvalue(),
                           file_name="hx_results.csv", mime="text/csv",
                           use_container_width=True)
else:
    st.info("Configure inputs above and click **Run Simulation** to solve.")

    with st.expander("Reference Formulas (HTOA 2025)", expanded=False):
        st.markdown("""
        **Energy balance:**  q = m_h*Cp_h*(Th_i - Th_o) = m_c*Cp_c*(Tc_o - Tc_i)

        **LMTD:**  dT_lm = (dT1 - dT2) / ln(dT1/dT2)

        **Overall U:**  1/U_o = (D_o/D_i)/h_i + D_o*ln(D_o/D_i)/(2k) + 1/h_o

        **Dittus-Boelter:**  Nu = 0.023 * Re^0.8 * Pr^n

        **Donohue:**  Nu = 0.2 * Re^0.6 * Pr^0.33

        **epsilon-NTU (counter):**  e = (1 - exp[-NTU(1-Cr)]) / (1 - Cr*exp[-NTU(1-Cr)])
        """)
