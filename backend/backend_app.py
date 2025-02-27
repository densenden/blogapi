from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

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
    return jsonify(POSTS)

@app.route('/api/add/', methods=['POST'])
def add_post():
    data = request.get_json()
    title = data.get('title')
    content = data.get('content')

    post = {"id": len(POSTS) + 1, "title": title, "content": content}
    POSTS.append(post)
    return jsonify(post), 201

@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    for index, post in enumerate(POSTS):
        if post['id'] == post_id:
            POSTS.pop(index)
            return jsonify({"message": f"Post with id {post_id} has been deleted successfully."}), 200
    returnapp.route('/api/posts/<int:post_id>', methods=['PUT'])
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

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)