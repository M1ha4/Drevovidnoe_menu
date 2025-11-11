from django import template
from django.urls import reverse, NoReverseMatch
from menu_app.models import MenuItem, Menu

register = template.Library()


@register.inclusion_tag('menu_app/menu.html', takes_context=True)
def draw_menu(context, menu_name):
    """
    Return context with tree for menu with name `menu_name`.
    IMPORTANT: this should execute exactly 1 DB query to get all items for this menu.
    """
    request = context.get('request')
    # 1 DB query here:
    items_qs = MenuItem.objects.filter(menu__name=menu_name).select_related('parent').order_by('order', 'id')
    items = list(items_qs)  # evaluate queryset (still 1 query)
    # Build mapping id -> dict
    nodes = {}
    children_map = {}
    for it in items:
        nodes[it.id] = {
            'id': it.id,
            'title': it.title,
            'parent_id': it.parent_id,
            'raw_obj': it,
            'url': it.get_resolved_url(),
            'children': [],
            'active': False,
            'expanded': False,
        }
        children_map.setdefault(it.parent_id, []).append(nodes[it.id])

    # attach children
    for node in nodes.values():
        parent_id = node['parent_id']
        if parent_id in nodes:
            nodes[parent_id]['children'].append(node)

    roots = children_map.get(None, [])

    # find active item by comparing resolved urls to request.path
    active_node = None
    if request is not None:
        path = request.path
        # normalize simple trailing slash mismatch by ensuring trailing slash on both when comparing
        def norm(p):
            return p.rstrip('/') or '/'
        path_norm = norm(path)
        for n in nodes.values():
            try:
                url = n['url'] or ''
                if url == '#':
                    continue
                # try to treat url as path; if named reverse produced full path that's fine
                if norm(url) == path_norm:
                    active_node = n
                    n['active'] = True
                    break
            except Exception:
                continue

    # mark ancestors
    if active_node:
        cur = active_node
        # mark the first-level under active as expanded (the children of active)
        for child in cur['children']:
            child['expanded'] = True
        # walk up parents
        parent_id = cur['parent_id']
        while parent_id:
            parent = nodes.get(parent_id)
            if not parent:
                break
            parent['expanded'] = True
            # also mark its children visible to show the path
            parent_id = parent['parent_id']
            # also mark ancestor nodes to show which is along path
        # Also expand all ancestors (this already sets expanded True)
        # Mark ancestors as 'active_ancestor' optionally
        p = cur['parent_id']
        while p:
            if p in nodes:
                nodes[p]['expanded'] = True
                p = nodes[p]['parent_id']
            else:
                break

    # For any ancestor nodes we want them to show their children (we already set expanded above)
    return {
        'menu_name': menu_name,
        'roots': roots,
        'request': request,
    }
