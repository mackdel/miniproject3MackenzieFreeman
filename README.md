### INF601 - Advanced Programming in Python
### Mackenzie Freeman
### Mini Project 3


# MiniProject3

## Description

This project is for artists to upload their artwork. Users can create an account, log in, and share their artwork with others. They can also view, like, and comment on other users' artwork. Each user has their own profile page to display the artwork they've uploaded.

## Getting Started

### Dependencies

```
pip install -r requirements.txt
```

### Setup Database

```
flask --app artit init-db
```

### Running server

```
flask --app artit run
```

## Output

* Homepage: Shows a list of artworks from different users, with options to like and comment.
* User Profile: Displays the logged-in user's profile with their uploaded artwork.
* Upload Artwork: Users can upload their artwork using a form.
* Comment and Like System: Users can leave comments and like artwork.

## Authors

Contributors names and contact info

Mackenzie Freeman

## Acknowledgments

Inspiration, code snippets, etc.
* [Flask Tutorial](https://flask.palletsprojects.com/en/3.0.x/tutorial/)