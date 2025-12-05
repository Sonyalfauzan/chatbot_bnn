import streamlit as st
import json
from datetime import datetime
from typing import Dict, List, Tuple
import re

# Konfigurasi halaman
st.set_page_config(
    page_title="BANTU - Chatbot Edukasi Anti-Narkoba BNN",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS untuk styling profesional
def load_css():
    st.markdown("""
        <style>
        .main {
            background-color: #f8f9fa;
        }
        .stApp {
            max-width: 1200px;
            margin: 0 auto;
        }
        .chat-message {
            padding: 1.5rem;
            border-radius: 0.5rem;
            margin-bottom: 1rem;
            display: flex;
            flex-direction: column;
        }
        .user-message {
            background-color: #e3f2fd;
            border-left: 4px solid #2196f3;
        }
        .bot-message {
            background-color: #ffffff;
            border-left: 4px solid #4caf50;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .warning-message {
            background-color: #fff3cd;
            border-left: 4px solid #ff9800;
            padding: 1rem;
            border-radius: 0.5rem;
            margin: 1rem 0;
        }
        .header-banner {
            background: linear-gradient(135deg, #1976d2 0%, #0d47a1 100%);
            color: white;
            padding: 2rem;
            border-radius: 0.5rem;
            margin-bottom: 2rem;
            text-align: center;
        }
        .stats-card {
            background: white;
            padding: 1.5rem;
            border-radius: 0.5rem;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            margin: 1rem 0;
        }
        .intent-badge {
            display: inline-block;
            padding: 0.25rem 0.75rem;
            border-radius: 1rem;
            font-size: 0.85rem;
            font-weight: 600;
            margin-top: 0.5rem;
        }
        .intent-education {
            background-color: #e3f2fd;
            color: #1976d2;
        }
        .intent-prevention {
            background-color: #f3e5f5;
            color: #7b1fa2;
        }
        .intent-support {
            background-color: #e8f5e9;
            color: #388e3c;
        }
        .intent-forbidden {
            background-color: #ffebee;
            color: #c62828;
        }
        </style>
    """, unsafe_allow_html=True)

# Knowledge Base - Konten Edukasi
class KnowledgeBase:
    def __init__(self):
        self.education_content = {
            "bahaya_narkoba": {
                "title": "Bahaya Narkoba bagi Kesehatan",
                "content": """
                Narkoba memiliki dampak serius bagi kesehatan fisik dan mental:
                
                **Dampak Fisik:**
                - Kerusakan organ vital (jantung, paru-paru, hati, ginjal)
                - Penurunan sistem kekebalan tubuh
                - Gangguan koordinasi dan keseimbangan
                - Risiko overdosis yang dapat berakibat fatal
                
                **Dampak Mental:**
                - Gangguan kecemasan dan depresi
                - Perubahan perilaku dan kepribadian
                - Penurunan kemampuan kognitif dan memori
                - Risiko gangguan mental jangka panjang
                
                **Dampak Sosial:**
                - Putusnya hubungan keluarga dan pertemanan
                - Kesulitan dalam pekerjaan dan pendidikan
                - Isolasi sosial dan stigma
                - Beban ekonomi untuk diri dan keluarga
                """,
                "keywords": ["bahaya", "dampak", "kesehatan", "fisik", "mental", "efek"]
            },
            "jenis_narkoba": {
                "title": "Pengenalan Jenis-Jenis Narkoba",
                "content": """
                Narkoba dapat dikategorikan berdasarkan efeknya:
                
                **Depresan:**
                Menekan sistem saraf pusat, menyebabkan rasa tenang berlebihan, mengantuk, hingga tidak sadarkan diri.
                
                **Stimulan:**
                Merangsang sistem saraf pusat, menyebabkan hiperaktif, euforia berlebihan, dan dapat merusak jantung.
                
                **Halusinogen:**
                Mengubah persepsi, pikiran, dan perasaan, menyebabkan halusinasi dan kehilangan realitas.
                
                ⚠️ Semua jenis narkoba berbahaya dan ilegal. Tidak ada yang "aman" untuk dikonsumsi.
                """,
                "keywords": ["jenis", "macam", "kategori", "tipe", "golongan"]
            },
            "tanda_penyalahgunaan": {
                "title": "Tanda-Tanda Penyalahgunaan Narkoba",
                "content": """
                Kenali tanda-tanda umum penyalahgunaan narkoba:
                
                **Perubahan Fisik:**
                - Mata merah atau pupil melebar/menyempit abnormal
                - Perubahan berat badan drastis
                - Kebersihan diri menurun
                - Bekas suntikan atau luka yang tidak biasa
                
                **Perubahan Perilaku:**
                - Perubahan mood yang ekstrem
                - Menarik diri dari keluarga dan teman
                - Kehilangan minat pada aktivitas favorit
                - Sering berbohong atau menyembunyikan sesuatu
                
                **Perubahan Sosial:**
                - Berganti lingkungan pertemanan secara tiba-tiba
                - Masalah di sekolah atau tempat kerja
                - Kesulitan keuangan yang tidak dijelaskan
                - Sering meminta atau mencuri uang
                
                💡 Jika Anda atau orang terdekat menunjukkan tanda-tanda ini, segera cari bantuan profesional.
                """,
                "keywords": ["tanda", "ciri", "gejala", "mengenali", "indikasi", "penyalahgunaan"]
            },
            "cara_menolak": {
                "title": "Strategi Menolak Ajakan Narkoba",
                "content": """
                Teknik efektif untuk menolak ajakan menggunakan narkoba:
                
                **Teknik Komunikasi Asertif:**
                1. **Katakan "TIDAK" dengan tegas dan jelas**
                   - "Tidak, terima kasih. Aku tidak tertarik."
                   - "Maaf, itu bukan untukku."
                
                2. **Berikan alasan singkat dan jelas**
                   - "Aku ingin menjaga kesehatanku."
                   - "Aku punya tujuan yang ingin kucapai."
                
                3. **Tawarkan alternatif positif**
                   - "Yuk, main basket aja."
                   - "Gimana kalau kita nonton film?"
                
                4. **Tinggalkan situasi jika perlu**
                   - Jangan ragu untuk pergi dari lingkungan yang tidak aman
                
                **Tips Tambahan:**
                - Latih penolakan di depan cermin
                - Cari teman yang mendukung keputusan positifmu
                - Percaya diri dengan pilihanmu
                - Ingat tujuan dan cita-citamu
                
                🎯 Menolak narkoba adalah tanda kekuatan, bukan kelemahan!
                """,
                "keywords": ["menolak", "nolak", "ajakan", "tekanan", "peer pressure", "teman"]
            },
            "dukungan_keluarga": {
                "title": "Cara Mendukung Anggota Keluarga",
                "content": """
                Panduan untuk keluarga dalam mendukung anggota yang terpapar narkoba:
                
                **Komunikasi Empatik:**
                - Dengarkan tanpa menghakimi
                - Ekspresikan kekhawatiran dengan penuh kasih sayang
                - Hindari menyalahkan atau melabeli
                - Tunjukkan bahwa Anda peduli dan siap membantu
                
                **Langkah-Langkah Praktis:**
                1. Cari informasi tentang rehabilitasi dan konseling
                2. Konsultasikan dengan profesional kesehatan
                3. Dukung proses pemulihan dengan sabar
                4. Jaga kesehatan mental keluarga lainnya
                5. Bergabung dengan support group untuk keluarga
                
                **Yang Harus Dihindari:**
                - Jangan menyangkal masalah
                - Jangan menutup-nutupi perilaku berbahaya
                - Jangan memberikan uang tanpa pengawasan
                - Jangan menyerah pada proses pemulihan
                
                **Sumber Daya:**
                📞 Hotline BNN: 184
                🏥 Puskesmas dan Rumah Sakit terdekat
                👥 Komunitas pemulihan dan support group
                
                💚 Pemulihan adalah perjalanan, bukan tujuan akhir. Dukungan keluarga sangat berarti.
                """,
                "keywords": ["keluarga", "orang tua", "dukungan", "support", "membantu", "kerabat"]
            },
            "rehabilitasi": {
                "title": "Informasi Rehabilitasi dan Pemulihan",
                "content": """
                Informasi tentang proses rehabilitasi narkoba:
                
                **Jenis Layanan Rehabilitasi:**
                - Rehabilitasi rawat inap (intensive care)
                - Rehabilitasi rawat jalan (outpatient)
                - Program konseling dan terapi
                - Komunitas pemulihan (recovery community)
                
                **Tahapan Pemulihan:**
                1. **Detoksifikasi** - Membersihkan tubuh dari zat adiktif
                2. **Rehabilitasi** - Terapi dan konseling intensif
                3. **Aftercare** - Dukungan pasca rehabilitasi
                4. **Reintegrasi** - Kembali ke masyarakat
                
                **Cara Mengakses Layanan:**
                - Hubungi hotline BNN: 184 (24/7)
                - Kunjungi Puskesmas atau RS terdekat
                - Datang langsung ke Loka Rehabilitasi BNN
                - Konsultasi online dengan konselor
                
                **Hak Pasien Rehabilitasi:**
                - Mendapat perlakuan manusiawi dan bermartabat
                - Privasi dan kerahasiaan data pribadi
                - Akses ke layanan kesehatan yang layak
                - Dukungan reintegrasi sosial
                
                🌟 Meminta bantuan adalah langkah pertama menuju perubahan!
                """,
                "keywords": ["rehabilitasi", "pemulihan", "bantuan", "terapi", "konseling", "rawat"]
            },
            "hukum": {
                "title": "Aspek Hukum Narkoba di Indonesia",
                "content": """
                Informasi umum tentang hukum narkoba di Indonesia:
                
                **Undang-Undang yang Mengatur:**
                - UU No. 35 Tahun 2009 tentang Narkotika
                - Fokus pada pencegahan, rehabilitasi, dan penegakan hukum
                
                **Kategori Tindak Pidana:**
                - Menggunakan narkoba: dapat dikenai pidana atau rehabilitasi
                - Menyimpan/membawa: hukuman penjara
                - Mengedarkan: hukuman berat hingga hukuman mati
                - Memproduksi: hukuman maksimal
                
                **Pendekatan Rehabilitasi:**
                Indonesia menerapkan pendekatan rehabilitasi untuk pengguna, bukan hanya hukuman. Pecandu narkoba berhak mendapat rehabilitasi.
                
                **Pelaporan Sukarela:**
                Jika Anda atau keluarga terlibat narkoba, melapor ke pihak berwenang secara sukarela dapat membantu Anda mendapat rehabilitasi, bukan hukuman.
                
                ⚖️ Tujuan hukum adalah melindungi masyarakat dan membantu pemulihan.
                
                📞 Untuk informasi lebih lanjut: Hubungi BNN 184
                """,
                "keywords": ["hukum", "undang-undang", "uu", "pidana", "sanksi", "legal"]
            },
            "mitos_fakta": {
                "title": "Mitos vs Fakta tentang Narkoba",
                "content": """
                Membedah mitos dan fakta seputar narkoba:
                
                **MITOS #1:** "Coba sekali saja tidak apa-apa"
                **FAKTA:** Sekali coba bisa membuat kecanduan. Otak remaja sangat rentan terhadap adiksi.
                
                **MITOS #2:** "Narkoba bisa meningkatkan kreativitas"
                **FAKTA:** Narkoba merusak fungsi otak dan justru menurunkan kemampuan kognitif jangka panjang.
                
                **MITOS #3:** "Ganja itu natural, jadi aman"
                **FAKTA:** Natural tidak berarti aman. Ganja dapat menyebabkan gangguan mental dan adiksi.
                
                **MITOS #4:** "Saya bisa berhenti kapan saja"
                **FAKTA:** Adiksi mengubah kimia otak. Berhenti membutuhkan bantuan profesional.
                
                **MITOS #5:** "Hanya orang lemah yang kecanduan"
                **FAKTA:** Adiksi adalah penyakit medis yang bisa dialami siapa saja, bukan masalah karakter.
                
                **MITOS #6:** "Narkoba membuat masalah hilang"
                **FAKTA:** Narkoba hanya mengalihkan masalah sementara dan menciptakan masalah baru yang lebih besar.
                
                💡 Edukasi yang benar adalah kunci pencegahan!
                """,
                "keywords": ["mitos", "fakta", "hoax", "benar", "salah", "myth"]
            }
        }
        
        self.forbidden_patterns = [
            r"cara\s+(pakai|pake|menggunakan|memakai|konsumsi)",
            r"(dosis|takaran|ukuran)\s+",
            r"(beli|buat|bikin|racik|tanam|budidaya)",
            r"(menyembunyikan|sembunyikan|tutupi)",
            r"(lolos|lulus|lewat)\s+tes",
            r"(aman|safety)\s+(cara|pakai|pake|konsumsi)",
            r"cara\s+(mendapat|dapat|cari)\s+",
            r"(resep|formula|komposisi)\s+",
            r"(harga|jual|beli)\s+",
            r"tempat\s+(beli|jual|cari)",
        ]
        
        self.intent_patterns = {
            "education": [
                r"(bahaya|dampak|efek|akibat)",
                r"(jenis|macam|tipe|golongan)",
                r"(pengertian|definisi|apa itu)",
                r"(informasi|info|penjelasan)",
            ],
            "prevention": [
                r"(menolak|nolak|hindari|cegah)",
                r"(ajakan|tawaran|tekanan)",
                r"(strategi|cara|tips)\s+(menolak|nolak)",
            ],
            "support": [
                r"(bantuan|tolong|help)",
                r"(rehabilitasi|pemulihan|terapi)",
                r"(keluarga|orang tua|teman)",
                r"(dukungan|support|dukung)",
            ],
            "signs": [
                r"(tanda|ciri|gejala)",
                r"(mengenali|kenali|deteksi)",
                r"(penyalahgunaan|pecandu)",
            ],
            "legal": [
                r"(hukum|undang|sanksi|pidana)",
                r"(legal|ilegal)",
            ]
        }

    def classify_intent(self, query: str) -> str:
        query_lower = query.lower()
        
        # Cek forbidden patterns terlebih dahulu
        for pattern in self.forbidden_patterns:
            if re.search(pattern, query_lower):
                return "forbidden"
        
        # Klasifikasi intent
        intent_scores = {intent: 0 for intent in self.intent_patterns}
        
        for intent, patterns in self.intent_patterns.items():
            for pattern in patterns:
                if re.search(pattern, query_lower):
                    intent_scores[intent] += 1
        
        max_score = max(intent_scores.values())
        if max_score > 0:
            return max(intent_scores, key=intent_scores.get)
        
        return "general"

    def search_content(self, query: str) -> Tuple[str, str, str]:
        query_lower = query.lower()
        intent = self.classify_intent(query)
        
        # Jika intent forbidden, kembalikan response penolakan
        if intent == "forbidden":
            return self.get_refusal_response(), "forbidden", intent
        
        # Cari konten yang relevan
        best_match = None
        best_score = 0
        
        for key, content in self.education_content.items():
            score = sum(1 for keyword in content["keywords"] if keyword in query_lower)
            if score > best_score:
                best_score = score
                best_match = key
        
        if best_match and best_score > 0:
            content = self.education_content[best_match]
            return content["content"], best_match, intent
        
        # Jika tidak ada match, kembalikan response umum
        return self.get_general_response(intent), "general", intent

    def get_refusal_response(self) -> str:
        return """
        ⚠️ **Maaf, saya tidak dapat membantu dengan permintaan tersebut.**
        
        Saya adalah chatbot edukasi yang dirancang untuk:
        ✅ Memberikan informasi tentang bahaya narkoba
        ✅ Membantu strategi pencegahan
        ✅ Memberikan informasi tentang bantuan dan rehabilitasi
        
        Saya **tidak dapat** memberikan informasi tentang:
        ❌ Cara menggunakan atau mendapatkan narkoba
        ❌ Dosis atau takaran
        ❌ Cara menghindari deteksi atau tes
        ❌ Cara membuat, meracik, atau menyembunyikan
        
        **Tahukah Anda?**
        Tidak ada cara "aman" untuk menggunakan narkoba ilegal. Semua penggunaan narkoba membawa risiko serius bagi kesehatan fisik, mental, dan masa depan Anda.
        
        **Butuh Bantuan?**
        📞 Hotline BNN: 184 (24/7, gratis, rahasia)
        🏥 Kunjungi Puskesmas atau RS terdekat
        💚 Rehabilitasi tersedia dan rahasia
        
        Saya di sini untuk membantu Anda membuat keputusan yang lebih sehat. Apakah ada yang bisa saya bantu tentang pencegahan, bahaya, atau cara mendapat bantuan?
        """

    def get_general_response(self, intent: str) -> str:
        responses = {
            "education": """
            Saya bisa membantu Anda dengan informasi edukasi tentang narkoba. Berikut beberapa topik yang bisa saya jelaskan:
            
            📚 **Topik Edukasi:**
            - Bahaya dan dampak narkoba bagi kesehatan
            - Jenis-jenis narkoba dan efeknya
            - Tanda-tanda penyalahgunaan narkoba
            - Mitos vs fakta seputar narkoba
            - Aspek hukum narkoba di Indonesia
            
            Silakan tanyakan topik yang Anda ingin ketahui lebih lanjut!
            """,
            "prevention": """
            Saya bisa membantu Anda dengan strategi pencegahan! Berikut yang bisa saya bantu:
            
            🛡️ **Pencegahan:**
            - Cara menolak ajakan menggunakan narkoba
            - Strategi komunikasi asertif
            - Tips menghadapi tekanan teman sebaya
            - Membangun lingkungan positif
            
            Apa yang ingin Anda pelajari lebih lanjut?
            """,
            "support": """
            Saya di sini untuk membantu Anda mencari dukungan yang tepat!
            
            💚 **Dukungan & Bantuan:**
            - Informasi tentang rehabilitasi
            - Cara mendukung anggota keluarga
            - Layanan konseling dan terapi
            - Hotline dan kontak bantuan
            
            📞 **Kontak Darurat:**
            - Hotline BNN: 184 (24/7)
            - Puskesmas/RS terdekat
            - Konselor online
            
            Bagaimana saya bisa membantu Anda hari ini?
            """,
            "general": """
            Halo! Saya BANTU, chatbot edukasi anti-narkoba dari BNN. 👋
            
            Saya dapat membantu Anda dengan:
            
            📚 **Edukasi**
            - Bahaya dan dampak narkoba
            - Jenis-jenis narkoba
            - Mitos vs fakta
            
            🛡️ **Pencegahan**
            - Cara menolak ajakan
            - Strategi menghadapi tekanan
            
            💚 **Dukungan**
            - Informasi rehabilitasi
            - Cara membantu keluarga
            - Kontak bantuan
            
            ⚖️ **Hukum**
            - Aspek legal narkoba
            
            Silakan tanyakan apa yang ingin Anda ketahui!
            """
        }
        
        return responses.get(intent, responses["general"])

# Inisialisasi Knowledge Base
@st.cache_resource
def get_knowledge_base():
    return KnowledgeBase()

# Inisialisasi Session State
def init_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "analytics" not in st.session_state:
        st.session_state.analytics = {
            "total_queries": 0,
            "intent_distribution": {
                "education": 0,
                "prevention": 0,
                "support": 0,
                "signs": 0,
                "legal": 0,
                "forbidden": 0,
                "general": 0
            },
            "topics_accessed": {}
        }
    if "mode" not in st.session_state:
        st.session_state.mode = "Remaja"

# Update Analytics
def update_analytics(intent: str, topic: str):
    st.session_state.analytics["total_queries"] += 1
    st.session_state.analytics["intent_distribution"][intent] += 1
    
    if topic != "general" and topic != "forbidden":
        if topic in st.session_state.analytics["topics_accessed"]:
            st.session_state.analytics["topics_accessed"][topic] += 1
        else:
            st.session_state.analytics["topics_accessed"][topic] = 1

# Render Chat Message
def render_message(role: str, content: str, intent: str = None):
    if role == "user":
        st.markdown(f"""
            <div class="chat-message user-message">
                <strong>🙋 Anda:</strong>
                <p>{content}</p>
            </div>
        """, unsafe_allow_html=True)
    else:
        intent_class = f"intent-{intent}" if intent else "intent-education"
        intent_label = {
            "education": "📚 Edukasi",
            "prevention": "🛡️ Pencegahan",
            "support": "💚 Dukungan",
            "signs": "🔍 Tanda-tanda",
            "legal": "⚖️ Hukum",
            "forbidden": "⚠️ Terlarang",
            "general": "💬 Umum"
        }.get(intent, "💬 Umum")
        
        st.markdown(f"""
            <div class="chat-message bot-message">
                <strong>🤖 BANTU:</strong>
                <span class="intent-badge {intent_class}">{intent_label}</span>
                <div>{content}</div>
            </div>
        """, unsafe_allow_html=True)

# Main App
def main():
    load_css()
    init_session_state()
    kb = get_knowledge_base()
    
    # Header
    st.markdown("""
        <div class="header-banner">
            <h1>🛡️ BANTU - Chatbot Edukasi Anti-Narkoba</h1>
            <p style="font-size: 1.1rem; margin-top: 0.5rem;">
                Badan Narkotika Nasional (BNN) Republik Indonesia
            </p>
            <p style="font-size: 0.95rem; opacity: 0.9;">
                Chatbot Edukasi, Pencegahan, dan Dukungan
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.image("https://via.placeholder.com/150x150.png?text=BNN+Logo", width=150)
        
        st.markdown("### ⚙️ Pengaturan")
        
        mode = st.selectbox(
            "Mode Pengguna",
            ["Remaja", "Orang Tua", "Pendidik", "Umum"],
            index=["Remaja", "Orang Tua", "Pendidik", "Umum"].index(st.session_state.mode)
        )
        st.session_state.mode = mode
        
        st.markdown("---")
        
        st.markdown("### 📊 Statistik Sesi")
        st.metric("Total Pertanyaan", st.session_state.analytics["total_queries"])
        
        if st.session_state.analytics["total_queries"] > 0:
            st.markdown("#### Distribusi Intent")
            for intent, count in st.session_state.analytics["intent_distribution"].items():
                if count > 0:
                    percentage = (count / st.session_state.analytics["total_queries"]) * 100
                    st.progress(percentage / 100)
                    st.caption(f"{intent.capitalize()}: {count} ({percentage:.1f}%)")
        
        st.markdown("---")
        
        st.markdown("### 📞 Kontak Darurat")
        st.info("""
        **Hotline BNN:**  
        📱 184 (24/7)
        
        **SMS/WhatsApp:**  
        💬 081-221-675-675
        
        **Email:**  
        📧 halo@bnn.go.id
        """)
        
        st.markdown("---")
        
        if st.button("🗑️ Hapus Riwayat Chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
        
        if st.button("📊 Reset Statistik", use_container_width=True):
            st.session_state.analytics = {
                "total_queries": 0,
                "intent_distribution": {
                    "education": 0,
                    "prevention": 0,
                    "support": 0,
                    "signs": 0,
                    "legal": 0,
                    "forbidden": 0,
                    "general": 0
                },
                "topics_accessed": {}
            }
            st.rerun()
    
    # Main Content
    tab1, tab2, tab3 = st.tabs(["💬 Chat", "📚 Panduan", "📊 Analitik"])
    
    with tab1:
        # Chat Container
        chat_container = st.container()
        
        with chat_container:
            if len(st.session_state.messages) == 0:
                st.markdown("""
                    <div class="stats-card">
                        <h3>👋 Selamat Datang di BANTU!</h3>
                        <p>Saya adalah chatbot edukasi yang siap membantu Anda dengan informasi tentang:</p>
                        <ul>
                            <li>📚 Bahaya dan dampak narkoba</li>
                            <li>🛡️ Cara mencegah dan menolak ajakan</li>
                            <li>💚 Informasi bantuan dan rehabilitasi</li>
                            <li>⚖️ Aspek hukum narkoba</li>
                        </ul>
                        <p><strong>Silakan mulai dengan mengetik pertanyaan Anda di bawah!</strong></p>
                    </div>
                """, unsafe_allow_html=True)
            
            for message in st.session_state.messages:
                render_message(
                    message["role"],
                    message["content"],
                    message.get("intent")
                )
        
        # Input Area
        st.markdown("---")
        col1, col2 = st.columns([5, 1])
        
        with col1:
            user_input = st.text_input(
                "Ketik pertanyaan Anda...",
                key="user_input",
                placeholder="Contoh: Apa bahaya narkoba? Bagaimana cara menolak ajakan teman?"
            )
        
        with col2:
            send_button = st.button("📤 Kirim", use_container_width=True)
        
        # Quick Questions
        st.markdown("#### 💡 Pertanyaan Cepat")
        quick_questions = [
            "Apa bahaya narkoba bagi kesehatan?",
            "Bagaimana cara menolak ajakan teman?",
            "Apa saja tanda-tanda penyalahgunaan narkoba?",
            "Bagaimana cara membantu anggota keluarga?",
            "Informasi tentang rehabilitasi"
        ]
        
        cols = st.columns(len(quick_questions))
        for idx, col in enumerate(cols):
            with col:
                if st.button(f"❓", key=f"quick_{idx}", help=quick_questions[idx]):
                    user_input = quick_questions[idx]
                    send_button = True
        
        # Process Input
        if send_button and user_input:
            # Add user message
            st.session_state.messages.append({
                "role": "user",
                "content": user_input,
                "timestamp": datetime.now().isoformat()
            })
            
            # Get response from Knowledge Base
            response, topic, intent = kb.search_content(user_input)
            
            # Update analytics
            update_analytics(intent, topic)
            
            # Add bot response
            st.session_state.messages.append({
                "role": "assistant",
                "content": response,
                "intent": intent,
                "topic": topic,
                "timestamp": datetime.now().isoformat()
            })
            
            # Rerun to update chat
            st.rerun()
    
    with tab2:
        st.markdown("## 📚 Panduan Lengkap")
        
        st.markdown("""
            <div class="stats-card">
                <h3>🎯 Cara Menggunakan BANTU</h3>
                <ol>
                    <li><strong>Ketik pertanyaan Anda</strong> di kolom chat</li>
                    <li><strong>Pilih mode pengguna</strong> di sidebar (Remaja/Orang Tua/Pendidik)</li>
                    <li><strong>Gunakan pertanyaan cepat</strong> untuk akses informasi populer</li>
                    <li><strong>Lihat analitik</strong> untuk memahami topik yang sering ditanyakan</li>
                </ol>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Topik yang Tersedia
        st.markdown("### 📖 Topik yang Tersedia")
        
        topics_data = [
            {
                "icon": "⚠️",
                "title": "Bahaya Narkoba",
                "desc": "Dampak fisik, mental, dan sosial dari penyalahgunaan narkoba",
                "keywords": "bahaya, dampak, efek, akibat"
            },
            {
                "icon": "🔍",
                "title": "Jenis-Jenis Narkoba",
                "desc": "Kategori dan efek berbagai jenis narkoba",
                "keywords": "jenis, macam, tipe, golongan"
            },
            {
                "icon": "👁️",
                "title": "Tanda Penyalahgunaan",
                "desc": "Mengenali tanda-tanda fisik, perilaku, dan sosial",
                "keywords": "tanda, ciri, gejala, indikasi"
            },
            {
                "icon": "🛡️",
                "title": "Cara Menolak Ajakan",
                "desc": "Strategi komunikasi asertif dan teknik penolakan",
                "keywords": "menolak, nolak, ajakan, tekanan"
            },
            {
                "icon": "👨‍👩‍👧",
                "title": "Dukungan Keluarga",
                "desc": "Panduan membantu anggota keluarga yang terpapar",
                "keywords": "keluarga, orang tua, dukungan"
            },
            {
                "icon": "🏥",
                "title": "Rehabilitasi",
                "desc": "Informasi layanan rehabilitasi dan pemulihan",
                "keywords": "rehabilitasi, pemulihan, terapi"
            },
            {
                "icon": "⚖️",
                "title": "Aspek Hukum",
                "desc": "Informasi umum tentang hukum narkoba di Indonesia",
                "keywords": "hukum, undang-undang, sanksi"
            },
            {
                "icon": "❓",
                "title": "Mitos vs Fakta",
                "desc": "Membedah kesalahpahaman tentang narkoba",
                "keywords": "mitos, fakta, hoax"
            }
        ]
        
        for topic in topics_data:
            with st.expander(f"{topic['icon']} {topic['title']}"):
                st.markdown(f"**Deskripsi:** {topic['desc']}")
                st.markdown(f"**Kata kunci:** `{topic['keywords']}`")
                st.markdown(f"**Contoh pertanyaan:** *\"{topic['title']}\"*")
        
        st.markdown("---")
        
        # Safety Guidelines
        st.markdown("""
            <div class="warning-message">
                <h3>⚠️ Pedoman Keamanan</h3>
                <p><strong>Chatbot ini TIDAK akan memberikan informasi tentang:</strong></p>
                <ul>
                    <li>❌ Cara menggunakan atau mengonsumsi narkoba</li>
                    <li>❌ Dosis atau takaran</li>
                    <li>❌ Cara mendapatkan, membeli, atau membuat narkoba</li>
                    <li>❌ Cara menyembunyikan atau menghindari deteksi</li>
                    <li>❌ Cara lolos tes narkoba</li>
                </ul>
                <p><strong>Jika Anda menanyakan hal-hal di atas, sistem akan:</strong></p>
                <ol>
                    <li>✅ Menolak dengan tegas namun empatik</li>
                    <li>✅ Menjelaskan mengapa informasi tersebut tidak dapat diberikan</li>
                    <li>✅ Mengarahkan ke informasi edukatif yang relevan</li>
                    <li>✅ Memberikan kontak bantuan profesional</li>
                </ol>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # FAQ
        st.markdown("### ❓ FAQ (Frequently Asked Questions)")
        
        faqs = [
            {
                "q": "Apakah percakapan saya dengan chatbot ini rahasia?",
                "a": "Ya. Chatbot ini tidak menyimpan data pribadi Anda. Data yang dikumpulkan hanya berupa statistik anonim untuk peningkatan layanan."
            },
            {
                "q": "Apakah chatbot ini menggantikan konselor profesional?",
                "a": "Tidak. Chatbot ini adalah alat edukasi. Untuk masalah serius, selalu konsultasikan dengan profesional melalui Hotline BNN 184 atau fasilitas kesehatan terdekat."
            },
            {
                "q": "Bagaimana jika saya atau keluarga membutuhkan bantuan darurat?",
                "a": "Segera hubungi Hotline BNN 184 (24/7, gratis, rahasia) atau kunjungi Puskesmas/RS terdekat. Untuk kondisi mengancam jiwa, hubungi 119 atau 112."
            },
            {
                "q": "Apakah rehabilitasi narkoba ditanggung pemerintah?",
                "a": "Ya. Pemerintah menyediakan layanan rehabilitasi gratis melalui Puskesmas, RS Pemerintah, dan Loka Rehabilitasi BNN. Hubungi 184 untuk informasi lebih lanjut."
            },
            {
                "q": "Bagaimana jika saya takut dilaporkan ke polisi?",
                "a": "Indonesia menerapkan pendekatan rehabilitasi untuk pengguna. Jika Anda melapor secara sukarela untuk rehabilitasi, Anda berhak mendapat perlindungan. Hubungi 184 untuk konsultasi rahasia."
            }
        ]
        
        for faq in faqs:
            with st.expander(f"❓ {faq['q']}"):
                st.markdown(faq['a'])
    
    with tab3:
        st.markdown("## 📊 Analitik Penggunaan")
        
        if st.session_state.analytics["total_queries"] == 0:
            st.info("📭 Belum ada data analitik. Mulai bertanya untuk melihat statistik!")
        else:
            # Overview Metrics
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(
                    "Total Pertanyaan",
                    st.session_state.analytics["total_queries"]
                )
            
            with col2:
                forbidden_count = st.session_state.analytics["intent_distribution"]["forbidden"]
                st.metric(
                    "Pertanyaan Terlarang",
                    forbidden_count,
                    delta=f"{(forbidden_count/st.session_state.analytics['total_queries']*100):.1f}%" if st.session_state.analytics['total_queries'] > 0 else "0%"
                )
            
            with col3:
                topics_count = len(st.session_state.analytics["topics_accessed"])
                st.metric(
                    "Topik Diakses",
                    topics_count
                )
            
            st.markdown("---")
            
            # Intent Distribution Chart
            st.markdown("### 📈 Distribusi Intent Pertanyaan")
            
            intent_data = {
                k: v for k, v in st.session_state.analytics["intent_distribution"].items()
                if v > 0
            }
            
            if intent_data:
                # Create data for visualization
                intent_labels = {
                    "education": "📚 Edukasi",
                    "prevention": "🛡️ Pencegahan",
                    "support": "💚 Dukungan",
                    "signs": "🔍 Tanda-tanda",
                    "legal": "⚖️ Hukum",
                    "forbidden": "⚠️ Terlarang",
                    "general": "💬 Umum"
                }
                
                for intent, count in intent_data.items():
                    percentage = (count / st.session_state.analytics["total_queries"]) * 100
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.progress(percentage / 100)
                        st.caption(f"{intent_labels.get(intent, intent)}")
                    with col2:
                        st.metric("", f"{count} ({percentage:.1f}%)")
            
            st.markdown("---")
            
            # Top Topics
            st.markdown("### 🔥 Topik Paling Sering Diakses")
            
            if st.session_state.analytics["topics_accessed"]:
                sorted_topics = sorted(
                    st.session_state.analytics["topics_accessed"].items(),
                    key=lambda x: x[1],
                    reverse=True
                )
                
                topic_names = {
                    "bahaya_narkoba": "⚠️ Bahaya Narkoba",
                    "jenis_narkoba": "🔍 Jenis Narkoba",
                    "tanda_penyalahgunaan": "👁️ Tanda Penyalahgunaan",
                    "cara_menolak": "🛡️ Cara Menolak",
                    "dukungan_keluarga": "👨‍👩‍👧 Dukungan Keluarga",
                    "rehabilitasi": "🏥 Rehabilitasi",
                    "hukum": "⚖️ Hukum",
                    "mitos_fakta": "❓ Mitos vs Fakta"
                }
                
                for idx, (topic, count) in enumerate(sorted_topics[:5], 1):
                    st.markdown(f"""
                        <div class="stats-card">
                            <h4>{idx}. {topic_names.get(topic, topic.title())}</h4>
                            <p>Diakses: <strong>{count} kali</strong></p>
                        </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("Belum ada topik yang diakses.")
            
            st.markdown("---")
            
            # Safety Alert
            forbidden_count = st.session_state.analytics["intent_distribution"]["forbidden"]
            if forbidden_count > 0:
                st.markdown("""
                    <div class="warning-message">
                        <h3>⚠️ Peringatan Keamanan</h3>
                        <p>Sistem telah mendeteksi <strong>{}</strong> pertanyaan yang termasuk kategori terlarang.</p>
                        <p>Chatbot telah merespons dengan:</p>
                        <ul>
                            <li>✅ Penolakan yang jelas dan empatik</li>
                            <li>✅ Penjelasan tentang batasan sistem</li>
                            <li>✅ Pengalihan ke informasi edukatif</li>
                            <li>✅ Penyediaan kontak bantuan profesional</li>
                        </ul>
                        <p><em>Ini menunjukkan sistem safety bekerja dengan baik.</em></p>
                    </div>
                """.format(forbidden_count), unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Export Data
            st.markdown("### 💾 Ekspor Data")
            
            if st.button("📥 Unduh Laporan Analitik (JSON)", use_container_width=True):
                analytics_export = {
                    "generated_at": datetime.now().isoformat(),
                    "summary": st.session_state.analytics,
                    "session_info": {
                        "mode": st.session_state.mode,
                        "total_messages": len(st.session_state.messages)
                    }
                }
                
                json_str = json.dumps(analytics_export, indent=2, ensure_ascii=False)
                st.download_button(
                    label="💾 Download JSON",
                    data=json_str,
                    file_name=f"bantu_analytics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
    
    # Footer
    st.markdown("---")
    st.markdown("""
        <div style="text-align: center; color: #666; padding: 2rem 0;">
            <p><strong>🛡️ BANTU - Chatbot Edukasi Anti-Narkoba BNN</strong></p>
            <p style="font-size: 0.9rem;">
                Dikembangkan untuk Badan Narkotika Nasional Republik Indonesia<br>
                📞 Hotline BNN: 184 (24/7, Gratis, Rahasia)<br>
                🌐 Website: <a href="https://bnn.go.id" target="_blank">www.bnn.go.id</a>
            </p>
            <p style="font-size: 0.85rem; margin-top: 1rem; opacity: 0.8;">
                ⚠️ Disclaimer: Chatbot ini adalah alat edukasi dan tidak menggantikan konsultasi profesional.<br>
                Untuk masalah serius, segera hubungi profesional kesehatan atau Hotline BNN.
            </p>
            <p style="font-size: 0.8rem; margin-top: 1rem; opacity: 0.7;">
                © 2024 BNN RI. Hak cipta dilindungi undang-undang.
            </p>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()