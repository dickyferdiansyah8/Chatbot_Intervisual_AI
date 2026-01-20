# chatbot_engine_ai.py
# Chatbot Engine dengan Groq API + RAB Parser + Price Scraper

import os
from typing import List, Dict
from groq import Groq
from rab_parser import RABParser, format_rab_response
from price_scraper import InteriorPriceScraper, format_price_response, format_package_response
from data_perusahaan import COMPANY_INFO
import json

class ChatbotIntervisualAI:
    """
    Chatbot PT Intervisual dengan AI (Groq)
    
    Features:
    - Natural conversation dengan Groq AI
    - Query harga konstruksi dari RAB
    - Query harga desain interior dari database/web
    - Info perusahaan
    """
    
    def __init__(self, groq_api_key: str = None):
        """
        Initialize chatbot dengan Groq API
        
        Args:
            groq_api_key: API key dari Groq (https://console.groq.com)
        """
        # Setup Groq client
        self.api_key = groq_api_key or os.getenv("GROQ_API_KEY")
        
        if not self.api_key:
            raise ValueError(
                "⚠️ GROQ_API_KEY tidak ditemukan!\n"
                "Cara setup:\n"
                "1. Daftar di https://console.groq.com\n"
                "2. Generate API key\n"
                "3. Set environment variable: GROQ_API_KEY=your_key\n"
                "   atau buat file .env dengan isi: GROQ_API_KEY=your_key"
            )
        
        self.client = Groq(api_key=self.api_key)
        
        # Model yang digunakan
        self.model = "llama-3.3-70b-versatile"  # Groq's fastest & most capable
        
        # Initialize parsers
        self.rab_parser = RABParser()
        self.price_scraper = InteriorPriceScraper()
        
        # Load RAB data
        self._load_rab_data()
        
        # Conversation history
        self.conversation_history: List[Dict] = []
        
        # System prompt
        self.system_prompt = self._create_system_prompt()
    
    def _load_rab_data(self):
        """Load dan parse semua file RAB"""
        try:
            # Parse RAB files
            rab_files = [
                "/mnt/user-data/uploads/RAB_Finishing_Kav10__r17_Juli_2020__-_Tahap_1.pdf",
                "/mnt/user-data/uploads/BQ_9x15.pdf"
            ]
            
            for rab_file in rab_files:
                if os.path.exists(rab_file):
                    print(f"📂 Loading RAB: {rab_file}")
                    self.rab_parser.parse_pdf(rab_file)
            
            print(f"✅ Loaded {len(self.rab_parser.rab_data)} items from RAB")
            
        except Exception as e:
            print(f"⚠️ Warning: Could not load RAB files: {e}")
    
    def _create_system_prompt(self) -> str:
        """Create system prompt untuk Groq AI"""
        return f"""Kamu adalah asisten virtual PT Intervisual, perusahaan kontraktor dan desain interior terpercaya di Indonesia sejak 2007.

BATASAN PENTING - HARUS DIPATUHI:
KAMU HANYA BOLEH MENJAWAB PERTANYAAN TENTANG:
1. PT Intervisual (perusahaan, layanan, kontak, lokasi)
2. Desain Interior (material, harga, paket, rekomendasi)
3. Konstruksi & Bangunan (RAB, harga pekerjaan, estimasi biaya)
4. Renovasi (rumah, kantor, komersial)
5. Konsultasi proyek konstruksi/interior

KAMU TIDAK BOLEH MENJAWAB PERTANYAAN TENTANG:
- Politik, agama, isu sensitif
- Topik umum tidak terkait konstruksi/interior (cuaca, olahraga, hiburan, dll)
- Matematika/sains umum yang tidak terkait proyek
- Coding/programming (kecuali untuk sistem smart home)
- Kesehatan, hukum, finansial umum
- Topik apapun di luar bidang konstruksi & desain interior

JIKA DITANYA TOPIK DI LUAR SCOPE:
Jawab dengan sopan: "Maaf, saya adalah asisten khusus untuk konsultasi konstruksi dan desain interior PT Intervisual. Saya hanya dapat membantu pertanyaan seputar:
- Layanan PT Intervisual
- Harga & estimasi konstruksi
- Desain & material interior
- Konsultasi proyek bangunan

Ada yang bisa saya bantu terkait konstruksi atau desain interior? 😊"

INFORMASI PERUSAHAAN:
- Nama: PT Intervisual (Interior) & PT Cipta Anta Visual (Kontraktor)
- Bidang: Kontraktor Bangunan & Desain Interior
- Pengalaman: Sejak 2007 (hampir 2 dekade)
- Filosofi: "Ruang bukan hanya dibangun, tetapi juga harus dapat 'dihidupi'"

LAYANAN UTAMA:
1. Desain Arsitektur - Desain bangunan hunian/komersial dari awal
2. Renovasi Komersial - Spesialis renovasi & peremajaan
3. Desain & Pembangunan Interior - Interior nyaman, estetis, fungsional
4. Kontraktor Bangunan/Sipil - Quality control berlapis
5. Sistem Otomasi & Tenaga Surya - Smart home & energi terbarukan
6. Konsultan Proyek - Perencanaan strategis semua skala

KONTAK:
- WhatsApp: {COMPANY_INFO['kontak']['whatsapp']} ({COMPANY_INFO['kontak']['whatsapp_link']})
- Email: {COMPANY_INFO['kontak']['email']}
- Website: {COMPANY_INFO['kontak']['website']}
- Head Office: {COMPANY_INFO['lokasi_kantor']['head_office']['alamat']}

PROMO:
- Free Smart Home System untuk proyek tertentu
- Konsultasi GRATIS
- Hubungi kami untuk detail promo terkini

CARA MERESPONS (HANYA UNTUK TOPIK YANG RELEVAN):
1. Ramah, profesional, dan helpful
2. Gunakan bahasa Indonesia yang natural
3. Jika ditanya harga konstruksi → gunakan fungsi query_rab()
4. Jika ditanya harga interior/material → gunakan fungsi query_interior_price()
5. Selalu tawarkan konsultasi gratis di akhir
6. Gunakan emoji secukupnya untuk friendly
7. Jika tidak tahu pasti → arahkan ke konsultasi dengan tim

PENTING:
- JANGAN membuat-buat harga
- Jika data tidak tersedia → tawarkan konsultasi
- Selalu berikan range harga, bukan angka pasti (kecuali dari RAB)
- Tekankan bahwa harga final tergantung survey & spesifikasi
- TOLAK DENGAN SOPAN jika pertanyaan di luar scope konstruksi/interior
"""
    
    def query_rab(self, keyword: str) -> str:
        """Query harga dari RAB data"""
        try:
            result = self.rab_parser.get_price_estimate(keyword)
            return format_rab_response(result)
        except Exception as e:
            return f"Maaf, terjadi error saat mengambil data RAB: {e}"
    
    def query_interior_price(self, item_name: str) -> str:
        """Query harga material/paket desain interior"""
        try:
            result = self.price_scraper.get_price_estimate(item_name)
            return format_price_response(result)
        except Exception as e:
            return f"Maaf, terjadi error saat mengambil data harga: {e}"
    
    def query_package(self, room_type: str, area: float = 15.0) -> str:
        """Query paket desain per ruangan"""
        try:
            result = self.price_scraper.get_package_estimate(room_type, area)
            return format_package_response(result)
        except Exception as e:
            return f"Maaf, terjadi error saat mengambil data paket: {e}"
    
    def _is_on_topic(self, message: str) -> bool:
        """
        Check apakah pertanyaan masih dalam scope konstruksi/desain interior
        
        Returns:
            True jika on-topic, False jika off-topic
        """
        message_lower = message.lower()
        
        # Keywords yang DIPERBOLEHKAN (on-topic)
        allowed_keywords = [
            # Perusahaan
            'intervisual', 'pt intervisual', 'perusahaan', 'kantor', 'alamat', 'kontak',
            'layanan', 'promo', 'gratis', 'konsultasi',
            
            # Konstruksi
            'bangun', 'bangunan', 'konstruksi', 'kontraktor', 'renovasi', 'pembangunan',
            'rumah', 'gedung', 'kantor', 'ruko', 'apartemen', 'villa',
            'pondasi', 'struktur', 'sipil', 'arsitek', 'arsitektur',
            
            # Material & Pekerjaan
            'plafon', 'dinding', 'lantai', 'atap', 'pintu', 'jendela', 'tangga',
            'cat', 'keramik', 'granit', 'marmer', 'parket', 'vinyl', 'wallpaper',
            'gypsum', 'pvc', 'bata', 'beton', 'semen',
            
            # Interior
            'interior', 'desain', 'design', 'furniture', 'mebel', 'furnitur',
            'kitchen set', 'dapur', 'lemari', 'meja', 'kursi', 'sofa',
            'kamar tidur', 'ruang tamu', 'kamar mandi', 'toilet',
            
            # Sanitasi
            'closet', 'wastafel', 'shower', 'kran', 'pipa', 'air',
            
            # Elektrikal
            'listrik', 'lampu', 'instalasi', 'kabel', 'saklar', 'stop kontak',
            
            # Finishing
            'finishing', 'waterproofing', 'pengecatan', 'pemasangan',
            
            # Harga & Estimasi
            'harga', 'biaya', 'budget', 'anggaran', 'rab', 'estimasi', 'paket',
            'berapa', 'mahal', 'murah',
            
            # Smart Home
            'smart home', 'otomasi', 'automation', 'solar', 'panel surya',
            
            # Umum terkait konstruksi
            'ukuran', 'luas', 'meter', 'm2', 'm²', 'dimensi',
            'material', 'bahan', 'kualitas', 'spesifikasi',
            'proyek', 'pembangunan', 'pengerjaan', 'durasi', 'waktu',
        ]
        
        # Keywords yang DILARANG (off-topic)
        blocked_keywords = [
            # Politik & Agama
            'politik', 'pilpres', 'pemilu', 'partai', 'presiden', 'menteri',
            'agama', 'islam', 'kristen', 'hindu', 'buddha',
            
            # Entertainment
            'film', 'movie', 'musik', 'lagu', 'artis', 'selebritis', 'celebrity',
            'sepak bola', 'football', 'basket', 'olahraga',
            
            # Programming (kecuali smart home)
            'python', 'javascript', 'code', 'coding', 'programming', 'github',
            'bug', 'debug', 'api',
            
            # Kesehatan & Hukum
            'dokter', 'obat', 'penyakit', 'sakit', 'hospital', 'medis',
            'lawyer', 'pengacara', 'hukum', 'undang-undang',
            
            # Finance umum
            'saham', 'trading', 'forex', 'kripto', 'bitcoin', 'investasi',
            
            # Lainnya
            'cuaca', 'weather', 'makanan', 'resep', 'masak',
            'game', 'gaming', 'anime', 'komik',
        ]
        
        # Check greeting/salam (always allowed)
        greetings = ['hai', 'halo', 'hi', 'hello', 'selamat', 'pagi', 'siang', 'sore', 'malam']
        if any(greeting in message_lower for greeting in greetings) and len(message_lower.split()) <= 3:
            return True
        
        # Check jika ada blocked keywords
        has_blocked = any(keyword in message_lower for keyword in blocked_keywords)
        if has_blocked:
            # Double check - mungkin konteksnya masih relevan
            # Misalnya: "harga cat dinding yang bagus untuk kesehatan"
            has_allowed = any(keyword in message_lower for keyword in allowed_keywords)
            if not has_allowed:
                return False  # Pure off-topic
        
        # Check jika ada allowed keywords
        has_allowed = any(keyword in message_lower for keyword in allowed_keywords)
        
        # Jika tidak ada keyword apapun, check panjang pertanyaan
        if not has_allowed and len(message_lower.split()) > 3:
            # Pertanyaan panjang tanpa keyword relevan = likely off-topic
            return False
        
        return True
    
    def _detect_intent(self, message: str) -> Dict:
        """
        Detect user intent untuk routing
        
        Returns:
            {
                'intent': 'rab_query' | 'interior_price' | 'package' | 'general',
                'keywords': [...],
                'confidence': 0.0-1.0
            }
        """
        message_lower = message.lower()
        
        # Keywords untuk berbagai intent
        rab_keywords = ['plafon', 'dinding', 'lantai', 'cat', 'waterproofing', 
                       'finishing', 'instalasi', 'pekerjaan', 'konstruksi', 'bangunan']
        
        interior_keywords = ['keramik', 'granit', 'marmer', 'parket', 'vinyl', 
                            'kitchen set', 'lemari', 'furniture', 'lampu', 'gorden',
                            'wallpaper', 'closet', 'wastafel', 'shower']
        
        package_keywords = ['paket', 'kamar tidur', 'ruang tamu', 'dapur', 
                           'kamar mandi', 'total biaya', 'budget']
        
        # Check RAB query
        rab_matches = sum(1 for kw in rab_keywords if kw in message_lower)
        if rab_matches > 0 and any(word in message_lower for word in ['harga', 'biaya', 'berapa']):
            return {
                'intent': 'rab_query',
                'keywords': [kw for kw in rab_keywords if kw in message_lower],
                'confidence': min(rab_matches / len(rab_keywords), 1.0)
            }
        
        # Check package query
        package_matches = sum(1 for kw in package_keywords if kw in message_lower)
        if package_matches > 0:
            return {
                'intent': 'package',
                'keywords': [kw for kw in package_keywords if kw in message_lower],
                'confidence': min(package_matches / len(package_keywords), 1.0)
            }
        
        # Check interior price query
        interior_matches = sum(1 for kw in interior_keywords if kw in message_lower)
        if interior_matches > 0 and any(word in message_lower for word in ['harga', 'biaya', 'berapa']):
            return {
                'intent': 'interior_price',
                'keywords': [kw for kw in interior_keywords if kw in message_lower],
                'confidence': min(interior_matches / len(interior_keywords), 1.0)
            }
        
        # Default: general conversation
        return {
            'intent': 'general',
            'keywords': [],
            'confidence': 1.0
        }
    
    def chat(self, user_message: str) -> str:
        """
        Main chat function
        
        Args:
            user_message: Pesan dari user
            
        Returns:
            Response dari chatbot
        """
        try:
            # CHECK ON-TOPIC FIRST
            if not self._is_on_topic(user_message):
                return """Maaf, saya adalah asisten khusus untuk konsultasi konstruksi dan desain interior PT Intervisual. Saya hanya dapat membantu pertanyaan seputar:

🏗️ **Konstruksi & Bangunan:**
- Harga pekerjaan konstruksi (pondasi, dinding, lantai, atap, dll)
- Estimasi biaya pembangunan/renovasi
- Material & spesifikasi bangunan

🏠 **Desain Interior:**
- Harga material interior (keramik, granit, marmer, parket, dll)
- Kitchen set, furniture, lemari
- Paket ruangan (kamar tidur, ruang tamu, dapur, kamar mandi)

🏢 **PT Intervisual:**
- Layanan perusahaan
- Promo & konsultasi gratis
- Kontak & lokasi kantor

Ada yang bisa saya bantu terkait konstruksi atau desain interior? 😊

Atau hubungi kami langsung:
📱 WhatsApp: """ + COMPANY_INFO['kontak']['whatsapp'] + """
📧 Email: """ + COMPANY_INFO['kontak']['email']
            
            # Detect intent
            intent_data = self._detect_intent(user_message)
            
            # Handle specific intents
            if intent_data['intent'] == 'rab_query':
                # Query RAB data
                keywords = ' '.join(intent_data['keywords'])
                rab_response = self.query_rab(keywords)
                
                # Enhance dengan AI
                enhanced_prompt = f"""User bertanya tentang harga konstruksi: "{user_message}"

Data dari RAB kami:
{rab_response}

Berikan response yang natural dan helpful berdasarkan data di atas. Jelaskan dengan ramah dan tawarkan konsultasi gratis untuk detail lebih lanjut."""
                
                return self._call_groq(enhanced_prompt)
            
            elif intent_data['intent'] == 'interior_price':
                # Query interior price
                keywords = ' '.join(intent_data['keywords'])
                price_response = self.query_interior_price(keywords)
                
                # Enhance dengan AI
                enhanced_prompt = f"""User bertanya tentang harga material interior: "{user_message}"

Data harga pasaran:
{price_response}

Berikan response yang natural dan helpful. Jelaskan range harga dan tawarkan konsultasi gratis untuk mendapatkan penawaran yang sesuai kebutuhan."""
                
                return self._call_groq(enhanced_prompt)
            
            elif intent_data['intent'] == 'package':
                # Query package
                # Extract room type dan area jika ada
                room_type = intent_data['keywords'][0] if intent_data['keywords'] else 'kamar tidur'
                
                package_response = self.query_package(room_type)
                
                enhanced_prompt = f"""User bertanya tentang paket desain: "{user_message}"

Paket yang tersedia:
{package_response}

Berikan response yang natural. Jelaskan paket-paket yang ada dan tawarkan konsultasi gratis untuk customisasi sesuai budget."""
                
                return self._call_groq(enhanced_prompt)
            
            else:
                # General conversation
                return self._call_groq(user_message)
        
        except Exception as e:
            return f"⚠️ Maaf, terjadi error: {e}\n\nSilakan hubungi kami langsung:\n📱 WhatsApp: {COMPANY_INFO['kontak']['whatsapp']}"
    
    def _call_groq(self, user_message: str) -> str:
        """Call Groq API untuk generate response"""
        try:
            # Add message to history
            self.conversation_history.append({
                "role": "user",
                "content": user_message
            })
            
            # Prepare messages untuk Groq
            messages = [
                {
                    "role": "system",
                    "content": self.system_prompt
                }
            ] + self.conversation_history
            
            # Call Groq API
            chat_completion = self.client.chat.completions.create(
                messages=messages,
                model=self.model,
                temperature=0.7,
                max_tokens=1024,
                top_p=0.9,
                stream=False
            )
            
            # Extract response
            assistant_message = chat_completion.choices[0].message.content
            
            # Add to history
            self.conversation_history.append({
                "role": "assistant",
                "content": assistant_message
            })
            
            return assistant_message
        
        except Exception as e:
            return f"⚠️ Error saat berkomunikasi dengan AI: {e}\n\nSilakan coba lagi atau hubungi kami di WhatsApp: {COMPANY_INFO['kontak']['whatsapp']}"
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
    
    def get_conversation_summary(self) -> str:
        """Get summary of conversation"""
        if not self.conversation_history:
            return "Belum ada percakapan"
        
        # Use Groq to summarize
        summary_prompt = f"""Buatkan ringkasan singkat dari percakapan berikut:

{json.dumps(self.conversation_history, indent=2)}

Ringkasan harus mencakup:
- Topik utama yang dibahas
- Informasi penting yang diberikan
- Follow-up action (jika ada)

Maksimal 3-4 kalimat."""
        
        try:
            response = self._call_groq(summary_prompt)
            return response
        except:
            return "Tidak dapat membuat ringkasan"


# Helper function untuk testing
def test_chatbot():
    """Test chatbot functionality"""
    print("🤖 Testing Chatbot Intervisual AI\n")
    
    # Check API key
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("❌ GROQ_API_KEY not found!")
        print("\nSetup instructions:")
        print("1. Get API key from https://console.groq.com")
        print("2. Create .env file with: GROQ_API_KEY=your_key_here")
        return
    
    # Initialize chatbot
    print("Initializing chatbot...")
    bot = ChatbotIntervisualAI(api_key)
    
    # Test queries
    test_messages = [
        "Halo, apa saja layanan yang ditawarkan PT Intervisual?",
        "Berapa harga plafond gypsum per meter?",
        "Saya mau renovasi kamar tidur 4x4 meter, kira-kira budget berapa ya?",
        "Harga keramik lantai berapa?",
    ]
    
    for msg in test_messages:
        print(f"\n{'='*60}")
        print(f"👤 User: {msg}")
        print(f"{'='*60}")
        
        response = bot.chat(msg)
        print(f"🤖 Bot: {response}\n")


if __name__ == "__main__":
    test_chatbot()
