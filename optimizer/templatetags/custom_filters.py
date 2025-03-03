from django import template

register = template.Library()  # Register custom filters

@register.filter
def get_item(dictionary, key):
    """Custom filter to get an item from a dictionary."""
    return dictionary.get(key, "")  # Return value or empty string if key not found
