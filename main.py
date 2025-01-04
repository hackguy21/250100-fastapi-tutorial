from typing import Annotated

from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from fastapi import FastAPI, Depends, HTTPException, status, Path
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

class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description : str = Field(min_length=3, max_length=100)
    priority: int = Field(gt=0, lt=6)
    complete: bool
    



@app.get("/", status_code=status.HTTP_200_OK)
async def read_all(db:Annotated[Session, Depends(get_db)]):
    return db.query(Todos).all()

@app.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo(db: db_dependency, todo_id:int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    # 일치하는 것을 찾는 순간 바로 반환
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code = 404, detail='Todo not found.')

@app.post("/todo", status_code = status.HTTP_201_CREATED)
async def create_todo(db: db_dependency, todo_request: TodoRequest):
    todo_model = Todos(**todo_request.dict())

    db.add(todo_model)
    db.commit()


@app.put("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(db: db_dependency, 
                    todo_id: int,
                    todo_request: TodoRequest):
    todo_model = db.qeury(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail='Todo not found.')
    
    todo_model.title = todo_request.title
    todo_model.description = todo_request.description
    todo_model.prioirity = todo_request.priority
    todo_model.complete = todo_request.complete
    
    db.add(todo_model)
    db.commit()

@app.delete("/todo/{todo_id}", status_code = status.HTTP_204_NO_CONTENT)
async def delete_todo(db: db_dependency, todo_id: int=Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail='Todo not found')
    db.query(Todos).filter(Todos.id == todo_id).delete()

    db.commit()


