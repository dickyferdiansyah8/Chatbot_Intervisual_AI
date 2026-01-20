# 📊 PERBANDINGAN: Chatbot Lama vs Chatbot AI Baru

## 🔍 Overview

| Aspek | Versi Lama (Rule-Based) | Versi Baru (AI-Powered) |
|-------|------------------------|------------------------|
| **Engine** | Pattern matching sederhana | Groq AI (Llama 3.3 70B) |
| **File** | `chatbot_engine.py` + `app.py` | `chatbot_engine_ai.py` + `app_ai.py` |
| **Biaya** | Gratis | Gratis (Groq API) |
| **Kecepatan** | Instant (~0.1s) | Cepat (~0.5-1s) |
| **Akurasi** | Terbatas | Sangat Tinggi |
| **Fleksibilitas** | Kaku | Sangat Fleksibel |

---

## 🆚 Detail Perbandingan

### 1. **Cara Kerja**

**Versi Lama:**
```python
# Rule-based pattern matching
if "harga" in message and "plafon" in message:
    return "Harga plafon sekitar Rp 100.000 - Rp 200.000"
```
- ❌ Hanya bisa jawab pattern yang sudah di-hardcode
- ❌ Tidak paham konteks
- ❌ Tidak bisa handle variasi pertanyaan

**Versi Baru:**
```python
# AI-powered dengan context understanding
response = groq_ai.chat("Berapa harga plafon gypsum untuk ruangan 4x4 meter?")
# AI akan:
# 1. Pahami intent (tanya harga)
# 2. Extract info (plafon gypsum, 4x4m)
# 3. Query database RAB
# 4. Generate natural response
```
- ✅ Paham berbagai cara bertanya
- ✅ Memahami konteks percakapan
- ✅ Bisa handle follow-up questions

---

### 2. **Kemampuan Menjawab**

| Pertanyaan | Lama | Baru |
|------------|------|------|
| "Harga plafon berapa?" | ✅ Bisa | ✅ Bisa (lebih detail) |
| "Plafon untuk kamar 4x4 kira-kira abis berapa ya?" | ❌ Tidak paham | ✅ Bisa calculate |
| "Apa bedanya plafon gypsum sama PVC?" | ❌ Tidak bisa | ✅ Bisa explain |
| "Tadi kan harga plafon 120rb ya, kalau 20 meter totalnya berapa?" | ❌ Tidak ingat context | ✅ Bisa calculate from context |

---

### 3. **Data Source**

**Versi Lama:**
```python
# Hardcoded di code
PRICE_DATA = {
    "plafon": "Rp 100.000 - 200.000",
    "cat": "Rp 30.000 - 80.000"
}
```
- ❌ Data statis
- ❌ Susah update
- ❌ Limited coverage

**Versi Baru:**
```python
# Dynamic dari RAB PDF + database
rab_parser.parse_pdf("RAB_Finishing.pdf")  # Parse real RAB
price_scraper.get_price_estimate("plafon")  # Database harga
```
- ✅ Data real dari RAB PT Intervisual
- ✅ Database lengkap material interior
- ✅ Easy to update

---

### 4. **User Experience**

**Versi Lama:**
```
User: "plafon berapa?"
Bot: "Harga plafon sekitar Rp 100.000"

User: "yang gypsum aja?"
Bot: "Maaf, saya tidak mengerti pertanyaan Anda" ❌
```

**Versi Baru:**
```
User: "plafon berapa?"
Bot: "📊 Untuk plafon, ada beberapa pilihan:
     • Plafon gypsum: Rp 80.000 - 200.000/m²
     • Plafon PVC: Rp 50.000 - 150.000/m²
     
     Mau yang mana? 😊"

User: "yang gypsum aja"
Bot: "Baik! Plafon gypsum rata-rata Rp 120.000/m². 
     Berapa luas ruangan yang mau dipasang?" ✅
```

---

### 5. **Fitur Tambahan**

