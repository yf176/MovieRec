from rest_framework.decorators import api_view
from rest_framework.response import Response
from user.models import MyUser


@api_view(['GET'])
def user_list(request):
    users = MyUser.objects.all()
    data = []
    for user in users:
        data.append({
            'id': user.id,
            'username': user.username,
            'email': user.email
        })
    return Response(data)