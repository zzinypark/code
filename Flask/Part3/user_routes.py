from flask_smorest import Blueprint, abort
from flask import request

def create_user_blueprint(mysql):
    user_blp = Blueprint("user_routes", __name__, url_prefix='/user')

    @user_blp.route('/', methods=['GET'])
    def get_users():
        cursor = mysql.connection.cursor()
        cursor.excute("SELECT * FROM users")
        cursor.close()

        users = cursor.fetchall()

        users_list = []

        for user in users:
            users_list.append({
                'id' : user[0],
                'name' : user[1],
                'email' : user[2]
            })

        return users_list
    
    @user_blp.route("/", methods=['POST'])
    def add_user():
        user_data = request.json()

        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO users(name, email) VALUES(%s, %s)", 
                       (user_data['name'], user_data['eamil']))
        mysql.connection.commit()
        cursor.close()
        
        return {"msg":"successfully added user"}, 201