import pytest
from uuid import uuid4
from backend_app import app, POSTS

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_get_posts(client):
    response = client.get('/api/posts')
    assert response.status_code == 200
    assert len(response.get_json()) == len(POSTS)

def test_post_new_post(client):
    new_post = {"title": "Test Post", "content": "This is a test post."}
    response = client.post('/api/posts', json=new_post)
    assert response.status_code == 201
    assert 'id' in response.get_json()

def test_delete_post(client):
    post_id = str(uuid4())
    POSTS.append({"id": post_id, "title": "To be deleted", "content": "This post will be deleted."})
    response = client.delete(f'/api/posts/{post_id}')
    assert response.status_code == 200
    assert response.get_json()['message'] == f"Post with id {post_id} has been deleted successfully."

def test_delete_nonexistent_post(client):
    response = client.delete(f'/api/posts/{uuid4()}')
    assert response.status_code == 404
    assert 'error' in response.get_json()

def test_update_post(client):
    post_id = str(uuid4())
    POSTS.append({"id": post_id, "title": "To be updated", "content": "This post will be updated."})
    updated_data = {"title": "Updated Title", "content": "Updated content."}
    response = client.put(f'/api/posts/{post_id}', json=updated_data)
    assert response.status_code == 200
    assert response.get_json()['title'] == "Updated Title"
    assert response.get_json()['content'] == "Updated content."

def test_update_nonexistent_post(client):
    updated_data = {"title": "Updated Title", "content": "Updated content."}
    response = client.put(f'/api/posts/{uuid4()}', json=updated_data)
    assert response.status_code == 404
    assert 'error' in response.get_json()

def test_search_posts(client):
    response = client.get('/api/posts/search?title=Cherry')
    assert response.status_code == 200
    assert len(response.get_json()) > 0

def test_invalid_uuid_format(client):
    response = client.delete('/api/posts/invalid-uuid')
    assert response.status_code == 400
    assert 'error' in response.get_json()