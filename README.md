## myportofolio
Nama : Ferdinandus Pakasi
NPM : 2506602643
Kelas : PBP-D

## Fitur yang Sudah Diimplementasikan

- **About Me** — profil, foto, NPM, dan bio pribadi.
- **Experience** — riwayat pengalaman organisasi/kepanitiaan, ditampilkan sebagai timeline
  vertikal, dengan tiap entri bisa di-expand/collapse.
- **Dark/Light mode toggle** — tombol di navbar untuk beralih tema.
- **Education** — riwayat pendidikan (nama institusi, jenjang, bidang studi, deskripsi),
  diimplementasikan dengan pola Model-View-Template Django. Dalam section ini juga terdapat
  fitur filtering berdasarkan jenjang pendidikan, dengan menerapkan method get dan fitur
  form pada HTML5.
- **Form & Data Delivery** lengkap: tambah data lewat `EducationForm` (ModelForm), ubah data
  lewat form yang sama (prefilled dari data existing), hapus data lewat tombol berkonfirmasi,
  dan penyajian datanya dalam format **JSON** (`/api/education/`) yang kemudian
  dideserialisasi sebelum ditampilkan ke halaman web.

## Cara Menjalankan Proyek 

```bash
# 1. Clone repository
git clone https://github.com/ferdinanduspakasi/myportofolio.git
cd myportofolio

# 2. Buat & aktifkan virtual environment
python -m venv env
source env/bin/activate      # Windows: env\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Jalankan development server
python manage.py runserver
```

Lalu buka `http://127.0.0.1:8000/` di browser.

> Catatan: instruksi setup ini akan diperbarui tiap minggu seiring bertambahnya
> ketergantungan proyek (mis. migrasi database begitu Tutorial berikutnya memperkenalkan
> model/MVT).

## Log Progres Mingguan

- **Tutorial 1** — Setup project Django awal, halaman "About Me" statis dengan HTML5 semantik
  dan styling dasar CSS3.
- **Tugas 1** — Menambahkan section Experience (timeline dengan 3 entri pengalaman
  organisasi), styling grid/flexbox khusus, efek hover, layout responsif, fitur expand/collapse
  per entri, dan dark/light mode toggle sebagai fitur tambahan di luar instruksi minggu ini.
- **Tutorial 2** — Menerapkan pola MVT Django untuk bagian Experience: model `Experience`,
  view `show_experience`, dan template `experience.html` yang menampilkan data dari
  database, menggantikan data yang sebelumnya di-hardcode di HTML.
- **Tugas 2** — Menambahkan bagian **Education** dengan pola MVT yang sama: model baru
  `Education` (institusi, jenjang, bidang studi, deskripsi, tanggal mulai/selesai), migrasi
  yang menyertakan berkas migrasinya, view `show_education` yang meneruskan queryset ke
  template baru `education.html`, named route `main:show_education` pada `main/urls.py`,
  tautan navbar baru menggunakan `{% url %}`, penanganan kondisi data kosong, serta unit
  test untuk aksesibilitas URL/template, tampilnya data, dan tampilan kondisi kosong.
- **Tutorial 3** — Menerapkan form & data delivery pada bagian Experience: `ExperienceForm`
  (ModelForm) di `main/forms.py`, fungsi view `create_experience` dan `delete_experience`,
  serta `get_experience_json` yang mengembalikan queryset `Experience` dalam format JSON
  menggunakan `django.core.serializers`. Halaman `show_experience` kemudian mengambil data
  lewat fungsi JSON tersebut dan melakukan deserialisasi sebelum dirender ke template.
- **Tugas 3** — Menerapkan mekanisme Form & Data Delivery yang sama pada bagian
  **Education**
  - **Extre feature**: Sebelumnya toggle dark/light mode di navbar murni
    CSS (`#dark-mode-toggle`) sehingga selalu kembali ke light mode setiap halaman
    direfresh atau pindah halaman. Ditambahkan script  di `base.html`
    yang menyimpan pilihan tema ke `localStorage` (client-side, per browser) setiap kali
    toggle diklik, lalu membaca kembali nilai tersebut sebelum render pertama halaman
    berikutnya sehingga tidak terjadi flash light-mode sesaat maupun kembali ke light
    mode saat refresh/navigasi. 

### Refleksi Tugas 1

