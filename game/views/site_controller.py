from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from game.models.FAQ import FAQ
from game.models.rule_image import RuleImage
from game.serializers.FAQ_serializer import FAQSerializer
from game.serializers.rule_serializer import RulesSerializer


class SiteRules(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        rules = RuleImage.objects.order_by('position')

        serializer = RulesSerializer(rules, many=True, context={'request': request})


        return Response({
           'rules': serializer.data
        })


class SiteFAQ(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        faq = FAQ.objects.order_by('position')

        serializer = FAQSerializer(faq, many=True, context={'request': request})

        return Response({
            'faq': serializer.data
        })