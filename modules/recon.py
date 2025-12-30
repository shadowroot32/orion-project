import requests

class ReconModule:
    def __init__(self, logger):
        self.logger = logger

    def scan(self, target_url):
        try:
            # Menggunakan timeout agar tidak hang
            response = requests.get(target_url, timeout=10)
            headers = response.headers
            
            # Mendeteksi teknologi dasar
            data = {
                "Server": headers.get("Server", "Hidden/Unknown"),
                "X-Powered-By": headers.get("X-Powered-By", "Hidden"),
                "Content-Security-Policy": headers.get("Content-Security-Policy", "Not Set (High Risk)"),
                "X-Frame-Options": headers.get("X-Frame-Options", "Not Set (Clickjacking Risk)")
            }
            return {"status": "success", "data": data}
        except Exception as e:
            return {"status": "error", "message": str(e)}
