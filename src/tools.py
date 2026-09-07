from langchain_tavily import TavilySearch
from langchain.tools import tool
from bs4 import BeautifulSoup
import requests, trafilatura, re
from readability import Document
from dotenv import load_dotenv
load_dotenv()

# initiate tavily
tavily = TavilySearch(
    max_results=5,
    topic="general"
)


@tool
def scrape_url(url: str):
    """
    Scrape and extract clean readable content from a URL
    Uses multiple extraction strategies for better reliability
    """
    
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        
        html = response.text
        
        #_________________________________
        # Strategy 1 - trafilatura (Best for articles/blogs)
        #__________________________________
        
        extracted = trafilatura.extract(
            html, 
            output_format="json", 
            with_metadata=True, 
            include_comments=False, 
            include_tables=False
            )
        
        if extracted and len(extracted.strip()) > 200:
            cleaned = re.sub(r'\s+', ' ', extracted)
            return cleaned[:5000]
        
        
        #______________________________________
        # Strategy 2 - Readability
        #____________________________________
        doc = Document(html)
        clean_html = doc.summary()
        
        soup = BeautifulSoup(clean_html, "html.parser")
        
        # strip these tags and return the remaining
        for tag in soup([
            "script",
            "style",
            "nav",
            "footer",
            "header",
            "aside",
            "form"
        ]):
            tag.decompose()
            
        text = soup.get_text(separator=" " , strip=True)
        
        if text and len(text.strip()) > 200:
            cleaned = re.sub(r'\s+', ' ', text)
            return cleaned[:5000]
        
        #_______________________________________
        # Strategy 3 - Fallback full page extraction
        #________________________________________
        soup = BeautifulSoup(html, "html.parser")
            
        for tag in soup([
            "script",
            "style",
            "nav",
            "footer",
            "header",
            "aside",
            "form"
        ]):
            tag.decompose()
            
        text = soup.get_text(separator=" " , strip=True)
        
        cleaned = re.sub(r'\s+', ' ', text)
        
        if cleaned:
            return cleaned[:5000]
        
        return "Could not extract meaningful content from the page"
    
    except requests.exceptions.Timeout:
        return "Request timed out while scraping the URL"
    
    except requests.exceptions.HTTPError as e:
        return f"HTTP error occurred: {str(e)}"
    except Exception as e:
        return f"Could not scrape URL: {str(e)}"