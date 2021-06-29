from random import choices
from string import ascii_uppercase, digits

from django.core.mail import send_mail
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from users.models import CustomUser

from .permissions import IsAdmin
from .serializers import RegistrationSerializer, UsersSerializer


class RegistrationViewSet(viewsets.ModelViewSet):
    """
    View class to represent registration for all users
    """
    queryset = CustomUser.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request):
        verification_code = ''.join(choices(ascii_uppercase + digits, k=12))
        email = request.data.get('email')
        serializer = self.serializer_class(
            data={
                'password': verification_code,
                'email': email,
            }
        )
        if serializer.is_valid():
            serializer.save()
            send_mail(
                subject='Verification Code from Yamdb',
                message=verification_code,
                from_email=None,
                recipient_list=[email],
            )
            return Response(serializer.data)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class UsersViewSet(viewsets.ModelViewSet):
    """
    A class to represent Users model.
    Use "username" or "me" slug for getting specific info
    """
    queryset = CustomUser.objects.all()
    serializer_class = UsersSerializer
    lookup_field = 'username'
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

    @action(
        detail=False,
        methods=['get', 'patch'],
        permission_classes=[permissions.IsAuthenticated],
    )
    def me(self, request):
        user = self.request.user
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
