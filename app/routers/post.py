from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(prefix = "/posts",                           # prefix de chaque route
                   tags=["Posts"])                              # for the docs

@router.get("/",response_model = List[schemas.PostOut])         # List[] car on veut une liste de tous les post au format PostOut
def get_posts(db: Session = Depends(get_db),                   
              current_user: int = Depends(oauth2.get_current_user),
              limit: int = 10,
              skip: int = 0,
              search: Optional[str] = ""):

    #posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes"))\
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)\
            .group_by(models.Post.id)\
                .filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    return posts

    #cursor.execute(""" SELECT * FROM posts """)
    #posts = cursor.fetchall()

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post) # sans le parametre status_code, l'envoi de cette requete retourn un status code 200 hors la creation doit etre un 201
def create_posts(post: schemas.PostCreate, 
                 db: Session = Depends(get_db), 
                 current_user: int = Depends(oauth2.get_current_user)):

    new_post = models.Post(owner_id = current_user.id , **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

    #cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s,%s,%s) RETURNING * """, (post.title, post.content, post.published))
    #new_post = cursor.fetchone()
    #conn.commit()

    #new_post = models.Post(title=post.title, content=post.content, published=post.published) is similar to :
    
@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int,  
             db: Session = Depends(get_db), 
             current_user: int = Depends(oauth2.get_current_user)): # id : int => pour forcer le type integer de id (sinon si on rentre un str dans l'url on aura un message d'erreur internal server error sans plus d'idée sur la nature de l'erreur)
    
    #post = db.query(models.Post).filter(models.Post.id == id).first()

    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes"))\
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)\
            .group_by(models.Post.id).filter(models.Post.id == id).first()

    if not post :
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f"post with id {id} was not found")
    
    return post

    #cursor.execute(""" SELECT * FROM posts WHERE id = %s  """, (str(id))) # str(id) car on a un type integer mais on le renseigne dans une query SQL qui est un string
    #post = cursor.fetchone()

@router.delete("/{id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), 
                current_user: int = Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = f"post with id {id} does not exist")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to delete the post")
    
    post_query.delete(synchronize_session = False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT) # avec une requete Delete on ne renvoit pas un message "données bien supprimée" car la méthode Delete n'attend pas de données en retour donc on renvoit une reponse status http

    #cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """, (str(id)))
    #deleted_post = cursor.fetchone()
    #conn.commit()

@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, 
                updated_post: schemas.PostCreate, 
                db: Session = Depends(get_db), 
                current_user: int = Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = f"post with id {id} does not exist")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to update the post")
    
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    
    return post_query.first()

    #cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE id  = %s RETURNING * """, (post.title, post.content, post.published, str(id)))
    #updated_post = cursor.fetchone()
    #conn.commit()

