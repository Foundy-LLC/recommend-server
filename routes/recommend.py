from fastapi import APIRouter, Depends, responses

from apis.recommend import *
from db.connection import connect_db

router = APIRouter(
    prefix="/users",  # url 앞에 고정적으로 붙는 경로추가
)  # Route 분리


@router.get("/{user_id}/recommended-friends")
def recommend_users(user_id: str, db: Session = Depends(connect_db)):
    status, res = get_recommended_friends(db, user_id)

    return responses.JSONResponse(status_code=status, content=res)


@router.get("{user_id}/recommended-rooms")
def recommend_rooms(user_id: str, db: Session = Depends(connect_db)):
    status, res = get_recommended_rooms(db, user_id)

    return responses.JSONResponse(status_code=status, content=res)


@router.get("update-room-vec")
def index(db: Session = Depends(connect_db), model=model):
    update_rooms_vector(db, model)
