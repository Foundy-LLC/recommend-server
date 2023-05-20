from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from core.scheduler import Scheduler
from crud.room_ranking import update_room_ranking
from crud.users_ranking import update_user_rating
from db.connection import connect_db
from routes.ranking import router as rank_router

app = FastAPI()
app.include_router(rank_router)  # 다른 route파일들을 불러와 포함시킴

db = connect_db()
room_scheduler = Scheduler(db)
room_scheduler.scheduler(update_room_ranking, 'cron', 'room_rating_update')

user_scheduler = Scheduler(db)
user_scheduler.scheduler()
user_scheduler.scheduler(update_user_rating, 'cron', 'user_rating_update')


@app.get("/ranking")  # Route Path
async def index():
    response = RedirectResponse(url="ranking")
    return response
