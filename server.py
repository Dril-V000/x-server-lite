import os
import requests
from flask import Flask, jsonify, request, abort
from datetime import datetime

app = Flask(__name__)

SERVER_URL = os.environ.get("SERVER_URL")
AUTH_TOKEN = os.environ.get("AUTH_TOKEN")
INTERNAL_KEY = os.environ.get("INTERNAL_KEY")
DISCORD_WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL") 

def send_discord_notification(message, status="success"):
    """Send notification to Discord"""
    if not DISCORD_WEBHOOK_URL:
        print("⚠️ DISCORD_WEBHOOK_URL is not set in environment variables")
        return
    
    try:
        payload = {
            "content": f"🔔 **Server Alert**",
            "embeds": [{
                "title": "📡 Request Executed",
                "description": message,
                "color": 0x00ff00 if status == "success" else 0xff0000,
                "fields": [
                    {
                        "name": "⏰ Time",
                        "value": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "inline": True
                    },
                    {
                        "name": "🌐 Sender IP",
                        "value": request.remote_addr if request else "Unknown",
                        "inline": True
                    }
                ],
                "footer": {
                    "text": "Sent from Flask Server"
                }
            }]
        }
        
        response = requests.post(DISCORD_WEBHOOK_URL, json=payload)
        response.raise_for_status()
        print("✅ Notification sent to Discord successfully")
        
    except Exception as e:
        print(f"❌ Failed to send Discord notification: {str(e)}")

@app.route('/config', methods=['GET'])
def get_config():
    # Verify internal key
    if request.headers.get("X-Internal-Key") != INTERNAL_KEY:
        send_discord_notification(
            f"🚫 Unauthorized access attempt! Invalid key",
            status="error"
        )
        abort(403)
    
    response_data = {
        "SERVER_URL": SERVER_URL,
        "AUTH_TOKEN": AUTH_TOKEN
    }
    
    send_discord_notification(
        f"✅ `/config` request executed successfully\n"
        f"• SERVER_URL: {SERVER_URL}\n"
        f"• AUTH_TOKEN: {'Set' if AUTH_TOKEN else 'Not set'}",
        status="success"
    )
    
    return jsonify(response_data)

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    send_discord_notification(
        "💚new one",
        status="success"
    )
    return jsonify({"status": "this ni*ga", "timestamp": datetime.now().isoformat()})

@app.errorhandler(404)
def not_found(error):
    send_discord_notification(
        f"⚠️ Non-existent path requested: {request.path}",
        status="error"
    )
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    send_discord_notification(
        f"❌ Internal server error: {str(error)}",
        status="error"
    )
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    if not DISCORD_WEBHOOK_URL:
        print("⚠️ Warning: DISCORD_WEBHOOK_URL is not defined in environment variables")
    
    print("🚀 Starting server...")
    print(f"📡 Port: {os.environ.get('PORT', 5000)}")
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
