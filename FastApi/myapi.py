from fastapi import FastAPI, Depends, HTTPException # Added Depends, HTTPException
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
from typing import Optional, List

app = FastAPI(title="Integration with sql")

# --- Database Setup ---
engine = create_engine("sqlite:///users.db", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# --- Database Model ---
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    role = Column(String(100), nullable=False)

Base.metadata.create_all(engine)

# --- Pydantic Models ---
class UserCreate(BaseModel):
    name: str
    email: str
    role: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str

    class Config:
        from_attributes = True

# --- Dependency ---
def get_db():
    db = SessionLocal() 
    try:
        yield db        
    finally:
        db.close()



# --- Routes ---
@app.get("/")
def root():
    return {"message": "intro to fastapi with sql"}

@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
  
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User Not Found")
    return user

@app.post("/users/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail="User already exists") 

    
    new_user = User(**user.model_dump()) 
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# update user
@app.put("/users/{user_id}", response_model=UserResponse)
def update_user(user_id:int, user:UserCreate, db:Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User Not Found")
    for field,value in user.dict().items():
        setattr(db_user, field, value)

    db.commit()
    db.refresh(db_user)
    return db_user

# delete user
@app.delete("/users/{user_id}")
def delete_user(user_id: int, db:Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User Not Found")

    db.delete(db_user)
    db.commit()
    
    return {"message":"user deleted"}

# get all user
@app.get("/users/", response_model=List[UserResponse])
def get_all_users(db:Session = Depends(get_db)):
    return db.query(User).all()

