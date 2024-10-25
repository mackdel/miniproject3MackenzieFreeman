### INF601 - Advanced Programming in Python
### Mackenzie Freeman
### Mini Project 3


# MiniProject3 - Artit

## Description

Artit is a platform for artists to showcase their artwork. Users can create an account, log in, and upload their artwork for others to see. They can engage with other users' artwork by liking and commenting. The platform offers a personal profile page where users can manage their own content, edit posts.

To assist users who may not have artwork readily available, a collection of sample images is included in the project for easy testing.

## Getting Started

### Dependencies

You can install all required libraries using the following command:
```
pip install -r requirements.txt
```

### Setup Database

After installing dependencies, set up the database for the application using this command:
```
flask --app artit init-db
```

### Running the Application

To start the application and run it locally, use the command:
```
flask --app artit run
```
Once the server is running, you can access the platform by visiting http://127.0.0.1:5000/ in your web browser.

## Sample Artwork for Testing

For users who do not have their own artwork available, a folder of sample images is provided for testing purposes:
1. Navigate to the sample_artworks/ folder within the project directory. 
2. Download an image from the folder to your local machine. 
3. When uploading artwork to the platform, select one of these downloaded images.
This allows users to test the image upload functionality without needing external files. 

## Features

* Homepage: Displays a list of artwork from various users, with options to like and comment.
* User Profile: Displays a public profile page viewable by all users. 
* Profile Editing: Users can edit their own profiles, updating their profile picture, name, and bio.
* Upload Artwork: Allows users to upload their own artwork.
* Edit and Delete Posts: Users can edit and delete their own posts.
* Like and Comment: Users can leave comments and like artwork. Users can delete their own comments.
* Responsive Navigation: Redirects and highlights are optimized for seamless navigation, including redirecting back to the correct page after editing a post or profile.

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
* [ChatGPT]( )
* [BootStrap Docs](https://getbootstrap.com/docs/5.3/getting-started/introduction/)
