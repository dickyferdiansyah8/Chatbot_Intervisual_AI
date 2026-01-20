# 🚀 QUICK START GUIDE - CHATBOT AI PT INTERVISUAL

## ⚡ Setup dalam 5 Menit!

### Step 1: Install Dependencies (2 menit)
```bash
pip install -r requirements.txt
```

### Step 2: Get Groq API Key (2 menit)
1. Buka https://console.groq.com
2. Sign up (gratis, pakai email Google aja)
3. Klik "API Keys" → "Create API Key"
4. Copy API key (mulai dengan `gsk_...`)

### Step 3: Setup API Key (30 detik)
**Opsi A - Via File .env (Recommended):**
```bash
# Copy template
cp .env.template .env

# Edit .env, ganti dengan API key kamu:
GROQ_API_KEY=gsk_paste_api_key_kamu_di_sini
```

**Opsi B - Via Environment Variable:**
```bash
export GROQ_API_KEY="gsk_paste_api_key_kamu_di_sini"
```

### Step 4: Jalankan! (30 detik)
```bash
streamlit run app_ai.py
```

Buka browser di: **http://localhost:8501**

---

## ✅ Checklist

- [ ] Python 3.9+ terinstall
- [ ] Install requirements.txt
- [ ] Punya Groq API key
- [ ] API key di .env atau environment variable
- [ ] File RAB PDF ada di folder project
- [ ] Run `streamlit run app_ai.py`
- [ ] Browser terbuka di localhost:8501

---

## 🎯 Test Cepat

Setelah app berjalan, coba tanya:

1. ✅ **"Halo, apa layanan PT Intervisual?"**
2. ✅ **"Berapa harga plafon gypsum?"**
3. ✅ **"Harga keramik lantai berapa?"**
4. ✅ **"Budget renovasi kamar tidur 4x4 meter?"**

Jika semua berfungsi → **SUKSES!** 🎉

---

## ❌ Troubleshooting Cepat

### Error: "GROQ_API_KEY tidak ditemukan"
```bash
# Check .env file ada dan isinya benar
cat .env

# Atau set manual:
export GROQ_API_KEY="your_key"
```

### Error: "Module 'groq' not found"
```bash
pip install groq --upgrade
```

### Error: "Could not load RAB files"
```bash
# Check file PDF ada
ls *.pdf

# Update path di chatbot_engine_ai.py jika perlu
```

### App tidak buka di browser
```bash
# Manual buka:
open http://localhost:8501

# Atau cek port lain:
streamlit run app_ai.py --server.port 8502
```

---

## 📞 Butuh Bantuan?

- 📖 Baca: `README_AI.md` (dokumentasi lengkap)
- 💬 Contact: dicky@example.com

---

**Happy Coding! 🚀**
