"""Streamlit presentation layer; authorization is enforced by services."""
import sqlite3
import time
import pandas as pd
import plotly.express as px
import streamlit as st
from ui import apply_styles, chart_style, login_welcome, PALETTE, STATUS_COLORS, INDICATOR_LABELS
from database import init_db, backup_database
from pathlib import Path
from datetime import datetime, timezone
from services import (authenticate, authorize, catalog, records_for, summarize,
                      export_report, save_student, save_subject, save_user,
                      save_record, administration, period_key)

st.set_page_config(page_title='Academic Performance Analytics', page_icon='📊', layout='wide')
apply_styles()
init_db()
st.markdown('<div class="brand-label">Academic insights · SE project</div>', unsafe_allow_html=True)
st.title('Academic Performance Analytics')
st.caption('Understand progress. Identify support needs. Act on evidence.')

if 'principal' not in st.session_state:
    intro, signin = st.columns([1.25, 1], gap='large')
    with intro:
        login_welcome()
    with signin:
        with st.form('login'):
            st.subheader('Welcome back')
            st.caption('Sign in to your academic workspace.')
            username = st.text_input('Username', placeholder='Enter your username')
            password = st.text_input('Password', type='password', placeholder='Enter your password')
            submitted = st.form_submit_button('Sign in', type='primary', width='stretch')
        st.caption('Your account determines which records and tools you can access. Contact your administrator if you need help signing in.')
    if submitted:
        principal = authenticate(username, password)
        if principal:
            st.session_state.principal = principal
            st.session_state.last_activity = time.time()
            st.rerun()
        st.error('Sign-in failed. Check your credentials. After five failed attempts, wait five minutes.')
    st.stop()

if time.time() - st.session_state.get('last_activity', 0) > 1800:
    st.session_state.clear()
    st.rerun()
st.session_state.last_activity = time.time()
p = st.session_state.principal
try:
    user = authorize(p)
except PermissionError:
    st.session_state.clear()
    st.rerun()
st.sidebar.markdown('### Academic insights')
st.sidebar.caption(f"{user['role']} workspace")
st.sidebar.write(f"Signed in as **{user['username']}**")
if st.sidebar.button('Sign out'):
    st.session_state.clear()
    st.rerun()
st.sidebar.caption('Sessions expire after 30 minutes without interaction.')
pages = ['Dashboard']
if user['role'] in ('Admin', 'Faculty'):
    pages += ['Academic data', 'Reports']
if user['role'] == 'Admin':
    pages += ['Administration']
page = st.sidebar.radio('Workspace', pages)
students, subjects = catalog(p)

def handle(action, *args):
    try:
        action(p, *args)
        st.success('Saved successfully. Open the dashboard to see the updated analysis.')
    except (ValueError, PermissionError, sqlite3.IntegrityError) as exc:
        st.error(f'Could not save: {exc}')

def filters(prefix):
    left, right = st.columns(2, gap='medium')
    subject_ids = [None] + subjects.subject_id.tolist()
    sid = left.selectbox('Subject', subject_ids, format_func=lambda v: 'All subjects' if v is None else f"{subjects.loc[subjects.subject_id == v, 'code'].iloc[0]} · {subjects.loc[subjects.subject_id == v, 'name'].iloc[0]}", key=prefix+'subject')
    data = records_for(p, sid)
    periods = sorted(data.period.unique(), key=period_key) if not data.empty else []
    period = right.selectbox('Assessment period', [None] + periods, format_func=lambda v: 'Latest available' if v is None else v, key=prefix+'period')
    return sid, period, data

