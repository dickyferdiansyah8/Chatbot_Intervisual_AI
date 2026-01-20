# test_filtering.py
# Script untuk test filtering on-topic vs off-topic

from chatbot_engine_ai import ChatbotIntervisualAI
import os

def test_chatbot_filtering():
    """Test apakah chatbot bisa reject off-topic questions"""
    
    print("🧪 TESTING CHATBOT FILTERING\n")
    print("="*60)
    
    # Setup
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("❌ GROQ_API_KEY not found!")
        print("Set dengan: export GROQ_API_KEY='your_key'")
        return
    
    print("✅ API Key loaded")
    print("Initializing chatbot...\n")
    
    bot = ChatbotIntervisualAI(api_key)
    
    # Test cases
    test_cases = [
        # ON-TOPIC (Should answer)
        {
            "category": "✅ ON-TOPIC",
            "questions": [
                "Halo, apa layanan PT Intervisual?",
                "Berapa harga plafon gypsum per meter?",
                "Saya mau renovasi rumah, budget minimal berapa?",
                "Harga keramik lantai untuk ruang tamu?",
                "Paket desain interior kamar tidur berapa?",
                "Beda granit sama marmer apa ya?",
                "Kitchen set per meter harganya berapa?",
                "Berapa lama pengerjaan renovasi rumah 2 lantai?",
            ]
        },
        # OFF-TOPIC (Should reject)
        {
            "category": "❌ OFF-TOPIC",
            "questions": [
                "Siapa presiden Indonesia sekarang?",
                "Gimana cara masak nasi goreng?",
                "Recommend film bagus dong",
                "Manchester United menang gak tadi malam?",
                "Harga saham BBRI sekarang berapa?",
                "Cara coding Python gimana?",
                "Cuaca hari ini gimana?",
                "Obat sakit kepala apa yang bagus?",
            ]
        }
    ]
    
    for test_group in test_cases:
        print(f"\n{'='*60}")
        print(f"{test_group['category']} QUESTIONS")
        print('='*60)
        
        for i, question in enumerate(test_group['questions'], 1):
            print(f"\n{i}. USER: {question}")
            print("-" * 60)
            
            response = bot.chat(question)
            
            # Check if response is rejection
            is_rejection = "maaf" in response.lower() and "asisten khusus" in response.lower()
            
            if test_group['category'] == "✅ ON-TOPIC":
                if is_rejection:
                    print("❌ FAIL: Bot rejected on-topic question!")
                else:
                    print("✅ PASS: Bot answered correctly")
            else:  # OFF-TOPIC
                if is_rejection:
                    print("✅ PASS: Bot correctly rejected off-topic question")
                else:
                    print("❌ FAIL: Bot answered off-topic question!")
            
            print(f"\nBOT: {response[:200]}...")  # Show first 200 chars
            
            # Clear history for next test
            bot.clear_history()
    
    print("\n" + "="*60)
    print("🎉 TESTING COMPLETE!")
    print("="*60)


if __name__ == "__main__":
    test_chatbot_filtering()
