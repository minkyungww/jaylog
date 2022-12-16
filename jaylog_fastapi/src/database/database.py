from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# id:password@database
SQLALCHEMY_DATABASE_URL = "mariadb+mariadbconnector://root:!skfkzldna123@13.125.85.217:3306/jaylog"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Session은 디비랑 서버 연결, commit, flush는 데이터를 쏴주면 수정불가해 false로 설정
DBase = declarative_base()
