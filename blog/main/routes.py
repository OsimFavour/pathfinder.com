from io import BytesIO
from flask import render_template, send_file, request, Blueprint
from flask_login import current_user
from blog import app, db
from blog.users.forms import SearchForm
from blog.models import PurposePost, RelationshipPost, Fiction, Newsletter, Upload

main = Blueprint("main", __name__)


# Passing searched data to the navbar
@app.context_processor
def base():
    form = SearchForm()
    return dict(form=form)


@main.route('/')
def home():
    page = request.args.get("page", 1, type=int)
    posts = PurposePost.query.order_by(PurposePost.date.desc()).paginate(page=page, per_page=5)
    # return render_template("index.html", all_posts=posts, current_user=current_user)
    return render_template("home.html", all_posts=posts, current_user=current_user)


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


@main.route("/newsletter")
def newsletter():
    page = request.args.get("page", 1, type=int)
    posts = Newsletter.query.order_by(Newsletter.date.desc()).paginate(page=page, per_page=5)
    return render_template("index-newsletter.html", all_posts=posts)


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


@main.route("/search", methods=["POST"])
def search():
    form = SearchForm()
    if form.validate_on_submit():
        searched_post = form.searched.data
        posts = [
            PurposePost.query.filter(PurposePost.body.like("%" + searched_post + "%")), 
            RelationshipPost.query.filter(RelationshipPost.body.like("%" + searched_post + "%")), 
            Fiction.query.filter(Fiction.body.like("%" + searched_post + "%")), 
            Newsletter.query.filter(Newsletter.body.like("%" + searched_post + "%"))
            ]
        for post in posts:
            blog_posts = post.order_by(posts.title).all()
            # ordered_posts = posts.order_by(post.title).all()
        return render_template("search.html", form=form, searched=searched_post, posts=blog_posts)


# @app.route("/search", methods=["POST"])
# def search():
#     form = SearchForm()
#     if form.validate_on_submit():
#         searched_post = form.searched.data
#         posts = BlogPost.query.filter(BlogPost.body.like("%" + searched_post + "%"))
#         ordered_posts = posts.order_by(BlogPost.title).all()
#         return render_template("search.html", form=form, searched=searched_post, posts=ordered_posts)


@main.route("/about")
def about():
    posts = PurposePost.query.order_by(PurposePost.date.desc())
    return render_template("about.html", all_posts=posts, current_user=current_user)


@main.route("/contact")
def contact():
    return render_template("contact.html", current_user=current_user)

