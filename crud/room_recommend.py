from collections import defaultdict

from sqlalchemy import text
from sqlalchemy.orm import Session

from core.user_overview import UserOverview


def get_rooms_vector(db: Session):
    query = """
    select id, title, room.master_id,
    case when password is not null then true else false end as hasPassword,
    thumbnail, room_vec->'item'
    from room
    where deleted_at is null
    and room_vec is not null
    """

    rooms = db.execute(text(query)).fetchall()

    rooms_info = defaultdict(list)

    for room in rooms:
        room_id, title, master_id, has_password, thumbnail, vec = room
        studying_users = get_studying_users(db, room_id)
        room_tags = get_rooms_tag(db, room_id)

        overview_list = []
        for user in studying_users:
            user_id, name, introduce, profile_image, status = user
            user_overview = UserOverview(user_id, name, profile_image, introduce, status)
            overview_list.append(user_overview)

        rooms_info[room_id] = [title, master_id, has_password, thumbnail, vec, overview_list, room_tags]

    return rooms_info


def get_rooms_tag(db: Session, room_id):
    query_tag = f"""
    select t.name from room_tag 
    join tag t on room_tag.tag_id = t.id
    where room_id='{room_id}'
    """

    tags = []
    result = db.execute(text(query_tag)).scalars()

    for tag in result:
        tags.append(tag)
    return tags


def get_studying_users(db: Session, room_id):
    query = f"""
    select user_id, name, introduce, profile_image, status from
        (select user_id
        from study_history
        join room r on study_history.room_id = r.id
        where exit_at is null
        and room_id='{room_id}') as joined
    join user_account on user_id = user_account.id
    """

    results = db.execute(text(query))

    return results


def get_rooms_info(db: Session):
    query_title = """
    select id, title from room
    """
    result = db.execute(text(query_title))

    rooms_info = defaultdict(list)

    for row in result:
        room_id, title = row
        rooms_info[room_id].append(title)

    query_tag = f"""
    select room_tag.room_id, t.name from room_tag 
    join tag t on room_tag.tag_id = t.id
    """

    result = db.execute(text(query_tag))

    for row in result:
        room_id, tag = row
        rooms_info[room_id].append(tag)
    return rooms_info


def insert_room_vector(db: Session, room, vector):
    query = f"""
    update room
    set room_vec = '{{"item" : {vector}}}'
    where id='{room}'
    """

    db.execute(text(query))
    db.commit()
