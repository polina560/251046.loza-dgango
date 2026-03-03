from django.urls import path

from game.views.game_controller import GameStartView, GamePauseView, GameAbortView, GameEndView
from game.views.item_controller import ItemShopView, ItemBuyView, ItemActivateView
from game.views.prize_controller import PrizeView
from game.views.rating_controller import RatingIndexView, RatingClanView, RatingUserView
from game.views.sale_controller import SaleView
from game.views.site_controller import SiteRules, SiteFAQ

urlpatterns = [
    path('game/start/', GameStartView.as_view(), name='game-start'),
    path('game/pause/', GamePauseView.as_view(), name='game-pause'),
    path('game/abort/', GameAbortView.as_view(), name='game-abort'),
    path('game/end/', GameEndView.as_view(), name='game-end'),
    path('game/params/', GamePauseView.as_view(), name='game-params'),

    path('item/shop/', ItemShopView.as_view(), name='item-shop'),
    path('item/buy/', ItemBuyView.as_view(), name='item-buy'),
    path('item/activate/', ItemActivateView.as_view(), name='item-activate'),

    path('sales/', SaleView.as_view(), name='sales'),
    path('prize/running-line/', PrizeView.as_view(), name='prize-running-line'),

    path('rules/', SiteRules.as_view(), name='rules'),
    path('faq/', SiteFAQ.as_view(), name='faq'),

    path('rating/index/', RatingIndexView.as_view(), name='rating-index'),
    path('rating/clan/', RatingClanView.as_view(), name='rating-clan'),
    path('rating/user/', RatingUserView.as_view(), name='rating-user'),


]