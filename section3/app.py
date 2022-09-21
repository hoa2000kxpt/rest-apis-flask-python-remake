from flask import Flask,jsonify,request,render_template

app = Flask(__name__)

stores = [{
    'name': 'My Store',
    'items': [{'name':'my item', 'price': 15.99 }]
}]

# POST - used to receive data
# GET - used to send data back only

@app.route('/')
def home():
  return render_template('index.html')

#POST /store data: {name :}
@app.route('/store' , methods=['POST'])
def create_store():
  request_data = request.get_json()
  new_store = {
    'name':request_data['name'],
    'items':[]
  }
  stores.append(new_store)
  return jsonify(new_store)
  #pass

#GET /store/<name> data: {name :}
@app.route('/store/<string:name>')
def get_store(name):
  # Iterate over stores
  for store in stores:

    # If the store name matches, return it
    if store['name'] == name:
          return jsonify(store)

  # If none match, return an error message
  return jsonify ({'message': 'store not found'})

#GET /store
@app.route('/store')
def get_stores():
  return jsonify({'stores': stores})
  #pass

#POST /store/<name> data: {name :}
@app.route('/store/<string:name>/item' , methods=['POST'])
def create_item_in_store(name):
  request_data = request.get_json()
  for store in stores:
    if store['name'] == name:
        new_item = {
            'name': request_data['name'],
            'price': request_data['price']
        }
        store['items'].append(new_item)
        return jsonify(new_item)
  return jsonify ({'message' :'store not found'})
  #pass

#GET /store/<name>/item data: {name :}
@app.route('/store/<string:name>/item')
def get_item_in_store(name):
  for store in stores:
    if store['name'] == name:
        return jsonify( {'items':store['items'] } )
  return jsonify ({'message':'store not found'})

  #pass

app.run(port=5000)
