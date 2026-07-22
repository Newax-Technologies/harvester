import httpx
from bs4 import BeautifulSoup

def analyze_website(url: str) -> str:
    """
    Fetches the website and extracts text to be analyzed for pains.
    In phase 1 this is a basic fetch.
    """
    if not url:
        return ""
        
    # Ensure scheme
    if not url.startswith("http"):
        url = "https://" + url
        
    try:
        with httpx.Client(timeout=10.0, follow_redirects=True) as client:
            response = client.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            
            # Remove scripts and styles
            for script in soup(["script", "style"]):
                script.extract()
                
            text = soup.get_text(separator=" ", strip=True)
            return text
            
    except Exception as e:
        print(f"Error fetching website {url}: {e}")
        return ""
