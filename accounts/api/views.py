from django.contrib.auth import get_user_model

from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveUpdateDestroyAPIView,
    RetrieveUpdateAPIView
)
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, \
    HTTP_404_NOT_FOUND

from .serializers import (
    ClientForManagerSerializer,
    ClientRegisterSerializer,
    ClientProfileSerializer,
    ClientProvidePINSerilizer,
    UserLoginSerializer,
)
from .permissions import (
    IsManagerPermission,
    IsClientPermission,
    ClientHavePINPermission
)


User = get_user_model()


class ManagerClientListView(ListAPIView):
    """Client list endpoint for Managers with filters 'is_closed', 'is_active'"""

    model = User
    queryset = User.objects.filter(
        is_manager=False,
        is_staff=False,
        is_superuser=False
    )
    serializer_class = ClientForManagerSerializer
    permission_classes = [IsManagerPermission, ]
    filter_fields = ('is_closed', 'is_active')


class ManagerClientDetailView(RetrieveUpdateDestroyAPIView):
    """Client resource endpoint for Managers"""

    model = User
    lookup_field = 'id'
    queryset = User.objects.filter(
        is_manager=False,
        is_staff=False,
        is_superuser=False
    )

    serializer_class = ClientForManagerSerializer
    permission_classes = [IsManagerPermission, ]


class ClientRegisterView(CreateAPIView):
    """Endpoint that provide user register"""

    model = User
    queryset = User.objects.all()
    serializer_class = ClientRegisterSerializer
    permission_classes = [AllowAny, ]


class ClientProfileView(RetrieveUpdateAPIView):
    """Endpoint to see and updtae client account """

    model = User
    queryset = User.objects.all()
    serializer_class = ClientProfileSerializer
    permission_classes = [ClientHavePINPermission, ]

    def get_object(self):
        obj = self.request.user
        self.check_object_permissions(self.request, obj)
        return obj


class ClientProvidePINView(RetrieveUpdateAPIView):
    """Endpoint to provide pin for Client User"""
    model = User
    queryset = User.objects.all()
    serializer_class = ClientProvidePINSerilizer
    permission_classes = [IsClientPermission, ]

    def get_object(self):
        obj = self.request.user
        self.check_object_permissions(self.request, obj)
        return obj

    def put(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            pin = serializer.data['password']
            user.set_password(pin)
            user.save()
            return Response(serializer.data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class UserLoginAPIView(APIView):
    """Endpoint for login users"""

    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):

        data = request.data
        serializer = UserLoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            new_data = serializer.data
            return Response(new_data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_404_NOT_FOUND)
