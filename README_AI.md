# 🤖 CHATBOT AI PT INTERVISUAL - DOKUMENTASI LENGKAP

## 📋 Daftar Isi
1. [Overview](#overview)
2. [Fitur Utama](#fitur-utama)
3. [Teknologi Stack](#teknologi-stack)
4. [Setup & Instalasi](#setup--instalasi)
5. [Cara Penggunaan](#cara-penggunaan)
6. [Struktur File](#struktur-file)
7. [API Reference](#api-reference)
8. [Troubleshooting](#troubleshooting)

---

## 🎯 Overview

**Chatbot AI PT Intervisual** adalah aplikasi chatbot pintar berbasis web untuk membantu customer mendapatkan informasi tentang:
- ✅ Harga konstruksi bangunan (dari RAB real)
- ✅ Harga material & paket desain interior
- ✅ Layanan PT Intervisual
- ✅ Konsultasi interaktif

**Keunggulan:**
- 🚀 **AI-Powered** menggunakan Groq (Llama 3.3 70B) - GRATIS & CEPAT
- 📊 **Data Real** dari file RAB PT Intervisual
- 💬 **Natural Conversation** seperti berbicara dengan manusia
- 🎨 **UI Modern** dengan Streamlit

---

## ✨ Fitur Utama

### 1. **Query Harga Konstruksi dari RAB**
Chatbot bisa menjawab pertanyaan tentang harga pekerjaan konstruksi berdasarkan data RAB asli:
- Pekerjaan finishing (plafon, dinding, lantai)
- Instalasi listrik, sanitasi, waterproofing
- Material & upah kerja

**Contoh:**
```
User: "Berapa harga plafon gypsum per meter?"
Bot: 📊 Estimasi Harga untuk 'plafon gypsum':
     • Harga rata-rata: Rp 120.000/m²
     • Harga minimum: Rp 80.000/m²
     • Harga maksimum: Rp 200.000/m²
```

### 2. **Harga Desain Interior**
Database lengkap harga material desain interior:
- Lantai: keramik, granit, marmer, parket, vinyl
- Dinding: cat, wallpaper
- Plafon: gypsum, PVC
- Furniture: kitchen set, lemari, meja
- Sanitasi: closet, wastafel, shower
- Lampu & aksesoris

**Contoh:**
```
User: "Harga keramik lantai berapa?"
Bot: 💰 Estimasi Harga keramik:
     Range: Rp 50.000 - Rp 500.000/m²
     Rata-rata: Rp 150.000/m²
```

### 3. **Paket Ruangan**
Estimasi biaya paket desain per ruangan:
- Kamar tidur
- Ruang tamu
- Dapur (kitchen set)
- Kamar mandi

**Contoh:**
```
User: "Budget kamar tidur 4x4 meter kira-kira berapa?"
Bot: 🏠 Paket Kamar Tidur (16m²)
     - Basic: Rp 4.000.000
     - Standard: Rp 10.700.000
     - Premium: Rp 26.700.000
```

### 4. **Konsultasi Interaktif**
AI memahami konteks percakapan dan bisa:
- Menjawab follow-up questions
- Memberikan rekomendasi
- Menjelaskan perbedaan material
- Mengarahkan ke konsultasi gratis

---

## 🛠️ Teknologi Stack

| Kategori | Teknologi | Fungsi |
|----------|-----------|--------|
| **Backend** | Python 3.9+ | Core language |
| **UI Framework** | Streamlit 1.31 | Web interface |
| **AI/LLM** | Groq (Llama 3.3 70B) | Natural language processing |
| **PDF Parser** | PyPDF2, pdfplumber | Extract data RAB dari PDF |
| **Data Processing** | Pandas | Manipulasi data RAB |
| **Environment** | python-dotenv | Manage API keys |

**Kenapa Groq?**
- ✅ **100% GRATIS** (generous free tier)
- ✅ **Super Cepat** (inference < 1 detik)
- ✅ **Model Terbaik** (Llama 3.3 70B)
- ✅ **Mudah Setup** (no credit card needed)

---

## 🚀 Setup & Instalasi

### Step 1: Clone/Download Project
```bash
# Clone atau download project ini
cd chatbot-intervisual-ai
```

### Step 2: Install Dependencies
```bash
# Install semua package yang dibutuhkan
pip install -r requirements.txt
```

### Step 3: Setup Groq API Key

1. **Daftar di Groq:**
   - Kunjungi https://console.groq.com
   - Sign up (gratis, no credit card)
   - Login ke dashboard

2. **Generate API Key:**
   - Klik "API Keys" di sidebar
   - Klik "Create API Key"
   - Copy API key yang dihasilkan

3. **Setup Environment Variable:**
   
   **Opsi A: File .env (Recommended)**
   ```bash
   # Copy template
   cp .env.template .env
   
   # Edit .env dan paste API key
   nano .env
   ```
   
   Isi dengan:
   ```
   GROQ_API_KEY=gsk_your_actual_api_key_here
   ```
   
   **Opsi B: System Environment Variable**
   ```bash
   # Linux/Mac
   export GROQ_API_KEY="gsk_your_actual_api_key_here"
   
   # Windows (CMD)
   set GROQ_API_KEY=gsk_your_actual_api_key_here
   
   # Windows (PowerShell)
   $env:GROQ_API_KEY="gsk_your_actual_api_key_here"
   ```

### Step 4: Jalankan Aplikasi
```bash
# Jalankan chatbot
streamlit run app_ai.py
```

Buka browser di: http://localhost:8501

---

## 💡 Cara Penggunaan

### Untuk User (Customer):

1. **Buka aplikasi** di browser
2. **Setup API Key** (jika belum):
   - Klik sidebar
   - Paste Groq API key
   - Klik "Aktifkan AI Chatbot"
3. **Mulai bertanya!**

**Contoh Pertanyaan:**
- "Halo, apa saja layanan PT Intervisual?"
- "Berapa harga cat dinding per meter?"
- "Saya mau renovasi kamar tidur, budget berapa ya?"
- "Beda keramik sama granit apa?"
- "Harga kitchen set per meter berapa?"
- "Paket kamar mandi lengkap kira-kira berapa?"

### Untuk Developer:

#### Test Chatbot di Terminal:
```python
from chatbot_engine_ai import ChatbotIntervisualAI
import os

# Setup
os.environ['GROQ_API_KEY'] = 'your_key_here'
bot = ChatbotIntervisualAI()

# Test
response = bot.chat("Harga plafon gypsum berapa?")
print(response)
```

#### Query RAB Manual:
```python
from rab_parser import RABParser

parser = RABParser()
parser.parse_pdf("path/to/rab.pdf")

# Search
result = parser.get_price_estimate("plafon")
print(result)
```

#### Query Harga Interior:
```python
from price_scraper import InteriorPriceScraper

scraper = InteriorPriceScraper()

# Single item
result = scraper.get_price_estimate("keramik")
print(result)

# Package
result = scraper.get_package_estimate("kamar tidur", 15)
print(result)
```

---

## 📁 Struktur File

```
chatbot-intervisual-ai/
│
├── app_ai.py                    # 🌟 Main Streamlit app (GUNAKAN INI!)
├── chatbot_engine_ai.py         # 🤖 AI Chatbot engine
├── rab_parser.py                # 📄 RAB PDF parser
├── price_scraper.py             # 💰 Interior price database
├── data_perusahaan.py           # 🏢 Company info
│
├── requirements.txt             # 📦 Dependencies
├── .env.template                # 🔑 API key template
├── .env                         # 🔒 Your API key (JANGAN COMMIT!)
│
├── RAB_*.pdf                    # 📊 File RAB (data source)
│
├── README.md                    # 📖 Dokumentasi ini
│
└── [legacy files]               # Versi lama (bisa dihapus)
    ├── app.py                   # Old app tanpa AI
    └── chatbot_engine.py        # Old rule-based engine
```

---

## 📚 API Reference

### ChatbotIntervisualAI

```python
class ChatbotIntervisualAI:
    def __init__(self, groq_api_key: str = None)
    def chat(self, user_message: str) -> str
    def query_rab(self, keyword: str) -> str
    def query_interior_price(self, item_name: str) -> str
    def query_package(self, room_type: str, area: float) -> str
    def clear_history(self)
```

**Contoh:**
```python
bot = ChatbotIntervisualAI(api_key="gsk_...")
response = bot.chat("Harga plafon berapa?")
```

### RABParser

```python
class RABParser:
    def parse_pdf(self, pdf_path: str) -> pd.DataFrame
    def search_items(self, keyword: str) -> pd.DataFrame
    def get_price_estimate(self, keyword: str) -> Dict
    def get_items_by_category(self, category: str) -> pd.DataFrame
```

### InteriorPriceScraper

```python
class InteriorPriceScraper:
    def get_price_estimate(self, item_name: str) -> Dict
    def get_package_estimate(self, room_type: str, area: float) -> Dict
```

---

## 🐛 Troubleshooting

### Error: "GROQ_API_KEY tidak ditemukan"
**Solusi:**
1. Pastikan file `.env` ada dan berisi API key
2. Atau set environment variable sebelum run app
3. Atau masukkan API key langsung di sidebar app

### Error: "Could not load RAB files"
**Solusi:**
1. Pastikan file RAB PDF ada di folder yang benar
2. Check path di `chatbot_engine_ai.py` line ~60
3. Pastikan PyPDF2 dan pdfplumber terinstall

### Chatbot tidak merespons / lambat
**Solusi:**
1. Check koneksi internet
2. Groq API mungkin down (cek https://status.groq.com)
3. Coba clear chat history dan restart

### Error: "Module not found"
**Solusi:**
```bash
# Install ulang dependencies
pip install -r requirements.txt --upgrade
```

### UI tidak muncul dengan benar
**Solusi:**
```bash
# Clear Streamlit cache
streamlit cache clear

# Restart app
streamlit run app_ai.py
```

---

## 🎓 Tips untuk Mahasiswa

### Untuk Tugas Akhir/Skripsi:

**Judul yang Bisa Dipakai:**
1. "Implementasi Chatbot Berbasis AI untuk Konsultasi Harga Konstruksi Menggunakan Groq API"
2. "Sistem Informasi Estimasi Biaya Desain Interior Menggunakan Natural Language Processing"
3. "Pengembangan Virtual Assistant untuk Perusahaan Kontraktor dengan Retrieval-Augmented Generation (RAG)"

**Metodologi:**
- **Rule-Based** (baseline) → file `chatbot_engine.py`
- **AI-Based** (proposed) → file `chatbot_engine_ai.py`
- **Hybrid** (kombinasi keduanya)

**Metrik Evaluasi:**
- Akurasi harga (error rate)
- Response time
- User satisfaction (survey)
- Intent classification accuracy

**Pengembangan Lanjutan:**
- [ ] Add database (PostgreSQL/MySQL)
- [ ] Add analytics dashboard
- [ ] Add user authentication
- [ ] Deploy to cloud (Streamlit Cloud/Heroku)
- [ ] Add voice input/output
- [ ] Multi-language support
- [ ] WhatsApp integration

---

## 📞 Support

**Untuk bantuan teknis:**
- 📧 Email: dicky@example.com (ganti dengan email kamu)
- 💬 WhatsApp: 0811-9933-588 (PT Intervisual)

**Untuk issue/bug:**
- Create issue di GitHub repository

---

## 📄 License

Project ini dibuat untuk keperluan edukasi dan portfolio.

© 2025 Dicky - Mahasiswa Teknik Informatika Semester 5

---

## 🙏 Credits

- **PT Intervisual** - Data perusahaan & RAB
- **Groq** - AI API (gratis!)
- **Streamlit** - UI framework
- **Anthropic Claude** - Bantuan development 😊

---

**Selamat menggunakan! Good luck untuk tugas akhir kamu, Dicky! 🚀**
