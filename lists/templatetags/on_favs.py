from django import template
from lists import models as list_models

register = template.Library()


@register.simple_tag(takes_context=True)
def on_favs(context, room):
    try:
        user = context.request.user
        the_list = list_models.List.objects.get(user=user, name="My Favourites Houses")
        return room in the_list.rooms.all()
    except list_models.List.DoesNotExist:
        return False
