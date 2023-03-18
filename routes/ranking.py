from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from apis import ranking
from db.connection import get_db

router = APIRouter(
    prefix="/ranking",  # url 앞에 고정적으로 붙는 경로추가
)  # Route 분리


@router.get("/")  # Route Path
def ranking_index(db: Session = Depends(get_db)):
    res = ranking.ranking_index(db=db)  # apis 호출

    return {
        "res": res,
    }  # 결과
