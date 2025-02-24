from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]

@app.route('/api/posts', methods=['GET'])
def get_posts():
    return jsonify(POSTS)

@app.route('/api/add/', methods=['POST'])
def add_post():
    data = request.get_json()
    title = data.get('title')
    content = data.get('content')

    post = {"id": len(POSTS) + 1, "title": title, "content": content}
    POSTS.append(post)
    return jsonify(post), 201

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)