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
- **Autentikasi & Session** — registrasi (`UserCreationForm`), login (`AuthenticationForm`), dan
  logout menggunakan sistem autentikasi bawaan Django. Cookie `last_login` di-set saat login,
  dihapus saat logout, dan ditampilkan di halaman utama. Halaman daftar dan detail tetap bisa
  dibaca siapa pun tanpa login.
- **Manajemen Peran (Authorization)** — empat peran dengan pengecekan di sisi server: pengunjung
  tanpa login (baca saja, diarahkan ke halaman login untuk aksi yang butuh akun), pengguna biasa
  (baca + star), **Editor** (hak pengguna biasa + ubah data, tanpa membuat/menghapus), dan
  pemilik portofolio/superuser (semua hak). Peran Editor diatur lewat Django Group di `/admin`.
  Aksi yang tidak diizinkan mengembalikan HTTP 403, dan tombol create/edit/delete
  disembunyikan di template bagi pengguna yang tidak berhak.
- **Star** — pengguna yang sudah login bisa memberi atau membatalkan star pada Experience dan
  Education lewat relasi `ManyToManyField` ke `User` (maksimal satu star per pengguna), dengan
  jumlah total star dan status star pengguna yang ditampilkan di tiap kartu. Aksi star hanya
  menerima `POST` beserta `{% csrf_token %}`.
- **Role badge di navbar** *(extra feature)* — badge kecil di navbar yang menunjukkan peran akun
  yang sedang login (Owner / Editor / User).
- **AJAX pada Education & Experience** — daftar data dimuat lewat `fetch()` dari endpoint JSON
  (`/api/education/`, `/api/experience/`) tanpa reload halaman, lengkap dengan kondisi loading,
  error, dan data kosong.
- **Pencarian & filter tanpa reload** — pencarian institusi/bidang studi dengan *debounce* 300 ms
  dan filter jenjang, memakai `AbortController` agar respons lama tidak menimpa yang baru.
- **Tambah data lewat modal + AJAX** — form dikirim dengan `fetch()` beserta header
  `X-CSRFToken`, dibalas JSON (`201`/`400`/`403`) dengan pengecekan peran di server, lalu daftar
  diperbarui otomatis dan toast notifikasi ditampilkan.
- **Perlindungan XSS** — `strip_tags` di `clean_<field>` pada form (server) dan `escapeHtml()`
  sebelum data disisipkan ke HTML (client).
- **Jumlah hasil & tombol hapus pencarian** *(extra feature)* — menampilkan "N hasil untuk '...'"
  dan tombol untuk mengosongkan pencarian.

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

# 4. Terapkan migrasi database
python manage.py migrate

# 5. (Tugas 4) Buat akun pemilik portofolio (superuser)
python manage.py createsuperuser

