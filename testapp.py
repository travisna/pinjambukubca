import unittest
from flask_testing import TestCase
from flask import url_for
from databooks import app, db, Book,Borrowing  # Import modul-modul yang diperlukan

# Kelas MyTest untuk melakukan testing pada aplikasi
class MyTest(TestCase):

    # Metode untuk membuat aplikasi dalam mode testing
    def create_app(self):
        app.config['TESTING'] = True  # Mengaktifkan mode testing
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sipus.db'  # Menggunakan database in-memory untuk testing
        return app

    # Metode yang dijalankan sebelum setiap test
    def setUp(self):
        db.create_all()  # Membuat semua tabel dalam database

    # Metode yang dijalankan setelah setiap test
    def tearDown(self):
        db.session.remove()  # Menghapus sesi database
        db.drop_all()  # Menghapus semua tabel dalam database

    # Test untuk endpoint index '/'
    def test_index(self):
        response = self.client.get('/')  # Melakukan request GET ke '/'
        self.assert200(response)  # Memastikan response adalah 200 OK
        self.assert_template_used('index.html')  # Memastikan template yang digunakan adalah 'index.html'

    # Test untuk membuat karyawan baru
    def test_create_buku(self):
        # Melakukan request POST ke '/karyawan' dengan data buku baru
        response = self.client.post('/inputBuku', json={
            'title': 'Perang Dunia Shinobi',
            'author': 'Obito',
            'genre': 'Gelut',
            'stock' : '1'
        })
        self.assertStatus(response, 200)  # Memastikan response adalah 201 Created
        buku = Book.query.first()  # Mengambil buku pertama dari database
        print(buku)
        self.assertEqual(buku.title, 'Perang Dunia Shinobi')  # Memastikan nama karyawan adalah 'John Doe'
        
    # Test untuk mendapatkan semua karyawan
    def test_get_all_buku(self):
        # Membuat dua objek karyawan baru dan menyimpannya ke database
        buku1 = Book(title='Perang Dunia Shinobi', author='Obito',genre = 'Gelut',stock = '1')
        buku2 = Book(title='Cara Membaca Batu', author='Madara',genre = 'Literatur',stock = '2')
        db.session.add(buku1)
        db.session.add(buku2)
        db.session.commit()

        # Melakukan request GET ke '/display_all'
        response = self.client.get('/tampilBuku')
        self.assert200(response)  # Memastikan response adalah 200 OK
        self.assert_template_used('display_book.html')  # Memastikan template yang digunakan adalah 'displayall.html'
        self.assertIn(b'Perang Dunia Shinobi', response.data)  # Memastikan 'John Doe' ada dalam response data
        self.assertIn(b'Cara Membaca Batu', response.data)  # Memastikan 'Jane Doe' ada dalam response data

    # Test untuk mendapatkan satu karyawan berdasarkan id
    def test_get_one_buku(self):
        # Membuat objek karyawan baru dan menyimpannya ke database
        buku1 = Book(title='Perang Dunia Shinobi', author='Obito',genre = 'Gelut',stock = '1')
        db.session.add(buku1)
        db.session.commit()

        # Melakukan request GET ke '/karyawan/{id_karyawan}'
        response = self.client.get(f'/tampilBuku/{buku1.id}')
        self.assert200(response)  # Memastikan response adalah 200 OK
        
        # Test untuk menghapus karyawan
    def test_delete_buku(self):
        # Membuat objek karyawan baru dan menyimpannya ke database
        buku = Book(title='Perang Dunia Shinobi', author='Obito',genre = 'Gelut',stock = '1')
        db.session.add(buku)
        db.session.commit()

        # Melakukan request DELETE ke '/karyawan/{id_karyawan}'
        response = self.client.delete(f'/deleteBuku/{buku.id}')
        self.assert200(response)  # Memastikan response adalah 200 OK
        self.assertIsNone(Book.query.get(buku.id))  # Memastikan karyawan dengan id tersebut sudah dihapus

    # Test untuk menghapus karyawan melalui UI
    def test_delete_buku_ui(self):
        # Membuat objek karyawan baru dan menyimpannya ke database
        buku1 = Book(title='Perang Dunia Shinobi', author='Obito',genre = 'Gelut',stock = '1')
        db.session.add(buku1)
        db.session.commit()

        # Melakukan request POST ke '/delete_karyawan' dengan data nama karyawan
        response = self.client.post('/deleteBuku', data={'title': 'Perang Dunia Shinobi'})
        self.assert200(response)  # Memastikan response adalah 200 OK
        self.assert_template_used('delete_book.html')  # Memastikan template yang digunakan adalah 'deletedata.html'
        self.assertIn(b'Perang Dunia Shinobi', response.data)  # Memastikan 'John Doe' ada dalam response data

    def tampil_pinjam(self):
        # Membuat objek karyawan baru dan menyimpannya ke database
        buku1 = Book(title='Perang Dunia Shinobi', author='Obito',genre = 'Gelut',stock = '1')
        db.session.add(buku1)
        db.session.commit()
        
        borrow1 = Borrowing(id_book='1', user_id='Zetsu',borrow_date = '2023-09-29')
        db.session.add(borrow1)
        db.session.commit()

        response = self.client.get('/tampilPinjam')
        self.assert200(response)  # Memastikan response adalah 200 OK
        self.assert_template_used('display_borrow.html')  # Memastikan template yang digunakan adalah 'displayall.html'
        self.assertIn(b'Zetsu', response.data)  # Memastikan 'John Doe' ada dalam response data
        
if __name__ == '__main__':
    unittest.main()  # Menjalankan semua test