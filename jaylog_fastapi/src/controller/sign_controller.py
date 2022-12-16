from fastapi import APIRouter, Depends
from dependencies import get_db
from sqlalchemy.orm import Session
from dto import sign_dto
from service import sign_service

from fastapi.responses import JSONResponse


router = APIRouter(
    prefix="/api/v1/sign",
    tags=["sign"]
)
# /api/...는 json형식으로 보낼 때
# /api/v1/.. 형식은 템플릿으로 보낼 때


@router.post("/in")
async def sign_in(reqDTO: sign_dto.ReqSignIn, db: Session = Depends(get_db)) -> JSONResponse:
    return sign_service.sign_in(reqDTO, db)

@router.post("/up")
async def sign_up(reqDTO: sign_dto.ReqSignUp, db: Session = Depends(get_db)) -> JSONResponse:
    return sign_service.sign_up(reqDTO, db)
