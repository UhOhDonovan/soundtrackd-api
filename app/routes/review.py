import json
from fastapi import APIRouter, Depends, Query
from typing import Annotated
from datetime import datetime, date
from sqlmodel import select
from ..dependencies.authentication import get_current_user
from ..dependencies.apimodels import ReviewSubmission
from ..db_tools.database import SessionDep
from ..db_tools.models import Review, ReviewComment
from .search import get_token
from requests import post, get

router = APIRouter()


@router.get("/list/{album_id}")
async def list_reviews(
    album_id: str,
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 10,
):
    statement = (
        select(Review)
        .where(Review.album_spotify_id == album_id)
        .offset(offset)
        .limit(limit)
    )
    reviews = session.exec(statement).all()
    print("Found:", reviews)
    return reviews


@router.get("/list/user/{username}")
async def list_reviews(
    username: str,
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 10,
):
    statement = (
        select(Review).where(Review.posted_by == username).offset(offset).limit(limit)
    )
    reviews = session.exec(statement).all()
    print("Found:", reviews)
    reviews = [dict(review) for review in reviews]
    print("converted:", reviews)
    for i in range(len(reviews)):
        token = get_token()
        url = "https://api.spotify.com/v1/albums/" + reviews[i]["album_spotify_id"]
        headers = {"Authorization": "Bearer " + token}
        response = get(url, headers=headers)
        result = json.loads(response.content)
        print(result)
        album_info = {
            "title": result["name"],
            "cover_url": result["images"][0]["url"],
        }
        reviews[i]["album_info"] = album_info
    print("Found:", reviews)
    return reviews


@router.get("/read/{review_id}")
async def read_review(
    review_id: int,
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=10)] = 10,
):
    review = session.get(Review, review_id)
    comments = session.exec(
        select(ReviewComment)
        .where(ReviewComment.review_id == review_id)
        .offset(offset)
        .limit(limit)
    )
    print("Found:", review)
    return review, comments


@router.post("/write")
async def submit_review(
    submission: ReviewSubmission,
    session: SessionDep,
    current_user: Annotated[str, Depends(get_current_user)],
):
    post_date = date.today()
    post_time = datetime.now().time()
    review = Review(
        album_spotify_id=submission.album_spotify_id,
        posted_by=current_user,
        post_date=post_date,
        post_time=post_time,
        rating=submission.rating,
        body=submission.body,
    )
    print("Writing review:\n", review)
    session.add(review)
    session.commit()
    session.refresh(review)
    return review
