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
    posts = db.execute(
        'SELECT p.id, artwork, description, created, user_id, firstname, avatar, '
        '(SELECT COUNT(*) FROM likes WHERE post_id = p.id) as likes_count, '
        '(SELECT COUNT(*) FROM comment WHERE post_id = p.id) as comments_count '
        'FROM post p JOIN user u ON p.user_id = u.id '
        'ORDER BY p.created DESC'
    ).fetchall()
    return render_template('post/index.html', posts=posts)

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

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('post.index'))