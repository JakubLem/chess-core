from rest_framework.response import Response


def room(request, room_name):
    return Response({
        'room_name': room_name
    })
