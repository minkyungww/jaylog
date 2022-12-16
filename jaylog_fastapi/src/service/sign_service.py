from datetime import datetime
import time
import bcrypt
import jwt
from sqlalchemy.orm import Session
from dto import res_dto, sign_dto
from entity.user_entity import UserEntity
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from util import functions
from config import constants
from fastapi.encoders import jsonable_encoder


USER_ID_EXIST_ERROR = {"code": 1, "message": "이미 존재하는 아이디입니다."}
ID_NOT_EXIST_ERROR = {"code": 2, "message": "가입되지 않은 아이디입니다."}
DELETED_USER_ERROR = {"code": 3, "message": "삭제된 유저입니다."}
PASSWORD_INCORRECT_ERROR = {"code": 4, "message": "비밀번호가 틀립니다."}
INTERNAL_SERVER_ERROR = {"code": 99, "message": "서버 내부 에러입니다."}


def sign_in(reqDTO: sign_dto.ReqSignIn, db: Session):
    userEntity: UserEntity = db.query(UserEntity).filter(
        UserEntity.id == reqDTO.id).first()

    # 아이디가 없을 경우
    if userEntity == None:
        return functions.res_generator(status_code=400, error_dict=ID_NOT_EXIST_ERROR)

    # 아이디가 삭제된 경우
    if userEntity.delete_date != None:
        return functions.res_generator(status_code=400, error_dict=DELETED_USER_ERROR)

    # 비밀번호가 틀릴 경우
    if not bcrypt.checkpw(reqDTO.password.encode("utf-8"), userEntity.password.encode("utf-8")):
        return functions.res_generator(status_code=400, error_dict=PASSWORD_INCORRECT_ERROR)

    # 정상
    accessJwtDTO = sign_dto.AccessJwt(
        idx=userEntity.idx,
        id=userEntity.id,
        simpleDesc=userEntity.simple_desc,
        profileImage=userEntity.profile_image,
        role=userEntity.role,
        exp=time.time() + constants.JWT_ACCESS_EXP_SECONDS
    )

    accessToken = jwt.encode(jsonable_encoder(
        accessJwtDTO), constants.JWT_SALT, algorithm="HS256")

    refreshJwtDTO = sign_dto.RefreshJwt(
        idx=userEntity.idx,
        exp=time.time() + constants.JWT_REFRESH_EXP_SECONDS
    )

    refreshToken = jwt.encode(jsonable_encoder(
        refreshJwtDTO), constants.JWT_SALT, algorithm="HS256")

    resSignInDTO = sign_dto.ResSignIn(
        accessToken=accessToken,
        refreshToken=refreshToken
    )

    return functions.res_generator(content=resSignInDTO)


def sign_up(reqDTO: sign_dto.ReqSignUp, db: Session):
    userEntity: UserEntity = db.query(UserEntity).filter(
        UserEntity.id == reqDTO.id).first()

    if userEntity != None:
        return function.res_generator(status_code=400, error_dict=USER_ID_EXIST_ERROR)

    db_user = UserEntity(
        id=reqDTO.id,
        password=bcrypt.hashpw(
            reqDTO.password.encode("utf-8"), bcrypt.gensalt()),
        profile_image="https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png",
        simple_desc=reqDTO.simpleDesc if reqDTO.simpleDesc else "한 줄 소개가 없습니다.",
        role="BLOGER",
        create_date=datetime.now()
    )

    try:
        db.add(db_user)
        db.flush()

    except Exception as e:
        db.rollback()
        print(e)

        return functions.res_generator(status_code=500, error_dict=INTERNAL_SERVER_ERROR, content=e)

    finally:
        db.commit()

    db.refresh(db_user)

    return functions.res_generator(status_code=201, content=sign_dto.ResSignUp(idx=db_user.idx))

# def sign_up(reqDTO: sign_dto.ReqSignUp, db: Session):
#     userEntity: UserEntity = db.query(UserEntity).filter(
#         UserEntity.id == reqDTO.id).first()

#     if (userEntity != None):
#         resDTO = res_dto.ResDTO(
#             code=1,  # 정상인 경우는 0, 비정상일 때는 1 혹은 -1
#             message="이미 존재하는 아이디입니다."
#         )
#         encodedResDTO = jsonable_encoder(resDTO)

#         return JSONResponse(status_code=400, content=encodedResDTO)

#     db_user = UserEntity(
#         id=reqDTO.id,
#         password=bcrypt.hashpw(
#             reqDTO.password.encode("utf-8"), bcrypt.gensalt()),
#         simple_desc=reqDTO.simpleDesc if reqDTO.simpleDesc else "한 줄 소개가 없습니다.",  # 파이썬 삼항연산자
#         profile_image="https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png",
#         role="BLOGER",
#         create_date=datetime.now()
#     )

#     # 이제 데이터베이스에 넣기

#     try:
#         db.add(db_user)  # UserEntity에서 데이터 타입을 읽어서 알아서 디비에 넣어줌
#         db.flush()  # 서버에서 데이터베이스로 쿼리문을 날림
#     except Exception as e:  # 에러가 터졌을 경우는 아래문 실행, 데이터 하나라도 정상적으로 입력 안되면 다시 시작
#         db.rollback()  # 에러 터지기 전에 값으로 돌아감
#         print(e)
#         resDTO = res_dto.ResDTO(
#             code=99,
#             message="서버 내부 에러입니다.",
#             content=e
#         )
#         encodedError = jsonable_encoder(resDTO)
#         return JSONResponse(status_code=500, content=encodedError)

#     finally:
#         db.commit()

#     db.refresh(db_user)

#     resDTO = res_dto.ResDTO(
#         code=0,
#         message="성공",
#         content=sign_dto.ResSignUp(
#             idx=db_user.idx
#         ))

#     encodedResDTO = jsonable_encoder(resDTO)
#     return JSONResponse(status_code=201, content=encodedResDTO)

# # resDTO처럼 중복되는 코드는 리팩토링을 통해 가독성을 높일 수 있음
