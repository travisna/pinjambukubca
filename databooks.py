#import library
from flask import Flask, jsonify,request,render_template
from flask import redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger,swag_from
from datetime import datetime
import os

#Mendefinisikan app
app=Flask(__name__)

#Lokasi database
#DATABASE_PATH = 'C:/DATA TRV/TRAINING/PYTHON 230922/mypy/bcaflask/pinjambukubca/sipus.db'

#Konfigurai Database
#app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///' + DATABASE_PATH
app.config['SQLALCHEMY_DATABASE_URI']= 'mysql+mysqlconnector://root:hd9k9kgtJTI2g2oxJuqc@containers-us-west-185.railway.app:6589/railway'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SWAGGER'] = {
    'title': 'API Sistem Informasi Perpustakaan',
    'uiversion': 3,
    'headers':[],
    'specs':[
        {
            'endpoint' : 'apispec_1',
            'route': '/apispec_1.json',
            'rule_filter' : lambda rule : True,
            'model_filter' : lambda tag : True,
        }
    ],
    'static_url_path':'/flasgger_static',
    'swagger_ui':True,
    'specs_route':'/apidocs'
}

swagger = Swagger(app)

db = SQLAlchemy(app)

class Book(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    title = db.Column(db.String(100),nullable = False)
    author = db.Column(db.String(100),nullable = False)
    genre = db.Column(db.String(100),nullable = False)
    stock = db.Column(db.Integer,nullable = False)
    
class Borrowing(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    id_book = db.Column(db.Integer,db.ForeignKey('book.id'))
    user_id = db.Column(db.String(100),nullable = False)
    borrow_date = db.Column(db.Date,nullable = False)
    return_date = db.Column(db.Date,nullable = True)


@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

# #Koneksi API Delete
# @app.route('/karyawan/<int:id_karyawan>',methods=['DELETE'])
# @swag_from('swagger_docs/delete_data_bca.yaml')
# def delete_karyawan(id_karyawan):
#         pass

#Koneksi API Show All Data
@app.route('/tampilBuku',methods=['GET'])
@swag_from('swagger_docs/get_all_book_data.yaml')
def get_all_book():
        buku_list = []
        try:
            all_buku = Book.query.all();

            #membuat daftar dari data karyawan untyuk dikirimkan ke template
            for buku in all_buku:
                buku_data = {
                    'id': buku.id,
                    'title': buku.title,
                    'author': buku.author,
                    'genre': buku.genre,
                    'stock': buku.stock,
                }
                buku_list.append(buku_data)
        except Exception as e:
            return render_template('error.html',pesan="Terjadi kesalahan saat mengambil data {}".format(str(e))),500
        finally:
            if buku_list:
                return render_template('display_book.html',buku_list = buku_list)
            else:
                return render_template('error.html',pesan="Tidak ada data buku yang ditampilkan"),404

#Koneksi API untuk Ambil Spesifik Data
@app.route('/tampilBuku/<int:id>',methods=['GET'])
@swag_from('swagger_docs/get_one_book.yaml')
def get_one_karyawan(id_karyawan):
        pass

#Fungsi menambahkan Data
@app.route('/inputBuku', methods=['GET','POST'])
def input_buku():
    if request.method == 'POST':
        #Menambahkan data dari form
        title = request.form.get('title')
        author = request.form.get('author')
        genre = request.form.get('genre')
        stock = request.form.get('stock')

        #Cek apakah field terisi
        if not title or not author or not genre or not stock:
            return render_template('create_book.html',error="Semua field wajib diisi")

        new_Buku = Book (
            title = title,
            author = author,
            genre = genre,
            stock = stock
        )

        db.session.add(new_Buku)
        db.session.commit()

        return render_template('confirmation_book.html')
    return render_template('create_book.html')

@app.route('/updateBuku',methods=['GET','POST'])
def update_buku_ui():
    if request.method == 'POST':
        title = request.form.get('title')
        data_list = Book.query.filter(Book.title.like(f"%{title}%")).all()
        return render_template('update_book.html',data_list=data_list)
    return render_template('update_book.html')

@app.route('/form_update_buku',methods=['POST'])
def update_buku():
    try:
        id = request.form.get('id')
        title = request.form.get('title')
        author = request.form.get('author')
        genre = request.form.get('genre')
        stock = request.form.get('stock')
        
        buku = Book.query.get(id)
        
        if not buku:
            return jsonify({'message':'Buku tidak ditemukan'}),404
        
        buku.title = title
        buku.author = author
        buku.genre = genre
        buku.stock = stock
        
        db.session.commit()
        
        return redirect(url_for('get_all_book'))
    except Exception as e:
        return jsonify({'message':f'Terjadi kesalahan {str(e)}'}),500
    
@app.route('/deleteBuku/<int:id>',methods=['DELETE'])
@swag_from('swagger_docs/delete_data_book.yaml')
def delete_karyawan(id):
    try:
        book_to_delete = Book.query.filter_by(id=id).first()
        
        if book_to_delete:
            db.session.delete(book_to_delete)
            db.session.commit()
            return jsonify({'message':f'Data buku dengan ID {id} berhasil dihapus'}),200
        else:
            return jsonify({'message':f'Data book_to_delete dengan ID {id} tidak ditemukan'}),404
    except Exception as e:
        return jsonify({'message':f'Terjadi kesalahan {str(e)}'}),500
  
@app.route('/deleteBuku',methods=['GET','POST'])
def delete_buku_ui():
    data_list = []
    try:
        if request.method == 'POST':
            search_name = request.form['title'].lower()
            all_buku = Book.query.all()
            data_list = [buku for buku in all_buku if search_name in buku.title.lower()]
    except Exception as e:
        error_message =f"Terjadi kesalahan: {e}"
        print(error_message)
        return render_template('error.html',pesan = error_message),500
    finally:
        return render_template('delete_book.html',data_list = data_list),500
    
#Fungsi menambahkan Data
@app.route('/inputPinjam', methods=['GET','POST'])
def input_pinjam():
    if request.method == 'GET':
        data_list = Book.query.all()
    
    if request.method == 'POST':
        #Menambahkan data dari form
        user_id = request.form.get('user_id')
        id_book = request.form.get('id')
        borrow_date = datetime.strptime(request.form.get('borrow_date'),'%Y-%m-%d')
        #Cek apakah field terisi
        if not user_id or not id_book or not borrow_date:
            return render_template('create_borrow.html',error="Semua field wajib diisi")

        new_Borrow = Borrowing (
            user_id = user_id,
            id_book = id_book,
            borrow_date = borrow_date,
            
        )

        db.session.add(new_Borrow)
        db.session.commit()

        return render_template('confirmation_borrow.html')
    return render_template('create_borrow.html',data_list=data_list)

if __name__ == '__main__':
    app.run(debug = True, port = 5020)