1. Ya, saya menggunakan elemen semantik HTML5 seperti `<header>`, `<nav>`, `<main>`,
   `<section>`, `<article>`, `<footer>`, `<time>`, serta `<details>`/`<summary>` untuk
   section Experience. Elemen-elemen ini membantu memisahkan struktur halaman berdasarkan
   makna kontennya (bukan cuma `<div>` generik), sehingga kode lebih mudah dibaca, lebih
   ramah untuk accessibility (screen reader bisa mengenali batas antar section/artikel),
   dan `<details>`/`<summary>` secara khusus memungkinkan saya membuat interaksi
   expand/collapse tanpa menulis JavaScript sama sekali karena browser sudah menyediakan
   perilaku toggle-nya secara native.

2. Tantangan utamanya ada di bagian yang informasinya berpasangan secara visual di
   desktop tapi harus dipisah di layar sempit, contohnya heading nama-peran dan tanggal
   yang di desktop sejajar (`justify-content: space-between`), tapi di mobile perlu ditumpuk
   vertikal supaya tidak terpotong. Saya mengevaluasi elemen mana yang perlu diprioritaskan
   dengan memikirkan urutan baca (foto vs bio mana yang lebih penting dilihat duluan di
   layar kecil), lalu mengatur ulang `grid-template-areas` dan menambah breakpoint
   `@media (max-width: 600px)` untuk elemen yang paling rawan bertabrakan, seperti
   marker/garis timeline yang perlu dipersempit spacing-nya di layar kecil.

3. Batasan terbesar dari static web murni adalah semua data (pengalaman, foto, bio)
   harus dihardcode langsung di HTML. Kalau saya mau menambah atau mengubah satu entri
   Experience, saya harus mengedit file template secara manual dan push ulang. Preferensi
   tema dark/light juga tidak tersimpan (reset tiap reload). Untuk iterasi berikutnya, fungsionalitas 
   dinamis yang paling ingin saya siapkan adalah backend berbasis database  supaya konten
   seperti Experience atau Projects bisa dikelola lewat admin panel tanpa perlu mengubah
   kode HTML secara langsung, sesuai arah materi tutorial selanjutnya.

   ### Refleksi Tugas 2

1. Ketika pengguna membuka halaman `/education/`, permintaan HTTP pertama kali ditangkap
   oleh `urls.py` milik proyek (`portofolio/urls.py`). Di sana Django mencocokkan path
   `education/` dan mendelegasikannya ke `urls.py` milik aplikasi `main` melalui
   `include("main.urls")`. Pada `main/urls.py`, path kosong setelah prefix tersebut
   dicocokkan dengan named route `main:show_education`, yang terhubung ke fungsi view
   `show_education` di `main/views.py`. View ini memanggil `Education.objects.all()` untuk
   mengambil seluruh baris tabel `Education` dari database lewat Django ORM (model
   `Education` di `main/models.py` merepresentasikan struktur tabel tersebut), memasukkan
   hasilnya ke dalam sebuah dictionary context bersama data lain seperti nama, lalu
   memanggil `render()` dengan context tersebut dan nama template `education.html`. Django
   kemudian merender template itu: bagian `{% for education in education_list %}` melakukan
   perulangan pada queryset dan mengisi HTML dengan atribut tiap objek `Education`
   (`institution_name`, `field_of_study`, dll.), sementara blok `{% empty %}` akan
   ditampilkan sebagai gantinya jika queryset kosong. HTML hasil render inilah yang
   dikirim kembali sebagai response dan ditampilkan browser.

2. Data untuk bagian Education (dan bagian lain) sebaiknya disimpan pada model, bukan
   ditulis langsung di template, karena model memisahkan data dari presentasi mengikuti
   prinsip MVT. Jika data di-hardcode di HTML, menambah atau mengubah satu entri berarti
   harus mengedit file template secara manual dan melakukan deploy ulang setiap kali ada
   perubahan konten, meskipun perubahan itu tidak mengubah struktur maupun tampilan
   halaman. Dengan model, data cukup ditambah atau diubah lewat Django admin atau shell
   tanpa menyentuh kode template maupun view, sehingga template bisa fokus murni pada
   presentasi. Ini juga membuat data lebih mudah divalidasi (lewat field type dan
   `choices` pada model), lebih mudah diuji lewat unit test yang membuat objek model
   secara terprogram, serta membuka kemungkinan pengembangan lanjutan seperti pencarian,
   filter, atau relasi antar model tanpa perlu menulis ulang HTML.

