# app_ai.py
# Aplikasi Chatbot PT Intervisual dengan Groq AI

import streamlit as st
import os
from dotenv import load_dotenv
from chatbot_engine_ai import ChatbotIntervisualAI
from data_perusahaan import COMPANY_INFO

# Load environment variables
load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("GROQ_API_KEY belum diset di environment")


# Konfigurasi halaman
st.set_page_config(
    page_title="Chatbot AI PT Intervisual",
    page_icon="🏗️",
    layout="centered"
)

# Custom CSS (sama seperti sebelumnya tapi lebih modern)
st.markdown("""
<style>
    /* Font Modern */
    * {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    
    /* Background Gradient */
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* Header Modern */
    .header-modern {
        text-align: center;
        padding: 1.5rem 0;
        margin-bottom: 1rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        color: white;
    }
    
    .header-modern h1 {
        color: white;
        font-size: 2rem;
        font-weight: 700;
        margin: 0;
    }
    
    .header-modern p {
        color: #f0f0f0;
        font-size: 0.95rem;
        margin-top: 0.5rem;
    }
    
    .ai-badge {
        display: inline-block;
        background: rgba(255,255,255,0.2);
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.85rem;
        margin-top: 0.5rem;
    }
    
    /* Chat Messages dengan Animasi */
    .stChatMessage {
        border-radius: 12px !important;
        margin-bottom: 0.8rem !important;
        padding: 1rem !important;
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
    
    /* User Message - Gradient Blue */
    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white;
    }
    
    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) p,
    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) strong {
        color: white !important;
    }
    
    /* Bot Message - White dengan Shadow */
    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {
        background-color: white !important;
        border: 1px solid #e0e0e0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    /* Sidebar Modern */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #ffffff 0%, #f8f9fa 100%);
        border-right: 1px solid #e0e0e0;
    }
    
    /* Button Modern */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.6rem 1.5rem;
        font-weight: 600;
        width: 100%;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(102, 126, 234, 0.4);
    }
    
    /* Info Box Modern */
    .info-box {
        background: white;
        padding: 1.2rem;
        border-radius: 12px;
        margin-bottom: 1rem;
        border-left: 4px solid #667eea;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    
    .info-box h4 {
        color: #2c3e50;
        font-size: 1rem;
        margin: 0 0 0.8rem 0;
        font-weight: 600;
    }
    
    .info-box p {
        color: #34495e;
        font-size: 0.9rem;
        margin: 0.4rem 0;
        line-height: 1.6;
    }
    
    /* WhatsApp Button Modern */
    .wa-button {
        display: block;
        background: linear-gradient(135deg, #25D366 0%, #128C7E 100%);
        color: white;
        padding: 0.9rem;
        border-radius: 12px;
        text-align: center;
        text-decoration: none;
        font-weight: 600;
        margin: 1rem 0;
        box-shadow: 0 4px 8px rgba(37, 211, 102, 0.3);
        transition: all 0.3s ease;
    }
    
    .wa-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(37, 211, 102, 0.4);
        text-decoration: none;
        color: white;
    }
    
    /* Footer Modern */
    .footer-modern {
        text-align: center;
        padding: 1rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 12px;
        margin: 1rem 0;
        font-size: 0.85rem;
        color: white;
    }
    
    /* Status Badge */
    .status-badge {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        margin: 0.5rem 0;
    }
    
    .status-online {
        background: #d4edda;
        color: #155724;
    }
    
    .status-ai {
        background: #d1ecf1;
        color: #0c5460;
    }
    
    /* Hide Streamlit Elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
</style>
""", unsafe_allow_html=True)

