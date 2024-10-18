DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;
DROP TABLE IF EXISTS comment;
DROP TABLE IF EXISTS likes;
DROP TABLE IF EXISTS artwork;


CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  firstname TEXT NOT NULL,
  lastname TEXT NOT NULL,
  bio TEXT, -- User bio (optional)
  avatar TEXT, -- URL or path to user's profile picture (optional)
);

CREATE TABLE post (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL, -- References user who created the post
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  FOREIGN KEY (user_id) REFERENCES user (id)
);

CREATE TABLE comment (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL, -- References user who wrote comment
  post_id INTEGER NOT NULL, -- References the post who comment belongs to
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  body TEXT NOT NULL,
  FOREIGN KEY (post_id) REFERENCES post (id),
  FOREIGN KEY (user_id) REFERENCES user (id)
);

CREATE TABLE likes (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL, -- References user who liked the post
  post_id INTEGER NOT NULL, -- References the post that was liked
  FOREIGN KEY (post_id) REFERENCES post (id),
  FOREIGN KEY (user_id) REFERENCES user (id)
);

CREATE TABLE artwork (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL, -- References user who uploaded the art
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  image_url TEXT NOT NULL, -- URL or path to art image (optional)
  description TEXT, -- Description of art (optional)
  FOREIGN KEY (user_id) REFERENCES user (id)
);
