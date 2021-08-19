from django.shortcuts import redirect, reverse
from django.views.generic import TemplateView
from rooms import models as room_models
from reservations import models as reservation_models
from . import models


def toggle_room(request, room_pk):
    action = request.GET.get("action", None)
    room = room_models.Room.objects.get_or_none(pk=room_pk)
    if room is not None and action is not None:
        the_list, created = models.List.objects.get_or_create(
            user=request.user, name="My Favourites Houses"
        )
        if action == "add":
            the_list.rooms.add(room)
        elif action == "remove":
            the_list.rooms.remove(room)
    return redirect(reverse("rooms:detail", kwargs={"pk": room_pk}))


class SeeFavsView(TemplateView):

    template_name = "lists/favs_list.html"


class SeeReservationView(TemplateView):

    template_name = "lists/reservations_list.html"

    def get_context_data(self, **kwargs):
        if self.request.session.get("is_hosting"):
            my_reservation = []
            my_rooms = room_models.Room.objects.filter(host=self.request.user)
            for _, room in enumerate(my_rooms):
                if reservation_models.Reservation.objects.filter(room=room):
                    reservations = reservation_models.Reservation.objects.filter(
                        room=room
                    )
                    my_reservation.append(reservations)
            context = super(SeeReservationView, self).get_context_data(**kwargs)
            context.update({"reservations": my_reservation})
            return context
