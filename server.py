import http.server
import socketserver
import json
import os
import sys

PORT = 8080
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class DashboardHTTPHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def do_POST(self):
        if self.path == '/update':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                # Validate JSON format
                data = json.loads(post_data.decode('utf-8'))
                
                # Write to predictions.json
                json_path = os.path.join(DIRECTORY, 'predictions.json')
                with open(json_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                
                # Send success response
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "success", "message": "predictions.json updated successfully"}).encode('utf-8'))
                print("[Server] Successfully updated predictions.json")
            except Exception as e:
                # Handle error
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode('utf-8'))
                print(f"[Error] Failed to update predictions.json: {e}", file=sys.stderr)
        else:
            self.send_response(404)
            self.end_headers()

    def do_OPTIONS(self):
        # Handle CORS preflight
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

def main():
    # Force change directory to where the script is located
    os.chdir(DIRECTORY)
    
    # Configure socket server to reuse addresses
    socketserver.TCPServer.allow_reuse_address = True
    
    with socketserver.TCPServer(("", PORT), DashboardHTTPHandler) as httpd:
        print(f"\n========================================================")
        print(f"⚽ FIFA 2026 World Cup Predictions Tracker is running!")
        print(f"🌐 Dashboard URL: http://localhost:{PORT}/index.html")
        print(f"📂 Project Path: {DIRECTORY}")
        print(f"========================================================\n")
        print("Press Ctrl+C to stop the server.")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server. Goodbye!")
            sys.exit(0)

if __name__ == '__main__':
    main()
