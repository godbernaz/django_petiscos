from loja.models import Category

def categories_context(request):
    desired_order = ['Entradas', 'Saladas', 'Carnes', 'Peixes', 'Tabuas', 'Tartes', 'Sobremesas']
    categories = sorted(
        Category.objects.all(),
        key=lambda x: desired_order.index(x.name) if x.name in desired_order else len(desired_order)
    )
    return {'categories': categories}

