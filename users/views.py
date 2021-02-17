from datetime import datetime

from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from api_yamdb import settings
from users.serializers import UsersSerializer, GetTokenSerializer
from .models import User
from api.permissions import IsAdminOrStaff


class UsersViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdminOrStaff,)
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    lookup_field = 'username'

    @action(
        detail=False,
        methods=('GET', 'PATCH'),
        permission_classes=(IsAuthenticated,)
    )
    def me(self, request):
        if request.method == 'GET':
            serializer = UsersSerializer(request.user)
            return Response(serializer.data)

        if request.method == 'PATCH':
            serializer = UsersSerializer(
                request.user,
                data=request.data,
                partial=True
            )
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(('POST',))
def email_code(request):
    data = {
        'email': request.data.get('email'),
        'username': f'newuser_{datetime.timestamp(datetime.now())}',
    }

    user = User.objects.filter(email=data['email']).first()
    if user:
        serializer = UsersSerializer(user)
    else:
        serializer = UsersSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        subject=settings.MAIL_SUBJECT,
        message=settings.MAIL_TEXT.format(confirmation_code),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=(data['email'],),
    )
    return Response({'email': serializer.data['email']},
                    status=status.HTTP_201_CREATED)


@api_view(('POST',))
def get_token(request):
    data = {
        'email': request.data['email'],
        'confirmation_code': request.data['confirmation_code']
    }

    serializer = GetTokenSerializer(data=data)
    if serializer.is_valid(raise_exception=True):
        user = get_object_or_404(User, email=data['email'])
        if default_token_generator.check_token(
                user,
                data['confirmation_code']):
            access_token = AccessToken.for_user(user)
            return Response(data={'token': str(access_token)},
                            status=status.HTTP_200_OK)

        return Response(
            data={'confirmation_code': 'wrong code'},
            status=status.HTTP_400_BAD_REQUEST
        )
