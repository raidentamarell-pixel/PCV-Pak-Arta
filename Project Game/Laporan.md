# Game Tangkap Buah Berbasis OpenCV

## Deskripsi Proyek

**Game Tangkap Buah** merupakan proyek Pengolahan Citra dan Visi Komputer (PCV) berbasis Python yang memanfaatkan OpenCV untuk mendeteksi warna melalui kamera secara *real-time*. Hasil deteksi kamera digunakan untuk mengendalikan posisi keranjang dalam permainan, sehingga pemain dapat menangkap buah dan menghindari bom melalui gerakan objek berwarna biru di depan kamera.

Proyek ini menggabungkan teknologi pengolahan citra menggunakan OpenCV dengan antarmuka permainan yang dibuat menggunakan Pygame.

## Teknologi yang Digunakan

- **Python** — bahasa pemrograman utama.
- **OpenCV (`cv2`)** — mengambil gambar dari kamera, mengolah citra, mengubah ruang warna BGR menjadi HSV, dan mendeteksi objek berdasarkan rentang warna.
- **NumPy** — mengolah data citra dan menentukan rentang warna yang digunakan dalam proses deteksi.
- **Pygame** — menampilkan permainan, mengatur pergerakan buah dan bom, serta mengelola skor dan nyawa.

## Cara Kerja Program

### Kamera dan Pengambilan Citra

Program menggunakan `cv2.VideoCapture(0)` untuk mengakses kamera utama PC atau laptop. Kamera mengambil gambar secara berulang selama permainan berlangsung. Setiap gambar kemudian dibalik secara horizontal menggunakan `cv2.flip()` agar pergerakan objek terasa lebih alami bagi pemain.

Resolusi gambar disesuaikan dengan ukuran jendela permainan menggunakan `cv2.resize()`. Program juga menggunakan `cv2.GaussianBlur()` untuk mengurangi gangguan atau *noise* pada gambar sebelum proses deteksi warna dilakukan.

### Pengolahan Citra dengan OpenCV

Gambar yang diperoleh dari kamera awalnya menggunakan ruang warna BGR. Program mengubahnya menjadi HSV (*Hue, Saturation, Value*) menggunakan `cv2.cvtColor()`.

Ruang warna HSV digunakan karena pemisahan komponen warna, kejenuhan, dan kecerahan memudahkan proses deteksi warna tertentu. Pada proyek ini, program menggunakan rentang nilai HSV yang telah ditentukan untuk mendeteksi objek berwarna biru.

Rentang warna tersebut disimpan dalam variabel `BIRU_BAWAH` dan `BIRU_ATAS`. Fungsi `cv2.inRange()` kemudian menghasilkan *mask* yang menampilkan area gambar yang memenuhi rentang warna tersebut.

### Deteksi Objek Berwarna Biru

Hasil *mask* digunakan untuk mencari kontur dengan `cv2.findContours()`. Kontur merupakan batas area objek yang terdeteksi pada gambar.

Program memilih kontur dengan luas terbesar menggunakan `max()` dan memeriksa apakah luasnya melebihi 500 piksel. Pemeriksaan ini bertujuan mengabaikan sebagian objek kecil atau gangguan yang tidak memenuhi batas luas minimum.

Jika ditemukan kontur yang memenuhi kriteria, program menggunakan `cv2.boundingRect()` untuk memperoleh posisi dan ukuran area objek. Titik tengah objek dihitung dari koordinat dan lebar kotak pembatas tersebut.

### Pengendalian Keranjang

Posisi horizontal keranjang ditentukan berdasarkan titik tengah objek biru yang terdeteksi oleh kamera. Dengan demikian, ketika objek biru bergerak ke kiri atau kanan, keranjang pada permainan juga bergerak mengikuti perubahan posisinya.

Pendekatan ini memungkinkan pemain mengendalikan permainan tanpa menggunakan keyboard untuk menggerakkan keranjang. Kamera berfungsi sebagai masukan utama untuk interaksi antara pemain dan permainan.

### Pemuatan Gambar Objek

Program menggunakan fungsi `muat()` untuk memuat gambar buah, bom, dan keranjang dari folder proyek. Gambar diubah ukurannya sesuai kebutuhan permainan menggunakan `pygame.transform.scale()`.

Jika berkas gambar tidak ditemukan, program menampilkan pesan dan membuat bentuk pengganti sederhana. Mekanisme ini membantu permainan tetap berjalan meskipun aset gambar belum tersedia, selama proses pemuatan dan penampilan objek lainnya tidak mengalami kesalahan.

