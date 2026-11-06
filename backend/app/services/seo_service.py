import aiohttp
from typing import List, Dict, Optional
from datetime import datetime
from pytrends.request import TrendReq
import asyncio


class SEOResearchService:
    def __init__(self):
        self.pytrends = None
        self._initialize_pytrends()

    def _initialize_pytrends(self):
        """Initialize PyTrends for Google Trends data"""
        try:
            self.pytrends = TrendReq(hl='en-US', tz=360)
        except Exception as e:
            print(f"Warning: Could not initialize PyTrends: {str(e)}")
            self.pytrends = None

    async def get_search_suggestions(self, seed_keyword: str) -> List[str]:
        """Get search suggestions from Google"""
        suggestions = []

        try:
            if self.pytrends:
                # Get related queries
                self.pytrends.build_payload([seed_keyword], timeframe='today 12-m', geo='IN')
                related = self.pytrends.related_queries()

                if seed_keyword in related and related[seed_keyword]['top'] is not None:
                    top_queries = related[seed_keyword]['top']['query'].tolist()
                    suggestions.extend(top_queries[:10])
        except Exception as e:
            print(f"PyTrends error: {str(e)}")

        # Add manual suggestions specific to digital marketing in Coimbatore
        manual_suggestions = [
            "digital marketing course in coimbatore",
            "best digital marketing institute in coimbatore",
            "digital marketing training in coimbatore",
            "seo course in coimbatore",
            "digital marketing course fees in coimbatore",
            "digital marketing course with placement in coimbatore",
            "digital marketing classes for beginners",
            "social media marketing course coimbatore",
            "google ads training coimbatore",
            "content marketing course coimbatore"
        ]

        suggestions.extend(manual_suggestions)

        # Remove duplicates and return unique suggestions
        return list(set(suggestions))[:15]

    async def get_keyword_interest(self, keyword: str) -> Dict:
        """Get relative interest score for a keyword using Google Trends"""
        result = {
            "keyword": keyword,
            "interest_score": "unavailable",
            "data_confidence": "unavailable",
            "source": None,
            "timestamp": datetime.utcnow().isoformat()
        }

        try:
            if self.pytrends:
                self.pytrends.build_payload([keyword], timeframe='today 12-m', geo='IN')
                interest_over_time = self.pytrends.interest_over_time()

                if not interest_over_time.empty and keyword in interest_over_time.columns:
                    avg_interest = interest_over_time[keyword].mean()
                    result["interest_score"] = f"{int(avg_interest)}/100"
                    result["data_confidence"] = "verified"
                    result["source"] = "Google Trends"
        except Exception as e:
            print(f"Error getting interest for {keyword}: {str(e)}")

        return result

    def calculate_internal_score(self, keyword: str, business_category: str) -> float:
        """Calculate internal relevance and opportunity score"""
        score = 50.0  # Base score

        # Relevance scoring
        keyword_lower = keyword.lower()
        category_lower = business_category.lower()

        # High relevance terms
        if "digital marketing" in keyword_lower:
            score += 20
        if "coimbatore" in keyword_lower:
            score += 15
        if "course" in keyword_lower or "training" in keyword_lower:
            score += 10
        if "best" in keyword_lower or "top" in keyword_lower:
            score += 5
        if "placement" in keyword_lower:
            score += 5
        if "seo" in keyword_lower or "social media" in keyword_lower:
            score += 5

        # Intent scoring
        if "fees" in keyword_lower or "cost" in keyword_lower:
            score += 8  # Commercial intent
        if "near me" in keyword_lower:
            score += 7  # Local intent

        return min(score, 100.0)

    async def analyze_keyword_batch(self, keywords: List[str], business_category: str) -> List[Dict]:
        """Analyze a batch of keywords"""
        results = []

        for keyword in keywords:
            # Get trends data
            trends_data = await self.get_keyword_interest(keyword)

            # Calculate internal score
            internal_score = self.calculate_internal_score(keyword, business_category)

            # Determine search intent
            intent = self._determine_search_intent(keyword)

            # Estimate competition
            competition = self._estimate_competition(keyword)

            keyword_data = {
                "keyword": keyword,
                "search_intent": intent,
                "relevance": self._score_to_label(internal_score),
                "competition": competition,
                "search_volume": trends_data["interest_score"],
                "data_confidence": trends_data["data_confidence"],
                "source": trends_data["source"],
                "opportunity_score": internal_score,
                "timestamp": trends_data["timestamp"]
            }

            results.append(keyword_data)

            # Small delay to avoid rate limiting
            await asyncio.sleep(0.5)

        return results

    def _determine_search_intent(self, keyword: str) -> str:
        """Determine search intent based on keyword analysis"""
        keyword_lower = keyword.lower()

        if any(word in keyword_lower for word in ["best", "top", "review", "vs", "compare"]):
            return "informational"
        elif any(word in keyword_lower for word in ["fees", "cost", "price", "enroll", "join"]):
            return "transactional"
        elif any(word in keyword_lower for word in ["near me", "in coimbatore", "location"]):
            return "local"
        elif any(word in keyword_lower for word in ["how to", "what is", "learn"]):
            return "educational"
        else:
            return "informational"

    def _estimate_competition(self, keyword: str) -> str:
        """Estimate competition level based on keyword characteristics"""
        keyword_lower = keyword.lower()
        word_count = len(keyword_lower.split())

        # Long-tail keywords typically have lower competition
        if word_count >= 5:
            return "low"
        elif word_count >= 3:
            # Location-specific keywords typically have medium competition
            if "coimbatore" in keyword_lower:
                return "medium"
            return "medium-high"
        else:
            return "high"

    def _score_to_label(self, score: float) -> str:
        """Convert numerical score to relevance label"""
        if score >= 80:
            return "very high"
        elif score >= 65:
            return "high"
        elif score >= 50:
            return "medium"
        else:
            return "low"


# Singleton instance
seo_service = SEOResearchService()
