import os

from flask import Flask


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'artit.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # initialize db within app
    from . import db
    db.init_app(app)

    # Set the folder configurations for uploads
    static_folder = os.path.join(app.root_path, 'static', 'uploads')
    avatars_folder = os.path.join(static_folder, 'avatars')
    artworks_folder = os.path.join(static_folder, 'artworks')

    os.makedirs(avatars_folder, exist_ok=True)
    os.makedirs(artworks_folder, exist_ok=True)

    app.config['UPLOAD_FOLDER'] = static_folder
    app.config['AVATARS_FOLDER'] = avatars_folder
    app.config['ARTWORKS_FOLDER'] = artworks_folder

    # import and register blueprint from factory
    from . import auth
    app.register_blueprint(auth.bp)

    from . import post
    app.register_blueprint(post.bp)
    app.add_url_rule('/', endpoint='index')

    return app