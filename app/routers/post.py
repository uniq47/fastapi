
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import schemas, models
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List

router = APIRouter()


@router.get("/posts", response_model=List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    post = db.query(models.Post).all()
    return post


@router.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
    # cursor.execute("""INSERT INTO posts(course, teacher, rating, take_again) VALUES(%s, %s, %s,%s) RETURNING *""",
    #                (post.course, post.teacher, post.rating, post.take_again))
    # new_post = cursor.fetchone()
    # conn.commit()

    # new_post = models.Post(course=post.course, teacher=post.teacher,
    #                        rating=post.rating, take_again=post.take_again)

    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

    # convert the object to dictionary, retriving posts from the database


@router.get("/posts/{id}", response_model=schemas.PostResponse)
def get_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute(
    #     """SELECT * from posts WHERE id = %s""", (str(id)))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"post not found with id {id}")

    return post


@router.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""DELETE FROM posts WHERE id =%s returning *""", (str(id)))
    # deleted_post = cursor.fetchone()
    # conn.commit()

    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post not found with id {id}")
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@ router.put("/posts/{id}", response_model=schemas.PostResponse)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db)):
    # cursor.execute(
    #     """UPDATE posts SET course = %s, teacher = %s, rating = %s, take_again = %s WHERE id = %s RETURNING *""", (post.course, post.teacher, post.rating, post.take_again, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post not found with id {id}")

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()