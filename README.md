# BANTU - Chatbot Edukasi Anti-Narkoba BNN

Chatbot edukasi yang aman, etis, dan profesional untuk program pencegahan narkoba Badan Narkotika Nasional (BNN) Republik Indonesia.

## 🎯 Fitur Utama

### Edukasi Komprehensif
- ⚠️ Bahaya dan dampak narkoba (fisik, mental, sosial)
- 🔍 Jenis-jenis narkoba dan efeknya
- 👁️ Tanda-tanda penyalahgunaan
- ❓ Mitos vs fakta seputar narkoba
- ⚖️ Aspek hukum narkoba di Indonesia

### Pencegahan Aktif
- 🛡️ Strategi menolak ajakan
- 💪 Teknik komunikasi asertif
- 🎯 Tips menghadapi peer pressure
- ✨ Panduan membangun lingkungan positif

### Dukungan & Bantuan
- 🏥 Informasi rehabilitasi
- 👨‍👩‍👧 Panduan dukungan keluarga
- 📞 Kontak layanan bantuan
- 💚 Jalur rujukan profesional

### Safety by Design
- ❌ Menolak pertanyaan berbahaya secara otomatis
- ✅ Guardrail ketat untuk keamanan
- 🔒 Tidak menyimpan data sensitif
- 📊 Analitik anonim untuk peningkatan layanan

## 🚀 Cara Menjalankan

### Persyaratan Sistem
- Python 3.8 atau lebih tinggi
- pip (Python package manager)

### Instalasi

1. **Clone atau unduh repository ini**
```bash
   # Jika menggunakan git
   git clone <repository-url>
   cd bantu-chatbot
```

2. **Buat virtual environment (opsional tapi disarankan)**
```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
```

3. **Install dependencies**
```bash
   pip install -r requirements.txt
```

4. **Jalankan aplikasi**
```bash
   streamlit run app.py
```

5. **Buka browser**
   - Aplikasi akan otomatis terbuka di `http://localhost:8501`
   - Jika tidak, buka URL tersebut secara manual

## 📖 Cara Penggunaan

### Untuk Pengguna

1. **Pilih Mode Pengguna** di sidebar:
   - Remaja (bahasa santai, edukatif)
   - Orang Tua (fokus dukungan keluarga)
   - Pendidik (materi pembelajaran)
   - Umum (informasi lengkap)

2. **Ajukan Pertanyaan** dengan mengetik di kolom chat:
   - "Apa bahaya narkoba?"
   - "Bagaimana cara menolak ajakan teman?"
   - "Gimana cara bantu keluarga yang kecanduan?"

3. **Gunakan Pertanyaan Cepat** untuk akses informasi populer

4. **Lihat Analitik** untuk memahami topik yang sering ditanyakan

### Topik yang Dapat Ditanyakan

✅ **AMAN & DIDUKUNG:**
- Bahaya dan dampak narkoba
- Cara pencegahan dan penolakan
- Informasi rehabilitasi
- Dukungan keluarga
- Aspek hukum umum
- Tanda-tanda penyalahgunaan

❌ **TIDAK DIDUKUNG (Auto-Refuse):**
- Cara menggunakan/mengonsumsi
- Dosis atau takaran
- Cara mendapatkan/membeli
- Cara menyembunyikan
- Cara lolos tes
- Cara membuat/meracik

## 🛡️ Fitur Keamanan

### Guardrail Otomatis
Sistem secara otomatis mendeteksi dan menolak pertanyaan yang:
- Meminta instruksi penggunaan
- Menanyakan dosis/takaran
- Mencari cara mendapatkan narkoba
- Menghindari deteksi/tes
- Membuat/meracik narkoba

### Respons Safety
Ketika pertanyaan terlarang terdeteksi, sistem:
1. ❌ Menolak dengan tegas namun empatik
2. 📚 Menjelaskan batasan sistem
3. ✅ Mengarahkan ke informasi edukatif
4. 📞 Memberikan kontak bantuan profesional

### Privasi & Data
- 🔒 Tidak menyimpan data pribadi pengguna
- 📊 Hanya menyimpan statistik anonim
- 💾 Data tidak dibagikan ke pihak ketiga
- 🗑️ Riwayat chat dapat dihapus kapan saja

## 📊 Analitik & Monitoring

### Dashboard Analitik
- Total pertanyaan yang diajukan
- Distribusi intent (edukasi, pencegahan, dukungan, dll.)
- Topik paling sering diakses
- Jumlah pertanyaan terlarang yang berhasil diblok ir

