## myportofolio
Nama : Ferdinandus Pakasi
NPM : 2506602643
Kelas : PBP-D

## Fitur yang Sudah Diimplementasikan

- **About Me** — profil, foto, NPM, dan bio pribadi.
- **Experience** — riwayat pengalaman organisasi/kepanitiaan, ditampilkan sebagai timeline
  vertikal, dengan tiap entri bisa di-expand/collapse.
- **Dark/Light mode toggle** — tombol di navbar untuk beralih tema.

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

### Tugas 1

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


## AI Disclosure

Saya menggunakan Claude (Anthropic, via claude.ai) untuk membantu pengerjaan Tugas 1 ini.
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

