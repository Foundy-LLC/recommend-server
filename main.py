from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from core.scheduler import Scheduler
from crud.room_ranking import update_room_ranking
from db.connection import connect_db
from routes.ranking import router as rank_router

app = FastAPI()
app.include_router(rank_router)  # 다른 route파일들을 불러와 포함시킴

db = connect_db()
scheduler = Scheduler(db)
scheduler.scheduler(update_room_ranking, 'cron', 'room_rating_update')


@app.get("/ranking")  # Route Path
async def index():
    response = RedirectResponse(url="ranking")
    return response