3. `makemigrations` membaca perubahan pada model (`models.py`) dan menerjemahkannya
   menjadi berkas migrasi baru berisi instruksi perubahan skema, tanpa benar-benar
   menyentuh database. `migrate` yang kemudian mengeksekusi berkas migrasi tersebut,
   menerapkan perubahan skema itu ke database yang sedang dipakai. Contoh perubahan model
   yang mengharuskan menjalankan keduanya: saat menambahkan model `Education` pada tugas
   ini, saya perlu menjalankan `python manage.py makemigrations` untuk menghasilkan berkas
   migrasi yang mendeskripsikan tabel baru tersebut (termasuk field seperti
   `institution_name`, `degree`, dan `field_of_study`), lalu menjalankan
   `python manage.py migrate` agar Django benar-benar membuat tabel `Education` itu di
   database `db.sqlite3` sehingga aplikasi bisa menyimpan dan membaca datanya.

   ### Refleksi Tugas 3

1. `ModelForm` dipakai alih-alih membuat form HTML manual karena `ModelForm` menurunkan
   field form-nya langsung dari definisi model (`Education`, `Experience`), sehingga tipe
   input, validasi (misalnya `max_length`, `choices`, apakah field boleh kosong), serta
   proses penyimpanan (`form.save()`) sudah otomatis konsisten dengan skema database tanpa
   perlu ditulis ulang secara manual. Kalau formnya ditulis manual di HTML, saya harus
   memvalidasi setiap input sendiri di view, menjaga field-nya tetap sinkron setiap kali
   model berubah, dan rawan lolos data yang tidak valid ke database. `ModelForm` juga
   otomatis menyediakan pesan error per field (`field.errors`) yang tinggal ditampilkan di
   template. Adapun `{% csrf_token %}` wajib ditambahkan pada setiap form `method="post"`
   karena Django menerapkan proteksi CSRF (Cross-Site Request Forgery) secara default: tanpa
   token ini, request `POST` akan ditolak (403 Forbidden), karena token tersebut membuktikan
   bahwa request memang berasal dari form yang di-render oleh server itu sendiri, bukan dari
   situs lain yang mencoba mengirim request atas nama pengguna yang sedang login tanpa
   sepengetahuannya.

2. JSON lebih disukai dibanding XML pada pengembangan web modern karena beberapa alasan.
   Pertama, JSON strukturnya jauh lebih ringkas — tidak ada closing tag berulang seperti
   pada XML — sehingga ukuran payload-nya lebih kecil dan lebih hemat bandwidth, terutama
   untuk API yang dipanggil berkali-kali. Kedua, JSON adalah representasi native dari objek
   JavaScript, sehingga di sisi client (browser) data JSON bisa langsung di-parse menjadi
   objek/array JavaScript dengan `JSON.parse()` tanpa perlu library tambahan, sedangkan XML
   butuh parser DOM/XML yang lebih rumit untuk diakses. Ketiga, hampir seluruh bahasa dan
   framework modern (termasuk Django lewat `django.core.serializers`) sudah punya dukungan
   serialisasi/deserialisasi JSON bawaan, sehingga proses encode-decode antara backend dan
   frontend jadi jauh lebih sederhana. XML masih dipakai di beberapa domain lama (misalnya
   dokumen enterprise/SOAP) karena dukungan skema dan namespace-nya lebih ketat, tapi untuk
   kebutuhan pertukaran data web pada umumnya JSON jauh lebih efisien dan mudah digunakan.

3. Ketika fungsi view seperti `get_education_json` dipanggil, alurnya dimulai dari
   `Education.objects.all()` (atau versi ter-filter-nya) yang mengambil queryset objek
   `Education` dari database lewat Django ORM. Objek-objek model ini pada dasarnya adalah
   instance Python (bertipe `Education`) yang tidak bisa langsung dikirim sebagai response
   HTTP karena HTTP hanya bisa mengirim data dalam bentuk teks/bytes, bukan objek Python.
   Di sinilah proses **serialization** diperlukan: `serializers.serialize("json", education)`
   mengubah setiap objek model beserta field-fieldnya menjadi struktur data sederhana
   (dictionary/list) yang kemudian di-encode menjadi string JSON. String JSON inilah yang
   dibungkus dalam `HttpResponse` dengan `content_type="application/json"` dan dikirim ke
   client. Pada `show_education`, string JSON tersebut diambil kembali lalu diproses dengan
   `serializers.deserialize("json", ...)` untuk mengubahnya kembali menjadi objek Python
   (proses **deserialization**), sehingga atribut-atributnya (`institution_name`,
   `get_degree_display`, `is_ongoing`, dll.) bisa dipakai kembali secara normal di dalam
   template Django. Proses serialization-deserialization ini penting karena memisahkan
   representasi data untuk pertukaran (JSON, bisa dipakai API/frontend lain) dari
   representasi objek model yang dipakai secara internal oleh Django, sekaligus memastikan
   data yang dikirim lewat jaringan berbentuk teks yang aman dan dapat dibaca oleh berbagai
   platform, tidak bergantung pada implementasi Python/Django secara spesifik.


