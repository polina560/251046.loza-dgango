from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from game.models.sale import Sale
from game.serializers.sale_serializer import SaleSerializer


class SaleView(APIView):
    permission_classes = [AllowAny]

    def get(self,request):
        sales = Sale.objects.order_by('position')

        serializer = SaleSerializer(sales, many=True, context={'request': request})


        return Response({
            serializer.data
        })
