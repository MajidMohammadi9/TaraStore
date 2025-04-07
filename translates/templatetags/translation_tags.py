from django import template
from django.utils.translation import get_language

from babel.dates import format_datetime
from jalali_date.templatetags.jalali_tags import to_jalali
from decimal import Decimal


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


@register.filter
def convert_currency(price):
    CURRENCY_SYMBOLS = {
    'fa': 'تومان',
    'ar': 'ريال عماني',
    'en': '$'
    }

    CURRENCY_RATES = {
    'fa': 92000,
    'ar': 0.386,
    'en': 1
    }

    DECIMAL_PLACES = {
    'fa': 0,
    'ar': 3,
    'en': 2
    }

    language=get_language()

    # rate=Decimal(CURRENCY_RATES.get(language, 1))
    rate=CURRENCY_RATES.get(language, 1)
    symbol=CURRENCY_SYMBOLS.get(language, '$')
    decimal_places=DECIMAL_PLACES.get(language, 2)

    converted_price=Decimal(price)*Decimal(rate)

    return f'{converted_price:,.{decimal_places}f} {symbol}'

    