# 6. Jalankan development server
python manage.py runserver
```

**Menyiapkan peran Editor (Tugas 4):** login ke `/admin`, buka *Groups* → *Add group*,
buat grup bernama tepat `Editor` (tanpa permission tambahan; pengecekan dilakukan di view),
lalu masukkan akun tertentu ke grup tersebut lewat *Users*.

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

- **Tutorial 4** — Menerapkan autentikasi bawaan Django: view `register`, `login_user`, dan
  `logout_user`, cookie `last_login` yang di-set saat login dan dihapus saat logout, serta status
  login di navbar. Pada Experience, create dan delete dibatasi untuk superuser, sedangkan star
  dibuka untuk pengguna yang sudah login lewat field `starred_by` (`ManyToManyField` ke `User`).
- **Tugas 4** — Menerapkan pola otorisasi yang sama pada **Education**: field `starred_by` beserta
  migrasinya, view `toggle_education_star`, dan peran **Editor** lewat Django Group dengan helper
  `is_editor()` (Editor boleh mengubah data, sedangkan create dan delete tetap khusus superuser).
  Tombol aksi pada template disembunyikan sesuai peran, `/api/education/` tidak lagi mengekspos
  `starred_by`, dan ditambahkan unit test `EducationAuthorizationTest`.
  - **Extra feature**: Role badge di navbar. Sebelumnya tidak ada penanda peran akun yang sedang
    login. Ditambahkan context processor `user_role` (`owner`, `editor`, atau `user`) sehingga
    `base.html` dapat menampilkan badge di semua halaman tanpa mengirim variabel dari tiap view,
    lengkap dengan `RoleBadgeTest`.

- **Tutorial 5** — Menerapkan AJAX pada Experience: endpoint JSON, `create_experience_ajax`,
  modal form, toast (`toast.js`), dan sanitasi XSS dengan `strip_tags`.
- **Tugas 5** — Menerapkan pola yang sama pada **Education**: `show_education` hanya merender
  kerangka halaman, data dimuat dari `get_education_json` (mendukung `q` dan `degree`),
  ditambah `create_education_ajax` dengan pengecekan peran, modal form, pencarian ber-debounce,
  dan unit test `EducationAjaxTest`.
  - **Extra feature**: Jumlah hasil dan tombol hapus pencarian. Sebelumnya pengguna tidak tahu
    berapa data yang cocok dan harus menghapus kata kunci secara manual. Ditambahkan
    keterangan "N hasil untuk '...'" (tetap tampil saat hasil 0) dan tombol hapus yang
    mengosongkan input lalu memuat ulang data.

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

  ### Refleksi Tugas 5

1. *Debouncing* adalah teknik menunda eksekusi sebuah fungsi sampai pengguna berhenti memicu
   event tersebut selama jeda tertentu. Setiap kali event terjadi, timer sebelumnya dibatalkan
   dan timer baru dimulai, sehingga fungsi hanya berjalan sekali setelah event berhenti. Pada
   proyek ini, setiap ketikan di kolom pencarian Education memicu event `input`. Handler-nya
   memanggil `clearTimeout(searchDebounceTimer)` lalu `setTimeout(...)` dengan jeda
   `SEARCH_DEBOUNCE_DELAY` (300 ms), sehingga `searchEducation()` baru dipanggil setelah
   pengguna berhenti mengetik. Tanpa debouncing, mengetik "universitas" (11 huruf) akan
   mengirim 11 request ke `/api/education/`, padahal hanya hasil akhirnya yang dibutuhkan. Hal
   ini memboroskan bandwidth dan membebani server serta database (tiap request menjalankan
   query `icontains`). Request juga bisa selesai dengan urutan terbalik sehingga hasil lama
   menimpa hasil baru, dan UI berkedip karena `#grid` terus dibangun ulang. Itu sebabnya
   debouncing penting pada fitur pencarian AJAX. Pada proyek ini debouncing dilengkapi
   `AbortController` untuk membatalkan request lama yang masih berjalan.

2. `await` membuat fungsi `async` menunggu sebuah *Promise* selesai sebelum baris berikutnya
   dijalankan, lalu mengembalikan nilai hasil Promise tersebut, tanpa memblokir halaman
   (browser tetap bisa menangani event lain selama menunggu). `fetch()` mengembalikan Promise
   yang baru terpenuhi setelah header respons diterima. Pada `fetchEducation()`, saya memakai
   `const response = await fetch(...)` agar `response` berisi objek `Response` sungguhan,
   kemudian `await response.json()` untuk membaca body-nya sebagai array JavaScript (proses
   ini juga asinkron). Jika `await` tidak dipakai, `response` hanyalah objek Promise yang
   belum selesai: `response.ok` bernilai `undefined` (sehingga `!response.ok` selalu benar dan
   kode salah mengira request gagal), dan `response.json` tidak tersedia pada Promise sehingga
   memunculkan error. Kalau kode setelahnya tetap berjalan, `educationData` hanya berisi
   Promise, bukan array, sehingga `.length` dan `.forEach()` tidak bekerja. Selain itu,
   `try/catch` tidak akan menangkap kegagalan jaringan karena error baru terjadi nanti,
   di luar blok `try`, sehingga state error (`#error`) tidak pernah tampil, dan state loading
   bisa langsung hilang sebelum data datang. Singkatnya, `await` menjamin urutan eksekusi
   (ambil data, lalu parse, lalu tampilkan) dan membuat penanganan error lewat `try/catch`
   bekerja.

