from flask_restful import Resource, Api
from flask import Flask, request, Response, json, jsonify, abort
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost:3306/mahasiswa'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
ma = Marshmallow(app)

# pertemuan 3
@app.route('/')
def hello_world():
    return 'Selamat datang'

@app.route('/admin')
def admin():
    return "Ini adalah halaman admin"
# akhir pertemuan 3

# pertemuan4
class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

api.add_resource(HelloWorld, '/helloworld')
# akhir pertemuan 4

# pertemuan 5
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nim = db.Column(db.String(8), unique=True)
    nama = db.Column(db.String(30))
    kelas = db.Column(db.String(2))

    def __init__(self, nim, nama, kelas):
        self.nim = nim
        self.nama = nama
        self.kelas = kelas

    @staticmethod
    def get_all_user():
        return User.query.all()

class UserSchema(ma.Schema):
    class Meta:
        #Field to expose
        fields = ('id', 'nim', 'nama', 'kelas')

user_schema = UserSchema()
users_schema = UserSchema(many=True)

# get all user
@app.route('/mahasiswa', methods=["GET"])
def get_user():
    all_users = User.get_all_user()
    result = users_schema.dump(all_users)
    return jsonify(result)

# akhir pertemuan 5

# ini adalah materi pertemuan 7
# get mahasiswa by id
@app.route("/mahasiswa/<int:id>/", methods=["GET"])
def one_user(id):
    user = User.query.get(id)
    result = user_schema.dump(user)
    return jsonify(result)

# create data mahasiswa
@app.route("/mahasiswa/", methods=["POST"])
def create_user():
    if not request.json or not 'nim' in request.json and not 'nama' in request.json and not 'kelas' in request.json:
        abort(400)

    user = User(request.json['nim'], request.json['nama'], request.json['kelas'])
    db.session.add(user)
    db.session.commit()

    result = user_schema.dump(user)
    return jsonify(result)

# update data mahasiswa
@app.route("/mahasiswa/<int:id>/", methods=["PUT"])
def update_user(id):
    if not request.json or not 'nim' in request.json and not 'nama' in request.json and not 'kelas' in request.json:
        abort(400)

    user = User.query.get(id)
    user.nim = request.json['nim']
    user.nama = request.json['nama']
    user.kelas = request.json['kelas']
    db.session.commit()

    result = user_schema.dump(user)
    return jsonify(result)

# delete data mahasiswa by id
@app.route("/mahasiswa/<int:id>/", methods=["DELETE"])
def delete_user(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()

    return jsonify()

# materi pertemuan 7 berakhir di sini


if __name__ == '__main__':
    app.run()
