from http.server import BaseHTTPRequestHandler
import json
import asyncio
from bot import HybridBot

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        """Handle POST requests from Telegram webhook"""
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            update_data = json.loads(post_data.decode('utf-8'))
            
            # Process the update
            asyncio.create_task(self.process_update(update_data))
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'status': 'ok'}).encode())
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': str(e)}).encode())
    
    async def process_update(self, update_data):
        """Process Telegram update"""
        try:
            bot = HybridBot()
            await bot.application.process_update(update_data)
        except Exception as e:
            print(f"Error processing update: {e}")
    
    def do_GET(self):
        """Health check endpoint"""
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({'status': 'healthy', 'service': 'vercel-bot'}).encode())
