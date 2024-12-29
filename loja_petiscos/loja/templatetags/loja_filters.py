from django import template

register = template.Library()

@register.filter
def render_stars(rating):
    """
    Renderiza 5 estrelas, pintando as completas, meia estrela, e o restante vazio.
    """
    try:
        rating = float(rating)
    except (ValueError, TypeError):
        rating = 0

    full_stars = int(rating)
    half_star = 1 if (rating - full_stars) >= 0.5 else 0
    empty_stars = 5 - (full_stars + half_star)

    stars_html = ''

    # Adiciona as estrelas completas
    stars_html += '<span class="star full">★</span>' * full_stars

    # Adiciona a meia estrela, se necessário
    if half_star:
        stars_html += '<span class="star half">★</span>'

    # Adiciona as estrelas vazias
    stars_html += '<span class="star empty">☆</span>' * empty_stars

    return stars_html