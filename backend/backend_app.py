from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
from uuid import uuid4



app = Flask(__name__)
CORS(app)

SWAGGER_URL = "/api/docs"
API_URL = "/static/masterblog.json"

swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': 'Masterblog API'
    }
)
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

POSTS = [
    {"id": 1, "title": "Cherry Blossom", "content": "Pink petals falling\nDancing in the spring breeze now\nNature's sweet goodbye"},
    {"id": 2, "title": "Morning Dew", "content": "Dewdrops on grass blades\nSparkling in morning sunshine\nDay begins anew"},
    {"id": 3, "title": "Autumn Moon", "content": "Harvest moon rises\nCasting shadows on the ground\nCrickets sing tonight"},
    {"id": 4, "title": "Winter Snow", "content": "Soft flakes drifting down\nBlanket of white covers earth\nSilent winter's dream"},
    {"id": 5, "title": "Mountain Path", "content": "Climbing mountain trails\nMist surrounds the rocky peaks\nBirds soar up above"},
    {"id": 6, "title": "Ocean Waves", "content": "Waves crash on the shore\nFoam spreads across golden sand\nTide pulls back again"},
    {"id": 7, "title": "Summer Rain", "content": "Thunder rolls distant\nRain drums against windowpanes\nLightning splits the sky"},
    {"id": 8, "title": "Forest Walk", "content": "Green leaves filter light\nMossy stones mark ancient paths\nQuiet forest peace"},
    {"id": 9, "title": "Night Sky", "content": "Stars pierce velvet dark\nMilky Way flows overhead\nCosmic river flows"},
    {"id": 10, "title": "Garden Life", "content": "Busy bees hover\nButterflies dance through the air\nFlowers wave hello"}
]

@app.route('/api/posts', methods=['GET'])
def get_posts():
    """
    List all posts with optional sorting by title or content.
    Supports query parameters: sort (title/content) and direction (asc/desc).
    Returns: JSON response with posts list.
    """
    sort_field = request.args.get('sort')
    sort_direction = request.args.get('direction', 'asc')

    if not sort_field:
        return jsonify(POSTS)

    # Validate sort parameters
    if sort_field not in ['title', 'content']:
        return jsonify({'error': 'Sort field must be either "title" or "content"'}), 400

    if sort_direction not in ['asc', 'desc']:
        return jsonify({'error': 'Direction must be either "asc" or "desc"'}), 400

    # Sort the posts
    sorted_posts = sorted(
        POSTS,
        key=lambda x: x[sort_field].lower(),
        reverse=(sort_direction == 'desc')
    )

    return jsonify(sorted_posts)

@app.route('/api/posts/', methods=['POST'])
def add_post():
    """
    Create a new post with a UUID.
    Accepts: JSON with title and content fields.
    Returns: Created post with 201 status code.
    """
    data = request.get_json()
    post = {
        "id": str(uuid4()),
        "title": data.get('title'),
        "content": data.get('content')
    }
    POSTS.append(post)
    return jsonify(post), 201

@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    """
    Delete a post by ID.
    Parameters: post_id (int)
    Returns: Success/error message with appropriate status code.
    """
    for index, post in enumerate(POSTS):
        if post['id'] == post_id:
            POSTS.pop(index)
            return jsonify({"message": f"Post with id {post_id} has been deleted successfully."}), 200

    return jsonify({"error": f"Post with id {post_id} not found"}), 404

@app.route('/api/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    """
    Update a post by ID.
    Parameters: post_id (int)
    Accepts: JSON with optional title and content fields.
    Returns: Updated post or error message.
    """
    data = request.get_json()
    for post in POSTS:
        if post['id'] == post_id:
            if 'title' in data:
                post['title'] = data['title']
            if 'content' in data:
                post['content'] = data['content']
            return jsonify(post), 200
    return jsonify({"error": f"Post with id {post_id} not found"}), 404

@app.route('/api/posts/search', methods=['GET'])
def search_posts():
    """
    Search posts by title or content.
    Accepts query parameters: title, content
    Returns: List of matching posts.
    """
    title_query = request.args.get('title', '').lower()
    content_query = request.args.get('content', '').lower()

    for post in POSTS:
        if (title_query and title_query in post['title'].lower()) or \
                (content_query and content_query in post['content'].lower()):
            matching_posts.append(post)

    return jsonify(matching_posts)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)