if page in ('Dashboard', 'Reports'):
    is_student = user['role'] == 'Student'
    st.subheader('Your progress' if is_student else ('Performance reports' if page == 'Reports' else 'Class overview'))
    if is_student and not students.empty:
        profile = students.iloc[0]
        st.write(f"Welcome, **{profile['name']}**. Here is your academic overview.")
        st.caption(f"{profile['program']} · Semester {profile['semester']} · Student ID {profile['student_id']}")
    elif not is_student:
        st.caption('Explore class performance, follow changes over time, and identify where support is needed.')
    subject_id, period, data = filters(page)
    summary = summarize(data, period)
    if summary.empty:
        st.info('No records are available for this selection. Your faculty can help if a record is missing.' if is_student else 'No academic records match this selection. Add a record in Academic data or choose another subject.')
    else:
        c1,c2,c3,c4 = st.columns(4)
        if is_student:
            own = summary.iloc[0]
            c1.metric('Performance score', f'{own.Score:.2f} / 100')
            c2.metric('Attendance', f'{own.Attendance:.1f}%')
            c3.metric('Performance trend', own.Trend)
            c4.metric('Assessment period', own.Period)
            if own.Status == 'Needs Intervention':
                st.warning('Academic support recommended · ' + own.Reasons)
                st.caption('Speak with your faculty about a plan for attendance, revision or assessment preparation.')
            else:
                st.success('On track · No intervention criteria are currently triggered.')
        else:
            c1.metric('Students with records', len(summary))
            c2.metric('Average performance', f'{summary.Score.mean():.2f} / 100')
            c3.metric('Average attendance', f'{summary.Attendance.mean():.1f}%')
            c4.metric('Needs intervention', int((summary.Status == 'Needs Intervention').sum()))
        risk_only = False
        if user['role'] == 'Faculty':
            risk_only = st.checkbox('Show only students who need intervention', key=page+'risk')
        shown = summary[summary.Status == 'Needs Intervention'] if risk_only else summary
        if not is_student:
            st.subheader('Student overview')
            st.dataframe(shown, hide_index=True, width='stretch', column_config={
                'Score': st.column_config.ProgressColumn('Performance / 100', min_value=0, max_value=100, format='%.2f'),
                'Attendance': st.column_config.NumberColumn('Attendance (%)', format='%.1f'),
            })
            if shown.empty:
                st.info('No students meet the intervention criteria in this selection.')
            else:
                st.plotly_chart(chart_style(px.bar(shown, x='Student', y='Score', color='Status', range_y=[0,100], color_discrete_map=STATUS_COLORS), 'Performance by student'), width='stretch')
        st.subheader('Performance over time')
        choices = summary['Student ID'].tolist()
        selected = choices[0] if is_student else st.selectbox('Student', choices, format_func=lambda sid: f"{sid} · {data.loc[data.student_id == sid, 'name'].iloc[0]}")
        history = data[data.student_id == selected].copy()
        if period:
            history = history[history.period.map(lambda v: period_key(v) <= period_key(period))]
        means = history.groupby('period')[['attendance_pct','assignment_score','internal_score','exam_score']].mean().reset_index()
        order = sorted(means.period, key=period_key)
        chart = means.melt(id_vars='period', var_name='Indicator', value_name='Percentage')
        chart['Indicator'] = chart['Indicator'].map(INDICATOR_LABELS)
        st.plotly_chart(chart_style(px.line(chart, x='period', y='Percentage', color='Indicator', markers=True, color_discrete_sequence=PALETTE, category_orders={'period':order}, range_y=[0,100])), width='stretch')
        with st.expander('Assessment details', expanded=is_student):
            history = history.assign(_period_order=history.period.map(period_key)).sort_values(['_period_order','code'])
            st.dataframe(history[['code','period','attendance_pct','assignment_score','internal_score','exam_score']].rename(columns={
                'code':'Subject', 'period':'Period', 'attendance_pct':'Attendance (%)',
                'assignment_score':'Assignment', 'internal_score':'Internal', 'exam_score':'Exam',
            }), hide_index=True, width='stretch')
        if user['role'] in ('Admin','Faculty'):
            st.subheader('Export a report')
            report_student = st.selectbox('Report scope', [None] + choices,
                format_func=lambda sid: 'Class summary' if sid is None else f"{sid} · {data.loc[data.student_id == sid, 'name'].iloc[0]}")
            st.caption('Exports use the selected subject, period, student scope and faculty intervention filter.')
            st.download_button('Download performance report (CSV)', export_report(p, subject_id, period, report_student, risk_only), 'performance-report.csv', 'text/csv', type='primary')
    with st.expander('How performance is calculated'):
        st.write('Score: 40% examination + 25% assignment + 20% attendance + 15% internal assessment. Subjects are equally weighted within each period.')
        st.write('Support is recommended if the score is below 50, attendance is below 75%, or performance falls by at least 10 points compared with the previous available period.')
        st.caption('These are project assumptions, not institutional policy. When using the latest available period, students may have different assessment periods.')

