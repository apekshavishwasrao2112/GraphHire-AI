import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from backend.app import app


if __name__ == '__main__':
    client = app.test_client()
    res = client.get('/dashboard')
    print('STATUS', res.status_code)
    try:
        import json

        print(json.dumps(res.get_json(), indent=2))
    except Exception:
        print(res.get_data(as_text=True))
