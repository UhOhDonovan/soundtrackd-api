DROP DATABASE IF EXISTS Soundtrackd;
DROP DATABASE IF EXISTS soundtrackd;
CREATE DATABASE soundtrackd;
USE soundtrackd;

CREATE TABLE user(
    email VARCHAR(254) UNIQUE NOT NULL,
    username VARCHAR(60) PRIMARY KEY,
    password VARCHAR(64) NOT NULL
);

CREATE TABLE follows_user(
    follower VARCHAR(60),
    followed VARCHAR(60),
    PRIMARY KEY (follower, followed),
    CONSTRAINT fk_follower_email FOREIGN KEY (follower) REFERENCES user(username),
    CONSTRAINT fk_followed_email FOREIGN KEY (followed) REFERENCES user(username)
);

CREATE TABLE artist(
    id VARCHAR(22) PRIMARY KEY,
    name VARCHAR(254) NOT NULL,
    spotify_link VARCHAR(254) NOT NULL
);

CREATE TABLE follows_artist(
    user_id VARCHAR(60),
    artist_id VARCHAR(22),
    PRIMARY KEY (user_id, artist_id),
    CONSTRAINT follows_fk_user_id FOREIGN KEY (user_id) REFERENCES user(username),
    CONSTRAINT follows_fk_artist_id FOREIGN KEY (artist_id) REFERENCES artist(id)
);

CREATE TABLE album(
    id VARCHAR(22) PRIMARY KEY,
    title VARCHAR(254) NOT NULL,
    release_date DATE NOT NULL,
    num_tracks INTEGER NOT NULL,
    spotify_link VARCHAR(254) NOT NULL,
    image_link VARCHAR(254) NOT NULL
);

CREATE TABLE released_album(
    artist_id VARCHAR(22) NOT NULL,
    album_id VARCHAR(22) NOT NULL,
    PRIMARY KEY (artist_id, album_id),
    CONSTRAINT released_album_fk_artist_id FOREIGN KEY (artist_id) REFERENCES artist(id),
    CONSTRAINT released_album_fk_album_id FOREIGN KEY (album_id) REFERENCES album(id)
);

CREATE TABLE review(
    id INTEGER AUTO_INCREMENT PRIMARY KEY,
    posted_by VARCHAR(60) NOT NULL,
    album_id VARCHAR(22) NOT NULL,
    post_date DATE NOT NULL,
    post_time TIME NOT NULL,
    rating INTEGER,
    body TEXT,
    CONSTRAINT review_fk_posted_by FOREIGN KEY (posted_by) REFERENCES user(username),
    CONSTRAINT review_fk_album_id FOREIGN KEY (album_id) REFERENCES album(id)
);

CREATE TABLE review_comment(
    id INTEGER AUTO_INCREMENT PRIMARY KEY,
    review_id INTEGER NOT NULL,
    posted_by VARCHAR(60) NOT NULL,
    post_date DATE NOT NULL,
    post_time TIME NOT NULL,
    body TEXT,
    CONSTRAINT review_comment_fk_review_id FOREIGN KEY (review_id) REFERENCES review(id),
    CONSTRAINT review_comment_fk_posted_by FOREIGN KEY (posted_by) REFERENCES user(username)
);

CREATE TABLE track(
    id VARCHAR(22) PRIMARY KEY,
    title VARCHAR(254) NOT NULL,
    spotify_link VARCHAR(254) NOT NULL
);

CREATE TABLE released_track(
    artist_id VARCHAR(22),
    track_id VARCHAR(22),
    PRIMARY KEY (artist_id, track_id),
    CONSTRAINT released_track_fk_artist_id FOREIGN KEY (artist_id) REFERENCES artist(id),
    CONSTRAINT released_track_fk_track_id FOREIGN KEY (track_id) REFERENCES track(id)
);

CREATE TABLE track_comment(
    id INTEGER AUTO_INCREMENT PRIMARY KEY,
    track_id VARCHAR(22) NOT NULL,
    posted_by VARCHAR(60) NOT NULL,
    post_date DATE NOT NULL,
    post_time TIME NOT NULL,
    body TEXT,
    CONSTRAINT track_comment_fk_track_id FOREIGN KEY (track_id) REFERENCES track(id),
    CONSTRAINT track_comment_fk_posted_by FOREIGN KEY (posted_by) REFERENCES user(username)
);

CREATE TABLE appears_on(
    track_id VARCHAR(22),
    album_id VARCHAR(22),
    track_num INTEGER NOT NULL,
    PRIMARY KEY (track_id, album_id),
    CONSTRAINT appears_on_fk_album_id FOREIGN KEY (album_id) REFERENCES album(id),
    CONSTRAINT appears_on_fk_track_id FOREIGN KEY (track_id) REFERENCES track(id)
);