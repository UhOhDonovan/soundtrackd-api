from sqlmodel import Field, SQLModel, Relationship
from datetime import date, time
from typing import Optional


class User(SQLModel, table=True):
    __tablename__ = "user"

    email: str = Field(unique=True, max_length=254)
    username: str = Field(primary_key=True, max_length=60)
    password: str = Field(max_length=64)


class FollowsUser(SQLModel, table=True):
    __tablename__ = "follows_user"

    follower: str = Field(primary_key=True, foreign_key="user.username", max_length=60)
    followed: str = Field(primary_key=True, foreign_key="user.username", max_length=60)


class Artist(SQLModel, table=True):
    __tablename__ = "artist"

    id: str = Field(primary_key=True, max_length=22)
    name: str = Field(max_length=254)
    spotify_link: str = Field(max_length=254)


class FollowsArtist(SQLModel, table=True):
    __tablename__ = "follows_artist"

    user_id: str = Field(primary_key=True, foreign_key="user.username", max_length=60)
    artist_id: str = Field(primary_key=True, foreign_key="artist.id", max_length=22)


class Album(SQLModel, table=True):
    __tablename__ = "album"

    id: str = Field(primary_key=True, max_length=22)
    title: str = Field(max_length=254)
    release_date: date = Field()
    num_tracks: int = Field()
    spotify_link: str = Field(max_length=254)
    image_link: str = Field(max_length=254)


class ReleasedAlbum(SQLModel, table=True):
    __tablename__ = "released_album"

    artist_id: str = Field(primary_key=True, foreign_key="artist.id", max_length=22)
    album_id: str = Field(primary_key=True, foreign_key="album.id", max_length=22)


class Review(SQLModel, table=True):
    __tablename__ = "review"

    id: int = Field(primary_key=True)
    posted_by: str = Field(foreign_key="user.username", max_length=60)
    album_id: str = Field(foreign_key="album.id", max_length=22)
    post_date: date = Field()
    post_time: time = Field()
    rating: Optional[int] = Field()
    body: Optional[str] = Field(max_length=65535)


class ReviewComment(SQLModel, table=True):
    __tablename__ = "review_comment"

    id: int = Field(primary_key=True)
    review_id: int = Field(foreign_key="review.id")
    posted_by: str = Field(foreign_key="user.username", max_length=60)
    post_date: date = Field()
    post_time: time = Field()
    body: Optional[str] = Field(max_length=65535)


class Track(SQLModel, table=True):
    __tablename__ = "track"
    id: str = Field(primary_key=True, max_length=22)
    title: str = Field(max_length=254)
    spotify_link: str = Field(max_length=254)


class ReleasedTrack(SQLModel, table=True):
    __tablename__ = "released_track"

    artist_id: str = Field(primary_key=True, foreign_key="artist.id", max_length=22)
    track_id: str = Field(primary_key=True, foreign_key="track.id", max_length=22)


class TrackComment(SQLModel, table=True):
    __tablename__ = "track_comment"

    id: int = Field(primary_key=True)
    track_id: str = Field(primary_key=True, foreign_key="track.id", max_length=22)
    posted_by: str = Field(foreign_key="user.username", max_length=60)
    post_date: date = Field()
    post_time: time = Field()
    body: Optional[str] = Field(max_length=65535)


class AppearsOn(SQLModel, table=True):
    __tablename__ = "appears_on"

    track_id: str = Field(primary_key=True, foreign_key="track.id", max_length=22)
    album_id: str = Field(primary_key=True, foreign_key="album.id", max_length=22)
    track_num: int = Field()
