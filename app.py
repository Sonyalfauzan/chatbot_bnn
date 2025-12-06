import streamlit as st
import json
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import re
import hashlib
import time

# Konfigurasi halaman
st.set_page_config(
    page_title="BANTU - AI Chatbot Edukasi Anti-Narkoba BNN",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Import modules
from ai_engine import AIEngine
from knowledge_base import EnhancedKnowledgeBase
from safety_filter import SafetyFilter
from user_profiles import UserProfileManager
from analytics_engine import AnalyticsEngine

# Custom CSS
def load_css():
    st.markdown("""
        <style>
        /* Base Styles */
        .main {
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        }
        .stApp {
            max-width: 1400px;
            margin: 0 auto;
        }
        
        /* Chat Messages */
        .chat-message {
            padding: 1.5rem;
            border-radius: 1rem;
            margin-bottom: 1rem;
            display: flex;
            flex-direction: column;
            animation: slideIn 0.3s ease-out;
        }
        
        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translateY(10px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .user-message {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            margin-left: 20%;
            box-shadow: 0 4px 6px rgba(102, 126, 234, 0.3);
        }
        
        .bot-message {
            background: white;
            margin-right: 20%;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            border-left: 4px solid #4caf50;
        }
        
        .thinking-indicator {
            display: inline-block;
            padding: 0.5rem 1rem;
            background: #f0f0f0;
            border-radius: 1rem;
            margin: 0.5rem 0;
            font-style: italic;
            color: #666;
        }
        
        .thinking-dots::after {
            content: '.';
            animation: dots 1.5s steps(4, end) infinite;
        }
        
        @keyframes dots {
            0%, 20% { content: '.'; }
            40% { content: '..'; }
            60%, 100% { content: '...'; }
        }
        
        /* Warning and Info Boxes */
        .warning-message {
            background: linear-gradient(135deg, #fff3cd 0%, #ffe8a1 100%);
            border-left: 4px solid #ff9800;
            padding: 1.5rem;
            border-radius: 0.5rem;
            margin: 1rem 0;
            box-shadow: 0 2px 8px rgba(255, 152, 0, 0.2);
        }
        
        .emergency-alert {
            background: linear-gradient(135deg, #ffebee 0%, #ffcdd2 100%);
            border-left: 4px solid #f44336;
            padding: 1.5rem;
            border-radius: 0.5rem;
            margin: 1rem 0;
            animation: pulse 2s infinite;
        }
        
        @keyframes pulse {
            0%, 100% { box-shadow: 0 2px 8px rgba(244, 67, 54, 0.2); }
            50% { box-shadow: 0 2px 16px rgba(244, 67, 54, 0.4); }
        }
        
        /* Header */
        .header-banner {
            background: linear-gradient(135deg, #1976d2 0%, #0d47a1 100%);
            color: white;
            padding: 2.5rem;
            border-radius: 1rem;
            margin-bottom: 2rem;
            text-align: center;
            box-shadow: 0 4px 20px rgba(25, 118, 210, 0.3);
        }
        
        /* Stats Cards */
        .stats-card {
            background: white;
            padding: 1.5rem;
            border-radius: 1rem;
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
            margin: 1rem 0;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        
        .stats-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 6px 20px rgba(0,0,0,0.12);
        }
        
        /* Intent Badges */
        .intent-badge {
            display: inline-block;
            padding: 0.4rem 1rem;
            border-radius: 2rem;
            font-size: 0.85rem;
            font-weight: 600;
            margin-top: 0.5rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        .intent-education { background: #e3f2fd; color: #1976d2; }
        .intent-prevention { background: #f3e5f5; color: #7b1fa2; }
        .intent-support { background: #e8f5e9; color: #388e3c; }
        .intent-forbidden { background: #ffebee; color: #c62828; }
        .intent-personal { background: #fff3e0; color: #f57c00; }
        
        /* Mode Indicator */
        .mode-indicator {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 0.5rem 1.5rem;
            border-radius: 2rem;
            display: inline-block;
            margin: 0.5rem 0;
            font-weight: 600;
            box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
        }
        
        /* Quick Actions */
        .quick-action-btn {
            background: white;
            border: 2px solid #1976d2;
            color: #1976d2;
            padding: 0.75rem 1.5rem;
            border-radius: 2rem;
            margin: 0.5rem;
            cursor: pointer;
            transition: all 0.3s ease;
            font-weight: 600;
        }
        
        .quick-action-btn:hover {
            background: #1976d2;
            color: white;
            transform: scale(1.05);
        }
        
        /* Context Indicator */
        .context-info {
            background: #f5f5f5;
            padding: 0.75rem;
            border-radius: 0.5rem;
            margin: 0.5rem 0;
            font-size: 0.9rem;
            border-left: 3px solid #2196f3;
        }
        
        /* AI Status Indicator */
        .ai-status {
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.5rem 1rem;
            background: #e8f5e9;
            border-radius: 2rem;
            font-size: 0.85rem;
            font-weight: 600;
            color: #2e7d32;
        }
        
        .ai-status-dot {
            width: 8px;
            height: 8px;
            background: #4caf50;
            border-radius: 50%;
            animation: blink 2s infinite;
        }
        
        @keyframes blink {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.3; }
        }
        
        /* Source Attribution */
        .source-attribution {
            font-size: 0.85rem;
            color: #666;
            margin-top: 1rem;
            padding-top: 1rem;
            border-top: 1px solid #e0e0e0;
        }
        
        /* Typing Effect */
        .typing-effect {
            overflow: hidden;
            white-space: nowrap;
            animation: typing 2s steps(40, end);
        }
        
        @keyframes typing {
            from { width: 0; }
            to { width: 100%; }
        }
        </style>
    """, unsafe_allow_html=True)

# Initialize Session State
def init_session_state():
    """Initialize all session state variables"""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "conversation_context" not in st.session_state:
        st.session_state.conversation_context = []
    
    if "mode" not in st.session_state:
        st.session_state.mode = "Remaja"
    
    if "user_profile" not in st.session_state:
        st.session_state.user_profile = {
            "interaction_count": 0,
            "topics_interested": [],
            "risk_level": "low",
            "needs_escalation": False
        }
    
    if "ai_enabled" not in st.session_state:
        st.session_state.ai_enabled = True
    
    if "analytics" not in st.session_state:
        st.session_state.analytics = {
            "total_queries": 0,
            "ai_responses": 0,
            "template_responses": 0,
            "safety_blocks": 0,
            "intent_distribution": {},
            "topics_accessed": {},
            "mode_usage": {},
            "avg_response_time": [],
            "user_satisfaction": []
        }

# Initialize Components
@st.cache_resource
def get_components():
    """Initialize all major components"""
    return {
        "kb": EnhancedKnowledgeBase(),
        "ai": AIEngine(),
        "safety": SafetyFilter(),
        "profile": UserProfileManager(),
        "analytics": AnalyticsEngine()
    }

def render_message(role: str, content: str, metadata: dict = None):
    """Render chat message with enhanced styling"""
    if role == "user":
        st.markdown(f"""
            <div class="chat-message user-message">
                <strong>🙋 Anda</strong>
                <p style="margin-top: 0.5rem;">{content}</p>
            </div>
        """, unsafe_allow_html=True)
    else:
        intent_info = ""
        if metadata and "intent" in metadata:
            intent = metadata["intent"]
            intent_labels = {
                "education": "📚 Edukasi",
                "prevention": "🛡️ Pencegahan",
                "support": "💚 Dukungan",
                "signs": "🔍 Tanda-tanda",
                "legal": "⚖️ Hukum",
                "forbidden": "⚠️ Terlarang",
                "personal": "👤 Personal",
                "general": "💬 Umum"
            }
            intent_class = f"intent-{intent}"
            intent_label = intent_labels.get(intent, "💬 Umum")
            intent_info = f'<span class="intent-badge {intent_class}">{intent_label}</span>'
        
        ai_indicator = ""
        if metadata and metadata.get("ai_generated"):
            ai_indicator = '<div class="ai-status"><span class="ai-status-dot"></span>AI-Generated Response</div>'
        
        mode_info = ""
        if metadata and "mode" in metadata:
            mode_info = f'<span class="mode-indicator">Mode: {metadata["mode"]}</span>'
        
        context_info = ""
        if metadata and metadata.get("has_context"):
            context_info = '<div class="context-info">💡 Respons ini mempertimbangkan konteks percakapan sebelumnya</div>'
        
        source_info = ""
        if metadata and "sources" in metadata and metadata["sources"]:
            sources = ", ".join(metadata["sources"])
            source_info = f'<div class="source-attribution">📖 Sumber: {sources}</div>'
        
        st.markdown(f"""
            <div class="chat-message bot-message">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                    <strong>🤖 BANTU</strong>
                    {ai_indicator}
                </div>
                {intent_info} {mode_info}
                {context_info}
                <div style="margin-top: 1rem;">{content}</div>
                {source_info}
            </div>
        """, unsafe_allow_html=True)

def process_user_input(user_input: str, components: dict) -> Tuple[str, dict]:
    """Process user input and generate response"""
    start_time = time.time()
    
    # Extract components
    kb = components["kb"]
    ai = components["ai"]
    safety = components["safety"]
    profile = components["profile"]
    analytics = components["analytics"]
    
    # Update user profile
    profile.update_interaction(user_input, st.session_state.mode)
    
    # Safety check on input
    is_safe, safety_issues = safety.check_input(user_input)
    
    if not is_safe:
        st.session_state.analytics["safety_blocks"] += 1
        response = kb.get_refusal_response(safety_issues)
        metadata = {
            "intent": "forbidden",
            "ai_generated": False,
            "mode": st.session_state.mode,
            "safety_blocked": True,
            "sources": ["Safety Filter"]
        }
        return response, metadata
    
    # Classify intent
    intent = kb.classify_intent(user_input)
    
    # Build conversation context
    context = build_conversation_context(
        st.session_state.messages,
        st.session_state.mode,
        intent
    )
    
    # Try AI generation if enabled
    if st.session_state.ai_enabled:
        try:
            # Generate AI response
            ai_response = ai.generate_response(
                user_input=user_input,
                intent=intent,
                mode=st.session_state.mode,
                context=context,
                user_profile=st.session_state.user_profile
            )
            
            # Safety check on output
            is_safe_output, output_issues = safety.check_output(ai_response)
            
            if is_safe_output:
                st.session_state.analytics["ai_responses"] += 1
                
                # Get relevant knowledge base content for sources
                kb_content = kb.get_relevant_content(user_input, intent)
                
                metadata = {
                    "intent": intent,
                    "ai_generated": True,
                    "mode": st.session_state.mode,
                    "has_context": len(context) > 0,
                    "sources": kb_content.get("sources", []),
                    "response_time": time.time() - start_time
                }
                
                return ai_response, metadata
            else:
                # Fallback to template if AI output is unsafe
                st.warning("⚠️ AI response tidak lolos safety check, menggunakan template")
                st.session_state.analytics["safety_blocks"] += 1
        
        except Exception as e:
            st.error(f"❌ Error dalam AI generation: {str(e)}")
    
    # Fallback to template-based response
    st.session_state.analytics["template_responses"] += 1
    template_response, topic = kb.get_template_response(user_input, intent, st.session_state.mode)
    
    metadata = {
        "intent": intent,
        "ai_generated": False,
        "mode": st.session_state.mode,
        "has_context": False,
        "sources": [topic] if topic else [],
        "response_time": time.time() - start_time
    }
    
    return template_response, metadata

def build_conversation_context(messages: List[dict], mode: str, current_intent: str) -> List[dict]:
    """Build conversation context from recent messages"""
    # Get last 5 messages for context
    recent_messages = messages[-10:] if len(messages) > 10 else messages
    
    context = []
    for msg in recent_messages:
        context.append({
            "role": msg["role"],
            "content": msg["content"][:500],  # Limit length
            "intent": msg.get("metadata", {}).get("intent", "general")
        })
    
    return context

def main():
    """Main application"""
    load_css()
    init_session_state()
    components = get_components()
    
    # Header
    st.markdown("""
        <div class="header-banner">
            <h1>🛡️ BANTU - AI Chatbot Edukasi Anti-Narkoba</h1>
            <p style="font-size: 1.2rem; margin-top: 0.5rem;">
                Powered by Advanced AI • Badan Narkotika Nasional RI
            </p>
            <p style="font-size: 0.95rem; opacity: 0.9;">
                Chatbot Cerdas untuk Edukasi, Pencegahan, dan Dukungan
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("### ⚙️ Pengaturan")
        
        # Mode Selection
        mode_options = {
            "Remaja": "👨‍🎓 Remaja (13-21 tahun)",
            "Orang Tua": "👨‍👩‍👧 Orang Tua",
            "Pendidik": "👨‍🏫 Pendidik/Guru",
            "Umum": "👥 Umum"
        }
        
        mode = st.selectbox(
            "Pilih Mode Pengguna",
            list(mode_options.keys()),
            format_func=lambda x: mode_options[x],
            index=list(mode_options.keys()).index(st.session_state.mode)
        )
        
        if mode != st.session_state.mode:
            st.session_state.mode = mode
            st.rerun()
        
        # Mode Description
        mode_descriptions = {
            "Remaja": "Bahasa santai, relatable, dengan contoh kehidupan sehari-hari remaja",
            "Orang Tua": "Fokus pada parenting, komunikasi dengan anak, dan dukungan keluarga",
            "Pendidik": "Strategi mengajar, materi edukasi, dan pendekatan pedagogis",
            "Umum": "Informasi balanced dan komprehensif untuk semua kalangan"
        }
        
        st.info(f"ℹ️ {mode_descriptions[mode]}")
        
        st.markdown("---")
        
        # AI Toggle
        ai_enabled = st.toggle(
            "🤖 Aktifkan AI Enhanced Response",
            value=st.session_state.ai_enabled,
            help="Gunakan AI untuk response yang lebih natural dan context-aware"
        )
        st.session_state.ai_enabled = ai_enabled
        
        if ai_enabled:
            st.success("✅ AI Mode: Active")
        else:
            st.warning("⚠️ AI Mode: Disabled (menggunakan template)")
        
        st.markdown("---")
        
        # Statistics
        st.markdown("### 📊 Statistik Sesi")
        st.metric("Total Pertanyaan", st.session_state.analytics["total_queries"])
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("AI Response", st.session_state.analytics["ai_responses"])
        with col2:
            st.metric("Template", st.session_state.analytics["template_responses"])
        
        if st.session_state.analytics["safety_blocks"] > 0:
            st.metric("Safety Blocks", st.session_state.analytics["safety_blocks"], delta="⚠️")
        
        st.markdown("---")
        
        # Emergency Contact
        st.markdown("### 📞 Kontak Darurat")
        st.markdown("""
            <div class="emergency-alert">
                <h4 style="margin-top:0;">🚨 Butuh Bantuan Segera?</h4>
                <p><strong>Hotline BNN:</strong><br>📱 184 (24/7, Gratis)</p>
                <p><strong>WhatsApp:</strong><br>💬 081-221-675-675</p>
                <p><strong>Darurat Medis:</strong><br>🏥 119 atau 112</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Actions
        if st.button("🗑️ Hapus Riwayat", use_container_width=True):
            st.session_state.messages = []
            st.session_state.conversation_context = []
            st.rerun()
        
        if st.button("📊 Reset Statistik", use_container_width=True):
            init_session_state()  # Reset analytics
            st.rerun()
        
        if st.button("💾 Ekspor Percakapan", use_container_width=True):
            export_data = {
                "exported_at": datetime.now().isoformat(),
                "mode": st.session_state.mode,
                "messages": st.session_state.messages,
                "analytics": st.session_state.analytics
            }
            st.download_button(
                "⬇️ Download JSON",
                data=json.dumps(export_data, indent=2, ensure_ascii=False),
                file_name=f"bantu_chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
    
    # Main Content Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["💬 Chat", "📚 Panduan", "📊 Analitik", "⚙️ Advanced"])
    
    with tab1:
        # Welcome Message
        if len(st.session_state.messages) == 0:
            welcome_messages = {
                "Remaja": """
                    <div class="stats-card">
                        <h2>👋 Halo! Aku BANTU</h2>
                        <p>Aku di sini untuk ngobrol sama kamu tentang narkoba dan gimana cara menghindarinya. 
                        Jangan khawatir, semua yang kita obrolin aman dan rahasia kok!</p>
                        <h3>🎯 Aku bisa bantu kamu dengan:</h3>
                        <ul>
                            <li>📚 Jelasin bahaya narkoba dengan bahasa yang gampang dimengerti</li>
                            <li>🛡️ Kasih tips gimana cara nolak ajakan teman</li>
                            <li>💪 Cara tetap keren tanpa narkoba</li>
                            <li>💚 Bantu kamu atau temen yang butuh support</li>
                        </ul>
                        <p><strong>Yuk, tanya apa aja yang pengen kamu tau!</strong></p>
                    </div>
                """,
                "Orang Tua": """
                    <div class="stats-card">
                        <h2>👋 Selamat Datang, Bapak/Ibu</h2>
                        <p>Saya BANTU, asisten AI yang dirancang untuk membantu orang tua dalam 
                        melindungi anak-anak dari bahaya narkoba.</p>
                        <h3>🎯 Saya dapat membantu Anda dengan:</h3>
                        <ul>
                            <li>👨‍👩‍👧 Strategi komunikasi efektif dengan anak</li>
                            <li>🔍 Mengenali tanda-tanda awal penyalahgunaan</li>
                            <li>💚 Cara memberikan dukungan tanpa menghakimi</li>
                            <li>📞 Informasi layanan profesional dan rehabilitasi</li>
                        </ul>
                        <p><strong>Silakan ajukan pertanyaan Anda</strong></p>
                    </div>
                """,
                "Pendidik": """
                    <div class="stats-card">
                        <h2>👋 Selamat Datang, Bapak/Ibu Guru</h2>
                        <p>Saya BANTU, resource AI untuk pendidik dalam program pencegahan narkoba.</p>
                        <h3>🎯 Saya dapat mendukung Anda dengan:</h3>
                        <ul>
                            <li>📖 Materi edukasi untuk berbagai tingkat pendidikan</li>
                            <li>🎓 Metode pengajaran interaktif dan efektif</li>
                            <li>👥 Strategi mendeteksi dan merespons kasus di sekolah</li>
                            <li>📋 Resource dan panduan program pencegahan</li>
                        </ul>
                        <p><strong>Mari kita diskusikan kebutuhan edukasi Anda</strong></p>
                    </div>
                """,
                "Umum": """
                    <div class="stats-card">
                        <h2>👋 Selamat Datang di BANTU</h2>
                        <p>Chatbot AI edukasi dan pencegahan narkoba dari BNN RI.</p>
                        <h3>🎯 Layanan Kami:</h3>
                        <ul>
                            <li>📚 Informasi komprehensif tentang narkoba</li>
                            <li>🛡️ Strategi pencegahan yang efektif</li>
                            <li>💚 Panduan dukungan dan rehabilitasi</li>
                            <li>⚖️ Informasi aspek hukum</li>
                        </ul>
                        <p><strong>Silakan ajukan pertanyaan Anda</strong></p>
                    </div>
                """
            }
            
            st.markdown(welcome_messages.get(st.session_state.mode, welcome_messages["Umum"]), 
                       unsafe_allow_html=True)
        
        # Display Messages
        for message in st.session_state.messages:
            render_message(
                message["role"],
                message["content"],
                message.get("metadata")
            )
        
        # Quick Questions based on mode
        st.markdown("---")
        st.markdown("#### ⚡ Pertanyaan Cepat")
        
        quick_questions_by_mode = {
            "Remaja": [
                "Gimana cara nolak ajakan temen?",
                "Apa sih bahayanya coba-coba?",
                "Narkoba itu apa aja sih?",
                "Kalau temen gue kecanduan gimana?"
            ],
            "Orang Tua": [
                "Bagaimana cara bicara dengan anak tentang narkoba?",
                "Apa tanda-tanda anak menggunakan narkoba?",
                "Bagaimana jika menemukan narkoba di kamar anak?",
                "Cara mendukung anak dalam rehabilitasi?"
            ],
            "Pendidik": [
                "Metode mengajar pencegahan narkoba untuk remaja?",
                "Bagaimana mendeteksi siswa yang berisiko?",
                "Program pencegahan efektif di sekolah?",
                "Cara menangani kasus di lingkungan sekolah?"
            ],
            "Umum": [
                "Apa bahaya narkoba?",
                "Bagaimana cara menolak ajakan?",
                "Tanda-tanda penyalahgunaan?",
                "Informasi rehabilitasi?"
            ]
        }
        
        questions = quick_questions_by_mode.get(st.session_state.mode, quick_questions_by_mode["Umum"])
        cols = st.columns(len(questions))
        
        for idx, col in enumerate(cols):
            with col:
                if st.button(questions[idx], key=f"quick_{idx}", use_container_width=True):
                    user_input = questions[idx]
                    process_and_display_response(user_input, components)
        
        # Input Area
        st.markdown("---")
        
        user_input = st.chat_input(
            placeholder=f"Ketik pertanyaan Anda di sini... (Mode: {st.session_state.mode})",
            key="chat_input"
        )
        
        if user_input:
            process_and_display_response(user_input, components) 
        with tab2:
    render_guide_tab(components)

with tab3:
    render_analytics_tab()

with tab4:
    render_advanced_tab(components)

# Footer
st.markdown("---")
st.markdown("""
    <div style="text-align: center; color: #666; padding: 2rem 0;">
        <p><strong>🛡️ BANTU - AI Chatbot Edukasi Anti-Narkoba BNN</strong></p>
        <p style="font-size: 0.9rem;">
            Powered by Advanced AI Technology • BNN Republik Indonesia<br>
            📞 Hotline BNN: 184 (24/7, Gratis, Rahasia)<br>
            🌐 Website: <a href="https://bnn.go.id" target="_blank">www.bnn.go.id</a>
        </p>
        <p style="font-size: 0.85rem; margin-top: 1rem; opacity: 0.8;">
            ⚠️ Disclaimer: Chatbot ini menggunakan AI untuk memberikan response yang lebih baik.<br>
            Untuk masalah serius, segera hubungi profesional kesehatan atau Hotline BNN.
        </p>
        <p style="font-size: 0.8rem; margin-top: 1rem; opacity: 0.7;">
            © 2024 BNN RI. Hak cipta dilindungi undang-undang.
        </p>
    </div>
""", unsafe_allow_html=True)
def process_and_display_response(user_input: str, components: dict):
"""Process input and display response with thinking indicator"""
# Add user message
st.session_state.messages.append({
"role": "user",
"content": user_input,
"timestamp": datetime.now().isoformat()
})
# Update analytics
st.session_state.analytics["total_queries"] += 1

# Show thinking indicator
with st.spinner("🤔 BANTU sedang berpikir..."):
    response, metadata = process_user_input(user_input, components)

# Add bot response
st.session_state.messages.append({
    "role": "assistant",
    "content": response,
    "metadata": metadata,
    "timestamp": datetime.now().isoformat()
})

# Update analytics
if "response_time" in metadata:
    st.session_state.analytics["avg_response_time"].append(metadata["response_time"])

# Rerun to show new messages
st.rerun()
def render_guide_tab(components: dict):
"""Render guide tab with comprehensive information"""
st.markdown("## 📚 Panduan Lengkap BANTU AI")
# ... (Panduan lengkap seperti kode asli, ditambah informasi tentang AI)

st.markdown("""
    <div class="stats-card">
        <h3>🤖 Tentang AI di BANTU</h3>
        <p>BANTU menggunakan teknologi AI (Claude) untuk memberikan respons yang:</p>
        <ul>
            <li>✅ Lebih natural dan conversational</li>
            <li>✅ Context-aware (memahami percakapan sebelumnya)</li>
            <li>✅ Dipersonalisasi sesuai mode pengguna</li>
            <li>✅ Bervariasi dan tidak template</li>
        </ul>
        <h4>🛡️ Keamanan AI:</h4>
        <ul>
            <li>🔒 Multi-layer safety filtering</li>
            <li>🔍 Content moderation sebelum dan sesudah AI generate</li>
            <li>⚠️ Automatic fallback ke template jika output tidak aman</li>
            <li>📋 Semua respons tetap berdasarkan knowledge base BNN</li>
        </ul>
    </div>
""", unsafe_allow_html=True)
def render_analytics_tab():
"""Render analytics tab with detailed statistics"""
st.markdown("## 📊 Analitik Komprehensif")
if st.session_state.analytics["total_queries"] == 0:
    st.info("📭 Belum ada data analitik. Mulai bertanya untuk melihat statistik!")
    return

# Performance Metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Queries", st.session_state.analytics["total_queries"])

with col2:
    ai_pct = (st.session_state.analytics["ai_responses"] / 
             st.session_state.analytics["total_queries"] * 100)
    st.metric("AI Response", f"{ai_pct:.1f}%")

with col3:
    if st.session_state.analytics["avg_response_time"]:
        avg_time = sum(st.session_state.analytics["avg_response_time"]) / len(st.session_state.analytics["avg_response_time"])
        st.metric("Avg Response Time", f"{avg_time:.2f}s")
    else:
        st.metric("Avg Response Time", "N/A")

with col4:
    st.metric("Safety Blocks", st.session_state.analytics["safety_blocks"])
def render_advanced_tab(components: dict):
"""Render advanced settings tab"""
st.markdown("## ⚙️ Advanced Settings & Tools")
st.markdown("""
    <div class="stats-card">
        <h3>🔧 Developer Tools</h3>
        <p>Advanced settings untuk testing dan debugging</p>
    </div>
""", unsafe_allow_html=True)

# Export options
st.markdown("### 💾 Export Options")

col1, col2 = st.columns(2)

with col1:
    if st.button("📥 Export Full Analytics", use_container_width=True):
        data = {
            "exported_at": datetime.now().isoformat(),
            "analytics": st.session_state.analytics,
            "user_profile": st.session_state.user_profile,
            "mode": st.session_state.mode
        }
        st.download_button(
            "⬇️ Download",
            json.dumps(data, indent=2, ensure_ascii=False),
            f"analytics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            "application/json"
        )

with col2:
    if st.button("📥 Export Conversation", use_container_width=True):
        data = {
            "exported_at": datetime.now().isoformat(),
            "mode": st.session_state.mode,
            "messages": st.session_state.messages
        }
        st.download_button(
            "⬇️ Download",
            json.dumps(data, indent=2, ensure_ascii=False),
            f"conversation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            "application/json"
        )
if name == "main":
main()
