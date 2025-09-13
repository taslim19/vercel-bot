import os
import json
import requests
from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        """Handle POST requests from Telegram webhook - Simple relay to HF Spaces"""
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            update_data = json.loads(post_data.decode('utf-8'))
            
            # Forward the entire Telegram update to HF Spaces
            self.forward_to_hf_spaces(update_data)
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'status': 'ok'}).encode())
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': str(e)}).encode())
    
    def do_GET(self):
        """Health check endpoint"""
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({
            'status': 'healthy', 
            'service': 'vercel-relay',
            'version': '1.0.0',
            'description': 'Simple relay to HF Spaces'
        }).encode())
    
    def forward_to_hf_spaces(self, update_data):
        """Forward Telegram update to HF Spaces"""
        try:
            hf_url = os.getenv('HF_SPACES_URL')
            if not hf_url:
                print("HF_SPACES_URL not configured")
                return
                
            # Forward the entire Telegram update to HF Spaces
            response = requests.post(
                f"{hf_url}/api/telegram_webhook",
                json=update_data,
                timeout=30
            )
            
            print(f"HF Spaces response: {response.status_code}")
            
        except Exception as e:
            print(f"Error forwarding to HF Spaces: {e}")