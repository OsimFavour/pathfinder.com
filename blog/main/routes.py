import os
from io import BytesIO
from flask import render_template, send_file, flash, redirect, url_for, request, Blueprint
from flask_login import current_user
from blog import db
from blog.models import PurposePost, RelationshipPost, Fiction, Newsletter, Upload, EmailSubscriber
from blog.users.forms import EmailSubscriberForm, ContactForm
from blog.users.utils import send_email

main = Blueprint("main", __name__)


# SHOW POSTS

@main.route('/')
def home():
    posts = PurposePost.query.order_by(PurposePost.date.desc()).limit(4).all()
    fiction_posts = Fiction.query.order_by(Fiction.date.desc()).limit(4).all()
    # return render_template("index.html", all_posts=posts, current_user=current_user)
    return render_template("home.html", all_posts=posts, fiction_stories=fiction_posts, current_user=current_user)


@main.route("/purpose")
def purpose():
    page = request.args.get("page", 1, type=int)
    posts = PurposePost.query.order_by(PurposePost.date.desc()).paginate(page=page, per_page=5)
    return render_template("index-purpose.html", all_posts=posts, current_user=current_user)
    

@main.route("/relationship")
def relationship():
    page = request.args.get("page", 1, type=int)
    posts = RelationshipPost.query.order_by(RelationshipPost.date.desc()).paginate(page=page, per_page=5)
    return render_template("index-relationship.html", all_posts=posts, current_user=current_user)


@main.route("/fiction")
def fiction():
    page = request.args.get("page", 1, type=int)
    posts = Fiction.query.order_by(Fiction.date.desc()).paginate(page=page, per_page=5)
    return render_template("index-fiction.html", all_posts=posts, current_user=current_user)


@main.route("/newsletter", methods=["GET", "POST"])
def newsletter():
    form = EmailSubscriberForm()
    if request.method == "POST":
    # if form.validate_on_submit():
        # email = form.email.data
        email = request.form.get("email")
        print(email)
        if current_user.is_authenticated:
            name = current_user.name
            print(name)
        else:
            name = None
        subscriber = EmailSubscriber(
            name=name, 
            email=email
            )
        db.session.add(subscriber)
        db.session.commit()
        flash("You have subscribed successfully", "success")
        return redirect(url_for('main.newsletter'))
    page = request.args.get("page", 1, type=int)
    posts = Newsletter.query.order_by(Newsletter.date.desc()).paginate(page=page, per_page=5)
    return render_template("index-newsletter.html", all_posts=posts, form=form)


@main.route("/my-books", methods=["GET", "POST"])
def others():
    if request.method == "POST":
        # file = request.files["file"]
        file = request.files.get("file")
        upload = Upload(filename=file.filename, data=file.read())
        db.session.add(upload)
        db.session.commit()
        return f"Uploaded: {file.filename}"
    return render_template("others.html")


@main.route("/download/<upload_id>")
def download(upload_id):
    upload = Upload.query.filter_by(id=upload_id).first()
    return send_file(BytesIO(upload.data), attachment_filename=upload.filename, as_attachment=True)




# @app.route("/search", methods=["POST"])
# def search():
#     form = SearchForm()
#     if form.validate_on_submit():
#         searched_post = form.searched.data
#         posts = BlogPost.query.filter(BlogPost.body.like("%" + searched_post + "%"))
#         ordered_posts = posts.order_by(BlogPost.title).all()
#         return render_template("search.html", form=form, searched=searched_post, posts=ordered_posts)


# @main.route("/about")
# def about():
#     posts = PurposePost.query.order_by(PurposePost.date.desc())
#     return render_template("about-new.html", all_posts=posts, current_user=current_user)


@main.route("/contact", methods=["GET", "POST"])
def contact():
    form = ContactForm()
    if request.method == "POST":
        MAIL_USERNAME = os.environ.get("MY_EMAIL")
        name = request.form.get("name")
        email = request.form.get("email")
        telephone = request.form.get("telephone")
        message = request.form.get("message")
        send_email(
            admin_email=MAIL_USERNAME,
            name=name,
            email=email,
            phone=telephone,
            message=message
        )
        flash("We've received your mail, You'd get a response from us soon.", "success")
        return redirect(url_for('main.contact'))
    return render_template("contact.html", form=form)


