from django.shortcuts import render
from .models import MenuItem

def menu_view(request):
    """
    Этот view не обязателен для работы шаблонного тега,
    но полезен, чтобы протестировать отображение меню отдельно.
    """
    # Можно передать все элементы меню для проверки
    menu_items = MenuItem.objects.all().select_related('parent', 'menu')

    return render(request, 'menu/menu_debug.html', {
        'menu_items': menu_items,
    })
