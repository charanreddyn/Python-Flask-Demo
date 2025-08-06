from flask import Flask, jsonify, request, abort, render_template

app = Flask(__name__)

# In-memory database
items = [
    {'id':1,"name":"laptop","price":50000},
    {'id':2,"name":"phone","price":20000}
]

# Home route (HTML page)
@app.route("/")
def home():
    return render_template("index.html")  # Make sure 'index.html' is in the 'templates' folder

# Get all items
@app.route("/items", methods=["GET"])
def get_items():
    return jsonify(items)

# Get item by ID
@app.route("/items/<int:itemid>", methods=["GET"])
def get_item(itemid):
    item = next((i for i in items if i['id'] == itemid), None)
    if item:
        return jsonify(item)
    abort(404, description="Item not found!")

# Create a new item
@app.route("/items", methods=["POST"])
def create_item():
    data = request.get_json()
    if not data or "name" not in data or "price" not in data:
        abort(400, description="Invalid item data")
    newid = items[-1]['id'] + 1 if items else 1
    item = {
        "id": newid,
        "name": request.json["name"],
        "price": float(request.json["price"])
    }
    items.append(item)
    return jsonify(item), 201

@app.route('/items/<int:itemid>',methods=['PUT'])
def update_item(itemid):
    item=next((i for i in items if i['id'] == itemid),None)
    if item is None:
        abort(404)
    if not request.json:
        abort(400)
    item['name']=request.json.get('name',item['name'])
    item['price']=request.json.get('price',item['price'])
    return jsonify(item)

#delete items
@app.route('/items/<int:itemid>',methods=['DELETE'])
def delete_item(itenid):
    global items
    items= [ i for i in items if i['id']!=itemid]
    return jsonify({'message':'Item deleted'}),200
# Run the app
if __name__ == "__main__":
    app.run(debug=True)
