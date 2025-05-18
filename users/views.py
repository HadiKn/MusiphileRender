from rest_framework import generics, status,filters
from rest_framework.response import Response
from .serializers import UserSerializer,MiniUserSerializer
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied


User = get_user_model()

# list or search for artists
class ArtistSearchView(generics.ListAPIView):
    serializer_class = MiniUserSerializer
    queryset = User.objects.filter(is_artist=True)
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['username']


# get artist profile
class PublicArtistDetailView(generics.RetrieveAPIView):
    queryset = User.objects.filter(is_artist=True,is_active=True)
    serializer_class = MiniUserSerializer
    lookup_field = 'pk'
    permission_classes = [IsAuthenticated]

# create account 
class UserSignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        user_data = UserSerializer(user).data
        return Response({
            "status": "success",
            "data": {
                "user": user_data,
                "token": token.key
            }
        }, status=status.HTTP_201_CREATED)
    

# log in
class UserLoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)
        if user is not None:
            token, _ = Token.objects.get_or_create(user=user)
            user_data = UserSerializer(user).data
            return Response({
                "status": "success",
                "data": {
                    "user": user_data,
                    "token": token.key
    }
                },status=status.HTTP_200_OK)
        return Response({"detail": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)

# log out
class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response({"detail": "Logged out successfully."}, status=status.HTTP_200_OK)
        

# private retrieve or update user account
class UserDetailUpdateView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'pk'
    permission_classes = [IsAuthenticated]
    def get_object(self):
        obj = super().get_object()
        if self.request.user != obj and not self.request.user.is_superuser:
            raise PermissionDenied("you do not have permission to performe this action")
        return obj

# decactivate user accout without deleting
class UserDeactivateView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        obj = super().get_object()
        if self.request.user != obj and not self.request.user.is_superuser:
            raise PermissionDenied("You do not have permissions to deactivate this account.")
        return obj

    def patch(self, request, *args, **kwargs):
        user = self.get_object()
        user.is_active = False
        user.save()
        return Response({'detail': 'User account deactivated.'}, status=status.HTTP_200_OK)
    

