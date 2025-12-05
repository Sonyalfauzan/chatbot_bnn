import streamlit as st
import json
from datetime import datetime
from typing import Dict, List, Tuple
import re
import logging
import google.generativeai as genai

# --- SETUP DASAR ---
st.set_page_config(
    page_title="BANTU - Chatbot Anti-Narkoba (Integrasi Gemini)",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Setup logging sederhana
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# --- CUSTOM CSS ---
def load_css():
    st.markdown("""
        <style>
        .main { background-color: #f8f9fa; }
        .stApp { max-width: 1200px; margin: 0 auto; }
        .chat-message { padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 1rem; display: flex; flex-direction: column; }
        .user-message { background-color: #e3f2fd; border-left: 4px solid #2196f3; }
        .bot-message { background-color: #ffffff; border-left: 4px solid #4caf50; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .warning-message { background-color: #fff3cd; border-left: 4px solid #ff9800; padding: 1rem; border-radius: 0.5rem; margin: 1rem 0; }
        .header-banner { background: linear-gradient(135deg, #1976d2 0%, #0d47a1 100%); color: white; padding: 2rem; border-radius: 0.5rem; margin-bottom: 2rem; text-align: center; }
        .stats-card { background: white; padding: 1.5rem; border-radius: 0.5rem; box-shadow: 0 2px 8px rgba(0,0,0,0.1); margin: 1rem 0; }
        .intent-badge { display: inline-block; padding: 0.25rem 0.75rem; border-radius: 1rem; font-size: 0.85rem; font-weight: 600; margin-top: 0.5rem; }
        .intent-education { background-color: #e3f2fd; color: #1976d2; }
        .intent-prevention { background-color: #f3e5f5; color: #7b1fa2; }
        .intent-support { background-color: #e8f5e9; color: #388e3c; }
        .intent-forbidden { background-color: #ffebee; color: #c62828; }
        </style>
    """, unsafe_allow_html=True)

# --- CLASS KNOWLEDGE BASE (Tetap seperti sebelumnya) ---
class KnowledgeBase:
    def __init__(self):
        self.content = {
            "bahaya_narkoba": {
                "title": "Bahaya Narkoba bagi Kesehatan",
                "content": {
                    "fisik": [
                        "Kerusakan organ vital (jantung, paru-paru, hati, ginjal)",
                        "Penurunan sistem kekebalan tubuh",
                        "Gangguan koordinasi dan keseimbangan",
                        "Risiko overdosis yang dapat berakibat fatal"
                    ],
                    "mental": [
                        "Gangguan kecemasan dan depresi",
                        "Perubahan perilaku dan kepribadian",
                        "Penurunan kemampuan kognitif dan memori",
                        "Risiko gangguan mental jangka panjang"
                    ],
                    "sosial": [
                        "Putusnya hubungan keluarga dan pertemanan",
                        "Kesulitan dalam pekerjaan dan pendidikan",
                        "Isolasi sosial dan stigma",
                        "Beban ekonomi untuk diri dan keluarga"
                    ]
                },
                "keywords": ["bahaya", "dampak", "kesehatan", "fisik", "mental", "efek", "sosial"]
            },
            "jenis_narkoba": {
                "title": "Pengenalan Jenis-Jenis Narkoba",
                "content": {
                    "depresan": "Menekan sistem saraf pusat, menyebabkan rasa tenang berlebihan, mengantuk, hingga tidak sadarkan diri.",
                    "stimulan": "Merangsang sistem saraf pusat, menyebabkan hiperaktif, euforia berlebihan, dan dapat merusak jantung.",
                    "halusinogen": "Mengubah persepsi, pikiran, dan perasaan, menyebabkan halusinasi dan kehilangan realitas.",
                    "general": "⚠️ Semua jenis narkoba berbahaya dan ilegal. Tidak ada yang \"aman\" untuk dikonsumsi."
                },
                "keywords": ["jenis", "macam", "kategori", "tipe", "golongan"]
            },
            "tanda_penyalahgunaan": {
                "title": "Tanda-Tanda Penyalahgunaan Narkoba",
                "content": {
                    "fisik": [
                        "Mata merah atau pupil melebar/menyempit abnormal",
                        "Perubahan berat badan drastis",
                        "Kebersihan diri menurun",
                        "Bekas suntikan atau luka yang tidak biasa"
                    ],
                    "perilaku": [
                        "Perubahan mood yang ekstrem",
                        "Menarik diri dari keluarga dan teman",
                        "Kehilangan minat pada aktivitas favorit",
                        "Sering berbohong atau menyembunyikan sesuatu"
                    ],
                    "sosial": [
                        "Berganti lingkungan pertemanan secara tiba-tiba",
                        "Masalah di sekolah atau tempat kerja",
                        "Kesulitan keuangan yang tidak dijelaskan",
                        "Sering meminta atau mencuri uang"
                    ]
                },
                "keywords": ["tanda", "ciri", "gejala", "mengenali", "indikasi", "penyalahgunaan"]
            },
            "cara_menolak": {
                "title": "Strategi Menolak Ajakan Narkoba",
                "content": {
                    "asertif": [
                        "Katakan \"TIDAK\" dengan tegas dan jelas (contoh: \"Tidak, terima kasih. Aku tidak tertarik.\")",
                        "Berikan alasan singkat dan jelas (contoh: \"Aku ingin menjaga kesehatanku.\")",
                        "Tawarkan alternatif positif (contoh: \"Yuk, main basket aja.\")",
                        "Tinggalkan situasi jika perlu."
                    ],
                    "tips": [
                        "Latih penolakan di depan cermin.",
                        "Cari teman yang mendukung keputusan positifmu.",
                        "Percaya diri dengan pilihanmu.",
                        "Ingat tujuan dan cita-citamu."
                    ]
                },
                "keywords": ["menolak", "nolak", "ajakan", "tekanan", "peer pressure", "teman"]
            },
            "dukungan_keluarga": {
                "title": "Cara Mendukung Anggota Keluarga",
                "content": {
                    "komunikasi": [
                        "Dengarkan tanpa menghakimi.",
                        "Ekspresikan kekhawatiran dengan penuh kasih sayang.",
                        "Hindari menyalahkan atau melabeli.",
                        "Tunjukkan bahwa Anda peduli dan siap membantu."
                    ],
                    "langkah_praktis": [
                        "Cari informasi tentang rehabilitasi dan konseling.",
                        "Konsultasikan dengan profesional kesehatan.",
                        "Dukung proses pemulihan dengan sabar.",
                        "Jaga kesehatan mental keluarga lainnya.",
                        "Bergabung dengan support group untuk keluarga."
                    ],
                    "dihindari": [
                        "Jangan menyangkal masalah.",
                        "Jangan menutup-nutupi perilaku berbahaya.",
                        "Jangan memberikan uang tanpa pengawasan.",
                        "Jangan menyerah pada proses pemulihan."
                    ],
                    "sumber_daya": [
                        "📞 Hotline BNN: 184",
                        "🏥 Puskesmas dan Rumah Sakit terdekat",
                        "👥 Komunitas pemulihan dan support group"
                    ]
                },
                "keywords": ["keluarga", "orang tua", "dukungan", "support", "membantu", "kerabat"]
            },
            "rehabilitasi": {
                "title": "Informasi Rehabilitasi dan Pemulihan",
                "content": {
                    "jenis_layanan": [
                        "Rehabilitasi rawat inap (intensive care)",
                        "Rehabilitasi rawat jalan (outpatient)",
                        "Program konseling dan terapi",
                        "Komunitas pemulihan (recovery community)"
                    ],
                    "tahapan": [
                        "Detoksifikasi - Membersihkan tubuh dari zat adiktif",
                        "Rehabilitasi - Terapi dan konseling intensif",
                        "Aftercare - Dukungan pasca rehabilitasi",
                        "Reintegrasi - Kembali ke masyarakat"
                    ],
                    "akses": [
                        "Hubungi hotline BNN: 184 (24/7)",
                        "Kunjungi Puskesmas atau RS terdekat",
                        "Datang langsung ke Loka Rehabilitasi BNN",
                        "Konsultasi online dengan konselor"
                    ],
                    "hak_pasien": [
                        "Mendapat perlakuan manusiawi dan bermartabat",
                        "Privasi dan kerahasiaan data pribadi",
                        "Akses ke layanan kesehatan yang layak",
                        "Dukungan reintegrasi sosial"
                    ]
                },
                "keywords": ["rehabilitasi", "pemulihan", "bantuan", "terapi", "konseling", "rawat"]
            },
            "hukum": {
                "title": "Aspek Hukum Narkoba di Indonesia",
                "content": {
                    "undang_undang": "UU No. 35 Tahun 2009 tentang Narkotika. Fokus pada pencegahan, rehabilitasi, dan penegakan hukum.",
                    "kategori_pidana": {
                        "Menggunakan": "dapat dikenai pidana atau rehabilitasi",
                        "Menyimpan/membawa": "hukuman penjara",
                        "Mengedarkan": "hukuman berat hingga hukuman mati",
                        "Memproduksi": "hukuman maksimal"
                    },
                    "pendekatan": "Indonesia menerapkan pendekatan rehabilitasi untuk pengguna, bukan hanya hukuman.",
                    "pelaporan_sukarela": "Melapor ke pihak berwenang secara sukarela dapat membantu Anda mendapat rehabilitasi, bukan hukuman."
                },
                "keywords": ["hukum", "undang-undang", "uu", "pidana", "sanksi", "legal"]
            },
            "mitos_fakta": {
                "title": "Mitos vs Fakta tentang Narkoba",
                "content": {
                    "mitos_1": {"mitos": "Coba sekali saja tidak apa-apa", "fakta": "Sekali coba bisa membuat kecanduan. Otak remaja sangat rentan terhadap adiksi."},
                    "mitos_2": {"mitos": "Narkoba bisa meningkatkan kreativitas", "fakta": "Narkoba merusak fungsi otak dan justru menurunkan kemampuan kognitif jangka panjang."},
                    "mitos_3": {"mitos": "Ganja itu natural, jadi aman", "fakta": "Natural tidak berarti aman. Ganja dapat menyebabkan gangguan mental dan adiksi."},
                    "mitos_4": {"mitos": "Saya bisa berhenti kapan saja", "fakta": "Adiksi mengubah kimia otak. Berhenti membutuhkan bantuan profesional."},
                    "mitos_5": {"mitos": "Hanya orang lemah yang kecanduan", "fakta": "Adiksi adalah penyakit medis yang bisa dialami siapa saja, bukan masalah karakter."},
                    "mitos_6": {"mitos": "Narkoba membuat masalah hilang", "fakta": "Narkoba hanya mengalihkan masalah sementara dan menciptakan masalah baru yang lebih besar."}
                },
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

    def classify_intent(self, query: str) -> str:
        query_lower = query.lower()
        for pattern in self.forbidden_patterns:
            if re.search(pattern, query_lower):
                return "forbidden"
        intent_patterns = {
            "education": [r"(bahaya|dampak|efek|akibat)", r"(jenis|macam|tipe|golongan)", r"(pengertian|definisi|apa itu)", r"(informasi|info|penjelasan)"],
            "prevention": [r"(menolak|nolak|hindari|cegah)", r"(ajakan|tawaran|tekanan)", r"(strategi|cara|tips)\s+(menolak|nolak)"],
            "support": [r"(bantuan|tolong|help)", r"(rehabilitasi|pemulihan|terapi)", r"(keluarga|orang tua|teman)", r"(dukungan|support|dukung)"],
            "signs": [r"(tanda|ciri|gejala)", r"(mengenali|kenali|deteksi)", r"(penyalahgunaan|pecandu)"],
            "legal": [r"(hukum|undang|sanksi|pidana)", r"(legal|ilegal)"]
        }
        intent_scores = {intent: 0 for intent in intent_patterns}
        for intent, patterns in intent_patterns.items():
            for pattern in patterns:
                if re.search(pattern, query_lower):
                    intent_scores[intent] += 1
        max_score = max(intent_scores.values())
        if max_score > 0:
            return max(intent_scores, key=intent_scores.get)
        return "general"

    def search_content(self, query: str) -> Tuple[Dict, str]:
        query_lower = query.lower()
        intent = self.classify_intent(query)
        if intent == "forbidden":
            return None, intent
        best_match = None
        best_score = 0
        for key, content in self.content.items():
            score = sum(1 for keyword in content["keywords"] if keyword in query_lower)
            if score > best_score:
                best_score = score
                best_match = key
        if best_match and best_score > 0:
            return self.content[best_match], best_match
        return None, "general"

# --- CLASS LLM INTEGRATION (Menggunakan Gemini) ---
class LLMInterface:
    """
    Kelas untuk berinteraksi dengan Google Gemini API.
    """
    def __init__(self, knowledge_base: KnowledgeBase, api_key: str):
        self.kb = knowledge_base
        genai.configure(api_key=api_key)
        # Pilih model Gemini (gemini-1.5-flash adalah pilihan gratis/ekonomis yang baik)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        logger.info("LLM Interface (Gemini) initialized.")

    def generate_response(self, query: str, mode: str, context_content: Dict) -> str:
        """
        Fungsi utama untuk menghasilkan respons dari Gemini.
        """
        intent = self.kb.classify_intent(query)
        if intent == "forbidden":
            return self._get_forbidden_response()

        # Format konteks dari KnowledgeBase
        formatted_context = self._format_context(context_content)
        if not formatted_context:
            # Jika tidak ada konteks spesifik, gunakan respons umum dari KB
            fallback_content, _ = self.kb.search_content(query)
            formatted_context = self._format_context(fallback_content) if fallback_content else "Saya adalah chatbot edukasi anti-narkoba. Tanyakan apa pun tentang bahaya, pencegahan, atau bantuan terkait narkoba."

        # Buat prompt untuk Gemini
        prompt = self._build_prompt(query, mode, formatted_context)

        try:
            # Generate content using the model
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=1000, # Sesuaikan jika perlu
                    temperature=0.7,        # Sesuaikan jika perlu
                )
            )
            # Extract the text from the response
            generated_text = response.text
            if not generated_text or generated_text.isspace():
                 logger.warning("Gemini returned an empty response. Falling back to default message.")
                 return "Maaf, saya tidak bisa menghasilkan jawaban yang relevan saat ini. Silakan coba tanyakan dalam cara yang berbeda."
            return generated_text.strip()

        except Exception as e:
            logger.error(f"Error calling Gemini API: {e}")
            # Return a safe fallback message
            return "Maaf, terjadi kesalahan saat menghubungi layanan AI. Silakan coba lagi nanti."

    def _build_prompt(self, query: str, mode: str, context: str) -> str:
        """
        Membangun prompt yang akan dikirim ke Gemini.
        Prompt ini memberi instruksi jelas tentang mode pengguna dan konteks.
        """
        prompt_template = f"""
        Kamu adalah BANTU, sebuah chatbot edukasi anti-narkoba milik BNN (Badan Narkotika Nasional) Republik Indonesia.
        Tugas kamu adalah memberikan informasi edukatif, pencegahan, dan dukungan terkait narkoba.
        Gaya bahasa dan fokus informasi kamu HARUS disesuaikan dengan 'Mode Pengguna' yang diberikan.
        Mode Pengguna: {mode}
        - Jika Mode Pengguna adalah 'Remaja', berikan informasi yang mudah dipahami, relevan dengan kehidupan sehari-hari remaja, dan berikan dorongan positif. Fokus pada pencegahan dan dampak jangka panjang.
        - Jika Mode Pengguna adalah 'Orang Tua', berikan informasi yang empatik, informatif, dan memberikan panduan praktis untuk mendukung anak. Fokus pada tanda-tanda dan langkah-langkah mendukung.
        - Jika Mode Pengguna adalah 'Pendidik', berikan informasi yang profesional, berbasis bukti, dan mendukung peran pendidik dalam pencegahan. Fokus pada strategi edukasi dan identifikasi dini.
        - Jika Mode Pengguna adalah 'Umum', berikan informasi netral dan informatif.
        Berikut adalah konteks informasi yang relevan dari Knowledge Base:
        <konteks>
        {context}
        </konteks>
        Pertanyaan dari pengguna:
        "{query}"
        Jawablah pertanyaan pengguna secara lengkap dan jelas, sesuai dengan Mode Pengguna dan konteks yang diberikan. Gunakan bahasa yang sopan dan empatik. Jika pertanyaan bersifat terlarang (seperti cara menggunakan, mendapatkan, atau menghindari deteksi narkoba), tolak dengan tegas dan arahkan ke informasi bantuan.
        """
        return prompt_template.strip()

    def _format_context(self, content_data):
        """Membantu memformat data konten dari KnowledgeBase menjadi string."""
        if not content_data:
            return ""
        if isinstance(content_data, dict):
            parts = []
            if "title" in content_data:
                parts.append(f"**{content_data['title']}**")
            if "content" in content_data:
                raw_content = content_data["content"]
                if isinstance(raw_content, dict):
                    for key, value in raw_content.items():
                        if isinstance(value, list):
                            parts.append(f"**{key.title()}:**\n" + "\n".join([f"- {item}" for item in value]))
                        else:
                            parts.append(f"**{key.title()}:** {value}")
                elif isinstance(raw_content, list):
                    parts.append("\n".join([f"- {item}" for item in raw_content]))
                else:
                    parts.append(str(raw_content))
            return "\n\n".join(parts)
        else:
            return str(content_data)

    def _get_forbidden_response(self):
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

# --- CLASS CHATBOT (Menggunakan LLM) ---
class Chatbot:
    def __init__(self, api_key: str):
        self.kb = KnowledgeBase()
        self.llm = LLMInterface(self.kb, api_key)

    def get_response(self, query: str, mode: str) -> Tuple[str, str, str]:
        logger.info(f"Menerima query: '{query}' untuk mode: {mode}")
        content, topic = self.kb.search_content(query)
        intent = self.kb.classify_intent(query)
        if intent == "forbidden":
            response = self.llm.generate_response(query, mode, content)
            logger.info(f"Memberikan respons FORBIDDEN untuk intent: {intent}")
            return response, "general", intent # Topic bisa general atau tetap forbidden

        response = self.llm.generate_response(query, mode, content)
        logger.info(f"Memberikan respons untuk intent: {intent}, topic: {topic}")
        return response, topic, intent

# --- FUNGSI UNTUK INTEGRASI API ---
@st.cache_resource
def get_chatbot(api_key: str):
    return Chatbot(api_key)

def get_response_for_api(query: str, mode: str = "Umum", api_key: str = None) -> str:
    if not api_key:
        # Jika api_key tidak disediakan, coba ambil dari secrets Streamlit
        api_key = st.secrets.get("GEMINI_API_KEY")
        if not api_key:
            logger.error("Gemini API key tidak ditemukan di parameter atau secrets.")
            return "Error: API key tidak tersedia."
    bot = get_chatbot(api_key)
    response, topic, intent = bot.get_response(query, mode)
    # Untuk integrasi API, kembalikan hanya teks respons
    return response

# --- STREAMLIT UI ---
def main():
    load_css()
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "mode" not in st.session_state:
        st.session_state.mode = "Remaja"

    # Ambil API key dari secrets Streamlit
    api_key = st.secrets.get("GEMINI_API_KEY")
    if not api_key:
        st.error("❌ **Error: Gemini API key tidak ditemukan!**\n\nSilakan atur `GEMINI_API_KEY` di `.streamlit/secrets.toml` atau pastikan API key valid.")
        st.stop() # Hentikan eksekusi jika tidak ada API key

    bot = get_chatbot(api_key)

    st.markdown("""
        <div class="header-banner">
            <h1>🛡️ BANTU - Chatbot Anti-Narkoba (Integrasi Gemini)</h1>
            <p style="font-size: 1.1rem; margin-top: 0.5rem;">Badan Narkotika Nasional (BNN) Republik Indonesia</p>
            <p style="font-size: 0.95rem; opacity: 0.9;">Chatbot Edukasi, Pencegahan, dan Dukungan (v4.0 - Gemini)</p>
        </div>
    """, unsafe_allow_html=True)

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

    tab1, tab2 = st.tabs(["💬 Chat", "📚 Panduan"])
    with tab1:
        chat_container = st.container()
        with chat_container:
            if len(st.session_state.messages) == 0:
                initial_greeting = {
                    "Remaja": "Hai Remaja! 😊 Aku BANTU. Aku di sini untuk bantu kamu belajar tentang bahaya narkoba dan cara menjaga diri dari bahaya itu. Apa yang ingin kamu tahu hari ini?",
                    "Orang Tua": "Selamat datang, Bapak/Ibu. 👨‍👩‍👧 Aku BANTU. Aku bisa bantu Anda memahami tanda-tanda penyalahgunaan narkoba pada anak dan cara mendukung mereka. Apa yang bisa aku bantu?",
                    "Pendidik": "Halo, Guru atau Pendidik. 👨‍🏫 Aku BANTU. Aku bisa bantu Anda dalam memberikan edukasi anti-narkoba kepada peserta didik. Apa yang ingin Anda bahas?",
                    "Umum": "Halo! 👋 Aku BANTU, chatbot edukasi anti-narkoba dari BNN. Aku siap memberikan informasi yang kamu butuhkan."
                }
                st.markdown(f"""
                    <div class="stats-card">
                        <h3>👋 Selamat Datang di BANTU!</h3>
                        <p>{initial_greeting.get(st.session_state.mode, initial_greeting['Umum'])}</p>
                        <p><strong>Silakan mulai dengan mengetik pertanyaan Anda di bawah!</strong></p>
                    </div>
                """, unsafe_allow_html=True)
            for message in st.session_state.messages:
                render_message(
                    message["role"],
                    message["content"],
                    message.get("intent")
                )

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

        if send_button and user_input:
            st.session_state.messages.append({
                "role": "user",
                "content": user_input,
                "timestamp": datetime.now().isoformat()
            })
            response, topic, intent = bot.get_response(user_input, st.session_state.mode)
            st.session_state.messages.append({
                "role": "assistant",
                "content": response,
                "intent": intent,
                "topic": topic,
                "timestamp": datetime.now().isoformat()
            })
            st.rerun()

    with tab2:
        st.markdown("## 📚 Panduan Lengkap")
        st.markdown("""
            <div class="stats-card">
                <h3>🎯 Cara Menggunakan BANTU (Versi Gemini)</h3>
                <p>Versi ini menggunakan Google Gemini API untuk menghasilkan respons yang lebih alami dan disesuaikan.</p>
                <ol>
                    <li><strong>Pastikan API key Gemini</strong> telah disimpan di <code>.streamlit/secrets.toml</code>.</li>
                    <li><strong>Pilih Mode Pengguna</strong> di sidebar (Remaja/Orang Tua/Pendidik/Umum).</li>
                    <li><strong>Ketik pertanyaan Anda</strong> di kolom chat.</li>
                    <li>Chatbot akan mengirim pertanyaan dan mode Anda ke Gemini, beserta konteks dari KnowledgeBase.</li>
                    <li>Gemini akan menghasilkan <strong>respons yang dinamis dan disesuaikan</strong> dengan mode Anda.</li>
                    <li>Gunakan <strong>pertanyaan cepat</strong> untuk akses informasi populer.</li>
                </ol>
            </div>
        """, unsafe_allow_html=True)
        st.markdown("---")
        st.markdown("### 🔌 Integrasi ke Platform Lain (WA/Tele)")
        st.markdown("""
            <div class="stats-card">
                <p>Kode ini siap untuk integrasi ke platform eksternal.</p>
                <p>Inti logika chatbot ada di fungsi <code>get_response_for_api(query, mode, api_key)</code>.</p>
                <p>Untuk integrasi, buat API server (misalnya dengan FastAPI atau Flask) yang:</p>
                <ol>
                    <li>Menerima pesan dari platform (WA/Telegram).</li>
                    <li>Menentukan <code>mode</code> pengguna (misalnya dari database profil atau perintah).</li>
                    <li>Memanggil <code>get_response_for_api(pesan, mode, api_key)</code> dengan API key yang valid.</li>
                    <li>Mengirimkan balik hasilnya ke pengguna.</li>
                </ol>
                <p>API key Gemini harus tersedia di server tempat API dijalankan.</p>
            </div>
        """, unsafe_allow_html=True)

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

if __name__ == "__main__":
    main()
