from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from starlette.requests import Request

from routes.ranking import router as rank_router

app = FastAPI()
app.include_router(rank_router)  # 다른 route파일들을 불러와 포함시킴


@app.get("/")  # Route Path
async def index(request: Request):
    response = RedirectResponse(url="ranking")
    return response
