from datetime import datetime
import bcrypt
from sqlalchemy.orm import Session
from dto import res_dto, sign_dto
from entity.user_entity import UserEntity
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse


def sign_up(reqDTO: sign_dto.ReqSignUp, db: Session):
    userEntity: UserEntity = db.query(UserEntity).filter(
        UserEntity.id == reqDTO.id).first()

    if (userEntity != None):
        resDTO = res_dto.ResDTO(
            code=1,  # 정상인 경우는 0, 비정상일 때는 1 혹은 -1
            message="이미 존재하는 아이디입니다."
        )
        encodedResDTO = jsonable_encoder(resDTO)

        return JSONResponse(status_code=400, content=encodedResDTO)

    db_user = UserEntity(
        id=reqDTO.id,
        password=bcrypt.hashpw(
            reqDTO.password.encode("utf-8"), bcrypt.gensalt()),
        simple_desc=reqDTO.simpleDesc if reqDTO.simpleDesc else "한 줄 소개가 없습니다.",  # 파이썬 삼항연산자
        role="BLOGER",
        create_date=datetime.now()
    )

    # 이제 데이터베이스에 넣기

    try:
        db.add(db_user)  # UserEntity에서 데이터 타입을 읽어서 알아서 디비에 넣어줌
        db.flush()  # 서버에서 데이터베이스로 쿼리문을 날림
    except Exception as e:  # 에러가 터졌을 경우는 아래문 실행, 데이터 하나라도 정상적으로 입력 안되면 다시 시작
        db.rollback()
        print(e)
        resDTO = res_dto.ResDTO(
            code=99,
            message="서버 내부 에러입니다.",
            content=e
        )
        encodedError = jsonable_encoder(resDTO)
        return JSONResponse(status_code=500, content=encodedError)

    finally:
        db.commit()

    db.refresh(db_user)

    resDTO = res_dto.ResDTO(
        code=0,
        message="성공",
        content=sign_dto.ResSignUp(
            idx=db_user.idx
        ))

    encodedResDTO = jsonable_encoder(resDTO)
    return JSONResponse(status_code=201, content=encodedResDTO)
