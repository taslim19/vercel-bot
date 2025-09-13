import os
import json
import requests
from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        """Handle POST requests from Telegram webhook"""
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            update_data = json.loads(post_data.decode('utf-8'))
            
            # Process the update
            self.process_update(update_data)
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'status': 'ok'}).encode())
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': str(e)}).encode())
    
    def process_update(self, update_data):
        """Process Telegram update"""
        try:
            # Extract message data
            message = update_data.get('message', {})
            if not message:
                return
                
            text = message.get('text', '')
            user_id = message.get('from', {}).get('id')
            chat_id = message.get('chat', {}).get('id')
            
            # Forward to HF Spaces
            hf_url = os.getenv('HF_SPACES_URL')
            if hf_url:
                payload = {
                    'message': text,
                    'user_id': user_id,
                    'chat_id': chat_id,
                    'update_data': update_data
                }
                
                try:
                    response = requests.post(
                        f"{hf_url}/api/process_message",
                        json=payload,
                        timeout=10
                    )
                    
                    if response.status_code == 200:
                        reply = response.json().get('reply', 'Message processed')
                        self.send_telegram_message(chat_id, reply)
                        
                except Exception as e:
                    print(f"Error forwarding to HF Spaces: {e}")
                    self.send_telegram_message(chat_id, "❌ Service temporarily unavailable")
                    
        except Exception as e:
            print(f"Error processing update: {e}")
    
    def send_telegram_message(self, chat_id, text):
        """Send message back to Telegram"""
        try:
            bot_token = os.getenv('BOT_TOKEN')
            if not bot_token:
                return
                
            url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
            data = {
                'chat_id': chat_id,
                'text': text,
                'parse_mode': 'Markdown'
            }
            
            requests.post(url, json=data, timeout=5)
            
        except Exception as e:
            print(f"Error sending message: {e}")
    
    def do_GET(self):
        """Health check endpoint"""
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({
            'status': 'healthy', 
            'service': 'vercel-bot',
            'version': '1.0.0'
        }).encode())
