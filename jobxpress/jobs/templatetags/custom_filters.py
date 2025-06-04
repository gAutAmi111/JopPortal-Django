from django import template

register = template.Library()

@register.filter
def split_by_comma(value):
    """
    Splits a comma-separated string into a list of trimmed items.
    Usage in template: {{ job.requirements|split_by_comma }}
    """
    if not value:
        return []  # Return empty list if value is None or empty string
    return [item.strip() for item in value.split(',') if item.strip()]
