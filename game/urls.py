from django.urls import path

from game.views.game_controller import GameController

urlpatterns = [
    path('game/<str:action>/', GameController.as_view(), name='game-action'),
]