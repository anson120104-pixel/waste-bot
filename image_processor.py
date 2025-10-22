import requests
from io import BytesIO
import base64
import os

class ImageProcessor:
    def __init__(self):
        print("✅ 圖片處理器初始化完成")
    
    def download_line_image(self, message_id, line_bot_api):
        """下載 LINE 平台上的使用者圖片"""
        print(f"📥 開始下載圖片，訊息ID: {message_id}")
        
        try:
            # 使用 LINE SDK 取得圖片內容
            message_content = line_bot_api.get_message_content(message_id)
            
            # 將圖片內容轉為 bytes
            image_bytes = BytesIO()
            for chunk in message_content.iter_content():
                image_bytes.write(chunk)
            
            image_bytes.seek(0)
            print("✅ 圖片下載成功")
            return image_bytes
            
        except Exception as e:
            print(f"❌ 圖片下載失敗: {e}")
            return None
    
    def encode_image_to_base64(self, image_bytes):
        """將圖片轉為 Base64 編碼"""
        try:
            base64_image = base64.b64encode(image_bytes.read()).decode('utf-8')
            print("✅ 圖片編碼成功")
            return base64_image
        except Exception as e:
            print(f"❌ 圖片編碼失敗: {e}")
            return None

# 測試函數
def test_image_processor():
    """測試圖片處理器功能"""
    print("🧪 測試圖片處理器...")
    processor = ImageProcessor()
    print("✅ 圖片處理器測試完成")

if __name__ == "__main__":
    test_image_processor()
