import os
from openai import OpenAI
from config import Config

class AIImageAnalyzer:
    def __init__(self):
        self.client = OpenAI(api_key=Config.OPENAI_API_KEY)
        self.categories = Config.WASTE_CATEGORIES
        print("✅ AI 分析器初始化完成")
    
    def analyze_image(self, base64_image):
        """呼叫 GPT-4V 分析圖片內容"""
        print("🔍 開始分析圖片...")
        
        prompt = f"""
        You are a Taiwan waste classification expert. Analyze the main item in this image and reply strictly in this format: `item_name, category`

        Categories: {", ".join(self.categories)}

        Rules:
        - Identify the main item name in Chinese
        - Choose the correct category
        - If unclear, reply: "無法辨識"
        - No extra text or explanations

        Examples:
        - 寶特瓶, 資源回收
        - 香蕉皮, 廚餘
        - 電池, 有害垃圾
        """

        try:
            response = self.client.chat.completions.create(
                model="gpt-4-vision-preview",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=300
            )
            
            analysis_result = response.choices[0].message.content.strip()
            print(f"✅ AI 分析結果: {analysis_result}")
            return analysis_result
            
        except Exception as e:
            print(f"❌ GPT-4V 分析失敗: {e}")
            return "分析服務暫時無法使用"

# 測試函數
def test_ai_analyzer():
    """測試 AI 分析器功能"""
    print("🧪 測試 AI 分析器...")
    
    try:
        analyzer = AIImageAnalyzer()
        print("✅ AI 分析器初始化測試成功")
        
        # 測試金鑰
        if Config.OPENAI_API_KEY:
            print(f"✅ OpenAI 金鑰有效: {Config.OPENAI_API_KEY[:15]}...")
        else:
            print("❌ OpenAI 金鑰無效")
            
    except Exception as e:
        print(f"❌ AI 分析器測試失敗: {e}")

if __name__ == "__main__":
    test_ai_analyzer()