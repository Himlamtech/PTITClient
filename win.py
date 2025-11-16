#!/usr/bin/env python3
import json
import urllib.request
import urllib.error
import ssl
import sys
import os

# Windows encoding fix
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')

API_KEY = "sk-PpSk3Dey0p1SDywqy5dNbzrMGcw4aUzEjzFsIMgn6a9"
MODEL = "gpt-5.1"
URL = "https://api.yescale.io/v1/chat/completions"

history = []

# SSL fix for Windows
try:
    ssl_ctx = ssl.create_default_context()
    ssl_ctx.check_hostname = False
    ssl_ctx.verify_mode = ssl.CERT_NONE
except:
    ssl_ctx = ssl._create_unverified_context()

def chat(msg):
    history.append({"role": "user", "content": msg})
    data = json.dumps({"model": MODEL, "messages": history, "max_tokens": 4096}).encode('utf-8')
    req = urllib.request.Request(URL, data=data, 
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {API_KEY}"},
        method='POST')
    
    try:
        with urllib.request.urlopen(req, context=ssl_ctx, timeout=60) as r:
            res = json.loads(r.read().decode('utf-8'))
            ans = res["choices"][0]["message"]["content"]
            history.append({"role": "assistant", "content": ans})
            return ans
    except urllib.error.HTTPError as e:
        history.pop()
        try:
            err = json.loads(e.read().decode('utf-8'))
            return f"Error {e.code}: {err.get('error', {}).get('message', str(e))}"
        except:
            return f"Error {e.code}: {e.reason}"
    except Exception as e:
        history.pop()
        return f"Error: {str(e)}"

print("AI Chat (Windows Compatible)")
print("=" * 50)
print("Commands: exit/quit, clear")
print("=" * 50 + "\n")

while True:
    try:
        inp = input("You: ").strip()
        if not inp: 
            continue
        if inp.lower() in ['exit', 'quit']: 
            print("Goodbye!")
            break
        if inp.lower() == 'clear': 
            history.clear()
            print("History cleared!\n")
            continue
        print(f"AI: {chat(inp)}\n")
    except KeyboardInterrupt:
        print("\nGoodbye!")
        break
    except Exception as e:
        print(f"Error: {e}\n")
