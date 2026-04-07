from django.urls import path

from levels.views import IntroView

urlpatterns = [
    path('levels/intro/', IntroView.as_view(), name='intro'),

]