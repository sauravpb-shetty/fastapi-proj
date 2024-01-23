
from .. import models, schemas ,oauth2
from fastapi import FastAPI, Response,status,HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session 
from sqlalchemy import func
from typing import List,Optional
from ..database import engine,get_db


router = APIRouter(
    prefix="/posts",   # as in every path we will use posts as common we there prefix and use only / and
                      #path will be read as /posts
    tags = ['Posts']   #this is for grouping our posts in swagger api                
)
          
#as we are sending back list posts we need to usse LIST
# @router.get("/posts",response_model= List[schemas.Post])
# @router.get("/",response_model= List[schemas.Post])
@router.get("/",response_model= List[schemas.PostOut])
async def get_posts(db:Session = Depends(get_db),current_user:int = Depends(oauth2.get_current_user),
                    limit : int = 10,skip:int = 0,search: Optional[str]=""):
   
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    posts = db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(
        models.Vote,models.Vote.post_id == models.Post.id,isouter = True).group_by(models.Post.id).\
    filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # print(results)
    # posts = db.query(models.Post).filter(current_user.id ==models.Post.owner_id ).all()
    # cursor.execute("""select * from post""")
    # posts = cursor.fetchall()
    
    return  posts   

# @router.post("/posts",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
async def create_posts(post : schemas.PostCreate, db: Session = Depends(get_db),current_user:int = 
                       Depends(oauth2.get_current_user)):
    # print(post.model_dump())
    # post_dict = post.model_dump()
    # post_dict['id'] = randrange(0,100000)
    # my_posts.append(post_dict)
    # cursor.execute("""INSERT INTO POST (title,content,published) VALUES(%s,%s,%s) RETURNING *""",(post.title,
    #                 post.content,post.publish))
    
    # new_post = cursor.fetchone()  
    # conn.commit() 
    #5:15
    #will unpack the post update it automatically and we don't have to write one by one
    #as we also need to add owner id to the request we will add owner_id from the login details
    new_post = models.Post(owner_id = current_user.id,**post.model_dump())
    
    # new_post = models.Post(title = post.title, content= post.content,
    #                                 published= post.published )
    db.add(new_post)
    db.commit()
    db.refresh(new_post) # for returning the newly created post
    return new_post   

@router.get("/{id}",response_model=schemas.PostOut) 
def get_post(id: int,db:Session = Depends(get_db),current_user:int = 
                       Depends(oauth2.get_current_user)):
    # post = db.query(models.Post).filter(models.Post.id == id).first()
    # cursor.execute("""select * from post where id = %s""",(str(id),)) #, at the end is needed if not numbers mmore than 10 will throw error
    # post = cursor.fetchone()
    # print(post)
    post = db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(
        models.Vote,models.Vote.post_id == models.Post.id,isouter = True).group_by(models.Post.id)\
        .filter(models.Post.id == id).first()
    
    # post = find_post(int(id))
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with {id} was not found")
    # if post.owner_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
    #                         detail=f"Not authorized to perform the operation")
        
    return post

@router.delete("/{id}",status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id : int,db:Session = Depends(get_db),current_user:int = 
                       Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)

    # cursor.execute("""DELETE FROM POST WHERE ID = %s returning *""",(str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    # index = find_index_post(id)
    # if index == None:
    if post_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id:{id} does not exist")
    # my_posts.pop(index)
    #user should be able to delete only his post
    if post_query.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorized to perform the operation")
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    

@router.put("/{id}",response_model=schemas.Post)
def update_post(id:int, updated_post: schemas.PostCreate, db:Session = Depends(get_db),current_user:int = 
                       Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    # cursor.execute("""UPDATE POST SET title=%s, content=%s, published = %s 
    #                WHERE id = %s RETURNING *""",
    #                (post.title,post.content,post.publish,str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    # index = find_index_post(id
    # 
    
    
    

    if post== None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail=f"post with id:{id} does not exist")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorized to perform the operation")
    post_query.update(updated_post.model_dump(),synchronize_session=False)
    db.commit()
    # post_dict = post.model_dump()
    # post_dict['id'] = id
    # my_posts[index] = post_dict
    return post_query.first()

