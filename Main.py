import urllib.request
import re
from html import unescape

def scrape_titles(url):
    try:
        # User-Agentを設定してブロックを回避
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            html = response.read().decode('utf-8')
        
        html = unescape(html)
        title_pattern = re.compile(r'<title>(.*?)</title>', re.IGNORECASE | re.DOTALL)
        title = title_pattern.search(html)
        
        links = re.findall(r'<a\s+(?:[^>]*?\s+)?href="([^"]*)"[^>]*>(.*?)</a>', html)
        
        return {
            "page_title": title.group(1).strip() if title else "No Title Found",
            "links": [{"url": l[0], "text": re.sub(r'<[^>]*>', '', l[1]).strip()} for l in links]
        }
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    target_url = "https://www.python.org"
    result = scrape_titles(target_url)
    
    if "error" in result:
        print(f"Error: {result['error']}")
    else:
        print(f"Title: {result['page_title']}\n")
        for link in result['links'][:10]:
            print(f"- {link['text']}: {link['url']}")

    # --- ここで一時停止 ---
    print("\n" + "-"*30)
    input("Enterキーを押すと終了します...")
