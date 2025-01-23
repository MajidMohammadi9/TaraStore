from django import template
from django.utils.translation import get_language
from babel.dates import format_datetime
from jalali_date.templatetags.jalali_tags import to_jalali
from datetime import datetime

register = template.Library()


@register.filter
def translate_number(value):
    value = str(value)
    language = get_language()
    english_to_persian = value.maketrans("0123456789", "۰۱۲۳۴۵۶۷۸۹")
    english_to_arabic = value.maketrans("0123456789", "٠١٢٣٤٥٦٧٨٩")

    if language == 'fa':
        return value.translate(english_to_persian)
    elif language == 'ar':
        return value.translate(english_to_arabic)

    return value


@ register.filter
def translate_datetime(value):
    LOCALES = {
        'en': 'en_US',
        'fa': 'fa_IR',
        'ar': 'ar_SA',
    }

    language = get_language()
    locale = LOCALES.get(language, 'en_US')

    if language == 'fa':
        return to_jalali(value, '%Y/%m/%d _ %H:%M:%S')
    elif language == 'ar':
        return format_datetime(value, locale=locale, format='yyyy/MMMM/dd HH:mm:ss')

    return format_datetime(value, locale=locale, format='dd/MM/yyyy HH:mm:ss')
