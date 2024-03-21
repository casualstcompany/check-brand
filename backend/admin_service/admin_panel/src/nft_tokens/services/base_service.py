import logging

from django.db import models

from nft_tokens.utils import set_if_value

logger = logging.getLogger(__name__)


class BaseService:
    model = models.Model
    template_params_update = None
    list_params = []

    def __init__(
        self,
    ):
        self.get_template_params_update()

    def get_template_params_update(self):
        """
        Параметры должны быть указаны для annotate  в таком виде:
        {"items_count": Count('token'),}
        """
        if self.template_params_update is None:
            self.template_params_update = {}

    def update_counted_fields(
        self, model_id: str, list_params: list[str] = None
    ):
        queryset = self.model.objects.filter(id=model_id).distinct()
        annotate_params = {}
        update_params = {}

        if list_params is None:
            list_params = self.list_params

        for param in list_params:
            set_if_value(
                annotate_params,
                f"annotate_{param}",
                self.template_params_update[param],
            )

        if annotate_params:
            logger.info("annotate_params {}".format(annotate_params))
            query = queryset.annotate(**annotate_params).values().first()

            if query:
                for param in list_params:
                    set_if_value(
                        update_params, param, query[f"annotate_{param}"]
                    )

                if update_params:
                    logger.info(update_params)
                    queryset.update(**update_params)
