from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, current_app
)
from werkzeug.utils import secure_filename
from artit.auth import login_required
from artit.db import get_db
import os

bp = Blueprint('profile', __name__)

# Profile page (shows user's profile and uploaded artworks)
@bp.route('/profile', methods=('GET',))
@login_required
def profile():
    db = get_db()
    user = db.execute(
        'SELECT id, username, firstname, lastname, bio, avatar FROM user WHERE id = ?', (g.user['id'],)
    ).fetchone()
    artworks = db.execute(
        'SELECT id, artwork, description, created FROM post WHERE user_id = ? ORDER BY created DESC', (g.user['id'],)
    ).fetchall()
    print(artworks)
    return render_template('profile/index.html', user=user, artworks=artworks)

# Edit profile page
@bp.route('/profile/update', methods=('GET', 'POST'))
@login_required
def update():
    db = get_db()

    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        username = request.form['username']
        bio = request.form['bio']
        avatar = request.files.get('avatar')
        filename = g.user['avatar']

        if avatar:
            filename = secure_filename(avatar.filename)
            if filename != '':
                avatar_path = os.path.join(current_app.config['AVATARS_FOLDER'], filename)
                avatar.save(avatar_path)

        db.execute(
            'UPDATE user SET username = ?, firstname = ?, lastname = ?, bio = ?, avatar = ? WHERE id = ?',
            (username, firstname, lastname, bio, filename, g.user['id'])
        )
        db.commit()

        return redirect(url_for('profile.profile'))

    # Pre-populate the form with current user info
    user = db.execute(
        'SELECT firstname, lastname, username, bio, avatar FROM user WHERE id = ?', (g.user['id'],)
    ).fetchone()

    if user is None:
        flash('User not found.')
        return redirect(url_for('profile.profile'))

    return render_template('profile/update.html', user=user)

