from django import template

register = template.Library()

@register.filter(name='rupiah')
def rupiah(value):
    try:
        angka = int(float(value))
        
        hasil = f"Rp{angka:,}".replace(',', '.')
        return hasil
    except (ValueError, TypeError):
        return "Rp0"