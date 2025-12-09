import requests
from bs4 import BeautifulSoup

def scrape_article_text(url):
    try:
        print(f"Scraping: {url}")  
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        print(f"Status Code: {response.status_code}") 
        soup = BeautifulSoup(response.text, "html.parser")

        # Remove unnecessary tags
        for tag in soup(["script", "style", "noscript", "header", "footer", "aside", "nav"]):
            tag.decompose()

        content_block = soup.find("article") or soup.find("main") or soup.body
        paragraphs = content_block.find_all("p")

        cleaned = []
        for p in paragraphs:
            text = p.get_text(strip=True)
            if len(text) > 30 and not any(x in text.lower() for x in [
                "terms & conditions", "comments have to", "register", "login",
                "older comments", "vuukle"
            ]):
                cleaned.append(text)

        full_text = "\n".join(cleaned)
        print(f"Extracted length: {len(full_text)}") 

        if not full_text or len(full_text) < 100:
            return {"error": "Not enough content found"}

        return {"text": full_text[:10000]}  

    except Exception as e:
        return {"error": str(e)}
