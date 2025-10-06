from flask import Flask, jsonify, request

app = Flask(__name__)

# Sample data
items = [
    {"id": 1, "name": "Apple"}, 
    {"id": 2, "name": "Banana"},
]

# GET all items
@app.route('/items', methods=['GET'])
def get_items():
    return jsonify(items)

# GET item by ID
@app.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = next((item for item in items if item["id"] == item_id), None)
    if item:
        return jsonify(item)
    return jsonify({"error": "Item not found"}), 404

# POST a new item
@app.route('/items', methods=['POST'])
def add_item():
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({"error": "Invalid input"}), 400
    new_item = {
        "id": items[-1]["id"] + 1 if items else 1,
        "name": data["name"]
    }
    items.append(new_item)
    return jsonify(new_item), 201

# PUT (replace) item
@app.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    data = request.get_json()
    if not data or "name" not in data:
        return jsonify({"error": "Bad request"}), 400
    for item in items:
        if item["id"] == item_id:
            item["name"] = data["name"]
            return jsonify(item)
    return jsonify({"error": "Item not found"}), 404

# PATCH (partial update) item
@app.route('/items/<int:item_id>', methods=['PATCH'])
def patch_item(item_id):
    data = request.get_json()
    for item in items:
        if item["id"] == item_id:
            if "name" in data:
                item["name"] = data["name"]
            return jsonify(item)
    return jsonify({"error": "Item not found"}), 404

# DELETE an item by ID
@app.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    global items
    items = [item for item in items if item["id"] != item_id]
    return jsonify({"message": "Item deleted"}), 204

if __name__ == '__main__':
    app.run(debug=True)