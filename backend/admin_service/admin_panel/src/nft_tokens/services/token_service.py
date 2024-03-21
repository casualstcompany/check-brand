import logging

from nft_tokens import utils
from nft_tokens.models import Pack, Token
from nft_tokens.serializers import GetM2MPackSerializer

logger = logging.getLogger(__name__)


class TokenService:
    model = Token

    def __init__(
        self,
    ):
        pass

    @staticmethod
    def get_model_pack(pack_id):
        return Pack.objects.get(id=pack_id)

    @staticmethod
    def _set_params_from_pack(params: dict, pack) -> None:
        utils.set_if_value(params, "type", pack.type)
        utils.set_if_value(params, "status_price", pack.status_price)
        utils.set_if_value(params, "description", pack.description)
        utils.set_if_value(params, "close", pack.close)
        utils.set_if_value(params, "close_image", pack.close_image)
        utils.set_if_value(params, "unlockable", pack.unlockable)
        utils.set_if_value(
            params, "unlockable_content", pack.unlockable_content
        )
        utils.set_if_value(params, "status", pack.status)
        utils.set_if_value(params, "hide", pack.hide)
        utils.set_if_value(params, "price", pack.price)
        utils.set_if_value(params, "currency_token", pack.currency_token)
        utils.set_if_value(params, "investor_royalty", pack.investor_royalty)
        utils.set_if_value(params, "creator_royalty", pack.creator_royalty)

    def update_by_pack(self, pack_id: str = None, pack: Pack = None):
        data = {}
        if pack is None:
            pack = self.get_model_pack(pack_id)

        self._set_params_from_pack(data, pack)
        pack_m2m_dict = GetM2MPackSerializer(pack).data

        tokens_queryset = self.model.objects.filter(
            pack=pack, mint=False, block=False
        )
        if tokens_queryset:
            tokens_queryset.update(**data)

            for token in tokens_queryset:
                utils.set_m2m_from_dict_to_instance(pack_m2m_dict, token)


token_service_cls = TokenService()
