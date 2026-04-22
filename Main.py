import urllib.request
import re
from html import unescape

def scrape_titles(url):
    try:
        # HTTPリクエストの送信
        with urllib.request.urlopen(url) as response:
            html = response.read().decode('utf-8')
        
        # HTMLエンティティのデコード
        html = unescape(html)
        
        # <title>タグの抽出（正規表現）
        title_pattern = re.compile(r'<title>(.*?)</title>', re.IGNORECASE | re.DOTALL)
        title = title_pattern.search(html)
        
        # <a>タグ（リンク）のテキストとURLの抽出
        links = re.findall(r'<a\s+(?:[^>]*?\s+)?href="([^"]*)"[^>]*>(.*?)</a>', html)
        
        return {
            "page_title": title.group(1).strip() if title else "No Title Found",
            "links": [{"url": l[0], "text": re.sub(r'<[^>]*>', '', l[1]).strip()} for l in links]
        }

    except Exception as e:
        return {"error": str(e)}

# 実行例
if __name__ == "__main__":
    target_url = "https://www.python.org"
    result = scrape_titles(target_url)
    
    print(f"Title: {result['page_title']}")
    for link in result['links'][:5]:  # 最初の5件のみ表示
        print(f"Link: {link['text']} ({link['url']})")
