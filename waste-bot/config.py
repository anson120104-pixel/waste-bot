import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # LINE Bot 設定
    LINE_CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET', '123')
    LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', '456')
    
    # OpenAI 設定
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    
    # 應用程式設定
    DEBUG = os.getenv('DEBUG', 'True') == 'True'
    PORT = int(os.getenv('PORT', 5000))
    
    # 垃圾分類類別
    WASTE_CATEGORIES = [
        "一般垃圾",
        "資源回收", 
        "廚餘",
        "有害垃圾",
        "紙容器回收"
    ]

# 測試設定
if __name__ == "__main__":
    print("=== CONFIG TEST ===")
    if Config.OPENAI_API_KEY:
        print("✅ OpenAI Key Found")
        print(f"Key: {Config.OPENAI_API_KEY[:15]}...")
    else:
        print("❌ No OpenAI Key")
    print("=== TEST END ===")