# Initialize chatbot dengan API key dari environment
if 'chatbot' not in st.session_state:
    try:
        # Coba load API key dari environment
        api_key = os.getenv("GROQ_API_KEY")
        if api_key:
            st.session_state.chatbot = ChatbotIntervisualAI(api_key)
            st.session_state.api_key_set = True
            # Welcome message
            welcome_msg = st.session_state.chatbot.chat("Hai, perkenalkan dirimu singkat dan layanan PT Intervisual")
            st.session_state.messages = [{"role": "assistant", "content": welcome_msg}]
        else:
            st.session_state.chatbot = None
            st.session_state.api_key_set = False
            st.session_state.messages = []
    except Exception as e:
        st.session_state.chatbot = None
        st.session_state.api_key_set = False
        st.session_state.messages = []
        st.session_state.error_message = str(e)
        
if 'messages' not in st.session_state:
    st.session_state.messages = []
    
if 'api_key_set' not in st.session_state:
    st.session_state.api_key_set = False

# Sidebar
with st.sidebar:
    st.markdown("### 🤖 PT Intervisual AI")
    st.markdown("---")
    
    # API Key Setup - Only show if not already configured
    if not st.session_state.api_key_set:
        st.error("⚠️ **API Key Groq belum dikonfigurasi!**")
        st.markdown("""
        <div class="info-box">
            <h4>🔑 Developer Setup Required</h4>
            <p>Chatbot membutuhkan API key Groq untuk berfungsi.</p>
            <p><strong>Untuk Developer:</strong> Setup API key di file .env</p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.expander("📖 Cara Setup untuk Developer", expanded=False):
            st.markdown("""
            **Setup API Key (Hanya untuk Developer/Owner):**
            
            1. Daftar di [Groq Console](https://console.groq.com) (GRATIS)
            2. Generate API Key
            3. Buat file `.env` di folder project
            4. Isi dengan:
               ```
               GROQ_API_KEY=gsk_your_api_key_here
               ```
            5. Restart aplikasi
            
            **Atau input temporary di bawah:**
            """)
        
        api_key_input = st.text_input(
            "Groq API Key (Temporary):",
            type="password",
            help="Input API key untuk testing saja. Untuk production, gunakan file .env"
        )
        
        if st.button("🚀 Aktifkan Chatbot"):
            if api_key_input:
                try:
                    # Initialize chatbot
                    st.session_state.chatbot = ChatbotIntervisualAI(api_key_input)
                    st.session_state.api_key_set = True
                    
                    # Welcome message
                    welcome_msg = st.session_state.chatbot.chat("Hai, perkenalkan dirimu singkat dan layanan PT Intervisual")
                    st.session_state.messages = [{
                        "role": "assistant",
                        "content": welcome_msg
                    }]
                    
                    st.success("✅ AI Chatbot berhasil diaktifkan!")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error: {e}")
            else:
                st.warning("⚠️ Masukkan API key terlebih dahulu")
        
        st.markdown("---")
        st.info("💡 **Note:** Customer tidak perlu setup API key. Ini sudah otomatis jika .env file sudah dikonfigurasi oleh developer.")
        
    else:
        # AI Status
        st.markdown("""
        <div class="status-badge status-online">
            ✓ AI Online
        </div>
    
        """, unsafe_allow_html=True)
        
        st.markdown("---")
    
    # Info Perusahaan
    st.markdown(f"""
    <div class="info-box">
        <h4>🏢 Informasi</h4>
        <p><strong>Bidang:</strong><br>{COMPANY_INFO['bidang_usaha']}</p>
        <p><strong>Sejak:</strong> {COMPANY_INFO['tahun_berdiri']['operasi']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Kontak
    st.markdown(f"""
    <div class="info-box">
        <h4>📞 Kontak</h4>
        <p><strong>WhatsApp:</strong><br>{COMPANY_INFO['kontak']['whatsapp']}</p>
        <p><strong>Email:</strong><br>{COMPANY_INFO['kontak']['email']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # WhatsApp Button
    whatsapp_url = COMPANY_INFO['kontak']['whatsapp_link']
    st.markdown(f"""
    <a href="{whatsapp_url}" target="_blank" class="wa-button">
        💬 Chat via WhatsApp
    </a>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Layanan
    st.markdown("**🛠️ Layanan Kami:**")
    for i, layanan in enumerate(COMPANY_INFO['layanan_utama'], 1):
        st.markdown(f"{i}. {layanan['nama']}")
    
    st.markdown("---")
    
    # Features
    if st.session_state.api_key_set:
        st.markdown("**✨ Fitur AI:**")
        st.markdown("""
        - 💰 Estimasi harga konstruksi
        - 🏠 Harga desain interior
        - 📦 Paket ruangan
        - 💬 Konsultasi interaktif
        """)
        
        st.markdown("---")
    
    # Clear Button
    if st.session_state.api_key_set and st.button("🔄 Mulai Baru"):
        st.session_state.messages = []
        st.session_state.chatbot.clear_history()
        welcome_msg = st.session_state.chatbot.chat("Hai, perkenalkan dirimu singkat")
        st.session_state.messages.append({
            "role": "assistant",
            "content": welcome_msg
        })
        st.rerun()

# Main content
st.markdown("""
<div class="header-modern">
    <h1>🏗️ PT Intervisual AI Assistant</h1>
    <p>Chatbot Cerdas untuk Konsultasi Konstruksi & Desain Interior</p>
</div>
""", unsafe_allow_html=True)

# Display chat messages
if st.session_state.api_key_set:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Footer
    st.markdown("""
    <div class="footer-modern">
        <strong>PT Intervisual</strong> • Kontraktor & Desain Interior • Sejak 2007 • © 2025
    </div>
    """, unsafe_allow_html=True)
    
    # Chat input
    if prompt := st.chat_input("Tanya apa saja tentang konstruksi, desain interior, atau harga..."):
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Add to history
        st.session_state.messages.append({
            "role": "user",
            "content": prompt
        })
        
        # Get bot response dengan loading indicator
        with st.spinner("🤖 AI sedang berpikir..."):
            response = st.session_state.chatbot.chat(prompt)
        
        # Display assistant response
        with st.chat_message("assistant"):
            st.markdown(response)
        
        # Add to history
        st.session_state.messages.append({
            "role": "assistant",
            "content": response
        })
        
        st.rerun()
else:
    # Tampilan jika belum setup API key
    st.error("""
    ### ⚠️ Chatbot Belum Dikonfigurasi
    
    API Key Groq belum di-setup oleh developer.
    """)
    
    st.info("""
    ### 📌 Untuk Developer/Owner:
    
    Silakan setup API Key Groq di file `.env`:
    
    1. Buat file `.env` di folder project
    2. Isi dengan:
       ```
       GROQ_API_KEY=gsk_your_api_key_here
       ```
    3. Restart aplikasi dengan `streamlit run app_ai.py`
    
    Atau input API key temporary di sidebar (untuk testing saja).
    
    ---
    
    ### 🎯 Setelah Setup, Customer Dapat:
    
    1. **💰 Estimasi Harga Konstruksi**
       - Harga pekerjaan finishing
       - Harga instalasi listrik
       - Harga plafon, dinding, lantai
       - Dan masih banyak lagi!
    
    2. **🏠 Harga Desain Interior**
       - Material keramik, granit, marmer
       - Kitchen set & furniture
       - Sanitasi (closet, wastafel, shower)
       - Lampu & dekorasi
    
    3. **📦 Paket Ruangan**
       - Kamar tidur
       - Ruang tamu
       - Dapur
       - Kamar mandi
    
    4. **💬 Konsultasi Interaktif**
       - Tanya jawab dengan AI
       - Rekomendasi material
       - Tips desain interior
       - Dan lain-lain
    
    ---
    
    **📱 Atau hubungi kami langsung:**
    - WhatsApp: """ + COMPANY_INFO['kontak']['whatsapp'] + """
    - Email: """ + COMPANY_INFO['kontak']['email'] + """
    """)
    
    # Footer
    st.markdown("""
    <div class="footer-modern">
        <strong>PT Intervisual</strong> • Kontraktor & Desain Interior • Sejak 2007 • © 2025
    </div>
    """, unsafe_allow_html=True)