3. XSS (*Cross-Site Scripting*) adalah serangan ketika penyerang menyisipkan kode
   JavaScript berbahaya ke dalam halaman web yang kemudian dieksekusi di browser korban,
   misalnya lewat input `<img src="x" onerror="alert('XSS!')">`. Jika disimpan di database dan
   ditampilkan ke pengunjung lain (*stored XSS*), script tersebut berjalan atas nama situs
   dan bisa mencuri cookie/sesi, mengubah isi halaman, atau melakukan aksi atas nama korban.
   Data yang ditampilkan lewat AJAX/JavaScript lebih rentan karena Django Template secara
   default melakukan *auto-escaping* (`<` menjadi `&lt;`, dan seterusnya), sehingga `{{ education.institution_name }}`
   aman tanpa usaha tambahan. Sebaliknya, JavaScript yang membangun HTML sendiri, misalnya
   lewat template literal yang diberikan ke `innerHTML` seperti pada `buildEducationCardElement()`,
   tidak memiliki proteksi otomatis: string mentah dari JSON akan diparse browser sebagai
   HTML, sehingga tag dan atribut `onerror` ikut dieksekusi. Karena itu proyek ini memakai
   pertahanan berlapis. Di server, `clean_institution_name` dan sejenisnya memakai
   `strip_tags` sehingga tag HTML dibuang sebelum disimpan, input yang hanya berisi tag
   ditolak, dan URL berskema `javascript:` ditolak. Di client, setiap nilai teks dibungkus
   `escapeHtml()` sebelum disisipkan ke `innerHTML`, dan `textContent` dipakai untuk teks
   seperti keterangan jumlah hasil pencarian. Dua lapisan ini saling melengkapi: sanitasi
   server melindungi data yang tersimpan, sedangkan escaping client melindungi tampilan
   seandainya ada data kotor yang lolos.


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
Chat Link: https://claude.ai/share/91077e93-745d-4a0d-8959-168170083a8a 
Bagian yang dibantu AI:

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
Chat Link: https://claude.ai/share/46b6a9d1-632c-48ea-a130-8dadf2c59b46 
Bagian yang dibantu AI:

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

**Tugas 4** - Saya menggunakan Claude (Anthropic, via claude.ai) untuk membantu pengerjaan Tugas 4 ini.
Chat Link: https://claude.ai/share/07ac8a24-2886-4392-916d-1de320653bcf
Bagian yang dibantu AI:

- Menulis sebagian besar kode autentikasi, helper `is_editor()`, view star, dan pembatasan hak
  akses pada view CRUD, beserta template dan migrasinya.
- Menulis `EducationAuthorizationTest`, `RoleBadgeTest`, serta context processor dan CSS role badge.

Strategi prompting: Strateginya yakni memastikan kode yang digenerate sudah sesuai, bebas bug, dan
dengan pendekatan yang tepat. Saya juga aktif bertanya untuk memastikan pemahaman sudah baik, 
contohnya mengenai mekanisme penentuan Editor lalu memeriksa kode yang dihasilkan dan mengujinya 
langsung di browser dengan akun berbeda untuk tiap peran sebelum melakukan commit.

Keterbatasan yang saya temukan: AI mendorong pada pendekatan yang singkat dan modular. Walaupun
memang terlihat ringkas dan rapih, tapi di satu sisi mengurangi readability dan kurang baik
sebagai contoh untuk bahan pemebelajaran.

**Tugas 5** - Saya menggunakan Claude (Anthropic, via claude.ai) untuk membantu pengerjaan Tugas 5 ini.
Chat Link: https://claude.ai/share/276e5634-65ce-4bec-9ccc-c9d25f814369 
Bagian yang dibantu AI: 

- Menulis sebagian besar kode AJAX pada Education (`get_education_json`, `create_education_ajax`,
  `education.html`, modal form), toast, sanitasi XSS, dan `EducationAjaxTest`.
- Menulis fitur tambahan jumlah hasil dan tombol hapus pencarian, serta membantu menyusun README.

Strategi prompting: Untuk membuat sebagian kode, saya memanfaatkan bantuan AI, dengan tetap berusaha 
memahami kodenya. Saya mengunggah source code dan PDF instruksi tugas, meminta perubahan per bagian kecil, 
bertanya ketika ada yang belum jelas, lalu menguji langsung di browser dengan tiap peran serta payload XSS 
sebelum commit.

Keterbatasan yang saya temukan: AI tidak bisa menjalankan aplikasi di browser, sehingga pengujian
akhir harus saya lakukan sendiri. Kodenya cenderung padat dan melebihi permintaan, dan jawaban
refleksinya cenderung generik sehingga perlu saya sesuaikan dengan kode proyek. Terdapat juga beberapa
bug yang muncul, misalnya posisi jumlah dan hapus pencarian (extra feature) dimana terdapat kesalahan
pada posisi htmlnya, yang saya perbaiki secara manual.