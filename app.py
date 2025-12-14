# app.py - Updated Flask App for Full Church Management System Dashboard

from flask import Flask, render_template
import sqlite3
import pandas as pd
from database import init_db  # Assuming database.py from previous

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('chms.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    return render_template('home.html')  

@app.route('/dashboard')
def dashboard():
    conn = get_db_connection()
    
    # Pledge Progress (from previous)
    df_pledge = pd.read_sql_query('''
        SELECT 
            m.id,
            m.first_name || ' ' || m.last_name AS member,
            p.pledged_amount,
            COALESCE(SUM(c.amount), 0) AS given,
            ROUND(COALESCE(SUM(c.amount), 0) * 100.0 / p.pledged_amount, 1) AS pct
        FROM pledges p
        JOIN members m ON p.member_id = m.id
        JOIN pledge_campaigns pc ON p.campaign_id = pc.id
        LEFT JOIN contributions c ON c.member_id = m.id 
            AND c.contribution_date BETWEEN '2025-01-01' AND '2025-12-14'  -- Updated to Dec 14
            AND c.fund_id = 1
        WHERE pc.year = 2025
        GROUP BY m.id, p.pledged_amount
        ORDER BY pct DESC
    ''', conn)

    members_pledge = df_pledge.to_dict('records')
    total_pledged = df_pledge['pledged_amount'].sum()
    total_given = df_pledge['given'].sum()
    overall_pct = round(total_given / total_pledged * 100, 1) if total_pledged > 0 else 0

    # Sample for other visuals (simulate data since not all tables exist yet)
    # Demographics (simulate)
    demographics = {'Male': 45, 'Female': 55, 'Other': 0}
    # Attendance Trends (simulate monthly)
    attendance = {'Jan': 150, 'Feb': 160, 'Mar': 170, 'Apr': 165, 'May': 180, 'Jun': 190, 'Jul': 185, 'Aug': 200, 'Sep': 210, 'Oct': 220, 'Nov': 215, 'Dec': 225}
    # Donation Trends (from DB)
    df_donations = pd.read_sql_query('''
        SELECT strftime('%m', contribution_date) AS month, SUM(amount) AS total
        FROM contributions
        WHERE contribution_date BETWEEN '2025-01-01' AND '2025-12-14'
        GROUP BY month
    ''', conn)
    donation_trends = dict(zip(df_donations['month'], df_donations['total']))

    conn.close()
    return render_template('dashboard.html',
                           members_pledge=members_pledge,
                           total_pledged=total_pledged,
                           total_given=total_given,
                           overall_pct=overall_pct,
                           demographics=demographics,
                           attendance=attendance,
                           donation_trends=donation_trends)

@app.route('/members')
def members():
    conn = get_db_connection()
    members = conn.execute('SELECT id, first_name, last_name, email FROM members').fetchall()
    # Simulate groups and attendance
    sample_groups = {'Small Group': 20, 'Youth': 15, 'Choir': 10, 'Ushers': 8}
    sample_age_dist = {'0-18': 25, '19-35': 30, '36-50': 20, '51+': 25}
    conn.close()
    return render_template('members.html',
                           members=members,
                           sample_groups=sample_groups,
                           sample_age_dist=sample_age_dist)

@app.route('/member/<int:member_id>')
def member_detail(member_id):
    conn = get_db_connection()
    member = conn.execute('SELECT * FROM members WHERE id = ?', (member_id,)).fetchone()
    if not member:
        return "Member not found", 404

    # Pledge (updated date)
    pledge_row = conn.execute('''
        SELECT p.pledged_amount,
               COALESCE(SUM(c.amount), 0) AS given
        FROM pledges p
        LEFT JOIN contributions c ON c.member_id = p.member_id
            AND c.contribution_date BETWEEN '2025-01-01' AND '2025-12-14'
            AND c.fund_id = 1
        WHERE p.member_id = ? AND p.campaign_id = 1
    ''', (member_id,)).fetchone()

    pledged = pledge_row['pledged_amount'] if pledge_row else 0
    given = pledge_row['given'] if pledge_row else 0
    pct = round(given / pledged * 100, 1) if pledged else 0

    contributions = conn.execute('''
        SELECT c.contribution_date, f.name AS fund, c.amount, c.payment_method, c.memo
        FROM contributions c
        JOIN funds f ON c.fund_id = f.id
        WHERE c.member_id = ?
        ORDER BY c.contribution_date DESC
    ''', (member_id,)).fetchall()

    # Simulate attendance and groups
    sample_attendance = {'Service 1': 'Present', 'Service 2': 'Absent', 'Event': 'Present'}
    sample_member_groups = ['Small Group Leader', 'Volunteer Usher']

    conn.close()
    return render_template('member_detail.html',
                           member=member,
                           pledged=pledged,
                           given=given,
                           pct=pct,
                           contributions=contributions,
                           sample_attendance=sample_attendance,
                           sample_member_groups=sample_member_groups)

@app.route('/events')
def events():
    # Simulate events data (add table in future)
    sample_events = [
        {'title': 'Sunday Service', 'date': '2025-12-15', 'attendees': 200, 'capacity': 250},
        {'title': 'Youth Camp', 'date': '2025-12-20', 'attendees': 50, 'capacity': 60},
        {'title': 'Christmas Event', 'date': '2025-12-25', 'attendees': 300, 'capacity': 300}
    ]
    sample_registration = {'Registered': 80, 'Attended': 70, 'No-Show': 10}
    conn = get_db_connection()
    conn.close()
    return render_template('events.html',
                           sample_events=sample_events,
                           sample_registration=sample_registration)

@app.route('/finances')
def finances():
    conn = get_db_connection()
    df_contributions = pd.read_sql_query('''
        SELECT f.name AS fund, SUM(c.amount) AS total
        FROM contributions c
        JOIN funds f ON c.fund_id = f.id
        WHERE c.contribution_date BETWEEN '2025-01-01' AND '2025-12-14'
        GROUP BY f.id
    ''', conn)
    fund_distribution = dict(zip(df_contributions['fund'], df_contributions['total']))

    # Simulate expenses
    expenses = {'Salaries': 5000, 'Utilities': 2000, 'Supplies': 1000, 'Missions': 3000}

    conn.close()
    return render_template('finances.html',
                           fund_distribution=fund_distribution,
                           expenses=expenses)

@app.route('/volunteers')
def volunteers():
    # Simulate data
    sample_volunteers = [
        {'name': 'John Johnson', 'role': 'Usher', 'hours': 20},
        {'name': 'Mike Garcia', 'role': 'Group Leader', 'hours': 15}
    ]
    sample_availability = {'Mon': 5, 'Tue': 3, 'Wed': 8, 'Thu': 4, 'Fri': 2, 'Sat': 10, 'Sun': 15}
    return render_template('volunteers.html',
                           sample_volunteers=sample_volunteers,
                           sample_availability=sample_availability)

@app.route('/communication')
def communication():
    # Simulate
    sample_campaigns = {'Newsletter': {'sent': 500, 'opened': 350, 'clicked': 100},
                        'Prayer Chain': {'sent': 200, 'opened': 180, 'clicked': 50}}
    return render_template('communication.html', sample_campaigns=sample_campaigns)

@app.route('/child_ministry')
def child_ministry():
    # Simulate
    sample_age_groups = {'0-5': 20, '6-12': 30, '13-18': 25}
    sample_attendance = 85  # %
    return render_template('child_ministry.html',
                           sample_age_groups=sample_age_groups,
                           sample_attendance=sample_attendance)

@app.route('/reports')
def reports():
    # Simulate KPIs
    kpis = {'Total Members': 100, 'YTD Donations': 25000, 'Average Attendance': 180, 'Volunteer Hours': 500}
    return render_template('reports.html', kpis=kpis)

from database import init_db

init_db()  # runs once at startup

if __name__ == "__main__":
    app.run()
