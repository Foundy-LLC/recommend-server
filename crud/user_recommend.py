from collections import defaultdict

from sqlalchemy import text
from sqlalchemy.orm import Session


def get_my_tag_vector(db: Session, user_id: str):
    query = f"""
    select tag_vec->'item' from user_account
    where id = '{user_id}'
    """

    vector = db.execute(text(query)).scalar()
    return vector


def get_users_tag_vector(db: Session, user_id: str):
    query = f"""
    select id, name, profile_image, introduce, status, tag_vec->'item' from user_account
    where tag_vec -> 'item' is not null
    and id != '{user_id}'
    """

    rows = db.execute(text(query)).fetchall()
    return rows


def is_friend(db: Session, user_id: str, check_id: str):
    query = f"""
    select exists (
        select accepted from friend
        where requester_id='{user_id}'
        and acceptor_id='{check_id}'
    )
    """

    result = db.execute(text(query)).scalar()
    return result


def get_users_all_tag(db: Session):
    query_tag = f"""
    select user_id, name from user_tag
    join tag t on user_tag.tag_id = t.id
    """

    result = db.execute(text(query_tag))

    users_tag = defaultdict(list)

    for row in result:
        user_id, tag = row
        users_tag[user_id].append(tag)

    return users_tag


def insert_user_vector(db: Session, user, vector):
    query = f"""
    update user_account
    set tag_vec = '{{"item" : {vector}}}'
    where id='{user}'
    """

    db.execute(text(query))
    db.commit()
