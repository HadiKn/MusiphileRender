from django.urls import path
from .views import UserSignupView, UserRetrieveUpdateView, UserDeactivateView,UserLoginView,UserLogoutView,ArtistListView,ArtistRetrieveView,UserListView,UserRetrieveView

urlpatterns = [
    path('create/', UserSignupView.as_view(), name='user-signup'), 
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('logout/', UserLogoutView.as_view(), name='user-logout'),
    path('list/artist/', ArtistListView.as_view(), name='artist-list'),
    path('list/user/', UserListView.as_view(), name='user-list'),
    path('retrieve/artist/<int:pk>/', ArtistRetrieveView.as_view(), name='artist-profile'),
    path('retrieve/user/<int:pk>/', UserRetrieveView.as_view(), name='user-profile'),
    path('modify/', UserRetrieveUpdateView.as_view(), name='my-profile'),
    path('deactivate/', UserDeactivateView.as_view(), name='user-deactivate'),
]