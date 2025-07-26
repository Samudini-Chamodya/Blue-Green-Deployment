import requests
import sys

def test_health_check(port):
    try:
        url = f'http://localhost:{port}/'
        response = requests.get(url, timeout=5)
        if response.status_code == 200 and 'Environment' in response.text:
            print(f"Health check passed for port {port}")
            return True
        print(f"Health check failed for port {port}: {response.status_code} {response.text}")
        return False
    except Exception as e:
        print(f"Health check failed for port {port}: {str(e)}")
        return False

if __name__ == '__main__':
    port = int(sys.argv[1])
    if not test_health_check(port):
        sys.exit(1)