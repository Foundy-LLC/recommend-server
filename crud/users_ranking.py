from datetime import datetime

import pytz
from sqlalchemy import text


def get_report_count(user_id, db):
    query = f"""
    select count(id) from report
    where suspect_id='{user_id}' 
    and accepted=true
    """

    report_cnt = db.execute(text(query)).scalar()

    return report_cnt


def get_days_row_cnt(user_id, db):  # runs on every Sunday
    today = datetime.now()
    today_utc = today.astimezone(pytz.utc).strftime("%Y-%m-%d")

    query = f"""
    WITH inquiry as (
        SELECT
        user_id, DATE_TRUNC('week', join_at)::date+7 AS weeks,\
        COUNT(DISTINCT DATE_TRUNC('day', join_at)) AS row_days
        FROM study_history
        WHERE EXTRACT(DOW FROM join_at) >= 1 AND EXTRACT(DOW FROM join_at) <= 7
        GROUP BY user_id, DATE_TRUNC('week', join_at))
    
    select row_days from inquiry
    where user_id='{user_id}'
    and weeks like '{today_utc}%'
    """

    row_cnt = db.execute(text(query)).scalar()
    return row_cnt


def get_weekly_study_time(user_id, db):
    today = datetime.now()
    today_utc = today.astimezone(pytz.utc).strftime("%Y-%m-%d")

    query = f"""
    with inquiry as (
        SELECT user_id,
        DATE_TRUNC('week', join_at)::date+7 AS week_start,
        SUM(EXTRACT(EPOCH FROM (exit_at - join_at))) AS study_time_seconds
        FROM study_history
        WHERE EXTRACT(DOW FROM join_at) >= 1 AND EXTRACT(DOW FROM join_at) <= 7
          AND exit_at IS NOT NULL
        GROUP BY user_id, DATE_TRUNC('week', join_at))
        
    select study_time_seconds from inquiry
    where user_id='{user_id}'
    week_start like '{today_utc}%'
    """

    study_time = db.execute(text(query)).scalar()
    return study_time


def get_report_cnt():
    pass
