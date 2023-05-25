from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from routes.ranking import router as rank_router
from routes.recommend import router as rec_router

app = FastAPI()
app.include_router(rank_router)  # 다른 route파일들을 불러와 포함시킴
app.include_router(rec_router)


# db_generator = connect_db()
# db_instance = next(db_generator)
#
# scheduler = Scheduler(update_room_ranking, db_instance)
# scheduler.scheduler('cron', 'room_rating_update')


@app.get("/ranking")  # Route Path
async def index():
    response = RedirectResponse(url="ranking")
    return response


@app.get("/users")
async def index():
    response = RedirectResponse(url="users")
    return response
