from datetime import datetime
from fastapi import Request
from sqlalchemy.orm import Session

from dto import post_dto, sign_dto
from entity.like_entity import LikeEntity
from entity.post_entity import PostEntity
from entity.user_entity import UserEntity
from util import functions


def get_posts(db: Session):
    post_entity_list: list[PostEntity] = db.query(
        PostEntity).filter(PostEntity.delete_date == None).order_by(
            PostEntity.create_date.desc()).all()

    res_main_post_list = list(
        map(post_dto.ResMainPost.toDTO, post_entity_list))

    return functions.res_generator(content=res_main_post_list)
