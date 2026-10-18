"""
Institutional RegTech & Land Heritage Theme Module for JomiGuard.
Includes Bengali (Hind Siliguri), English (Plus Jakarta Sans),
Monospace (JetBrains Mono) typography, KrishiBondhu-inspired frosted navigation,
micro-animations (conflictPulse, capacity overflow), and strict dual-mode tokens.
"""

def get_theme_css(theme_mode: str = "Auto (System)") -> str:
    """Generate complete CSS for JomiGuard following Institutional RegTech standards."""

    # Light Mode Tokens (Institutional RegTech & Land Heritage)
    light_tokens = """
        --jg-brand: #0F3D2E;
        --jg-accent: #1B6B50;
        --jg-accent-hover: #14523D;
        --jg-accent-soft: #E8F5EE;
        --jg-secondary: #1E293B;

        --jg-bg: #F8FAFC;
        --jg-surface: #FFFFFF;
        --jg-surface-hover: #F1F5F9;
        --jg-surface-subtle: #F8FAFC;
        --jg-surface-card: #FFFFFF;

        --jg-ink: #0F172A;
        --jg-ink-secondary: #334155;
        --jg-muted: #64748B;
        --jg-border: #E2E8F0;
        --jg-border-subtle: #EDF2F7;
        --jg-radius: 12px;
        --jg-radius-pill: 999px;
        --jg-shadow-sm: 0 1px 3px rgba(15, 23, 42, 0.05);
        --jg-shadow: 0 4px 16px -4px rgba(15, 61, 46, 0.08), 0 1px 3px rgba(15, 23, 42, 0.04);
        --jg-shadow-lg: 0 12px 32px -8px rgba(15, 61, 46, 0.12);

        /* Nav & Header */
        --jg-nav-bg: rgba(255, 255, 255, 0.88);
        --jg-nav-border: rgba(226, 232, 240, 0.8);
        --jg-nav-text: #0F3D2E;

        /* Sidebar */
        --jg-sidebar-bg: #FFFFFF;
        --jg-sidebar-border: #E2E8F0;
        --jg-sidebar-text: #1E293B;
        --jg-sidebar-muted: #64748B;
        --jg-sidebar-item-hover: #F0FDF4;
        --jg-sidebar-item-active: #DCFCE7;

        /* Governance & Legal Notices (Compliance Cobalt / Ochre Amber) */
        --jg-notice-bg: #EFF6FF;
        --jg-notice-border: #93C5FD;
        --jg-notice-edge: #1D4ED8;
        --jg-notice-text: #1E3A8A;

        /* Status Colors */
        --jg-alert-high-bg: #FEF2F2;
        --jg-alert-high-text: #B91C1C;
        --jg-alert-high-border: #FCA5A5;

        --jg-alert-med-bg: #FFFBEB;
        --jg-alert-med-text: #B45309;
        --jg-alert-med-border: #FCD34D;

        --jg-alert-ok-bg: #F0FDF4;
        --jg-alert-ok-text: #15803D;
        --jg-alert-ok-border: #86EFAC;

        /* Table & Diff */
        --jg-tbl-head-bg: #F1F5F9;
        --jg-tbl-head-text: #1E293B;
        --jg-tbl-field-bg: #F8FAFC;
        --jg-tbl-field-text: #475569;
        --jg-tbl-cell-text: #0F172A;
        --jg-tbl-border: #E2E8F0;
        --jg-tbl-diff-field-bg: #FEF2F2;
        --jg-tbl-diff-field-text: #991B1B;
        --jg-tbl-diff-cell-bg: #FFF1F2;
        --jg-tbl-diff-cell-text: #9F1239;

        /* Monospace ID tag */
        --jg-mono-bg: #F1F5F9;
        --jg-mono-text: #0F172A;
        --jg-mono-border: #CBD5E1;
    """

    # Dark Mode Tokens (Institutional Dark Slate & Emerald)
    dark_tokens = """
        --jg-brand: #34D399;
        --jg-accent: #10B981;
        --jg-accent-hover: #059669;
        --jg-accent-soft: rgba(16, 185, 129, 0.18);
        --jg-secondary: #0F172A;

        --jg-bg: #090D14;
        --jg-surface: #111827;
        --jg-surface-hover: #1F2937;
        --jg-surface-subtle: #162032;
        --jg-surface-card: #111827;

        --jg-ink: #F9FAFB;
        --jg-ink-secondary: #E2E8F0;
        --jg-muted: #94A3B8;
        --jg-border: #1E293B;
        --jg-border-subtle: #172033;
        --jg-radius: 12px;
        --jg-radius-pill: 999px;
        --jg-shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.5);
        --jg-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.6);
        --jg-shadow-lg: 0 12px 36px -4px rgba(0, 0, 0, 0.8);

        /* Nav & Header */
        --jg-nav-bg: rgba(17, 24, 39, 0.94);
        --jg-nav-border: rgba(30, 41, 59, 0.85);
        --jg-nav-text: #34D399;

        /* Sidebar */
        --jg-sidebar-bg: #0B111E;
        --jg-sidebar-border: #1E293B;
        --jg-sidebar-text: #F8FAFC;
        --jg-sidebar-muted: #94A3B8;
        --jg-sidebar-item-hover: rgba(16, 185, 129, 0.14);
        --jg-sidebar-item-active: rgba(16, 185, 129, 0.24);

        /* Governance & Legal Notices */
        --jg-notice-bg: #0C1D38;
        --jg-notice-border: #1D4ED8;
        --jg-notice-edge: #3B82F6;
        --jg-notice-text: #BFDBFE;

        /* Status Colors */
        --jg-alert-high-bg: rgba(185, 28, 28, 0.25);
        --jg-alert-high-text: #FCA5A5;
        --jg-alert-high-border: #EF4444;

        --jg-alert-med-bg: rgba(180, 83, 9, 0.25);
        --jg-alert-med-text: #FDE047;
        --jg-alert-med-border: #EAB308;

        --jg-alert-ok-bg: rgba(21, 128, 61, 0.25);
        --jg-alert-ok-text: #86EFAC;
        --jg-alert-ok-border: #22C55E;

        /* Table & Diff */
        --jg-tbl-head-bg: #162032;
        --jg-tbl-head-text: #F8FAFC;
        --jg-tbl-field-bg: #121927;
        --jg-tbl-field-text: #CBD5E1;
        --jg-tbl-cell-text: #F8FAFC;
        --jg-tbl-border: #1E293B;
        --jg-tbl-diff-field-bg: rgba(239, 68, 68, 0.22);
        --jg-tbl-diff-field-text: #FECDD3;
        --jg-tbl-diff-cell-bg: rgba(239, 68, 68, 0.14);
        --jg-tbl-diff-cell-text: #FFE4E6;

        /* Monospace ID tag */
        --jg-mono-bg: #1A2436;
        --jg-mono-text: #38BDF8;
        --jg-mono-border: #334155;
    """

    if theme_mode == "Dark":
        root_css = f":root {{\n{dark_tokens}\n}}"
    elif theme_mode == "Light":
        root_css = f":root {{\n{light_tokens}\n}}"
    else:  # Auto (System)
        root_css = f":root {{\n{light_tokens}\n}}\n@media (prefers-color-scheme: dark) {{\n:root {{\n{dark_tokens}\n}}\n}}"

    return f"""
    <style>
    /* Google Fonts Import for Hind Siliguri, Plus Jakarta Sans, JetBrains Mono */
    @import url('https://fonts.googleapis.com/css2?family=Hind+Siliguri:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Noto+Sans+Bengali:wght@400;500;600;700&display=swap');

    {root_css}

    /* Base Typography & Canvas */
    html, body, [class*="css"], .stApp {{
        font-family: 'Plus Jakarta Sans', 'Hind Siliguri', 'Noto Sans Bengali', -apple-system, BlinkMacSystemFont, sans-serif;
        background-color: var(--jg-bg) !important;
        color: var(--jg-ink) !important;
        -webkit-font-smoothing: antialiased;
        text-rendering: optimizeLegibility;
    }}

    .bn-text, [lang="bn"] {{
        font-family: 'Hind Siliguri', 'Noto Sans Bengali', sans-serif !important;
        line-height: 1.68 !important;
        font-size: 0.98rem;
    }}

    /* JetBrains Mono strictly for all identifiers and decimals */
    .mono-id, code, .stCode, [data-testid="stCodeBlock"] {{
        font-family: 'JetBrains Mono', 'IBM Plex Mono', monospace !important;
        font-variant-numeric: tabular-nums !important;
        letter-spacing: -0.02em;
    }}

    .mono-id {{
        background: var(--jg-mono-bg);
        color: var(--jg-mono-text);
        border: 1px solid var(--jg-mono-border);
        padding: 2px 7px;
        border-radius: 5px;
        font-size: 0.88em;
        font-weight: 600;
        display: inline-block;
    }}

    .trigger-field-highlight {{
        font-family: 'JetBrains Mono', monospace !important;
        font-variant-numeric: tabular-nums;
        background-color: var(--jg-alert-high-bg) !important;
        color: var(--jg-alert-high-text) !important;
        border: 1px solid var(--jg-alert-high-border) !important;
        padding: 2px 8px;
        border-radius: 5px;
        font-weight: 700;
        display: inline-block;
    }}

    /* Streamlit Canvas Overrides */
    [data-testid="stAppViewContainer"], [data-testid="stHeader"] {{
        background: var(--jg-bg) !important;
        color: var(--jg-ink);
    }}
    [data-testid="stHeader"] {{
        background: transparent !important;
        backdrop-filter: none;
        border-bottom: none;
    }}
    [data-testid="stDecoration"],
    .stAppDeployButton,
    div[data-testid="stStatusWidget"] {{
        display: none !important;
    }}
    .block-container {{
        padding-top: 1.4rem;
        padding-bottom: 3.5rem;
        max-width: 1360px;
    }}

    /* Micro-Animation 1: Conflict Injection Pulse */
    @keyframes conflictPulse {{
        0% {{
            transform: translateY(-8px);
            opacity: 0.3;
            box-shadow: 0 0 0 0 rgba(220, 38, 38, 0.4);
        }}
        50% {{
            box-shadow: 0 0 0 8px rgba(220, 38, 38, 0.18);
        }}
        100% {{
            transform: translateY(0);
            opacity: 1;
            box-shadow: 0 0 0 0 rgba(220, 38, 38, 0);
        }}
    }}
    .conflict-injected {{
        animation: conflictPulse 0.45s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }}

    /* Micro-Animation 2: Animated Plot Capacity Bar */
    .capacity-bar-wrapper {{
        background: var(--jg-surface-subtle);
        border: 1px solid var(--jg-border);
        border-radius: 10px;
        padding: 14px 18px;
        margin: 12px 0 16px;
    }}
    .capacity-track {{
        width: 100%;
        height: 22px;
        background: var(--jg-border);
        border-radius: 999px;
        overflow: hidden;
        position: relative;
        display: flex;
        margin: 8px 0;
    }}
    .capacity-fill-normal {{
        height: 100%;
        background: linear-gradient(90deg, #1B6B50 0%, #15803D 100%);
        border-radius: 999px 0 0 999px;
        transition: width 500ms ease-out;
    }}
    .capacity-fill-overflow {{
        height: 100%;
        background: repeating-linear-gradient(
            45deg,
            #DC2626,
            #DC2626 10px,
            #B91C1C 10px,
            #B91C1C 20px
        );
        transition: width 500ms ease-out;
    }}

    /* KrishiBondhu-Style Floating Glass Navigation Pill */
    .kb-navbar {{
        position: sticky;
        top: 0;
        z-index: 9999;
        display: flex;
        align-items: center;
        justify-content: space-between;
        background: var(--jg-nav-bg);
        backdrop-filter: blur(14px);
        -webkit-backdrop-filter: blur(14px);
        border: 1px solid var(--jg-nav-border);
        border-radius: 16px;
        padding: 10px 20px;
        margin: -1rem 0 2rem 0;
        box-shadow: var(--jg-shadow);
    }}
    .kb-nav-left {{
        display: flex;
        align-items: center;
        gap: 12px;
    }}
    .kb-nav-brand {{
        font-size: 1.25rem;
        font-weight: 800;
        color: var(--jg-brand) !important;
        letter-spacing: -0.02em;
        display: flex;
        align-items: center;
        gap: 8px;
        text-decoration: none;
    }}
    .kb-nav-tag {{
        background: var(--jg-accent-soft);
        color: var(--jg-accent);
        border: 1px solid var(--jg-accent);
        font-size: 0.7rem;
        font-weight: 700;
        padding: 2px 8px;
        border-radius: 999px;
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }}
    .kb-nav-links {{
        display: flex;
        align-items: center;
        gap: 18px;
    }}
    .kb-nav-link {{
        color: var(--jg-ink-secondary) !important;
        font-weight: 600;
        font-size: 0.92rem;
        text-decoration: none;
        transition: color 0.15s ease;
    }}
    .kb-nav-link:hover {{
        color: var(--jg-accent) !important;
    }}

    /* Governance Shield Banner */
    .governance-shield {{
        background: var(--jg-notice-bg);
        border: 1px solid var(--jg-notice-border);
        border-left: 5px solid var(--jg-notice-edge);
        padding: 14px 18px;
        border-radius: 12px;
        color: var(--jg-notice-text) !important;
        font-size: 0.94rem;
        line-height: 1.68;
        margin: 1.2rem 0 1.6rem 0;
        box-shadow: var(--jg-shadow-sm);
    }}
    .governance-shield strong {{
        color: var(--jg-notice-text) !important;
    }}

    /* Hero Section */
    .hero-container {{
        text-align: center;
        padding: 2.8rem 1rem 2.2rem;
        max-width: 980px;
        margin: 0 auto;
    }}
    .hero-badge {{
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 6px 18px;
        background: var(--jg-accent-soft);
        border: 1px solid var(--jg-accent);
        border-radius: 999px;
        color: var(--jg-accent);
        font-size: 0.88rem;
        font-weight: 700;
        margin-bottom: 1.4rem;
        box-shadow: 0 0 16px -4px rgba(27, 107, 80, 0.25);
    }}
    .hero-title {{
        font-size: 2.85rem;
        font-weight: 850;
        line-height: 1.22;
        letter-spacing: -0.03em;
        color: var(--jg-brand) !important;
        margin-bottom: 1.2rem;
    }}
    .hero-subtitle {{
        font-size: 1.15rem;
        line-height: 1.75;
        color: var(--jg-ink-secondary) !important;
        margin-bottom: 2rem;
        max-width: 820px;
        margin-left: auto;
        margin-right: auto;
    }}
    .hero-trust-strip {{
        display: flex;
        justify-content: center;
        flex-wrap: wrap;
        gap: 20px;
        margin-top: 1.8rem;
        font-size: 0.88rem;
        font-weight: 600;
        color: var(--jg-muted);
    }}

    /* Stat Ticker */
    .stat-ticker-grid {{
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 16px;
        margin: 1.8rem 0 2.8rem;
    }}
    @media (max-width: 900px) {{
        .stat-ticker-grid {{ grid-template-columns: repeat(2, 1fr); }}
        .hero-title {{ font-size: 2.1rem; }}
    }}
    .stat-card {{
        background: var(--jg-surface);
        border: 1px solid var(--jg-border);
        border-top: 4px solid var(--jg-accent);
        border-radius: 12px;
        padding: 18px 20px;
        box-shadow: var(--jg-shadow);
        text-align: center;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }}
    .stat-card:hover {{
        transform: translateY(-3px);
        box-shadow: var(--jg-shadow-lg);
    }}
    .stat-val {{
        font-size: 2.2rem;
        font-weight: 850;
        color: var(--jg-brand);
        line-height: 1.1;
        margin-bottom: 6px;
        font-family: 'JetBrains Mono', 'Hind Siliguri', sans-serif;
    }}
    .stat-lbl {{
        font-size: 0.88rem;
        font-weight: 600;
        color: var(--jg-muted);
    }}

    /* Problem & Module Cards */
    .card-grid-3 {{
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 18px;
        margin: 1.5rem 0 2.5rem;
    }}
    .card-grid-2 {{
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 20px;
        margin: 1.5rem 0 2.5rem;
    }}
    @media (max-width: 900px) {{
        .card-grid-3, .card-grid-2 {{ grid-template-columns: 1fr; }}
    }}
    .jg-card {{
        background: var(--jg-surface);
        border: 1px solid var(--jg-border);
        border-radius: var(--jg-radius);
        padding: 22px;
        box-shadow: var(--jg-shadow);
        transition: transform 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
    }}
    .jg-card:hover {{
        transform: translateY(-3px);
        border-color: var(--jg-accent);
        box-shadow: var(--jg-shadow-lg);
    }}
    .jg-card-title {{
        font-size: 1.15rem;
        font-weight: 750;
        color: var(--jg-ink);
        margin: 10px 0 8px;
    }}
    .jg-card-desc {{
        font-size: 0.92rem;
        color: var(--jg-ink-secondary);
        line-height: 1.65;
    }}

    /* Section Headers */
    .section-badge-center {{
        text-align: center;
        margin-bottom: 8px;
    }}
    .section-badge {{
        display: inline-block;
        background: var(--jg-accent-soft);
        color: var(--jg-accent);
        font-weight: 700;
        font-size: 0.78rem;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        padding: 4px 14px;
        border-radius: 999px;
        border: 1px solid var(--jg-accent);
    }}
    .section-heading-center {{
        text-align: center;
        font-size: 2.1rem;
        font-weight: 800;
        color: var(--jg-brand);
        letter-spacing: -0.02em;
        margin-bottom: 8px;
    }}
    .section-subheading-center {{
        text-align: center;
        font-size: 1.02rem;
        color: var(--jg-muted);
        max-width: 720px;
        margin: 0 auto 1.8rem;
        line-height: 1.6;
    }}

    /* Institutional Evidence Table Styles */
    .diff-table-wrapper {{
        background: var(--jg-surface);
        border: 1px solid var(--jg-border);
        border-radius: var(--jg-radius);
        padding: 16px 18px;
        box-shadow: var(--jg-shadow);
        margin: 12px 0 16px;
        overflow-x: auto;
    }}
    .diff-card-header {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 1px solid var(--jg-border);
        padding-bottom: 10px;
        margin-bottom: 12px;
    }}
    .diff-header-title {{
        font-weight: 750;
        font-size: 0.98rem;
        color: var(--jg-ink);
    }}
    .diff-conflict-reason-badge {{
        font-size: 0.82rem;
        color: var(--jg-alert-high-text);
        font-weight: 700;
        background: var(--jg-alert-high-bg);
        border: 1px solid var(--jg-alert-high-border);
        padding: 3px 12px;
        border-radius: 999px;
    }}
    .diff-table {{
        width: 100%;
        border-collapse: separate;
        border-spacing: 0;
        font-size: 0.88rem;
        margin: 4px 0 8px;
    }}
    .diff-table thead th {{
        background: var(--jg-tbl-head-bg);
        color: var(--jg-tbl-head-text);
        font-weight: 700;
        padding: 10px 12px;
        border-bottom: 2px solid var(--jg-border);
        text-align: left;
        font-size: 0.82rem;
        text-transform: uppercase;
        letter-spacing: 0.03em;
    }}
    .diff-table thead th:first-child {{
        border-top-left-radius: 8px;
    }}
    .diff-table thead th:last-child {{
        border-top-right-radius: 8px;
    }}
    .diff-table tbody td {{
        padding: 9px 12px;
        border-bottom: 1px solid var(--jg-border-subtle);
        vertical-align: middle;
    }}
    .diff-row-match:hover td {{
        background: var(--jg-surface-hover);
    }}
    .diff-row-conflict {{
        background: var(--jg-tbl-diff-field-bg);
    }}
    .diff-row-conflict td {{
        border-bottom: 1px solid var(--jg-alert-high-border);
    }}
    .diff-cell-field {{
        font-weight: 600;
        color: var(--jg-muted);
    }}
    .diff-conflict-text {{
        color: var(--jg-alert-high-text) !important;
        font-weight: 750 !important;
    }}
    .diff-conflict-val {{
        background: var(--jg-tbl-diff-cell-bg);
        font-weight: 700;
    }}
    .diff-cell-badge {{
        text-align: center;
        padding: 4px !important;
    }}
    .diff-neq-pill {{
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 24px;
        height: 24px;
        border-radius: 50%;
        background: #FEF2F2;
        color: #B91C1C;
        border: 1px solid #FCA5A5;
        font-weight: 800;
        font-size: 0.95rem;
    }}
    .diff-match-pill {{
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 20px;
        height: 20px;
        border-radius: 50%;
        background: var(--jg-surface-subtle);
        color: var(--jg-muted);
        font-weight: 650;
        font-size: 0.85rem;
    }}
    .diff-conflict-dot {{
        display: inline-block;
        width: 16px;
        height: 16px;
        line-height: 16px;
        text-align: center;
        background: #DC2626;
        color: #FFFFFF;
        font-weight: 800;
        font-size: 0.72rem;
        border-radius: 50%;
        margin-right: 4px;
    }}
    .diff-empty {{
        color: var(--jg-muted);
        font-style: italic;
    }}

    /* Main Content Headers */
    .main-header {
        font-size: 1.85rem !important;
        font-weight: 850 !important;
        color: var(--jg-brand) !important;
        letter-spacing: -0.02em !important;
        margin-bottom: 6px !important;
        line-height: 1.25 !important;
    }
    .sub-header {
        font-size: 0.98rem !important;
        color: var(--jg-ink-secondary) !important;
        margin-bottom: 1.2rem !important;
        line-height: 1.6 !important;
    }
    .section-title {
        font-size: 1.25rem !important;
        font-weight: 750 !important;
        color: var(--jg-ink) !important;
        margin: 1.6rem 0 0.8rem !important;
        display: flex !important;
        align-items: center !important;
        gap: 8px !important;
    }

    /* Universal Streamlit Typography & Text Contrast Overrides */
    h1, h2, h3, h4, h5, h6 {
        color: var(--jg-ink) !important;
    }
    p, span, label, li, ul, ol {
        color: var(--jg-ink);
    }
    [data-testid="stMarkdownContainer"] p,
    [data-testid="stMarkdownContainer"] span,
    [data-testid="stMarkdownContainer"] li,
    [data-testid="stMarkdownContainer"] h1,
    [data-testid="stMarkdownContainer"] h2,
    [data-testid="stMarkdownContainer"] h3,
    [data-testid="stMarkdownContainer"] h4,
    [data-testid="stMarkdownContainer"] h5,
    [data-testid="stMarkdownContainer"] h6 {
        color: var(--jg-ink) !important;
    }
    [data-testid="stCaptionContainer"],
    [data-testid="stCaptionContainer"] p {
        color: var(--jg-muted) !important;
    }

    /* Streamlit Sidebar Overrides */
    [data-testid="stSidebar"] {
        background-color: var(--jg-sidebar-bg) !important;
        border-right: 1px solid var(--jg-sidebar-border) !important;
    }
    [data-testid="stSidebar"] * {
        color: var(--jg-sidebar-text);
    }
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] span,
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] div,
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h5,
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] label {
        color: var(--jg-sidebar-text) !important;
    }
    [data-testid="stSidebar"] [data-testid="stCaptionContainer"],
    [data-testid="stSidebar"] [data-testid="stCaptionContainer"] p {
        color: var(--jg-sidebar-muted) !important;
    }
    [data-testid="stSidebar"] hr {
        border-color: var(--jg-sidebar-border) !important;
    }

    /* Animated, Responsive, Full-Width Sidebar Navigation Cards */
    [class*="st-key-sidebar_nav_"],
    [data-testid="stSidebar"] div[data-testid="stButton"],
    [data-testid="stSidebar"] div.stButton,
    [data-testid="stSidebar"] div[data-testid="stButton"] > button,
    [data-testid="stSidebar"] div.stButton > button {
        width: 100% !important;
    }
    [class*="st-key-sidebar_nav_"] button,
    [data-testid="stSidebar"] div[data-testid="stButton"] > button,
    [data-testid="stSidebar"] div.stButton > button {
        display: flex !important;
        align-items: center !important;
        justify-content: flex-start !important;
        width: 100% !important;
        padding: 13px 18px !important;
        margin-bottom: 7px !important;
        border-radius: 12px !important;
        font-size: 0.96rem !important;
        font-weight: 650 !important;
        text-align: left !important;
        cursor: pointer !important;
        transition: all 0.22s cubic-bezier(0.16, 1, 0.3, 1) !important;
        border: 1.5px solid var(--jg-border) !important;
        background: var(--jg-surface) !important;
        color: var(--jg-ink) !important;
        box-shadow: var(--jg-shadow-sm) !important;
        position: relative !important;
        overflow: hidden !important;
        letter-spacing: -0.01em !important;
    }
    [class*="st-key-sidebar_nav_"] button p,
    [class*="st-key-sidebar_nav_"] button span,
    [data-testid="stSidebar"] div[data-testid="stButton"] > button p,
    [data-testid="stSidebar"] div[data-testid="stButton"] > button span,
    [data-testid="stSidebar"] div.stButton > button p,
    [data-testid="stSidebar"] div.stButton > button span {
        color: inherit !important;
        font-size: inherit !important;
        font-weight: inherit !important;
        cursor: pointer !important;
        user-select: none !important;
    }

    /* Hover State for Inactive Navigation Tabs */
    [class*="st-key-sidebar_nav_"] button[kind="secondary"]:hover,
    [class*="st-key-sidebar_nav_"] button[data-testid="baseButton-secondary"]:hover,
    [class*="st-key-sidebar_nav_"] button[data-testid="stBaseButton-secondary"]:hover,
    [data-testid="stSidebar"] div[data-testid="stButton"] > button[kind="secondary"]:hover,
    [data-testid="stSidebar"] div[data-testid="stButton"] > button[data-testid="baseButton-secondary"]:hover,
    [data-testid="stSidebar"] div.stButton > button[kind="secondary"]:hover,
    [data-testid="stSidebar"] div.stButton > button[data-testid="baseButton-secondary"]:hover {
        transform: translateX(6px) !important;
        background: var(--jg-surface-hover) !important;
        color: var(--jg-accent) !important;
        border-color: var(--jg-accent) !important;
        box-shadow: 0 4px 16px rgba(16, 185, 129, 0.18) !important;
    }

    /* Active Navigation Card (Prominent Emerald Ribbon) */
    [class*="st-key-sidebar_nav_"] button[kind="primary"],
    [class*="st-key-sidebar_nav_"] button[data-testid="baseButton-primary"],
    [class*="st-key-sidebar_nav_"] button[data-testid="stBaseButton-primary"],
    [data-testid="stSidebar"] div[data-testid="stButton"] > button[kind="primary"],
    [data-testid="stSidebar"] div[data-testid="stButton"] > button[data-testid="baseButton-primary"],
    [data-testid="stSidebar"] div.stButton > button[kind="primary"],
    [data-testid="stSidebar"] div.stButton > button[data-testid="baseButton-primary"] {
        background: linear-gradient(135deg, var(--jg-brand) 0%, #155E44 100%) !important;
        color: #FFFFFF !important;
        border: 1.5px solid var(--jg-accent) !important;
        border-left: 6px solid var(--jg-accent) !important;
        box-shadow: 0 4px 14px rgba(15, 61, 46, 0.35) !important;
        font-weight: 750 !important;
        transform: translateX(3px) !important;
    }
    [class*="st-key-sidebar_nav_"] button[kind="primary"] p,
    [class*="st-key-sidebar_nav_"] button[kind="primary"] span,
    [class*="st-key-sidebar_nav_"] button[data-testid="baseButton-primary"] p,
    [class*="st-key-sidebar_nav_"] button[data-testid="baseButton-primary"] span,
    [class*="st-key-sidebar_nav_"] button[data-testid="stBaseButton-primary"] p,
    [class*="st-key-sidebar_nav_"] button[data-testid="stBaseButton-primary"] span,
    [data-testid="stSidebar"] div[data-testid="stButton"] > button[kind="primary"] p,
    [data-testid="stSidebar"] div[data-testid="stButton"] > button[kind="primary"] span,
    [data-testid="stSidebar"] div.stButton > button[kind="primary"] p,
    [data-testid="stSidebar"] div.stButton > button[kind="primary"] span {
        color: #FFFFFF !important;
    }
    [class*="st-key-sidebar_nav_"] button:active,
    [data-testid="stSidebar"] div[data-testid="stButton"] > button:active,
    [data-testid="stSidebar"] div.stButton > button:active {
        transform: scale(0.98) !important;
    }

    /* Buttons Override (General) */
    .stButton > button {
        border-radius: 10px !important;
        font-weight: 650 !important;
        transition: all 0.18s ease !important;
        font-family: inherit !important;
        background: var(--jg-surface) !important;
        color: var(--jg-ink) !important;
        border: 1px solid var(--jg-border) !important;
    }
    .stButton > button:hover {
        background: var(--jg-surface-hover) !important;
        color: var(--jg-accent) !important;
        border-color: var(--jg-accent) !important;
    }
    .stButton > button[kind="primary"],
    .stButton > button[data-testid="baseButton-primary"] {
        background: var(--jg-accent) !important;
        border-color: var(--jg-accent) !important;
        color: #FFFFFF !important;
        box-shadow: 0 2px 8px rgba(27, 107, 80, 0.25) !important;
    }
    .stButton > button[kind="primary"]:hover,
    .stButton > button[data-testid="baseButton-primary"]:hover {
        background: var(--jg-accent-hover) !important;
        border-color: var(--jg-accent-hover) !important;
        transform: translateY(-1px);
        box-shadow: 0 4px 14px rgba(27, 107, 80, 0.35) !important;
    }

    /* Streamlit Radio Overrides (if used elsewhere) */
    [data-testid="stRadio"] div[role="radiogroup"] > label {
        display: flex !important;
        align-items: center !important;
        width: 100% !important;
        padding: 11px 14px !important;
        margin-bottom: 6px !important;
        border-radius: 10px !important;
        background: var(--jg-surface) !important;
        border: 1px solid var(--jg-border) !important;
        cursor: pointer !important;
        transition: all 0.2s ease !important;
    }
    [data-testid="stRadio"] div[role="radiogroup"] > label:hover {
        background: var(--jg-surface-hover) !important;
        border-color: var(--jg-accent) !important;
        transform: translateX(4px) !important;
    }
    [data-testid="stRadio"] div[role="radiogroup"] > label p,
    [data-testid="stRadio"] div[role="radiogroup"] > label span {
        color: var(--jg-ink) !important;
        font-weight: 600 !important;
        cursor: pointer !important;
    }

    /* Streamlit Expander Overrides */
    [data-testid="stExpander"] {
        background: var(--jg-surface) !important;
        border: 1px solid var(--jg-border) !important;
        border-radius: var(--jg-radius) !important;
        box-shadow: var(--jg-shadow-sm) !important;
        margin-bottom: 12px !important;
    }
    [data-testid="stExpander"] summary {
        background: var(--jg-surface) !important;
        color: var(--jg-ink) !important;
        font-weight: 650 !important;
        border-radius: var(--jg-radius) !important;
    }
    [data-testid="stExpander"] summary:hover {
        background: var(--jg-surface-hover) !important;
        color: var(--jg-accent) !important;
    }
    [data-testid="stExpander"] summary p,
    [data-testid="stExpander"] summary span,
    [data-testid="stExpander"] summary svg {
        color: var(--jg-ink) !important;
        fill: var(--jg-ink) !important;
    }
    [data-testid="stExpanderDetails"] {
        background: var(--jg-surface) !important;
        color: var(--jg-ink) !important;
        border-top: 1px solid var(--jg-border-subtle) !important;
    }

    /* Selectbox, Inputs & Popovers */
    [data-testid="stSelectbox"] label,
    [data-testid="stMultiSelect"] label,
    [data-testid="stTextInput"] label,
    [data-testid="stNumberInput"] label {
        color: var(--jg-ink) !important;
        font-weight: 600 !important;
    }
    div[data-baseweb="select"] > div {
        background-color: var(--jg-surface) !important;
        border-color: var(--jg-border) !important;
        color: var(--jg-ink) !important;
    }
    div[data-baseweb="select"] span,
    div[data-baseweb="select"] div,
    div[data-baseweb="select"] input {
        color: var(--jg-ink) !important;
    }
    div[data-baseweb="popover"],
    ul[role="listbox"] {
        background-color: var(--jg-surface) !important;
        border: 1px solid var(--jg-border) !important;
    }
    li[role="option"] {
        color: var(--jg-ink) !important;
        background-color: var(--jg-surface) !important;
    }
    li[role="option"]:hover,
    li[role="option"][aria-selected="true"] {
        background-color: var(--jg-surface-hover) !important;
        color: var(--jg-accent) !important;
    }

    /* Segmented Control */
    div[data-testid="stSegmentedControl"] {
        background: var(--jg-surface) !important;
        border: 1px solid var(--jg-border) !important;
        border-radius: 10px !important;
    }
    div[data-testid="stSegmentedControl"] button {
        color: var(--jg-ink) !important;
    }
    div[data-testid="stSegmentedControl"] button p,
    div[data-testid="stSegmentedControl"] button span {
        color: var(--jg-ink) !important;
    }

    /* Tabs Override */
    [data-baseweb="tab-list"] {
        background: var(--jg-surface-subtle) !important;
        border-radius: 10px !important;
        padding: 4px !important;
        border: 1px solid var(--jg-border) !important;
    }
    button[data-baseweb="tab"] {
        color: var(--jg-muted) !important;
        font-weight: 600 !important;
        border-radius: 8px !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        background: var(--jg-surface) !important;
        color: var(--jg-accent) !important;
        font-weight: 750 !important;
        box-shadow: var(--jg-shadow-sm) !important;
    }

    /* DataFrames & Tables */
    [data-testid="stDataFrame"], [data-testid="stTable"] {
        background: var(--jg-surface) !important;
        border: 1px solid var(--jg-border) !important;
        border-radius: var(--jg-radius) !important;
        color: var(--jg-ink) !important;
    }

    /* Top Application Bar (Inside Main App) */
    .app-topbar {
        display: flex;
        align-items: center;
        justify-content: space-between;
        background: var(--jg-surface);
        border: 1px solid var(--jg-border);
        border-radius: 12px;
        padding: 10px 16px;
        margin-bottom: 1.4rem;
        box-shadow: var(--jg-shadow-sm);
    }

    /* KPI Cards */
    .kpi-card {
        background: var(--jg-surface);
        border: 1px solid var(--jg-border);
        border-radius: var(--jg-radius);
        padding: 16px 18px;
        box-shadow: var(--jg-shadow);
        height: 100%;
        transition: transform 0.15s ease;
    }
    .kpi-card:hover {
        transform: translateY(-2px);
    }
    .kpi-label {
        font-size: 0.78rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.04em;
        color: var(--jg-muted) !important;
        margin-bottom: 6px;
    }
    .kpi-value {
        font-size: 1.85rem;
        font-weight: 800;
        color: var(--jg-brand) !important;
        line-height: 1.1;
        font-family: 'JetBrains Mono', 'Hind Siliguri', sans-serif;
    }
    .kpi-foot {
        font-size: 0.8rem;
        color: var(--jg-muted) !important;
        margin-top: 6px;
    }

    /* Badges (High Contrast in both Light and Dark Mode) */
    .badge-critical {
        background: var(--jg-alert-high-bg) !important;
        color: var(--jg-alert-high-text) !important;
        border: 1px solid var(--jg-alert-high-border) !important;
        padding: 3px 10px;
        border-radius: 999px;
        font-weight: 750;
        font-size: 0.74rem;
        letter-spacing: 0.03em;
        text-transform: uppercase;
    }
    .badge-high {
        background: var(--jg-alert-med-bg) !important;
        color: #F97316 !important;
        border: 1px solid #EA580C !important;
        padding: 3px 10px;
        border-radius: 999px;
        font-weight: 750;
        font-size: 0.74rem;
        letter-spacing: 0.03em;
        text-transform: uppercase;
    }
    .badge-medium {
        background: var(--jg-alert-med-bg) !important;
        color: var(--jg-alert-med-text) !important;
        border: 1px solid var(--jg-alert-med-border) !important;
        padding: 3px 10px;
        border-radius: 999px;
        font-weight: 750;
        font-size: 0.74rem;
        letter-spacing: 0.03em;
        text-transform: uppercase;
    }
    .badge-low {
        background: rgba(37, 99, 235, 0.18) !important;
        color: #60A5FA !important;
        border: 1px solid #3B82F6 !important;
        padding: 3px 10px;
        border-radius: 999px;
        font-weight: 750;
        font-size: 0.74rem;
        letter-spacing: 0.03em;
        text-transform: uppercase;
    }

    /* Timeline Legend and Items */
    .tl-legend {
        display: flex;
        flex-direction: column;
        gap: 8px;
        margin-top: 14px;
        background: var(--jg-surface);
        border: 1px solid var(--jg-border);
        border-radius: 12px;
        padding: 14px 18px;
        box-shadow: var(--jg-shadow-sm);
    }
    .tl-item {
        display: flex;
        align-items: center;
        gap: 12px;
        font-size: 0.9rem;
        color: var(--jg-ink);
        padding: 4px 0;
        border-bottom: 1px solid var(--jg-border-subtle);
    }
    .tl-item:last-child {
        border-bottom: none;
    }
    .tl-dot {
        width: 12px;
        height: 12px;
        border-radius: 50%;
        flex-shrink: 0;
    }
    .tl-event {
        color: var(--jg-ink) !important;
        font-weight: 600;
        flex: 1;
    }
    </style>
    """
