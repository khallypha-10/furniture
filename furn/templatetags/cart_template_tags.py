from django import template
from furn.models import Orders

register = template.Library()


@register.filter
def cart_item_count(user):
    if user.is_authenticated:
        qs = Orders.objects.filter(user=user, ordered=False)
        if qs.exists():
            return qs[0].orderItem.count()
    return 0