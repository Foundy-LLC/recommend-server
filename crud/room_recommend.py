from collections import defaultdict

from sqlalchemy import text
from sqlalchemy.orm import Session


def get_rooms_info(db: Session):
    query_tag = f"""
    select room_tag.room_id, t.name from room_tag 
    join tag t on room_tag.tag_id = t.id
    """

    result = db.execute(text(query_tag))

    rooms_info = defaultdict(list)

    for row in result:
        room_id, tag = row
        rooms_info[room_id].append(tag)

    query_title = """
    select id, title from room
    """

    result = db.execute(text(query_title))

    for row in result:
        room_id, title = row
        rooms_info[room_id].append(title)

    return rooms_info


def insert_room_vector(db: Session, room, vector):
    query = f"""
    update room
    set room_vec = '{{"item" : {vector}}}'
    where id='{room}'
    """

    db.execute(text(query))
    db.commit()
