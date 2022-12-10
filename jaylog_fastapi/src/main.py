from fastapi import FastAPI
import uvicorn
from controller import sign_controller, test_controller
from entity.user_entity import UserEntity
from entity.post_entity import PostEntity
from entity.like_entity import LikeEntity

app =  FastAPI()


# app.include_router(test_controller.router)
app.include_router(sign_controller.router)

if __name__ == "__main__" : 
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)