from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route("/api/v1/feeds", methods=["GET"])
def show_all_feeds():
    data = {"result":"success", "data":{"feed1":"data1", "feed2":"data2"}}

    return data

@app.route("/api/v1/feeds/<int:feed_id>", methods=["GET"])
def show_one_feed(feed_id):
    print(feed_id)
    data = {"result":"success", "data":{"feed1":"data1"}}

    return data

@app.route("/api/v1/feeds", methods=["POST"])
def create_one_feed():
    name = request.form["name"]
    age = request.form["age"]

    print(name, age)

    return jsonify({"result":"success"})

datas = [{"items": [{"name": "item1", "price": 10}]}]

@app.get("/datas")
def get_datas():
    return {"datas":datas}

@app.post("/datas")
def create_data():
    request_data = request.get_json()

    new_data = {"items": request_data.get("items", [])}
    datas.append(new_data)

    return new_data, 201