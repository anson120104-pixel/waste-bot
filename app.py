from flask import Flask, request, abort
from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import Configuration, ApiClient, MessagingApi, ReplyMessageRequest, TextMessage, PushMessageRequest
from linebot.v3.webhooks import MessageEvent, ImageMessageContent
from config import Config
from image_processor import ImageProcessor
from ai_analyzer import AIImageAnalyzer
import logging
import os

# 設定日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# 初始化 LINE Bot (新版本)
configuration = Configuration(access_token=Config.LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(Config.LINE_CHANNEL_SECRET)

# 初始化我們的模組
image_processor = ImageProcessor()
ai_analyzer = AIImageAnalyzer()

@app.route("/")
def home():
    return "✅ 垃圾分類機器人服務運行中！"

@app.route("/test")
def test():
    return "🔧 測試頁面 - 服務正常運作中"

@app.route("/callback", methods=['POST'])
def callback():
    """LINE Webhook 接收訊息"""
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    
    logger.info("📨 收到 LINE 請求")
    
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        logger.error("❌ 簽名驗證失敗")
        abort(400)
    
    return 'OK'

@handler.add(MessageEvent, message=ImageMessageContent)
def handle_image_message(event):
    """處理使用者傳送的圖片訊息"""
    logger.info("🖼️ 收到圖片訊息")
    
    try:
        # 使用新版本 API
        with ApiClient(configuration) as api_client:
            line_bot_api = MessagingApi(api_client)
            
            # 1. 先回覆「分析中」訊息
            line_bot_api.reply_message(ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text="🔍 收到圖片！AI 分析中，請稍候 10-20 秒...")]
            ))
            
            # 2. 下載圖片（需要調整 download_line_image 方法）
            image_bytes = image_processor.download_line_image(event.message.id, line_bot_api)
            
            if not image_bytes:
                line_bot_api.push_message(PushMessageRequest(
                    to=event.source.user_id,
                    messages=[TextMessage(text="❌ 圖片下載失敗，請重新傳送圖片。")]
                ))
                return
            
            # 3. 編碼圖片
            base64_image = image_processor.encode_image_to_base64(image_bytes)
            
            if not base64_image:
                line_bot_api.push_message(PushMessageRequest(
                    to=event.source.user_id,
                    messages=[TextMessage(text="❌ 圖片處理失敗，請確認傳送的是有效的圖片。")]
                ))
                return
            
            # 4. 呼叫 AI 分析
            analysis_result = ai_analyzer.analyze_image(base64_image)
            
            # 5. 處理分析結果
            final_response = process_analysis_result(analysis_result)
            
            # 6. 傳送最終結果
            line_bot_api.push_message(PushMessageRequest(
                to=event.source.user_id,
                messages=[TextMessage(text=final_response)]
            ))
            
        logger.info("✅ 圖片分析完成並回覆使用者")
        
    except Exception as e:
        logger.error(f"❌ 處理圖片訊息時發生錯誤: {e}")

def process_analysis_result(result):
    """處理 AI 分析結果"""
    logger.info(f"處理分析結果: {result}")
    
    if "無法辨識" in result:
        return """❓ 無法辨識圖片中的物品

建議：
• 拍攝更清晰、光線充足的照片
• 確保物品在畫面中央
• 或直接用文字描述物品"""

    if "," in result:
        try:
            item_name, category = result.split(",", 1)
            item_name = item_name.strip()
            category = category.strip()
            
            response = f"""✅ 分析完成！

物品：{item_name}
分類：{category}

💡 小提醒：各地區回收規定可能略有不同，請以當地清潔隊為準"""
            
            return response
            
        except Exception as e:
            logger.error(f"解析結果時發生錯誤: {e}")
    
    return "🤖 分析結果格式異常，請重新嘗試。"

if __name__ == "__main__":
    print("🚀 啟動垃圾分類機器人...")
    print("📁 模組載入狀態：")
    print(f"  • 圖片處理器: ✅ 就緒")
    print(f"  • AI 分析器: ✅ 就緒") 
    print(f"  • OpenAI 金鑰: ✅ 有效")
    print(f"🌐 服務網址: http://127.0.0.1:{Config.PORT}")
    print("⏹️  按 Ctrl+C 停止服務")
    app.run(debug=Config.DEBUG, port=Config.PORT, host='0.0.0.0')
