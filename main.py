from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from routes.ranking import router as rank_router
from routes.room_rating import router as room_rec_router

app = FastAPI()
app.include_router(rank_router)  # 다른 route파일들을 불러와 포함시킴
app.include_router(room_rec_router)


@app.get("/ranking")  # Route Path
async def index():
    response = RedirectResponse(url="ranking")
    return response


@app.get("/room_rec")
async def index():
    response = RedirectResponse(url="room_rec")
    return response
