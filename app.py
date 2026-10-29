"""Streamlit presentation layer; authorization is enforced by services."""
import sqlite3
import time
import pandas as pd
import plotly.express as px
import streamlit as st
from database import init_db, backup_database
from pathlib import Path
from datetime import datetime, timezone
from services import (authenticate, authorize, catalog, records_for, summarize,
                      export_report, save_student, save_subject, save_user,
                      save_record, administration, period_key)

st.set_page_config(page_title='Academic Performance Analytics', page_icon='📊', layout='wide')
init_db()
st.title('Academic Performance Analytics')
st.caption('Understand progress. Identify support needs. Act on evidence.')

if 'principal' not in st.session_state:
    with st.form('login'):
        st.subheader('Sign in')
        username = st.text_input('Username')
        password = st.text_input('Password', type='password')
        submitted = st.form_submit_button('Sign in', type='primary')
    if submitted:
        principal = authenticate(username, password)
        if principal:
            st.session_state.principal = principal
            st.session_state.last_activity = time.time()
            st.rerun()
        st.error('Sign-in failed. Check your credentials. After five failed attempts, wait five minutes.')
    st.info('For the local demonstration, run the seed script and use one of its generated accounts.')
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
st.sidebar.write(f"**{user['username']}** · {user['role']}")
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
    subject_ids = [None] + subjects.subject_id.tolist()
    sid = st.selectbox('Subject', subject_ids, format_func=lambda v: 'All subjects' if v is None else f"{subjects.loc[subjects.subject_id == v, 'code'].iloc[0]} · {subjects.loc[subjects.subject_id == v, 'name'].iloc[0]}", key=prefix+'subject')
    data = records_for(p, sid)
    periods = sorted(data.period.unique(), key=period_key) if not data.empty else []
    period = st.selectbox('Assessment period', [None] + periods, format_func=lambda v: 'Latest available per student' if v is None else v, key=prefix+'period')
    return sid, period, data

if page in ('Dashboard', 'Reports'):
    st.subheader('Your progress' if user['role'] == 'Student' else 'Class performance')
    subject_id, period, data = filters(page)
    summary = summarize(data, period)
    if summary.empty:
        st.info('No academic records match this selection. Faculty can add records in Academic data.')
    else:
        c1,c2,c3,c4 = st.columns(4)
        c1.metric('Students with records', len(summary))
        c2.metric('Average performance', f'{summary.Score.mean():.2f} / 100')
        c3.metric('Average attendance', f'{summary.Attendance.mean():.1f}%')
        c4.metric('Needs intervention', int((summary.Status == 'Needs Intervention').sum()))
        risk_only = st.checkbox('Show only students who need intervention')
        shown = summary[summary.Status == 'Needs Intervention'] if risk_only else summary
        st.dataframe(shown, hide_index=True, width='stretch')
        st.plotly_chart(px.bar(shown, x='Student', y='Score', color='Status', range_y=[0,100], color_discrete_map={'Normal':'#16816a','Needs Intervention':'#c04b37'}), width='stretch')
        st.subheader('Performance over time')
        choices = sorted(data.student_id.unique())
        selected = st.selectbox('Student', choices, format_func=lambda sid: f"{sid} · {data.loc[data.student_id == sid, 'name'].iloc[0]}")
        history = data[data.student_id == selected].copy()
        if period:
            history = history[history.period.map(lambda v: period_key(v) <= period_key(period))]
        means = history.groupby('period')[['attendance_pct','assignment_score','internal_score','exam_score']].mean().reset_index()
        order = sorted(means.period, key=period_key)
        chart = means.melt(id_vars='period', var_name='Indicator', value_name='Percentage')
        st.plotly_chart(px.line(chart, x='period', y='Percentage', color='Indicator', markers=True, category_orders={'period':order}, range_y=[0,100]), width='stretch')
        st.dataframe(history[['code','period','attendance_pct','assignment_score','internal_score','exam_score']], hide_index=True, width='stretch')
        if user['role'] in ('Admin','Faculty'):
            st.download_button('Download performance report (CSV)', export_report(p, subject_id, period), 'performance-report.csv', 'text/csv')
    st.caption('Score: 40% exam + 25% assignment + 20% attendance + 15% internal. Subjects are equally weighted within each period. Risk: score < 50, attendance < 75%, or decline of at least 10 points. These are project assumptions, not institutional policy.')

elif page == 'Academic data':
    st.subheader('Record attendance and marks')
    st.write('Save updates an existing student, subject and period combination. All changes are audited.')
    if students.empty or subjects.empty:
        st.info('Ask an administrator to add students and subjects first.')
    else:
        with st.form('record'):
            student = st.selectbox('Student', students.student_id.tolist(), format_func=lambda v: f"{v} · {students.loc[students.student_id == v, 'name'].iloc[0]}")
            subject = st.selectbox('Subject', subjects.subject_id.tolist(), format_func=lambda v: subjects.loc[subjects.subject_id == v,'code'].iloc[0])
            period = st.text_input('Period (P1, P2, …)', 'P1')
            c1,c2 = st.columns(2)
            attended = c1.number_input('Classes attended', min_value=0, value=8)
            total = c2.number_input('Classes conducted', min_value=1, value=10)
            c1,c2,c3 = st.columns(3)
            assignment = c1.number_input('Assignment / 100', min_value=0.0, max_value=100.0, value=80.0)
            internal = c2.number_input('Internal / 100', min_value=0.0, max_value=100.0, value=80.0)
            exam = c3.number_input('Exam / 100', min_value=0.0, max_value=100.0, value=80.0)
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
