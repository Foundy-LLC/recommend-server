import math

from sqlalchemy import text


def get_yesterday_studied_time(user_id, db):
    """
    user_id 를 통해 해당 유저의 하루 전 공부 시간을 계산하여 리턴합니다.

    :param user_id: user_id from study_history
    :param db: Session db
    :return: int
    """

    query = f"""
    SELECT EXTRACT(EPOCH FROM SUM(exit_at - join_at)) AS total_study_time_seconds
    FROM study_history
    WHERE DATE_TRUNC('day', join_at) = DATE_TRUNC('day', CURRENT_DATE - INTERVAL '1 day')
    and user_id='{user_id}'
    """

    studied_time = db.execute(text(query)).scalar()
    studied_time = max(studied_time, 0)

    return studied_time


def get_report_count(user_id, db):
    """
    해당 유저의 하루 전 신고기록을 조회합니다.

    :param user_id: user_id from report
    :param db: Session db
    :return: report count (int)
    """
    query = f"""
    SELECT COUNT(*) AS report_count
    FROM report
    WHERE DATE_TRUNC('day', reported_at) = DATE_TRUNC('day', CURRENT_DATE - INTERVAL '1 day')
      AND suspect_id = '{user_id}'
      AND accepted = true
    """

    report_cnt = db.execute(text(query)).scalar()

    return report_cnt


def get_days_row_cnt(user_id, db):  # runs on every Sunday
    query = f"""
    select days_row
    from user_ranking
    where user_id = '{user_id}'
    """

    row_cnt = db.execute(text(query)).scalar()
    return row_cnt


def reset_weekly_study_time(user_id, db):
    """
    해당 유저의 weekly_study_time 및 weekly_score 를 초기화합니다.

    해당 쿼리는 매 월요일 09시에 실행됩니다.

    :paramauser_id: user_id from user_ranking
    :param db: Session - DB
    :return: None
    """

    query = f"""
    update user_ranking
    set weekly_study_time = 0, weekly_score = 0
    where user_id = '{user_id}' 
    """

    db.execute(text(query))
    db.commit()


def update_user_rating(user_id, db):
    """
    전날의 기록으로 해당 유저의 점수를 업데이트합니다.

    weekly_score 및 total_score 를 업데이트합니다.

    해당 쿼리는 매일 09시마다 돌아가게 됩니다.

    :param user_id: user_id from user_ranking
    :param db: Session DB
    :return: None
    """
    studied_time = get_yesterday_studied_time(user_id, db)

    if studied_time > 0:
        query = f"""
        update user_ranking
        set weekly_study_time = weekly_study_time + {studied_time},
        total_study_time = total_study_time + {studied_time} 
        where user_id='{user_id}'
        """

        db.execute(text(query))

        query = f"""
            update user_ranking
            set days_row = days_row + 1
            where user_id = '{user_id}'
            """

        db.execute(text(query))

    days_row = get_days_row_cnt(user_id, db)
    report = get_report_count(user_id, db)

    score = math.sqrt(studied_time) + pow(1.5, days_row) - pow(2, report)
    score = max(score, 0)

    query = f"""
    update user_ranking
    set weekly_score = sqrt(weekly_score) + {score},
    total_score = total_score + weekly_score
    where user_id = '{user_id}'
    """

    db.execute(text(query))
    db.commit()
