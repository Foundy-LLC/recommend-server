from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from crud.room_ranking import update_room_ranking
from db.connection import connect_db

router = APIRouter(
    prefix="/room_rec",  # url 앞에 고정적으로 붙는 경로추가
)  # Route 분리


@router.get("")  # Route Path
def index(db: Session = Depends(connect_db)):
    update_room_ranking(db=db)
