from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'clubs', views.ClubViewSet)
router.register(r'board_games', views.BoardGameViewSet)
router.register(r'game_sets', views.GameSetViewSet)
router.register(r'genres', views.GenreViewSet)
router.register(r'addresses', views.AddressViewSet)


urlpatterns = [
    path('', views.home, name='homepage'),
    path('clubs/', views.BoardGameListView.as_view(), name='clubs'),
    path('club/', views.boardgame_view, name='club'),
    path('board_games/', views.СlubListView.as_view(), name='board_games'),
    path('board_game/', views.сlub_view, name='board_game'),
    path('genres/', views.СlubListView.as_view(), name='genres'),
    path('genre/', views.сlub_view, name='genre'),
    path('addresses/', views.СlubListView.as_view(), name='addresses'),
    path('address/', views.сlub_view, name='address'),
    path('game_sets/', views.GameSetListView.as_view(), name='game_sets'),
    path('game_set/', views.gameset_view, name='game_set'),
    path('api/', include(router.urls), name='api'),
    path('api-auth/', include('rest_framework.urls'), name='rest_framework'),
]