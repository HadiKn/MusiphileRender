from django.urls import path
from .views import UserSignupView, UserDetailUpdateView, UserDeactivateView,UserLoginView,UserLogoutView,ArtistSearchView,PublicArtistDetailView

urlpatterns = [
    path('signup/', UserSignupView.as_view(), name='user-signup'), 
    path('list/', ArtistSearchView.as_view(), name='artist-list'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('logout/', UserLogoutView.as_view(), name='user-logout'),
    path('modify/<int:pk>/', UserDetailUpdateView.as_view(), name='user-profile'),
    path('retrieve/<int:pk>/', PublicArtistDetailView.as_view(), name='artist-profile'),
    path('deactivate/<int:pk>/', UserDeactivateView.as_view(), name='user-deactivate'),
]