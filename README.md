### INF601 - Advanced Programming in Python
### Mackenzie Freeman
### Mini Project 3


# MiniProject3

## Description

ArtIt is a platform for artists to showcase their artwork. Users can create an account, log in, and upload their artwork for others to see. They can engage with other users' artwork by liking and commenting. The platform offers a personal profile page where users can manage their own content.

## Getting Started

### Dependencies

You can install all required libraries using the following command:
```
pip install -r requirements.txt
```

### Setup Database

Once the dependencies are installed, you will need to set up the database for the application. Use the following command to initialize the SQLite database:
```
flask --app artit init-db
```

### Executing program

To start the application and run it locally, use the following command:
```
flask --app artit run
```
You can then visit http://127.0.0.1:5000/ in your web browser to access the platform.

## Output

* Homepage: Shows a list of artworks from different users, with options to like and comment.
* User Profile: Displays the logged-in user's profile with their uploaded artwork.
* Upload Artwork: Users can upload their artwork using a form.
* Comment and Like System: Users can leave comments and like artwork.
* Post Management: Users can edit and delete their own posts.

## Help

Common issues and troubleshooting:
* If the server doesn't run, make sure you have installed all the dependencies.
* For database issues, try re-initializing the database:
```
flask --app artit init-db
```

## Authors

Mackenzie Freeman
[LinkedIn](https://www.linkedin.com/in/mackenzie-lyn-freeman/)

## Acknowledgments

Inspiration, code snippets, etc.
* [Flask Tutorial](https://flask.palletsprojects.com/en/3.0.x/tutorial/)
* [ChatGPT]()
* [BootStrap Docs](https://getbootstrap.com/docs/5.3/getting-started/introduction/)