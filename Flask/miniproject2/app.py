from flask import Flask, request, render_template

app = Flask(__name__)

users = [
    {
        "username": "leo",
        "posts": [{"title": "Town House", "likes": 120}]
    },
    {
        "username": "alex",
        "posts": [{"title": "Mountain Climbing", "likes": 350}, {"title": "River Rafting", "likes": 200}]
    },
    {
        "username": "kim",
        "posts": [{"title": "Delicious Ramen", "likes": 230}]
    }
]

@app.get('/')
def index():
    return render_template('index.html', users=users)

@app.get('/users')
def get_users():
    return {'users': users}

@app.post('/users')
def create_users():
    request_data = request.get_json()
    new_user = {'username': request_data['username']}
    users.append(new_user)
    return new_user, 201

@app.post('/user/post/<username>')
def add_post(username):
    request_data = request.get_json()
    for user in users:
        if user["username"] == username:
            new_post = {"title": request_data["title"], "likes": request_data["likes"]}
            user["posts"].append(new_post)
            return new_post
        
    return {"사용자를 찾을 수 없습니다"}, 404

@app.get("/users/post/<username>")
def get_posts_of_user(username):
    for user in users:
        if user["username"] == username:
            return {"posts": user["posts"]}

    return {"사용자를 찾을 수 없습니다"}, 404

@app.put("/users/post/like/<username>/<title>")
def like_post(username, title):
    for user in users:
        if user["username"] == username:
            for post in user["posts"]:
                if post["title"] == title:
                    post["likes"] += 1
                    return post

    return {"게시물을 찾을 수 없습니다"}, 404

@app.delete("/users/<username>")
def delete_user(username):
    global users
    users = [user for user in users if user["username"] != username]

    return {'계정이 삭제되었습니다'}, 200


if __name__ == '__main__':
    app.run(debug=True)