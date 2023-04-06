from flask import render_template, request, url_for, flash, redirect, abort, Blueprint
from flask_login import current_user, login_required
from blog import db, admin_only
from blog.models import PurposePost, RelationshipPost, Fiction, Newsletter, Comment
from blog.posts.forms import CreatePostForm, CommentForm
from bs4 import BeautifulSoup

posts = Blueprint("posts", __name__)


# SHOW POSTS

@posts.route("/purpose-post/<int:purpose_post_id>", methods=["GET", "POST"])
@login_required
def show_purpose_post(purpose_post_id):
    form = CommentForm()
    requested_post = PurposePost.query.get(purpose_post_id)
    if form.validate_on_submit():
        if not current_user.is_authenticated:
            flash("You need to login or register to comment.", "info")
            return redirect(url_for("login"))
        new_comment = Comment(
            text=form.comment.data,
            comment_author=current_user,
            parent_post=requested_post
        )
        db.session.add(new_comment)
        db.session.commit()
    return render_template("post-purpose.html", form=form, post=requested_post, title=requested_post.title, current_user=current_user, is_purpose=True)


@posts.route("/relationship/<int:relationship_post_id>", methods=["GET", "POST"])
@login_required
def show_relationship_post(relationship_post_id):
    form = CommentForm()
    requested_post = RelationshipPost.query.get(relationship_post_id)
    if form.validate_on_submit():
        if not current_user.is_authenticated:
            flash("You need to login or register to comment.", "info")
            return redirect(url_for("login"))
        new_comment = Comment(
            text=form.comment.data,
            comment_author=current_user,
            parent_post=requested_post
        )
        db.session.add(new_comment)
        db.session.commit()
    return render_template("post-relationship.html", form=form, post=requested_post, title=requested_post.title, current_user=current_user, is_relationship=True)


@posts.route("/fiction/<int:fiction_post_id>", methods=["GET", "POST"])
@login_required
def show_fiction_post(fiction_post_id):
    form = CommentForm()
    requested_post = Fiction.query.get(fiction_post_id)
    if form.validate_on_submit():
        if not current_user.is_authenticated:
            flash("You need to login or register to comment.", "info")
            return redirect(url_for("login"))
        new_comment = Comment(
            text=form.comment.data,
            comment_author=current_user,
            parent_post=requested_post
        )
        db.session.add(new_comment)
        db.session.commit()
    return render_template("post-fiction.html", form=form, post=requested_post, title=requested_post.title, current_user=current_user, is_fiction=True)


@posts.route("/newsletter/<int:newsletter_id>", methods=["GET", "POST"])
@login_required
def show_newsletter(newsletter_id):
    form = CommentForm()
    requested_post = Newsletter.query.get(newsletter_id)
    if form.validate_on_submit():
        if not current_user.is_authenticated:
            flash("You need to login or register to comment.", "info")
            return redirect(url_for("login"))
        new_comment = Comment(
            text=form.comment.data,
            comment_author=current_user,
            parent_post=requested_post
        )
        db.session.add(new_comment)
        db.session.commit()
    return render_template("post-newsletter.html", form=form, post=requested_post, title=requested_post.title, current_user=current_user, is_newsletter=True)


# MAKE NEW POSTS

