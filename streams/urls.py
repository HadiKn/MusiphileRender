from django.urls import path
from .views import StreamCreateView

app_name = 'streams'

urlpatterns = [
    path('songs/<int:song_id>/streams/', StreamCreateView.as_view(), name='stream-create'),
]