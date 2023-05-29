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


def is_recommendable(db: Session, user_id: str, check_id: str):
    # None type

    none_query = f"""
    select exists (
    select 1 from friend
    where (requester_id='{user_id}' and acceptor_id='{check_id}') or
          (requester_id='{check_id}' and acceptor_id='{user_id}')
    )
    """

    if not db.execute(text(none_query)).scalar():
        return True, "NONE"

    friend_query_1 = f"""
    select accepted from friend
    where '{user_id}' in (select distinct requester_id from friend)
    and '{check_id}' in (select distinct acceptor_id from friend)
    and requester_id = '{user_id}'
    and acceptor_id = '{check_id}'
    """

    friend_query_2 = f"""
    select accepted from friend
    where '{check_id}' in (select distinct requester_id from friend)
    and '{user_id}' in (select distinct acceptor_id from friend)
    and requester_id = '{check_id}'
    and acceptor_id = '{user_id}'
    """

    result_1 = db.execute(text(friend_query_1)).scalar() or False
    result_2 = db.execute(text(friend_query_2)).scalar() or False

    if result_1 | result_2:
        return False, ""

    # Requested : 내가 보낸적 있냐
    request_query = f"""
    select exists (
        select accepted from friend
        where requester_id='{user_id}'
          and acceptor_id='{check_id}'
    )
    """

    request_result = db.execute(text(request_query)).scalar()
    if request_result:
        return False, ""

    return True, "REQUEST_RECEIVED"


def get_users_all_tag(db: Session, user_id=None):
    query_tag = f"""
    select user_id, name from user_tag
    join tag t on user_tag.tag_id = t.id
    """

    if user_id:
        query_tag += f"""
        where user_id='{user_id}'
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
