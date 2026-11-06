import aiohttp
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
from app.config import settings


class WebsiteAnalyzer:
    def __init__(self):
        self.reference_website = settings.REFERENCE_WEBSITE
        self.business_name = settings.BUSINESS_NAME
        self.business_category = settings.BUSINESS_CATEGORY

    async def fetch_website_content(self) -> Optional[str]:
        """Fetch content from the reference website"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    self.reference_website,
                    timeout=aiohttp.ClientTimeout(total=10),
                    headers={'User-Agent': 'Mozilla/5.0'}
                ) as response:
                    if response.status == 200:
                        return await response.text()
        except Exception as e:
            print(f"Error fetching website: {str(e)}")
        return None

    async def extract_courses(self) -> List[str]:
        """Extract course information from website"""
        html_content = await self.fetch_website_content()
        courses = []

        if html_content:
            try:
                soup = BeautifulSoup(html_content, 'html.parser')

                # Look for common course-related elements
                course_keywords = ['digital marketing', 'seo', 'social media', 'google ads', 'content marketing']

                # Search in text content
                text_content = soup.get_text().lower()
                for keyword in course_keywords:
                    if keyword in text_content:
                        courses.append(keyword.title())
            except Exception as e:
                print(f"Error parsing website: {str(e)}")

        # Add default courses if extraction fails
        if not courses:
            courses = [
                "Digital Marketing Course",
                "SEO Training",
                "Social Media Marketing",
                "Google Ads Certification",
                "Content Marketing"
            ]

        return courses

    async def get_business_context(self) -> Dict:
        """Get business context for content generation"""
        courses = await self.extract_courses()

        return {
            "business_name": self.business_name,
            "business_category": self.business_category,
            "location": settings.BUSINESS_LOCATION,
            "courses": courses,
            "website": self.reference_website,
            "specialization": "Digital Marketing Training and Placement",
            "key_offerings": [
                "Hands-on practical training",
                "Industry expert trainers",
                "Live project experience",
                "Placement assistance",
                "Certification programs"
            ]
        }

    async def get_internal_link_suggestions(self, keyword: str) -> List[str]:
        """Suggest internal links based on keyword"""
        keyword_lower = keyword.lower()

        link_suggestions = []

        # Homepage
        link_suggestions.append(f"{self.reference_website}|Home")

        # Course-specific links
        if "seo" in keyword_lower:
            link_suggestions.append(f"{self.reference_website}/courses/seo|SEO Course")
        if "social media" in keyword_lower:
            link_suggestions.append(f"{self.reference_website}/courses/social-media|Social Media Marketing Course")
        if "google ads" in keyword_lower:
            link_suggestions.append(f"{self.reference_website}/courses/google-ads|Google Ads Training")

        # General links
        link_suggestions.append(f"{self.reference_website}/courses|All Courses")
        link_suggestions.append(f"{self.reference_website}/about|About Us")
        link_suggestions.append(f"{self.reference_website}/contact|Contact Us")

        return link_suggestions[:5]


# Singleton instance
website_analyzer = WebsiteAnalyzer()
