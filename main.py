from typing import Annotated
from sqlalchemy.orm import Session

from fastapi import FastAPI, Depends, HTTPException
import models
from models import Todos
from database import engine, SessionLocal

app = FastAPI()

models.Base.metadata.create_all(bind = engine)
# 이 문구는, todos.db가 없을때만 실행될 것이다.
# 모델로 돌아가서 todos테이블을 향상시키면,
# 이 문구는 todos 테이블에 영향을 주지 않을 것이다. 

# DB dependency를 관리하자.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]


@app.get("/")
async def read_all(db:Annotated[Session, Depends(get_db)]):
    return db.query(Todos).all

@app.get("/todo/{todo_id}")
async def read_todo(db: db_dependency, todo_id:int):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    # 일치하는 것을 찾는 순간 바로 반환
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code = 404, detail='Todo not found.')

