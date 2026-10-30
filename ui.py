"""Shared presentation styles and chart defaults; no database or authorization logic."""
import streamlit as st

PALETTE = ['#087F8C', '#5165AE', '#C98A24', '#A85F83']
STATUS_COLORS = {'Normal': '#087F8C', 'Needs Intervention': '#BA563F'}
INDICATOR_LABELS = {
    'attendance_pct': 'Attendance', 'assignment_score': 'Assignment',
    'internal_score': 'Internal assessment', 'exam_score': 'Examination',
}


def apply_styles():
    # Static application CSS only; never interpolate user-provided content here.
    st.markdown('''<style>
      .stApp {background: #f5f7fa;}
      .block-container {max-width: 1440px; padding-top: 2.5rem; padding-bottom: 3rem;}
      h1, h2, h3 {letter-spacing: -.035em; color: #172b45;}
      h1 {font-weight: 750 !important;}
      [data-testid="stSidebar"] {background: #eaf0f5; border-right: 1px solid #dbe3ec;}
      [data-testid="stSidebar"] .block-container {padding-top: 2rem;}
      [data-testid="stMetric"] {background: white; border: 1px solid #e1e8ef;
        border-radius: 16px; padding: 1.15rem 1.25rem; min-height: 120px;
        box-shadow: 0 4px 16px rgba(23,43,69,.025);}
      [data-testid="stMetricLabel"] {color: #52657a;}
      [data-testid="stMetricValue"] {color: #172b45; font-weight: 700;}
      [data-testid="stForm"] {background: white; padding: 1.5rem;
        border: 1px solid #e1e8ef; border-radius: 18px;}
      [data-testid="stPlotlyChart"], [data-testid="stDataFrame"] {
        border-radius: 16px; overflow: hidden;}
      .stButton > button, .stDownloadButton > button {border-radius: 10px; font-weight: 600;}
      [data-testid="stCaptionContainer"] {color: #52657a;}
      .brand-label {font-size: .75rem; font-weight: 750; letter-spacing: .16em;
        text-transform: uppercase; color: #087f8c; margin-bottom: .7rem;}
      .welcome-panel {border-radius: 22px; padding: 2.3rem; margin-bottom: 1rem;
        background: linear-gradient(130deg,#172b45,#145765); color: #fff;}
      .welcome-panel h2 {color: white; font-size: 2.2rem; line-height: 1.15; margin-bottom: 1rem;}
      .welcome-panel p {color: #e2f0f3; line-height: 1.8; max-width: 36rem;}
      .welcome-panel .eyebrow {color: #9ed9d7; font-size: .75rem; letter-spacing: .13em;
        font-weight: 700; text-transform: uppercase;}
      .welcome-panel .feature {padding-top: .9rem; border-top: 1px solid #ffffff25; margin-top: .9rem;}
      @media (max-width: 700px) {
        .block-container {padding: 1.5rem 1rem;}
        .welcome-panel {padding: 1.5rem;}
        .welcome-panel h2 {font-size: 1.7rem;}
        [data-testid="stMetric"] {min-height: 100px; padding: .9rem;}
      }
    </style>''', unsafe_allow_html=True)


def chart_style(figure, title=None):
    figure.update_layout(
        title=dict(text=title, font=dict(size=18)) if title else None,
        paper_bgcolor='#ffffff', plot_bgcolor='#ffffff',
        font=dict(family='Arial, sans-serif', color='#52657A', size=13),
        margin=dict(l=25, r=25, t=65 if title else 25, b=30),
        legend=dict(title=None, orientation='h', y=-.2, x=0),
        hovermode='closest', height=355,
    )
    figure.update_yaxes(gridcolor='#EDF1F5', zeroline=False)
    figure.update_xaxes(showgrid=False, title=None)
    return figure


def login_welcome():
    st.markdown('''<div class="welcome-panel">
      <div class="eyebrow">A clearer view of academic progress</div>
      <h2>Every assessment.<br>One connected picture.</h2>
      <p>Follow progress across subjects, understand performance trends,
      and find the right moment for academic support.</p>
      <div class="feature"><strong>Students</strong><br>Understand your progress and what to focus on next.</div>
      <div class="feature"><strong>Faculty</strong><br>Turn class insights into timely support.</div>
      <div class="feature"><strong>Administrators</strong><br>Keep academic records organized and accountable.</div>
    </div>''', unsafe_allow_html=True)
