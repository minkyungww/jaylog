from datetime import datetime
from pydantic import BaseModel
from dto import sign_dto
from entity.post_entity import PostEntity

from entity.user_entity import UserEntity


class ResMainPost(BaseModel):

    class _Writer(BaseModel):
        idx: int
        id: str
        profileImage: str

        class Config:
            orm_mode: True

        @staticmethod
        def toDTO(user_entity: UserEntity):
            return ResMainPost._Writer(
                idx=user_entity.idx,
                id=user_entity.id,
                profileImage=user_entity.profile_image
            )

    idx: int
    thumbnail: str | None
    title: str
    summary: str
    likeCount: int
    creatDate: datetime
    writer: _Writer

    class Config:
        orm_mode: True

    @staticmethod
    def toDTO(post_entity: PostEntity):

        like_count = len(list(filter(lambda like_entity: like_entity.delete_date == None,
                                     post_entity.like_entity_list)))

        return ResMainPost(
            idx=post_entity.idx,
            thumbnail=post_entity.thumbnail,
            title=post_entity.title,
            summary=post_entity.summary,
            likeCount=0,
            creatDate=post_entity.create_date,
            writer=ResMainPost._Writer.toDTO(post_entity.user_entity)
        )
