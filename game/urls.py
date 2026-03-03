from django.urls import path

from game.views.game_controller import GameController
from game.views.item_controller import ItemShopView, ItemBuyView, ItemActivateView
from game.views.prize_controller import PrizeView
from game.views.sale_controller import SaleView
from game.views.site_controller import SiteRules, SiteFAQ

urlpatterns = [
    path('<str:action>/', GameController.as_view(), name='game-action'),

    path('item/shop/', ItemShopView.as_view(), name='item-shop'),
    path('item/buy/', ItemBuyView.as_view(), name='item-buy'),
    path('item/activate/', ItemActivateView.as_view(), name='item-activate'),

    path('sales/', SaleView.as_view(), name='sales'),
    path('prize/running-line/', PrizeView.as_view(), name='prizes'),

    path('rules/', SiteRules.as_view(), name='rules'),
    path('faq/', SiteFAQ.as_view(), name='faq'),


]