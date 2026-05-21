from django import template
from django.utils.safestring import mark_safe

register = template.Library()

STORE_ICONS = {
    'litres': (
        '<svg width="20" height="20" viewBox="0 0 24 24" fill="none">'
        '<path d="M12 3C12 3 6 4.5 3 4.5V18C6 18 12 16.5 12 16.5C12 16.5 18 18 21 18V4.5C18 4.5 12 3 12 3Z"'
        ' stroke="white" stroke-width="1.5" fill="rgba(255,255,255,0.15)"/>'
        '<line x1="12" y1="3" x2="12" y2="16.5" stroke="white" stroke-width="1.2" opacity="0.6"/>'
        '<path d="M5.5 9.5H8.5V13.5H5.5V9.5ZM5.5 13.5H9" stroke="white" stroke-width="1.2" stroke-linecap="round"/>'
        '<path d="M13 9.5V13.5H14.2V12H15.8V13.5H17V9.5H15.8V11H14.2V9.5H13Z" fill="white"/>'
        '</svg>'
    ),
    'ozon': (
        '<svg width="20" height="20" viewBox="0 0 24 24" fill="none">'
        '<ellipse cx="12" cy="12" rx="9" ry="9" stroke="white" stroke-width="1.5" fill="rgba(255,255,255,0.15)"/>'
        '<text x="12" y="15.5" text-anchor="middle" font-family="Arial Black,Arial" font-weight="900"'
        ' font-size="6.5" fill="white" letter-spacing="0.3">OZON</text>'
        '</svg>'
    ),
    'yandex': (
        '<svg width="20" height="20" viewBox="0 0 24 24" fill="none">'
        '<rect x="3" y="3" width="18" height="18" rx="5" fill="rgba(255,255,255,0.15)" stroke="white" stroke-width="1.5"/>'
        '<text x="12" y="17" text-anchor="middle" font-family="Arial" font-weight="bold"'
        ' font-size="11" fill="white">\u044f</text>'
        '</svg>'
    ),
    'chitai': (
        '<svg width="20" height="20" viewBox="0 0 24 24" fill="none">'
        '<path d="M4 5h16M4 9h16M4 13h10" stroke="white" stroke-width="1.8" stroke-linecap="round"/>'
        '<circle cx="17.5" cy="17.5" r="3.5" fill="rgba(255,255,255,0.2)" stroke="white" stroke-width="1.5"/>'
        '<path d="M16.5 17.5l1 1 1.8-1.8" stroke="white" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"/>'
        '</svg>'
    ),
    'labirint': (
        '<svg width="20" height="20" viewBox="0 0 24 24" fill="none">'
        '<rect x="3" y="3" width="18" height="18" rx="3" stroke="white" stroke-width="1.5" fill="rgba(255,255,255,0.1)"/>'
        '<path d="M7 7h10v4H7V7ZM7 13h6" stroke="white" stroke-width="1.4" stroke-linecap="round"/>'
        '<path d="M15 13v4" stroke="white" stroke-width="1.4" stroke-linecap="round"/>'
        '<path d="M7 17h6" stroke="white" stroke-width="1.4" stroke-linecap="round"/>'
        '</svg>'
    ),
    'amazon': (
        '<svg width="20" height="20" viewBox="0 0 24 24" fill="none">'
        '<text x="12" y="12" text-anchor="middle" font-family="Arial" font-weight="bold"'
        ' font-size="6.5" fill="white" letter-spacing="0.2">amazon</text>'
        '<path d="M5 15.5 Q12 19.5 19 15.5" stroke="white" stroke-width="1.5" stroke-linecap="round" fill="none"/>'
        '<path d="M17.5 13.5 L19.5 15.5 L17.5 16.5" stroke="white" stroke-width="1.3"'
        ' stroke-linecap="round" stroke-linejoin="round" fill="none"/>'
        '</svg>'
    ),
    'generic': (
        '<svg width="20" height="20" viewBox="0 0 24 24" fill="none">'
        '<path d="M6 2L3 6v14a2 2 0 002 2h14a2 2 0 002-2V6l-3-4z"'
        ' stroke="white" stroke-width="1.5" fill="rgba(255,255,255,0.15)"/>'
        '<line x1="3" y1="6" x2="21" y2="6" stroke="white" stroke-width="1.5"/>'
        '<path d="M16 10a4 4 0 01-8 0" stroke="white" stroke-width="1.5"/>'
        '</svg>'
    ),
}


@register.simple_tag
def store_icon(icon_key):
    svg = STORE_ICONS.get(icon_key, '')
    if not svg:
        return mark_safe('')
    return mark_safe(f'<span class="buy-btn__icon" aria-hidden="true">{svg}</span>')
