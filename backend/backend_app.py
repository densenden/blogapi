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
    {"id": str(uuid4()), "title": "Cherry Blossom", "content": "Pink petals falling\nDancing in the spring breeze now\nNature's sweet goodbye"},
    {"id": str(uuid4()), "title": "Morning Dew", "content": "Dewdrops on grass blades\nSparkling in morning sunshine\nDay begins anew"},
    {"id": str(uuid4()), "title": "Autumn Moon", "content": "Harvest moon rises\nCasting shadows on the ground\nCrickets sing tonight"},
    {"id": str(uuid4()), "title": "Winter Snow", "content": "Soft flakes drifting down\nBlanket of white covers earth\nSilent winter's dream"},
    {"id": str(uuid4()), "title": "Mountain Path", "content": "Climbing mountain trails\nMist surrounds the rocky peaks\nBirds soar up above"},
    {"id": str(uuid4()), "title": "Ocean Waves", "content": "Waves crash on the shore\nFoam spreads across golden sand\nTide pulls back again"},
    {"id": str(uuid4()), "title": "Summer Rain", "content": "Thunder rolls distant\nRain drums against windowpanes\nLightning splits the sky"},
    {"id": str(uuid4()), "title": "Forest Walk", "content": "Green leaves filter light\nMossy stones mark ancient paths\nQuiet forest peace"},
    {"id": str(uuid4()), "title": "Night Sky", "content": "Stars pierce velvet dark\nMilky Way flows overhead\nCosmic river flows"},
    {"id": str(uuid4()), "title": "Garden Life", "content": "Busy bees hover\nButterflies dance through the air\nFlowers wave hello"}
]

@app.route('/api/posts', methods=['GET', 'POST'])
def posts():
    if request.method == 'GET':
        sort_field = request.args.get('sort')
        sort_direction = request.args.get('direction', 'asc')

        if not sort_field:
            return jsonify(POSTS)

        if sort_field not in ['title', 'content']:
            return jsonify({'error': 'Sort field must be either "title" or "content"'}), 400

        if sort_direction not in ['asc', 'desc']:
            return jsonify({'error': 'Direction must be either "asc" or "desc"'}), 400

        sorted_posts = sorted(
            POSTS,
            key=lambda x: x[sort_field].lower(),
            reverse=(sort_direction == 'desc')
        )

        return jsonify(sorted_posts)

    elif request.method == 'POST':
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
    for index, post in enumerate(POSTS):
        if post['id'] == post_id:
            POSTS.pop(index)
            return jsonify({"message": f"Post with id {post_id} has been deleted successfully."}), 200

    return jsonify({"error": f"Post with id {post_id} not found"}), 404

@app.route('/api/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
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
    title_query = request.args.get('title', '').lower()
    matching_posts = []
    for post in POSTS:
        if (title_query and title_query in post['title'].lower()) or \
                (content_query and content_query in post['content'].lower()):
            matching_posts.append(post)

    return jsonify(matching_posts)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)