### Kemunculan dan Pergerakan Buah serta Bom

Buah dan bom disimpan dalam sebuah daftar bernama `items`. Setiap objek memiliki koordinat posisi, gambar yang digunakan, dan penanda yang menunjukkan apakah objek tersebut merupakan bom.

Objek baru dimunculkan secara berkala berdasarkan nilai `timer`. Jenis objek ditentukan secara acak: sebagian merupakan bom, sedangkan sisanya merupakan buah seperti apel, pisang, dan kiwi.

Setiap objek bergerak ke bawah dengan menambahkan nilai koordinat Y pada setiap pembaruan permainan. Pergerakan ini menciptakan tantangan bagi pemain untuk mengarahkan keranjang ke posisi yang sesuai sebelum objek mencapai bagian bawah layar.

### Deteksi Tabrakan dan Sistem Skor

Program memeriksa apakah posisi objek memenuhi kondisi tabrakan dengan keranjang. Pemeriksaan dilakukan berdasarkan posisi vertikal objek dan jarak horizontalnya terhadap pusat keranjang.

Jika buah tertangkap, objek dihapus dari daftar dan skor pemain bertambah. Namun, jika objek yang tertangkap merupakan bom, jumlah nyawa pemain berkurang.

Buah yang terlewat hingga mencapai bagian bawah layar juga mengurangi nyawa, sedangkan bom yang terlewat tidak mengurangi nyawa. Permainan menggunakan tiga nyawa sebagai batas awal sebelum kondisi *game over* terjadi.

### Tampilan Permainan dengan Pygame

Pygame digunakan untuk menampilkan latar belakang dari kamera, keranjang, buah, bom, skor, dan jumlah nyawa. Gambar kamera dikonversi dari BGR menjadi RGB menggunakan `cv2.cvtColor()` agar dapat ditampilkan dengan format warna yang sesuai.

Program juga menggunakan `pygame.display.flip()` untuk memperbarui tampilan layar dan `clock.tick(60)` untuk membatasi laju pembaruan hingga sekitar 60 frame per detik.

Selain itu, gambar kamera dapat dibuat sedikit lebih terang menggunakan `cv2.convertScaleAbs()` dengan parameter kecerahan dan kontras yang telah ditentukan.

### Game Over dan Pengulangan Permainan

Permainan berakhir ketika jumlah nyawa pemain mencapai nol. Dalam kondisi tersebut, program menampilkan pesan *Game Over* dan memberikan informasi untuk memulai ulang permainan.

Pemain dapat menekan tombol `R` untuk mengatur kembali skor, nyawa, daftar objek, timer, dan status permainan. Tombol `Esc` digunakan untuk keluar dari permainan, sedangkan tombol penutup jendela digunakan untuk menghentikan program.

Setelah permainan dihentikan, program melepaskan akses kamera menggunakan `cap.release()` dan menutup seluruh jendela OpenCV melalui `cv2.destroyAllWindows()`.

## Hasil dan Pembahasan

Program mengintegrasikan pengolahan citra dan permainan interaktif melalui kamera. OpenCV berperan dalam mengambil dan mengolah citra serta mendeteksi objek berdasarkan warna biru, sedangkan Pygame mengatur mekanisme permainan dan menampilkan hasilnya.

Keberhasilan deteksi dipengaruhi oleh pencahayaan, warna objek, jarak objek dari kamera, dan kesesuaian rentang HSV yang digunakan. Apabila warna biru sulit terdeteksi, rentang HSV dapat disesuaikan berdasarkan kondisi lingkungan. Penggunaan *Gaussian blur* dan batas luas kontur juga membantu mengurangi deteksi gangguan, meskipun tidak sepenuhnya menghilangkan kesalahan deteksi.

## Kesimpulan

Game Tangkap Buah merupakan implementasi sederhana OpenCV dalam bidang Pengolahan Citra dan Visi Komputer. Melalui pengambilan citra kamera, konversi warna ke HSV, segmentasi warna, dan deteksi kontur, program dapat menentukan posisi objek biru secara *real-time*. Posisi tersebut digunakan untuk mengendalikan keranjang pada permainan yang dibangun dengan Pygame. Proyek ini menunjukkan penerapan teknik pengolahan citra untuk menghasilkan interaksi manusia dan komputer yang lebih interaktif.
