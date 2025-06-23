from rest_framework import generics, status, filters, parsers  
from rest_framework.response import Response
from .serializers import UserSerializer, MiniUserSerializer
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from .utils import api_response
from drf_spectacular.utils import extend_schema

User = get_user_model()

# list or search for artists
class ArtistListView(generics.ListAPIView):
    serializer_class = MiniUserSerializer
    queryset = User.objects.filter(is_artist=True)
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['username']

# list or search for users
class UserListView(generics.ListAPIView):
    serializer_class = MiniUserSerializer
    queryset = User.objects.filter(is_artist=False)
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['username']


# get artist profile
class ArtistRetrieveView(generics.RetrieveAPIView):
    queryset = User.objects.filter(is_artist=True,is_active=True)
    serializer_class = MiniUserSerializer
    lookup_field = 'pk'
    permission_classes = [IsAuthenticated]

# get User profile
class UserRetrieveView(generics.RetrieveAPIView):
    queryset = User.objects.filter(is_artist=False,is_active=True)
    serializer_class = MiniUserSerializer
    lookup_field = 'pk'
    permission_classes = [IsAuthenticated]


# retrieve or update my account
@extend_schema(
    request={
        'multipart/form-data': {
            'type': 'object',
            'properties': {
                'username': {
                    'type': 'string',
                    'description': 'New username (must be unique)',
                    'maxLength': 150
                },
                'profile_picture': {
                    'type': 'string',
                    'format': 'binary',
                    'description': 'Profile picture image file (optional)'
                },
                'email': {
                    'type': 'string',
                    'format': 'email',
                    'description': 'Email address (optional)'
                },
                'is_artist': {
                    'type': 'boolean',
                    'description': 'Whether the user is an artist (optional)'
                }
            }
        }
    }
)
class UserRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [parsers.MultiPartParser, parsers.FormParser, parsers.JSONParser]
    
    def get_object(self):
        return self.request.user

# create account 
class UserSignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        user_data = UserSerializer(user, context={'request': request}).data
        
        return api_response(
            data={"user": user_data, "token": token.key},
            message="User created successfully",
            status_code=status.HTTP_201_CREATED
        )
    

# log in
class UserLoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user is not None:
            token, _ = Token.objects.get_or_create(user=user)
            user_data = UserSerializer(user, context={'request': request}).data
            return api_response(
                data={"user": user_data, "token": token.key},
                message="Login successful",
                status_code=status.HTTP_200_OK
            )
        return api_response(
            message="Invalid credentials",
            status="error",
            status_code=status.HTTP_401_UNAUTHORIZED
        )

# log out
class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return api_response(
            message="Logged out successfully.",
            status="success",
            status_code=status.HTTP_200_OK
        )
        
# decactivate user accout without deleting
class UserDeactivateView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def patch(self, request, *args, **kwargs):
        user = self.get_object()
        user.is_active = False
        user.save()
        return api_response(
            message="User account deactivated.",
            status="success",
            status_code=status.HTTP_200_OK
        )
