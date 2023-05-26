from fastapi import APIRouter, Depends, responses
from sqlalchemy.orm import Session

from apis.recommend import *
from db.connection import connect_db
from gensim.models import fasttext
import datetime
import os
from dotenv import load_dotenv

print(f"== LOAD fasttext START at {datetime.datetime.now()}")
model = fasttext.load_facebook_model(os.getenv("MODEL"))
print(f"== LOAD fasttext   END at {datetime.datetime.now()}")

# model = None

router = APIRouter(
    prefix="/users",  # url 앞에 고정적으로 붙는 경로추가
)  # Route 분리


@router.get("/{user_id}/recommended-friends")
def recommend_users(user_id, db: Session = Depends(connect_db)):
    print("Accept")
    status, res = get_recommended_friends(db, user_id, model)

    return responses.JSONResponse(status_code=status, content=res)

@router.get("/update-vector")
def update_vector(db:Session = Depends(connect_db), model=model):
    update_users_vector(db, model)



