from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename
from artit.auth import login_required
from artit.db import get_db
import os
from flask import current_app

bp = Blueprint('post', __name__)

# List all posts (homepage)
@bp.route('/')
def index():
    db = get_db()
    if g.user:
        # If the user is logged in, check if they've liked each post
        posts = db.execute(
            'SELECT p.id, artwork, description, created, user_id, firstname, lastname, avatar, '
            '(SELECT COUNT(*) FROM likes WHERE post_id = p.id) as likes_count, '
            '(SELECT COUNT(*) FROM comment WHERE post_id = p.id) as comments_count, '
            '(SELECT 1 FROM likes WHERE post_id = p.id AND user_id = ?) as user_liked '
            'FROM post p JOIN user u ON p.user_id = u.id '
            'ORDER BY p.created DESC',
            (g.user['id'],)
        ).fetchall()
    else:
        # If the user is not logged in, don't check if they've liked each post
        posts = db.execute(
            'SELECT p.id, artwork, description, created, user_id, firstname, lastname, avatar, '
            '(SELECT COUNT(*) FROM likes WHERE post_id = p.id) as likes_count, '
            '(SELECT COUNT(*) FROM comment WHERE post_id = p.id) as comments_count '
            'FROM post p JOIN user u ON p.user_id = u.id '
            'ORDER BY p.created DESC'
        ).fetchall()
    # Fetch comments for each post
    comments_by_post = {}
    for post in posts:
        post_id = post['id']
        comments = db.execute(
            'SELECT c.body, c.created, u.username FROM comment c JOIN user u ON c.user_id = u.id WHERE c.post_id = ?',
            (post_id,)
        ).fetchall()
        comments_by_post[post_id] = comments
    return render_template('post/index.html', posts=posts, comments_by_post=comments_by_post)

# View Singular Post
@bp.route('/post/<int:id>', methods=['GET'])
def view_post(id):
    db = get_db()
    # Include user_id in the SELECT query
    post = db.execute(
        'SELECT p.id, p.artwork, p.description, p.created, p.user_id, u.avatar as user_avatar, u.firstname, u.lastname '
        'FROM post p JOIN user u ON p.user_id = u.id '
        'WHERE p.id = ?',
        (id,)
    ).fetchone()

    if not post:
        return redirect(url_for('post.index'))

    comments = db.execute('SELECT * FROM comment WHERE post_id = ?', (id,)).fetchall()
    likes_count = db.execute('SELECT COUNT(*) FROM likes WHERE post_id = ?', (id,)).fetchone()[0]

    return render_template('post/view.html', post=post, comments=comments, likes_count=likes_count)


# Create new post
@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        description = request.form['description']
        artwork = request.files.get('artwork')
        error = None

        if artwork:
            filename = secure_filename(artwork.filename)
            if filename != '':
                # Save to the 'artworks' folder
                artwork_path = os.path.join(current_app.config['ARTWORKS_FOLDER'], filename)
                artwork.save(artwork_path)
        else:
            error = 'Artwork is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (user_id, artwork, description) VALUES (?, ?, ?)',
                (g.user['id'], filename, description)
            )
            db.commit()
            return redirect(url_for('post.index'))

    return render_template('post/create.html')

# Update post
def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, artwork, description, created, user_id, username'
        ' FROM post p JOIN user u ON p.user_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and post['user_id'] != g.user['id']:
        abort(403)

    return post

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        description = request.form['description']
        artwork = request.files.get('artwork')
        error = None

        # If the user uploads a new artwork, save it, else keep the existing one
        if artwork:
            filename = secure_filename(artwork.filename)
            if filename != '':
                # Save to the 'artworks' folder
                artwork_path = os.path.join(current_app.config['ARTWORKS_FOLDER'], filename)
                artwork.save(artwork_path)
        else:
            filename = post['artwork']

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET description = ?, artwork = ? WHERE id = ?',
                (description, filename, id)
            )
            db.commit()
            return redirect(url_for('post.index'))

    return render_template('post/update.html', post=post)

# Delete Post
@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('post.index'))

# Likes
@bp.route('/post/<int:id>/like', methods=('POST',))
@login_required
def like(id):
    db = get_db()

    # Check if the user has already liked the post
    existing_like = db.execute(
        'SELECT id FROM likes WHERE user_id = ? AND post_id = ?', (g.user['id'], id)
    ).fetchone()

    if existing_like:
        # If the user already liked the post, remove the like (toggle behavior)
        db.execute('DELETE FROM likes WHERE id = ?', (existing_like['id'],))
    else:
        # Add a new like
        db.execute('INSERT INTO likes (user_id, post_id) VALUES (?, ?)', (g.user['id'], id))

    db.commit()
    return redirect(url_for('post.index'))

# Comments
@bp.route('/post/<int:id>/comment', methods=['POST'])
@login_required
def comment(id):
    comment_body = request.form['comment']
    db = get_db()
    db.execute('INSERT INTO comment (user_id, post_id, body) VALUES (?, ?, ?)', (g.user['id'], id, comment_body))
    db.commit()
    return redirect(url_for('post.view_post', id=id))





