from fastapi import APIRouter, Depends,  HTTPException, status
from sqlalchemy.orm import Session
from .. import schemas, models, utils, database

router = APIRouter(tags=["Authentication"])


@router.post("/login")
def login(user_credentials: schemas.UserLogin, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(
        models.User.email == user_credentials.email).first()
    print(user)
    print(db.query(models.User))
    print(user_credentials.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, details="Invalid credentials")
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    return {"token": "example tok"}