elif page == 'Academic data':
    st.subheader('Record attendance and marks')
    st.caption('Choose a student, subject and period. Existing marks load for review before you save. Every change is audited.')
    if students.empty or subjects.empty:
        st.info('Ask an administrator to add students and subjects first.')
    else:
        c1,c2,c3 = st.columns(3)
        student = c1.selectbox('Student', students.student_id.tolist(), format_func=lambda v: f"{v} · {students.loc[students.student_id == v, 'name'].iloc[0]}")
        subject = c2.selectbox('Subject', subjects.subject_id.tolist(), format_func=lambda v: subjects.loc[subjects.subject_id == v,'code'].iloc[0])
        period = c3.text_input('Period (P1, P2, …)', 'P1').strip().upper()
        existing = records_for(p, subject, period)
        existing = existing[existing.student_id == student]
        saved = existing.iloc[0] if not existing.empty else None
        if saved is not None:
            st.info(f"Editing an existing record · Attendance {saved.attendance_pct:.1f}% · Assignment {saved.assignment_score:.1f} · Internal {saved.internal_score:.1f} · Exam {saved.exam_score:.1f}")
        else:
            st.caption('New academic record')
        entry_key = f'{student}-{subject}-{period}'
        attendance_mode = st.radio('Enter attendance using', ['Class counts','Percentage'],
                                   index=1 if saved is not None else 0, horizontal=True, key='attendance-'+entry_key)
        with st.form('record-'+entry_key+'-'+attendance_mode):
            st.markdown('#### Attendance')
            if attendance_mode == 'Class counts':
                c1,c2 = st.columns(2)
                attended = c1.number_input('Classes attended', min_value=0, value=0)
                total = c2.number_input('Classes conducted', min_value=1, value=1)
                st.caption('Attendance is calculated as attended ÷ conducted × 100. The percentage is stored in the record.')
            else:
                attended = st.number_input('Attendance (%)', min_value=0.0, max_value=100.0,
                                           value=float(saved.attendance_pct) if saved is not None else 0.0)
                total = 100
            st.markdown('#### Assessment marks')
            c1,c2,c3 = st.columns(3)
            assignment = c1.number_input('Assignment / 100', min_value=0.0, max_value=100.0, value=float(saved.assignment_score) if saved is not None else 0.0)
            internal = c2.number_input('Internal / 100', min_value=0.0, max_value=100.0, value=float(saved.internal_score) if saved is not None else 0.0)
            exam = c3.number_input('Exam / 100', min_value=0.0, max_value=100.0, value=float(saved.exam_score) if saved is not None else 0.0)
            if st.form_submit_button('Save academic record', type='primary'):
                handle(save_record, student, subject, period, attended, total, assignment, internal, exam)

elif page == 'Administration':
    st.subheader('Administration')
    tabs = st.tabs(['Students','Subjects','Accounts','Audit and backup'])
    with tabs[0]:
        st.dataframe(students, hide_index=True)
        with st.form('student'):
            sid = st.number_input('Student ID (existing ID updates profile)', min_value=1, step=1)
            name = st.text_input('Student name')
            program = st.text_input('Program', 'CSE')
            semester = st.number_input('Semester', min_value=1, max_value=12, step=1)
            if st.form_submit_button('Save student'):
                handle(save_student, sid, name, program, semester)
    with tabs[1]:
        st.dataframe(subjects, hide_index=True)
        with st.form('subject'):
            sid = st.number_input('Subject ID (existing ID updates subject)', min_value=1, step=1)
            code = st.text_input('Subject code')
            name = st.text_input('Subject name')
            if st.form_submit_button('Save subject'):
                handle(save_subject, sid, code, name)
    accounts, audit = administration(p)
    with tabs[2]:
        st.dataframe(accounts, hide_index=True)
        with st.form('account'):
            username = st.text_input('Account username')
            password = st.text_input('New password (at least 10 characters)', type='password')
            role = st.selectbox('Account role', ['Student','Faculty','Admin'])
            student = st.selectbox('Linked student (required for Student role)', [None] + students.student_id.tolist())
            active = st.checkbox('Account active', value=True)
            if st.form_submit_button('Save account / reset password'):
                handle(save_user, username, password, role, student, active)
    with tabs[3]:
        st.dataframe(audit, hide_index=True, width='stretch')
        st.caption('Latest 200 changes. Backups contain account hashes and academic records; keep them private.')
        if st.button('Create local database backup'):
            authorize(p, ('Admin',))
            destination = Path(__file__).parent / 'backups' / (datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ') + '.db')
            backup_database(destination)
            st.success(f'Backup saved: {destination.name}')
