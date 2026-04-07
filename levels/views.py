from django.shortcuts import render

# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from levels.models import Intro
from levels.serializers.intro import IntroSerializer


class IntroView(APIView):
    """
    View для работы с единственной записью Intro
    """

    def get(self, request):
        """Получить единственную запись Intro"""
        intro = Intro.objects.first()
        if intro:
            serializer = IntroSerializer(intro)
            return Response(serializer.data)
        return Response(
            {"detail": "Intro not found"},
            status=status.HTTP_404_NOT_FOUND
        )
