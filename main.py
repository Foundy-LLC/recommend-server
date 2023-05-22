from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from core.scheduler import Scheduler
from crud.room_ranking import update_room_ranking
from db.connection import connect_db
from routes.ranking import router as rank_router

app = FastAPI()
app.include_router(rank_router)  # 다른 route파일들을 불러와 포함시킴

db_generator = connect_db()
db_instance = next(db_generator)

scheduler = Scheduler(update_room_ranking, db_instance)
scheduler.scheduler('cron', 'room_rating_update')


@app.get("/ranking")  # Route Path
async def index():
    response = RedirectResponse(url="ranking")
    return response
