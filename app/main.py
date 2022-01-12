from flask import Flask, request, jsonify
from flask_pymongo import PyMongo, ObjectId
from flask_cors import CORS

app = Flask(__name__)
app.config['MONGO_URI']='mongodb+srv://sagalo:Mm3d1a09@pruebanicepeople.xteck.mongodb.net/myFirstDatabase?retryWrites=true&w=majority' 
mongo = PyMongo(app)
CORS(app)

db = mongo.db.data

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
UPLOAD_FOLDER = '/tmp/'


@app.route('/astro', methods=['POST'])
def createUser():
    try:
        user = db.find_one_and_update({'user': request.json['user']},{'$set':{'positionX': request.json['positionX'],'positionY': request.json['positionY'], 'items': request.json['items'], 'Equipo': request.json['Equipo']}})
        return (str(ObjectId(user['_id']))) 
    except:
        mydict = { 'titulo': request.json['titulo'],
            'descripcion': request.json['descripcion'],
            'enlace': request.json['enlace'],
            'etiquetas': request.json['etiquetas'],
            'fechaL': request.json['fechaL'],
            'imagen_url': request.json['imagen_url'], 
        }
        
        id = db.insert_one(
            mydict
            # 'imagen': request.form['imagen'], 
        )
        return ("inserted") 
        
@app.route('/uploads/<path:filename>')
def get_upload(filename):
    fileimg = mongo.send_file(filename, base='fs', version=-1, cache_for=31536000)
    return fileimg
    
@app.route('/data/<titulo>', methods=['GET'])
def getUser(titulo):
    # try:
        data = db.find_one({'enlace': titulo})
        return jsonify({
            'titulo': data['titulo'],
            'descripcion': data['descripcion'],
            'enlace': data['enlace'],
            'etiquetas': data['etiquetas'],
            'fechaL': data['fechaL'],
            'imagen_url': data['imagen_url'], 
        })
    # except:
        return ("No Found")
@app.route('/alldata', methods=['GET'])
def getalldata():
    content= []
    for doc in db.find():
        content.append({
            'titulo': doc['titulo'],
            'descripcion': doc['descripcion'],
            'enlace': doc['enlace'],
            'etiquetas': doc['etiquetas'],
            'fechaL': doc['fechaL'],
            'imagen_url': doc['imagen_url'], 
        })
    return jsonify(content)

# if __name__ == '__main__':a
#     app.run(debug=True)
    