### Ekspor Data
- Unduh laporan analitik dalam format JSON
- Berguna untuk evaluasi dan peningkatan layanan
- Data agregat tanpa informasi personal

## 🏗️ Arsitektur Sistem

### RAG (Retrieval-Augmented Generation)
```
User Query → Intent Classification → Content Retrieval → Response Generation → Safety Check → Output
```

### Komponen Utama

1. **Knowledge Base**
   - Database konten edukasi terkurasi
   - Terorganisir berdasarkan topik
   - Mudah diperbarui dan diperluas

2. **Intent Classifier**
   - Mengklasifikasikan pertanyaan pengguna
   - 7 kategori intent (education, prevention, support, signs, legal, forbidden, general)
   - Regex-based pattern matching

3. **Safety Layer**
   - Deteksi pertanyaan terlarang
   - Respons refuse + redirect
   - Logging untuk audit

4. **Analytics Engine**
   - Tracking penggunaan anonim
   - Aggregasi statistik
   - Export untuk evaluasi

## 🎓 Use Cases untuk Magang BNN

### 1. Program Edukasi Sekolah
- Sumber informasi interaktif untuk siswa
- Materi pendukung guru BK
- Kampanye anti-narkoba digital

### 2. Layanan Masyarakat
- FAQ otomatis untuk pertanyaan umum
- Screening awal sebelum konsultasi
- Edukasi preventif 24/7

### 3. Dukungan Keluarga
- Panduan untuk orang tua
- Informasi rehabilitasi
- Support group referral

### 4. Research & Development
- Analisis topik yang banyak ditanyakan
- Identifikasi gap edukasi
- Evaluasi efektivitas kampanye

## 📈 Deliverables Magang

### 1. Aplikasi Chatbot
✅ Aplikasi web interaktif berbasis Streamlit
✅ UI/UX yang user-friendly dan profesional
✅ Multi-mode untuk berbagai pengguna

### 2. Dokumentasi
✅ README lengkap dengan panduan instalasi
✅ Dokumentasi kode yang rapi
✅ Panduan penggunaan untuk end-user

### 3. Safety Policy Document
✅ Daftar konten yang dilarang
✅ Prosedur handling pertanyaan sensitif
✅ Guidelines untuk perluasan konten

### 4. Test Scenarios
✅ 50+ pertanyaan aman dengan respons
✅ 30+ pertanyaan terlarang dengan refuse
✅ Hasil uji coba dan evaluasi

### 5. Analytics Dashboard
✅ Visualisasi penggunaan
✅ Tracking topik populer
✅ Safety monitoring

## 🔧 Pengembangan Lebih Lanjut

### Fitur yang Bisa Ditambahkan

1. **Integrasi AI Model**
   - OpenAI GPT untuk respons lebih natural
   - Fine-tuning dengan dataset BNN
   - Multilingual support

2. **Database Backend**
   - PostgreSQL/MongoDB untuk persistensi
   - User session management
   - Advanced analytics

3. **Fitur Interaktif**
   - Kuis edukatif
   - Sertifikat kompetensi
   - Gamification

4. **Integrasi Layanan**
   - Booking konsultasi online
   - Telemedicine integration
   - Rujukan otomatis ke fasyankes

5. **Mobile App**
   - iOS dan Android app
   - Push notifications
   - Offline mode

### Skalabilitas
- Deploy ke cloud (AWS, GCP, Azure)
- Containerization dengan Docker
- Load balancing untuk traffic tinggi
- CDN untuk performa global

## 📞 Kontak & Support

### Hotline BNN
- 📱 184 (24/7, Gratis, Rahasia)
- 💬 SMS/WhatsApp: 081-221-675-675
- 📧 Email: halo@bnn.go.id
- 🌐 Website: www.bnn.go.id

### Developer Contact
Untuk pertanyaan teknis atau kolaborasi pengembangan, silakan hubungi tim IT BNN.

## 📄 Lisensi & Disclaimer

© 2025 Badan Narkotika Nasional Republik Indonesia

**Disclaimer:**
Chatbot ini adalah alat edukasi dan tidak menggantikan konsultasi profesional. Untuk masalah serius terkait penyalahgunaan narkoba, segera hubungi profesional kesehatan atau Hotline BNN 184.

---

**Dikembangkan dengan ❤️ untuk Indonesia Bebas Narkoba**
