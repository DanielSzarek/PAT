from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User, Pack
from .serializers import UserSerializer, PackSerializer, UserPasswordSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import ReadOnly, UserEmailVerify
from django.utils import timezone


class UserCreateView(generics.CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, UserEmailVerify]
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserDetail2View(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = ()
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        obj = queryset.get(pk=self.request.user.id)
        self.check_object_permissions(self.request, obj)
        return obj


class UserPasswordChangeView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserPasswordSerializer

    def get_object(self):
        return self.request.user

    def put(self, request):
        self.object = self.get_object()
        serializer = UserPasswordChangeView(data=request.data)

        if serializer.is_valid():
            # Check old password
            old_password = serializer.data.get("old_password")
            if not self.object.check_password(old_password):
                return Response({"old_password": ["Wrong password."]},
                                status=status.HTTP_400_BAD_REQUEST)
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PackListView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PackSerializer
    queryset = Pack.objects.all()

    def get_queryset(self):
        status = self.request.query_params.get('status', None)
        courier = self.request.query_params.get('courier', None)
        if status is not None and courier is not None:
            queryset = Pack.objects.filter(status=status).filter(courier=courier).order_by('mod_date')
        elif status is not None and courier is None:
            queryset = Pack.objects.filter(status=status).order_by('mod_date')
        elif status is None and courier is not None:
            queryset = Pack.objects.filter(courier=courier).order_by('mod_date')
        else:
            queryset = Pack.objects.all()

        return queryset


class PackDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PackSerializer
    queryset = Pack.objects.all()

    def perform_update(self, serializer):
        serializer.save(mod_date=timezone.now())


class PackCourier(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PackSerializer
    queryset = Pack.objects.all()

    def perform_update(self, serializer):
        serializer.save(courier=self.request.user, status=2, mod_date=timezone.now())