@posts.route("/new-post-purpose", methods=["GET", "POST"])
@admin_only
def add_for_purpose():
    form = CreatePostForm()
    # soup = BeautifulSoup(form.body.data, "html.parser")
    if form.validate_on_submit():
        new_post = PurposePost(
            title=form.title.data,
            subtitle=form.subtitle.data,
            body=form.body.data,
            img_url=form.img_url.data,
            author=current_user
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("make-post.html", title="Post-Purpose", form=form, current_user=current_user, add_for_purpose=True)


@posts.route("/new-post-relationship", methods=["GET", "POST"])
@admin_only
def add_for_relationship():
    form = CreatePostForm()
    # soup = BeautifulSoup(form.body.data, "html.parser")
    if form.validate_on_submit():
        new_post = Newsletter(
            title=form.title.data,
            subtitle=form.subtitle.data,
            body=form.body.data,
            img_url=form.img_url.data,
            author=current_user
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("make-post.html", title="Post-Relationship", form=form, current_user=current_user, add_for_relationship=True)


@posts.route("/new-post-fiction", methods=["GET", "POST"])
@admin_only
def add_for_fiction():
    form = CreatePostForm()
    # soup = BeautifulSoup(form.body.data, "html.parser")
    if form.validate_on_submit():
        new_post = Fiction(
            title=form.title.data,
            subtitle=form.subtitle.data,
            body=form.body.data,
            img_url=form.img_url.data,
            author=current_user
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("make-post.html", title="Post-Fiction", form=form, current_user=current_user, add_for_fiction=True)


@posts.route("/new-post-newsletter", methods=["GET", "POST"])
@admin_only
def add_for_newsletter():
    form = CreatePostForm()
    # soup = BeautifulSoup(form.body.data, "html.parser")
    if form.validate_on_submit():
        new_post = Newsletter(
            title=form.title.data,
            subtitle=form.subtitle.data,
            body=form.body.data,
            img_url=form.img_url.data,
            author=current_user
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("make-post.html", title="Post-Newsletters", form=form, current_user=current_user, add_for_newsletter=True)


# EDIT POSTS


@posts.route("/edit-post-purpose/<int:purpose_post_id>", methods=["GET", "POST"])
@admin_only
def edit_purpose_post(purpose_post_id):
    post = PurposePost.query.get(purpose_post_id)
    edit_form = CreatePostForm(
        title=post.title,
        subtitle=post.subtitle,
        img_url=post.img_url,
        author=current_user,
        body=post.body
    )
    soup = BeautifulSoup(edit_form.body.data, "html.parser")
    if edit_form.validate_on_submit():
        post.title = edit_form.title.data
        post.subtitle = edit_form.subtitle.data
        post.img_url = edit_form.img_url.data
        post.body = soup.text
        db.session.commit()
        return redirect(url_for("show_purpose_post", purpose_post_id=post.id))

    return render_template("make-post.html", form=edit_form, current_user=current_user, edit_for_purpose=True)


@posts.route("/edit-post-relationship/<int:relationship_post_id>", methods=["GET", "POST"])
@admin_only
def edit_relationship_post(relationship_post_id):
    post = RelationshipPost.query.get(relationship_post_id)
    edit_form = CreatePostForm(
        title=post.title,
        subtitle=post.subtitle,
        img_url=post.img_url,
        author=current_user,
        body=post.body
    )
    soup = BeautifulSoup(edit_form.body.data, "html.parser")
    if edit_form.validate_on_submit():
        post.title = edit_form.title.data
        post.subtitle = edit_form.subtitle.data
        post.img_url = edit_form.img_url.data
        post.body = soup.text
        db.session.commit()
        return redirect(url_for("show_relationship_post", relationship_post_id=post.id))

    return render_template("make-post.html", form=edit_form, current_user=current_user, edit_for_relationship=True)


@posts.route("/edit-post-fiction/<int:fiction_post_id>", methods=["GET", "POST"])
@admin_only
def edit_fiction_post(fiction_post_id):
    post = Fiction.query.get(fiction_post_id)
    edit_form = CreatePostForm(
        title=post.title,
        subtitle=post.subtitle,
        img_url=post.img_url,
        author=current_user,
        body=post.body
    )
    soup = BeautifulSoup(edit_form.body.data, "html.parser")
    if edit_form.validate_on_submit():
        post.title = edit_form.title.data
        post.subtitle = edit_form.subtitle.data
        post.img_url = edit_form.img_url.data
        post.body = soup.text
        db.session.commit()
        return redirect(url_for("show_fiction_post", fiction_post_id=post.id))

    return render_template("make-post.html", form=edit_form, current_user=current_user, edit_for_fiction=True)


@posts.route("/edit-post-newsletter/<int:newsletter_id>", methods=["GET", "POST"])
@admin_only
def edit_newsletter(newsletter_id):
    post = Newsletter.query.get(newsletter_id)
    edit_form = CreatePostForm(
        title=post.title,
        subtitle=post.subtitle,
        img_url=post.img_url,
        author=current_user,
        body=post.body
    )
    soup = BeautifulSoup(edit_form.body.data, "html.parser")
    if edit_form.validate_on_submit():
        post.title = edit_form.title.data
        post.subtitle = edit_form.subtitle.data
        post.img_url = edit_form.img_url.data
        post.body = soup.text
        db.session.commit()
        return redirect(url_for("show_newsletter", newsletter_id=post.id))

    return render_template("make-post.html", form=edit_form, current_user=current_user, edit_for_newsletter=True)


# DELETE POSTS


@posts.route("/delete-purpose-post/<int:purpose_post_id>", methods=["POST"])
@admin_only
def delete_purpose_post(purpose_post_id):
    post_to_delete = PurposePost.query.get(purpose_post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


@posts.route("/delete-relationship-post/<int:relationship_post_id>", methods=["POST"])
@admin_only
def delete_relationship_post(relationship_post_id):
    post_to_delete = RelationshipPost.query.get(relationship_post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


@posts.route("/delete-fiction-post/<int:fiction_post_id>", methods=["POST"])
@admin_only
def delete_fiction_post(fiction_post_id):
    post_to_delete = Fiction.query.get(fiction_post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


@posts.route("/delete-newsletter/<int:newsletter_id>", methods=["POST"])
@admin_only
def delete_newsletter(newsletter_id):
    post_to_delete = Newsletter.query.get(newsletter_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('home'))
