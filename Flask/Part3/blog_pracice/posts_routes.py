from flask import request, jsonify
from flask_smorest import Blueprint, abort

def create_posts_blueprint(mysql):
    posts_blp = Blueprint('posts', __name__, description='posts api', url_prefix='/posts')

    @posts_blp.route('/', methods=['GET', 'POST'])
    def posts():
        cursor = mysql.connection.cursor()
        if request.method == 'GET':
            sql = 'SELECT * FROM posts'
            cursor.execute(sql)

            posts = cursor.fetchall()
            cursor.close()

            post_list = []

            for post in posts:
                post_list.append({
                    'id': post[0],
                    'title': post[1],
                    'content': post[2]
                })

            return jsonify(post_list)
        
        if request.method == 'POST':
            title = request.json.get('title')
            content = request.json.get('content')

            if not title or not content:
                abort(400, message='title이나 content는 비워둘 수 없습니다.')
            
            sql = 'INSERT INTO posts(title, content) VALUES(%s, %s)'
            cursor.execute(sql, (title, content))
            mysql.connection.commit()

            return jsonify({'msg':'데이터를 성공적으로 등록했습니다.', 'title':title, 'content':content})
        
    @posts_blp.route("/<int:id>", methods=["GET", "PUT", "DELETE"])
    def post(id):
        cursor = mysql.connection.cursor()

        if request.method == 'GET':
            sql = f'SELECT * FROM posts WHERE id = {id}'
            cursor.execute(sql)
            post = cursor.fetchone()

            if not post:
                abort(404, '포스트를 찾을 수 없습니다')
            return ({'id': post[0], 'title': post[1], 'content': post[2]})
        elif request.method == 'PUT':
            title = request.json.get('title')
            content = request.json.get('content')

            if not title or not content:
                abort(400, 'title이나 content는 비워둘 수 없습니다.')
                
            sql = f'UPDATE posts SET title="{title}", content="{content}" WHERE id={id}'
            cursor.execute(sql)
            mysql.connection.commit()

            return jsonify({'msg': 'title과 content가 성공적으로 업데이트되었습니다.'})
        elif request.method == 'DELETE':
            sql = f'DELETE FROM posts WHERE id={id}'
            cursor.execute(sql)
            mysql.connection.commit()

            return jsonify({'msg': 'title과 content가 성공적으로 제거되었습니다.'})
            
    return posts_blp