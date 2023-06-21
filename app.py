from flask import Flask, render_template, request, redirect
import json

app = Flask(__name__)


def get_data_from_json():
    """Gets a dict from the json data file"""
    with open("data.json", 'r') as file:
        return json.loads(file.read())


def save_data_to_json(data):
    """Saves provided dict to the json data file"""
    with open("data.json", 'w') as file:
        file.write(json.dumps(data, indent=4))


def fetch_post_by_id(id_, blog_posts):
    """Returns post based on provided id"""
    for i in range(len(blog_posts)):
        if blog_posts[i]["id"] == id_:
            return blog_posts[i]


def add_post_from_form(post_id, form_dict, blog_posts):
    """Adds or updates single post and saves new updated data to json file"""
    print(form_dict)
    post = fetch_post_by_id(post_id, blog_posts)
    if post is None:
        post = {'id': post_id}
        blog_posts.append(post)
    post['author'] = form_dict.get('author')
    post['title'] = form_dict.get('title')
    post['content'] = form_dict.get('content')
    post['likes'] = form_dict.get('likes', 0)
    save_data_to_json(blog_posts)


@app.route('/')
def index():
    """Homepage route"""
    blog_posts = get_data_from_json()
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    """Add new post func if method is GET shows form to add new post
    If method is POST, adds the post to data file"""
    blog_posts = get_data_from_json()
    if request.method == 'POST':
        id_ = len(blog_posts) + 1
        add_post_from_form(id_, request.form, blog_posts)

        return redirect(app.url_for("index"))
    return render_template('add.html')


@app.route('/delete/<int:post_id>')
def delete(post_id):
    """Deletes post from data file"""
    blog_posts = get_data_from_json()
    post = fetch_post_by_id(post_id, blog_posts)

    if post is None:
        return "Post not found", 404
    else:
        blog_posts.remove(post)
        save_data_to_json(blog_posts)

    return redirect(app.url_for("index"))


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    """Update post if method is GET shows form with current post data
    If method is POST, updates the post to data file"""
    blog_posts = get_data_from_json()
    post = fetch_post_by_id(post_id, blog_posts)

    if post is None:
        return "Post not found", 404

    if request.method == 'POST':
        add_post_from_form(post_id, request.form, blog_posts)
        return redirect(app.url_for("index"))

    return render_template('update.html', post=post)


@app.route('/like/<int:post_id>')
def like(post_id):
    blog_posts = get_data_from_json()
    post = fetch_post_by_id(post_id, blog_posts)
    post['likes'] += 1
    save_data_to_json(blog_posts)
    return redirect(app.url_for("index"))


if __name__ == "__main__":
    # Launch the Flask dev server
    app.run(host="0.0.0.0", port=5000, debug=True)
