from datetime import datetime
from fastapi import HTTPException, status,UploadFile
from sqlalchemy.orm import Session
from sqlalchemy import or_
from src.catogeries.model import Category
from src.posts.model import Post
from src.scheme.post import CreatePost, UpdatePost
from src.tags.model import Tag
from src.users.model import User

from src.uploadfile.controller import validate_image,save_image,delete_image

def create_post(db: Session, data: CreatePost, author_id: int,image:UploadFile|None):

    existing_post = db.query(Post).filter(Post.title == data.title).first()
    if existing_post is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A post with this title already exists",
        )

    if data.category_id is not None:
        category = db.query(Category).filter(Category.id == data.category_id).first()
        if category is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found",
            )

    tags = db.query(Tag).filter(Tag.id.in_(data.tag_ids)).all()
    if len(tags) != len(set(data.tag_ids)):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="One or more tags not found",
        )

#image validation and storing 

    validate_image(image)

    image_url = save_image(image)


    post = Post(
        title=data.title,
        content=data.content,
        author_id=author_id,
        category_id=data.category_id,
        image_url = image_url
    )
    post.tags = tags
    db.add(post)
    db.commit()
    db.refresh(post)
    return post

#get post
def get_posts(
    search: str|None,
    category: str|None , 
    sort_by:str|None ,
    tags:str|None,
    year:int|None,
    db: Session,
    page: int):

    limit = 10
    skip = (page - 1) * limit
    query = db.query(Post)
    if search:
        pattern = f"%{search}%"
        query = query.filter(
            or_(
                Post.title.ilike(pattern),
                Post.content.ilike(pattern),
            )
        )

    if category:
        query = query.join(Post.category).filter(
        Category.name.ilike(f"%{category}%")
    )

    if sort_by == "latest":
        query = query.order_by(Post.created_at.desc())
    elif sort_by == "oldest":
        query = query.order_by(Post.created_at.asc())

    if tags:
        query = query.join(Post.tags).filter(Tag.name.ilike(f"%{tags}%"))

    if year:
        start_date = datetime(year,1,1)
        end_date = datetime(year+1,1,1)
        query = query.filter(Post.created_at >= start_date, 
                             Post.created_at < end_date)


    return query.offset(skip).limit(limit).all()

#get post
def get_post(db: Session, post_id: int):
    post = db.query(Post).filter(Post.id == post_id).first()
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found",
        )
    post.views +=1
    db.commit()
    db.refresh(post)
    return post

#update post
def update_post(db: Session, post_id: int, data: UpdatePost, user: User,image:UploadFile|None=None):
    post = db.query(Post).filter(Post.id == post_id).first()
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found",
        )
    if post.author_id != user.id and user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only update your own posts",
        )

    existing_post = (
        db.query(Post)
        .filter(Post.title == data.title, Post.id != post_id)
        .first()
    )
    if existing_post is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A post with this title already exists",
        )

    tags = db.query(Tag).filter(Tag.id.in_(data.tag_ids)).all()
    post.title = data.title
    post.content = data.content
    post.tags = tags

    old_image_url = post.image_url
    image_url = post.image_url
    if image:
        image_url = save_image(image)
    
    post.image_url = image_url
    
    db.commit()
    db.refresh(post)
    
    if image:
        delete_image(old_image_url)
    return post

#delete post
def delete_post(db: Session, post_id: int, user: User):
    post = db.query(Post).filter(Post.id == post_id).first()
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found",
        )
    if post.author_id != user.id and user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete your own posts",
        )
    image_url = post.image_url
    db.delete(post)
    db.commit()
    delete_image(image_url)