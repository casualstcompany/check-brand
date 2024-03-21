import django_filters

from nft_tokens.models import Collection
from social_opportunities.models import CertificateTypeServiceChoices, Service


class ServiceFilter(django_filters.FilterSet):
    collection_id = django_filters.ModelMultipleChoiceFilter(
        queryset=Collection.objects.all(),
        field_name="collections",
        to_field_name="id",
    )
    certificate_type = django_filters.ChoiceFilter(
        choices=CertificateTypeServiceChoices.choices
        )

    class Meta:
        model = Service
        fields = (
            "collection_id",
            "certificate_type",
        )
