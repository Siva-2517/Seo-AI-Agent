from slugify import slugify
import re


def generate_slug(title: str) -> str:
    """Generate a URL-friendly slug from title"""
    return slugify(title, max_length=100)


def validate_slug(slug: str) -> bool:
    """Validate slug format"""
    # Check if slug contains only allowed characters
    pattern = r'^[a-z0-9-]+$'
    return bool(re.match(pattern, slug))


def ensure_unique_slug(base_slug: str, existing_slugs: list) -> str:
    """Ensure slug is unique by appending number if needed"""
    if base_slug not in existing_slugs:
        return base_slug

    counter = 1
    while True:
        new_slug = f"{base_slug}-{counter}"
        if new_slug not in existing_slugs:
            return new_slug
        counter += 1
