from fastapi import APIRouter, Depends, responses
from sqlalchemy.orm import Session

from apis import ranking
from db.connection import connect_db

router = APIRouter(
    prefix="/ranking",  # url 앞에 고정적으로 붙는 경로추가
)  # Route 분리


@router.get("/")  # Route Path
def ranking_index(organizationId: int = None, page: int = 0, db: Session = Depends(connect_db)):
    if organizationId:
        status, res = ranking.ranking_organization(db=db, organizationId=organizationId, page=page)
    else:
        status, res = ranking.ranking_total(db=db, page=page)

    return responses.JSONResponse(status_code=status, content=res)
