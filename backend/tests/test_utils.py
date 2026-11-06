"""
Basic tests for SEO Agent functionality
"""
import pytest
from app.utils.slug import generate_slug, validate_slug, ensure_unique_slug
from app.utils.seo_scoring import seo_validator


def test_slug_generation():
    """Test slug generation"""
    title = "Digital Marketing Course in Coimbatore"
    slug = generate_slug(title)
    assert slug == "digital-marketing-course-in-coimbatore"
    assert validate_slug(slug) is True


def test_slug_validation():
    """Test slug validation"""
    assert validate_slug("valid-slug-123") is True
    assert validate_slug("Invalid Slug") is False
    assert validate_slug("invalid_slug") is False


def test_unique_slug_generation():
    """Test unique slug generation"""
    existing = ["test-slug", "test-slug-1"]
    unique = ensure_unique_slug("test-slug", existing)
    assert unique == "test-slug-2"


def test_seo_validation():
    """Test SEO validation"""
    blog_data = {
        "meta_title": "Digital Marketing Course in Coimbatore - Learn SEO",
        "meta_description": "Discover the best digital marketing course in Coimbatore. Learn SEO, social media marketing, and more with expert trainers and placement assistance.",
        "slug": "digital-marketing-course-coimbatore",
        "h1": "Complete Digital Marketing Training in Coimbatore",
        "primary_keyword": "digital marketing course in coimbatore",
        "content": "<h2>Introduction</h2><p>Digital marketing is essential in today's world. This comprehensive course covers SEO, social media marketing, and more.</p>" * 10,
        "faq": [
            {"question": "What is digital marketing?", "answer": "Digital marketing involves online promotion."},
            {"question": "How long is the course?", "answer": "The course is 3 months long."},
            {"question": "Is placement provided?", "answer": "Yes, we provide placement assistance."},
            {"question": "What is the fee?", "answer": "Contact us for fee details."},
            {"question": "Do you offer certifications?", "answer": "Yes, we provide certifications."},
        ]
    }

    result = seo_validator.validate_blog(blog_data)
    assert "score" in result
    assert "passed_checks" in result
    assert "failed_checks" in result
    assert result["score"] > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
