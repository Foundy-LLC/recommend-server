from fastapi import APIRouter, Depends, responses
from sqlalchemy.orm import Session

from apis.ranking import ranking_organization, ranking_total, personal_ranking
from db.connection import connect_db

router = APIRouter(
    prefix="/ranking",  # url 앞에 고정적으로 붙는 경로추가
)  # Route 분리


@router.get("")  # Route Path
def get_all_ranking_index(organizationId: int = None, page: int = 0, db: Session = Depends(connect_db)):
    if organizationId:
        status, res = ranking_organization(
            db=db, organizationId=organizationId, page=page)
    else:
        status, res = ranking_total(db=db, page=page)

    return responses.JSONResponse(status_code=status, content=res)


@router.get("/{user_id}")
def get_my_ranking_index(user_id, db: Session = Depends(connect_db)):
    status, res = personal_ranking(db, user_id=user_id)
    return responses.JSONResponse(status_code=status, content=res)
