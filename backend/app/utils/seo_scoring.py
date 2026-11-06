from typing import Dict, List, Tuple
import re
from bs4 import BeautifulSoup


class SEOValidator:
    def __init__(self):
        self.min_title_length = 30
        self.max_title_length = 60
        self.min_meta_desc_length = 120
        self.max_meta_desc_length = 160
        self.min_content_length = 1000
        self.min_faq_count = 3

    def validate_blog(self, blog_data: Dict) -> Dict:
        """Validate blog content against SEO best practices"""
        passed_checks = []
        failed_checks = []
        suggestions = []

        # Validate SEO title
        title_check = self._validate_title(blog_data.get('meta_title', ''))
        if title_check[0]:
            passed_checks.append(title_check[1])
        else:
            failed_checks.append(title_check[1])
            suggestions.append(title_check[2])

        # Validate meta description
        meta_check = self._validate_meta_description(blog_data.get('meta_description', ''))
        if meta_check[0]:
            passed_checks.append(meta_check[1])
        else:
            failed_checks.append(meta_check[1])
            suggestions.append(meta_check[2])

        # Validate URL slug
        slug_check = self._validate_slug(blog_data.get('slug', ''))
        if slug_check[0]:
            passed_checks.append(slug_check[1])
        else:
            failed_checks.append(slug_check[1])
            suggestions.append(slug_check[2])

        # Validate H1
        h1_check = self._validate_h1(blog_data.get('h1', ''), blog_data.get('meta_title', ''))
        if h1_check[0]:
            passed_checks.append(h1_check[1])
        else:
            failed_checks.append(h1_check[1])
            suggestions.append(h1_check[2])

        # Validate content structure
        content = blog_data.get('content', '')
        structure_check = self._validate_content_structure(content)
        if structure_check[0]:
            passed_checks.append(structure_check[1])
        else:
            failed_checks.append(structure_check[1])
            suggestions.append(structure_check[2])

        # Validate keyword placement
        primary_keyword = blog_data.get('primary_keyword', '')
        keyword_check = self._validate_keyword_placement(content, primary_keyword, blog_data.get('h1', ''))
        if keyword_check[0]:
            passed_checks.append(keyword_check[1])
        else:
            failed_checks.append(keyword_check[1])
            suggestions.append(keyword_check[2])

        # Validate content length
        length_check = self._validate_content_length(content)
        if length_check[0]:
            passed_checks.append(length_check[1])
        else:
            failed_checks.append(length_check[1])
            suggestions.append(length_check[2])

        # Validate FAQ
        faq_check = self._validate_faq(blog_data.get('faq', []))
        if faq_check[0]:
            passed_checks.append(faq_check[1])
        else:
            failed_checks.append(faq_check[1])
            suggestions.append(faq_check[2])

        # Validate CTA
        cta_check = self._validate_cta(content)
        if cta_check[0]:
            passed_checks.append(cta_check[1])
        else:
            failed_checks.append(cta_check[1])
            suggestions.append(cta_check[2])

        # Calculate score
        total_checks = len(passed_checks) + len(failed_checks)
        score = (len(passed_checks) / total_checks * 100) if total_checks > 0 else 0

        return {
            'passed': score >= 70,
            'score': round(score, 2),
            'passed_checks': passed_checks,
            'failed_checks': failed_checks,
            'suggestions': suggestions
        }

    def _validate_title(self, title: str) -> Tuple[bool, str, str]:
        """Validate SEO title length"""
        length = len(title)
        if self.min_title_length <= length <= self.max_title_length:
            return True, f"SEO title length optimal ({length} chars)", ""
        else:
            return False, f"SEO title length ({length} chars)", f"Keep title between {self.min_title_length}-{self.max_title_length} characters"

    def _validate_meta_description(self, meta_desc: str) -> Tuple[bool, str, str]:
        """Validate meta description length"""
        length = len(meta_desc)
        if self.min_meta_desc_length <= length <= self.max_meta_desc_length:
            return True, f"Meta description length optimal ({length} chars)", ""
        else:
            return False, f"Meta description length ({length} chars)", f"Keep description between {self.min_meta_desc_length}-{self.max_meta_desc_length} characters"

    def _validate_slug(self, slug: str) -> Tuple[bool, str, str]:
        """Validate URL slug"""
        if slug and re.match(r'^[a-z0-9-]+$', slug) and len(slug) <= 100:
            return True, "URL slug is SEO-friendly", ""
        else:
            return False, "URL slug format", "Use lowercase letters, numbers, and hyphens only"

    def _validate_h1(self, h1: str, title: str) -> Tuple[bool, str, str]:
        """Validate H1 uniqueness"""
        if h1 and h1 != title:
            return True, "H1 is unique from title", ""
        else:
            return False, "H1 uniqueness", "H1 should differ from meta title"

    def _validate_content_structure(self, content: str) -> Tuple[bool, str, str]:
        """Validate heading hierarchy"""
        if '<h2>' in content or '<h2' in content:
            return True, "Content has proper heading structure", ""
        else:
            return False, "Heading structure", "Add H2 and H3 subheadings for better structure"

    def _validate_keyword_placement(self, content: str, keyword: str, h1: str) -> Tuple[bool, str, str]:
        """Validate keyword placement"""
        if not keyword:
            return False, "Keyword placement", "Primary keyword not defined"

        content_lower = content.lower()
        keyword_lower = keyword.lower()
        h1_lower = h1.lower()

        # Check if keyword is in H1
        keyword_in_h1 = keyword_lower in h1_lower

        # Check keyword frequency in content
        keyword_count = content_lower.count(keyword_lower)

        if keyword_in_h1 and keyword_count >= 3:
            return True, "Keyword placement is natural", ""
        else:
            return False, "Keyword placement", "Ensure keyword appears in H1 and naturally throughout content"

    def _validate_content_length(self, content: str) -> Tuple[bool, str, str]:
        """Validate content length"""
        # Remove HTML tags for word count
        text = re.sub(r'<[^>]+>', '', content)
        word_count = len(text.split())

        if word_count >= self.min_content_length / 5:  # Approximate words
            return True, f"Content length is sufficient ({word_count} words)", ""
        else:
            return False, f"Content length ({word_count} words)", f"Aim for at least {self.min_content_length // 5} words"

    def _validate_faq(self, faq: List) -> Tuple[bool, str, str]:
        """Validate FAQ section"""
        if faq and len(faq) >= self.min_faq_count:
            return True, f"FAQ section present ({len(faq)} questions)", ""
        else:
            return False, "FAQ section", f"Add at least {self.min_faq_count} frequently asked questions"

    def _validate_cta(self, content: str) -> Tuple[bool, str, str]:
        """Validate Call-to-Action"""
        content_lower = content.lower()
        cta_indicators = ['enroll', 'join', 'contact', 'register', 'learn more', 'get started']

        if any(indicator in content_lower for indicator in cta_indicators):
            return True, "CTA present in content", ""
        else:
            return False, "Call-to-action", "Add a clear CTA promoting the course"


# Singleton instance
seo_validator = SEOValidator()
