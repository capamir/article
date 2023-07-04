from django import template
register = template.Library()

@register.filter
def filter_review_body(values):
    return values.exclude(body='').count()