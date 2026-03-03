from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from game.models.user_stage_prize import UserStagePrizes
from game.serializers.user_stage_prize_serializer import UserStagePrizeSerializer


class PrizeView(APIView):
    permission_classes = [AllowAny]

    def get(self,request):
        prizes = UserStagePrizes.objects.order_by('received_at')

        serializer = UserStagePrizeSerializer(prizes, many=True, context={'request': request})


        return Response({
            'prizes': serializer.data
        })
