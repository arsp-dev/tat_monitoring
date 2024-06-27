# custom_filters.py

from django import template

register = template.Library()

@register.filter
def get_disk_value(site_disk, attribute_name):
    return getattr(site_disk, attribute_name, '')  # Return an empty string if attribute does not exist


@register.filter
def attr(obj, attr_name):
    return getattr(obj, attr_name, None)


@register.filter
def process_field_name(value):
    if 'ris' in value.lower():
        return 'RIS'
    else:
        return value[:3].upper()

@register.filter
def skip_ris(value):
    return 'ris' not in value.lower()
