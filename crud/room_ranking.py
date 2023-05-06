import math

from sqlalchemy import text
from sqlalchemy.orm import Session

BASE = 6


def get_active_secs_query(room_id, count):
    query = f"""
    select duration_sec from room_ignition
    where room_id = '{room_id}' 
    and user_count={count}
    """

    return query


def get_update_ranking_query(room_id, score):
    query = f"""
    update room
    set ranking_score = {score}
    where id='{room_id}'
    """

    return query


def get_report_count(room_id, db):
    query = f"""
    select count(id) from report
    where room_id='{room_id}' 
    and accepted=true
    """

    report_cnt = db.execute(text(query)).scalar()

    return max(1, report_cnt)


def calc_room_rating(active_secs, count):
    return (count - 1) * pow(1.2, count - 1) * math.log(active_secs, BASE - count)


def update_room_ranking(db: Session):
    rooms_q = db.execute(text('select room_id, user_count from room_ignition'))

    room_scores = {}

    for room_id, cnt in rooms_q:
        query = get_active_secs_query(room_id, cnt)
        active_secs = db.execute(text(query)).scalar()

        room_scores[room_id] = room_scores.get(room_id, 0) + calc_room_rating(active_secs, cnt)

    for room_id, score in room_scores.items():
        report_cnt = get_report_count(room_id, db)
        score -= math.log2(report_cnt)

        query = get_update_ranking_query(room_id, score)
        db.execute(text(query))
        db.commit()

    print("ROOM RATING UPDATE COMPLETE")