## AI Disclosure

**Tugas 1** - Saya menggunakan Claude (Anthropic, via claude.ai) untuk membantu pengerjaan Tugas 1 ini.
Bagian yang dibantu AI:

- Diskusi mengenai ide yang pas untuk tugas 1 ini, termasuk extra feature yang memungkinkan.
- Membantu dalam penyusunan CSS timeline (grid layout, garis penghubung, hover effect).
- Memberikan ide dibalik impelementasi dark mode dan penggunaan toggle.

Strategi prompting: Saya memberikan ketentuan tugas dan kode sementara agar AI
dapat memahami dan memberikan saran yang relevan dan kontekstual. Hampir seluruh prompt fokus
pada memberikan step-by-step atau tutorial untuk konsep dan implementasi yang belum dipahami. 
Adapun seluruh ide maupun kode yang disarankan telah melalui proses pemahaman dan pengambilan 
keputusan sesuai preferensi sendiri.

Keterbatasan yang saya temukan: Memberikan saran ataupun implementasi yang out of scope topik 
pembelajaran, sehingga peran untuk mengambil keputusan sesuai scope pembelajaran masih diperlukan.


**Tugas 2** - Saya menggunakan Claude (Anthropic, via claude.ai) untuk membantu pengerjaan Tugas 1 ini.
Bagian yang dibantu AI:
Chat Link: https://claude.ai/share/91077e93-745d-4a0d-8959-168170083a8a 

- Membantu menjelaskan alur pengerjaan dan spek yang diharapkan instruksi tugas 2.
- Membantu menjelaskan proses penggunaan git (branching, dsb).
- Menulis HTML untuk section education berdasarkan model yang telah dibuat.
- Menambahkan unit test (`EducationTest`) yang mencakup aksesibilitas URL/template,
  tampilnya data model di HTML, dan tampilan kondisi kosong.
- Turut membantu menemukan dan memperbaiki sejumlah bug saat development.

Strategi prompting: Saya selalu berusaha memberikan konteks yang lengkap agar AI dapat memahami permasalahan
serta goals secara tepat. Dalam meminta saran ataupun code, saya berusaha untuk memecah-mecah masalah agar 
menghindari kesalahan-kesalahan tak terlihat, dan memudahkan proses pemahaman bagi saya pribadi. Penggunaan AI
juga jadi efektif untuk belajar dengan aktif bertanya dan mengklarifikasi hal-hal yang belum dipahami. 

Keterbatasan yang saya temukan: Saya menemukan bahwa jika thread percakapan sudah terlalu panjang, 
AI sering amnesia dengan requirements yang sudah ditetapkan di awal, sehingga konteks dan requirements
harus diberikan kembali.

**Tugas 3** - Saya menggunakan Claude (Anthropic, via claude.ai) untuk membantu pengerjaan Tugas 3 ini.
Bagian yang dibantu AI:
Chat Link: https://claude.ai/share/46b6a9d1-632c-48ea-a130-8dadf2c59b46 

- Menulis `EducationForm` di `forms.py`, menambahkan beberapa fungsi di `views.py`, dan merefactor
  `show_education` agar mengambil data lewat JSON, mengikuti pola pada section yang sudah ada.
- Menulis template `education_form.html` dan `components/education_delete_modal.html`,
  serta memperbarui `education.html` (tombol tambah, edit, dan hapus per kartu).
- Menambahkan unit test baru untuk memverifikasi CRUD dan JSON delivery pada Education, serta
  memperbaiki satu bug pre-existing pada test Experience (field `started_at` yang wajib diisi).

Strategi prompting: Saya mengunggah berkas instruksi tugas (PDF) beserta seluruh source code
proyek yang sudah ada, sehingga AI bisa memahami pola dan gaya kode yang sudah dipakai sebelum
menambahkan fitur baru. 

Keterbatasan yang saya temukan: Sering overdo lebih dari perintah, sehingga outputnya perlu
dikurasi secara manual.

