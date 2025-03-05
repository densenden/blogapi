var savedBaseUrl = localStorage.getItem('apiBaseUrl');
    if (savedBaseUrl) {
        document.getElementById('api-base-url').value = savedBaseUrl;
        loadPosts();
    }
}

function loadPosts() {
    var baseUrl = document.getElementById('api-base-url').value;
    localStorage.setItem('apiBaseUrl', baseUrl);

    fetch(baseUrl + '/posts')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            const postContainer = document.getElementById('post-container');
            postContainer.innerHTML = '';

            data.forEach(post => {
                const postDiv = document.createElement('div');
                postDiv.className = 'post';
                postDiv.innerHTML = `
                    <h2>${escapeHtml(post.title)}</h2>
                    <p>${escapeHtml(post.content)}</p>
                    <button onclick="deletePost('${post.id}')">Delete</button>
                `;
                postContainer.appendChild(postDiv);
            });
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Failed to load posts');
        });
}

function addPost() {
    var baseUrl = document.getElementById('api-base-url').value;
    var postTitle = document.getElementById('post-title').value;
    var postContent = document.getElementById('post-content').value;

    if (!postTitle || !postContent) {
        alert('Please fill in both title and content');
        return;
    }

    fetch(baseUrl + '/posts', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title: postTitle, content: postContent })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(post => {
        document.getElementById('post-title').value = '';
        document.getElementById('post-content').value = '';
        loadPosts();
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Failed to add post');
    });
}

function deletePost(postId) {
    if (!postId) {
        console.error('Post ID is required');
        return;
    }

    var baseUrl = document.getElementById('api-base-url').value;

    fetch(baseUrl + '/posts/' + postId, {
        method: 'DELETE'
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(() => {
        loadPosts();
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Failed to delete post');
    });
}

function escapeHtml(unsafe) {
    return unsafe
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}