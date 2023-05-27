import uvicorn
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from routes.ranking import router as rank_router
from routes.recommend import router as rec_router
from gensim.models import fasttext
import datetime


app = FastAPI()
app.include_router(rec_router)


@app.get("/")  # Route Path
def root():
    return {"message" : "404 Not Found"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
