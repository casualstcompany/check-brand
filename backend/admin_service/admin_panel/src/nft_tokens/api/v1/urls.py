from rest_framework.routers import DefaultRouter

from nft_tokens.api.v1 import views

router = DefaultRouter()

# router.register("not_file/token", views.TokenNotFileView, basename="not_file_token")

router.register("page", views.PageViewSet, basename="page")
# router.register("page/hide", views.HidePageView, basename="page_hide")

router.register("account", views.AccountViewSet, basename="account")
# router.register("account/hide", views.HideAccountView, basename="account_hide")

router.register("collection", views.CollectionViewSet, basename="collection")
router.register(
    "collection/mini",
    views.CollectionMiniFilterListView,
    basename="collection_mini",
)  # TODO: нужна?
# router.register("collection/hide", views.HideCollectionView, basename="collection_hide")
router.register(
    "collection/status",
    views.StatusUpdateCollectionView,
    basename="collection_update_status",
)
router.register(
    "collection_filter",
    views.CollectionByPageView,
    basename="collection_filter",
)  # TODO: нужна?

router.register("pack", views.PackViewSet, basename="pack")
# router.register("pack/hide", views.HidePackViewSet, basename="pack_hide")
router.register(
    "pack_filter", views.PackByCollectionView, basename="pack_filter"
)  # TODO: нужна?

router.register("token", views.TokenViewSet, basename="token")
# router.register("token/hide", views.HideTokenView, basename="token_hide")
router.register(
    "token_by_pack", views.TokenByPackViewSet, basename="token_by_pack"
)
router.register(
    "token_by_pack/confirm_upload",
    views.TokenConfirmationUploadFileView,
    basename="token_confirm_upload",
)
router.register(
    "token_filter", views.TokenByCollectionView, basename="token_filter"
)  # TODO: нужна?
router.register("token/user/me", views.TokenUserView, basename="token_user_me")

router.register("properties", views.PropertiesViewSet, basename="properties")
router.register(
    "levels_stats", views.LevelsStatsViewSet, basename="levels_stats"
)

# TODO может быть временно закроем данные ручки
router.register("blockchain", views.BlockchainViewSet, basename="blockchain")
router.register(
    "currency_token", views.CurrencyTokenViewSet, basename="currency_token"
)

urlpatterns = router.urls
