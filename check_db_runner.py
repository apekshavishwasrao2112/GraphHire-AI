import os
import sys
ROOT = os.path.dirname(os.path.abspath(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from backend.app import app
from backend.database import db

client = app.test_client()
print('Flask app imported')
# Check DB ping
try:
    ping = db.ping()
except Exception as e:
    ping = False
    print('DB ping raised exception:', repr(e))
print('DB ping result:', ping)
if ping:
    qlist = [
        ('developers','MATCH (d:Developer) RETURN count(d) AS c'),
        ('companies','MATCH (c:Company) RETURN count(c) AS c'),
        ('projects','MATCH (p:Project) RETURN count(p) AS c'),
        ('skills','MATCH (s:Skill) RETURN count(s) AS c'),
        ('technologies','MATCH (t:Technology) RETURN count(t) AS c'),
        ('relationships','MATCH ()-[r]->() RETURN count(r) AS c'),
    ]
    for name,q in qlist:
        try:
            res = db.run_query(q)
            print(name, res[0].get('c'))
        except Exception as e:
            print(f'Query {name} raised', repr(e))
    # sample developers
    try:
        sample = db.run_query('MATCH (d:Developer) RETURN d.full_name AS full_name, d.email AS email, d.years_of_experience AS y LIMIT 5')
        print('sample developers:', sample)
    except Exception as e:
        print('sample query raised', repr(e))
# Test HTTP endpoints
print('HTTP GET / ->', client.get('/').status_code, client.get('/').get_json())
print('HTTP GET /dashboard ->', client.get('/dashboard').status_code, client.get('/dashboard').get_json())
print('HTTP GET /developers ->', client.get('/developers').status_code, client.get('/developers').get_json())
print('HTTP GET /search?q=React ->', client.get('/search', query_string={'q':'React'}).status_code, client.get('/search', query_string={'q':'React'}).get_json())
