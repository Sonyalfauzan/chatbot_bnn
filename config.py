"""
Konfigurasi aplikasi BANTU Chatbot
"""

# Informasi Aplikasi
APP_NAME = "BANTU - Chatbot Edukasi Anti-Narkoba BNN"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "Chatbot Edukasi, Pencegahan, dan Dukungan Anti-Narkoba"

# Kontak BNN
HOTLINE_NUMBER = "184"
SMS_WHATSAPP = "081-221-675-675"
EMAIL = "halo@bnn.go.id"
WEBSITE = "https://bnn.go.id"

# Mode Pengguna
USER_MODES = [
    "Remaja",
    "Orang Tua",
    "Pendidik",
    "Umum"
]

# Intent Categories
INTENT_CATEGORIES = {
    "education": {
        "label": "📚 Edukasi",
        "color": "#1976d2",
        "description": "Informasi tentang bahaya dan jenis narkoba"
    },
    "prevention": {
        "label": "🛡️ Pencegahan",
        "color": "#7b1fa2",
        "description": "Strategi menolak dan mencegah penyalahgunaan"
    },
    "support": {
        "label": "💚 Dukungan",
        "color": "#388e3c",
        "description": "Informasi bantuan dan rehabilitasi"
    },
    "signs": {
        "label": "🔍 Tanda-tanda",
        "color": "#f57c00",
        "description": "Mengenali tanda penyalahgunaan"
    },
    "legal": {
        "label": "⚖️ Hukum",
        "color": "#0288d1",
        "description": "Aspek hukum narkoba"
    },
    "forbidden": {
        "label": "⚠️ Terlarang",
        "color": "#c62828",
        "description": "Pertanyaan yang tidak dapat dijawab"
    },
    "general": {
        "label": "💬 Umum",
        "color": "#616161",
        "description": "Pertanyaan umum"
    }
}

# Quick Questions
QUICK_QUESTIONS = [
    "Apa bahaya narkoba bagi kesehatan?",
    "Bagaimana cara menolak ajakan teman?",
    "Apa saja tanda-tanda penyalahgunaan narkoba?",
    "Bagaimana cara membantu anggota keluarga?",
    "Informasi tentang rehabilitasi"
]

# Analytics Settings
ENABLE_ANALYTICS = True
ANALYTICS_RETENTION_DAYS = 30

# Safety Settings
ENABLE_FORBIDDEN_DETECTION = True
LOG_FORBIDDEN_QUERIES = True

# UI Settings
THEME = "light"
MAX_MESSAGE_HISTORY = 100
