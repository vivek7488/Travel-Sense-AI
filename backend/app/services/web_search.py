import httpx
from app.core.config import TAVILY_API_KEY

def search_web_reviews(property_name, city):
    query = property_name + " " + city + " hotel reviews"
    try:
        r = httpx.post(
            "https://api.tavily.com/search",
            json={
                "api_key": TAVILY_API_KEY,
                "query": query,
                "search_depth": "basic",
                "max_results": 5
            },
            timeout=15
        )
        data = r.json()
        results = data.get("results", [])
        reviews = []
        for result in results:
            content = result.get("content", "")
            if len(content) > 100:
                reviews.append(content)
        return reviews
    except Exception as e:
        return []