| Fitur | Lama | Baru |
|-------|------|------|
| Query harga dari RAB | ❌ | ✅ |
| Harga material interior | ❌ | ✅ |
| Paket ruangan | ❌ | ✅ |
| Context-aware | ❌ | ✅ |
| Multi-turn conversation | ❌ | ✅ |
| Calculate estimate | ❌ | ✅ |
| Rekomendasi material | ❌ | ✅ |
| Natural language | ⚠️ Terbatas | ✅ Penuh |

---

## 💰 Perbandingan Biaya

| Item | Lama | Baru |
|------|------|------|
| **Setup Cost** | Rp 0 | Rp 0 |
| **Running Cost** | Rp 0 | Rp 0 (Groq gratis!) |
| **Maintenance** | Mudah | Mudah |
| **Scaling** | Unlimited | 14,400 req/day (gratis) |

**Groq Free Tier:**
- ✅ 14,400 requests/day
- ✅ 20 requests/minute
- ✅ Unlimited tokens
- ✅ No credit card needed

---

## 🎯 Kapan Pakai Yang Mana?

### Gunakan Versi Lama (`app.py`) jika:
- ✅ Butuh response super cepat (< 0.1s)
- ✅ Pertanyaan user sangat predictable
- ✅ Tidak perlu internet
- ✅ Simple FAQ only
- ✅ Resource sangat terbatas

### Gunakan Versi Baru (`app_ai.py`) jika:
- ✅ Butuh conversation yang natural
- ✅ User bertanya dengan berbagai cara
- ✅ Perlu understanding context
- ✅ Data dari file external (RAB, etc)
- ✅ Mau impressive demo/presentasi! 🎓

---

## 🚀 Rekomendasi untuk Dicky

**Untuk Tugas Akhir/Portfolio:**
👉 **Pakai Versi Baru (AI)** karena:
1. ⭐ Lebih impressive di sidang
2. 📊 Bisa compare 2 approach (Rule vs AI)
3. 🎯 Lebih applicable untuk real use case
4. 💼 Better untuk portfolio
5. 🔬 Bisa research tentang NLP/AI

**Struktur Skripsi:**
```
BAB 3: Metodologi
├─ 3.1 Baseline: Rule-Based System
│  └─ Implementasi: chatbot_engine.py
├─ 3.2 Proposed: AI-Based System  
│  └─ Implementasi: chatbot_engine_ai.py
└─ 3.3 Hybrid Approach (optional)

BAB 4: Hasil & Pembahasan
├─ 4.1 Perbandingan Akurasi
├─ 4.2 Perbandingan Response Time
├─ 4.3 User Satisfaction Survey
└─ 4.4 Diskusi
```

---

## 📈 Metric Comparison (Estimasi)

| Metric | Lama | Baru | Improvement |
|--------|------|------|-------------|
| **Intent Accuracy** | 60% | 95% | +58% 🎉 |
| **Response Time** | 0.1s | 0.8s | -700% ⚠️ |
| **User Satisfaction** | 6/10 | 9/10 | +50% 🎉 |
| **Query Coverage** | 20 patterns | Unlimited | +∞ 🎉 |
| **Maintenance Time** | 2h/week | 0.5h/week | -75% 🎉 |

---

## 🎓 Tips Presentasi/Sidang

**Yang Harus Dijelaskan:**
1. "Saya develop 2 versi untuk comparison"
2. "Versi pertama rule-based sebagai baseline"
3. "Versi kedua AI-based dengan Groq API"
4. "Hasil evaluasi menunjukkan AI lebih akurat [data]"
5. "Trade-off: AI lebih lambat tapi lebih fleksibel"

**Demo:**
1. Show versi lama dengan pertanyaan yang tidak dimengerti
2. Show versi baru yang bisa jawab dengan natural
3. Highlight fitur query RAB real
4. Show calculation & recommendation

---

## 📞 Support

Punya pertanyaan? Contact:
- 📧 Email: dicky@example.com
- 💬 WhatsApp: [Your number]

---

**Good luck untuk TA kamu, Dicky! 🚀**

Kalau butuh bantuan lagi, just ask! 😊
