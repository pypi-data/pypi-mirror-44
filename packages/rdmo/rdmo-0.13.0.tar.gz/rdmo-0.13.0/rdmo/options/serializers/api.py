from rest_framework import serializers

from rdmo.core.serializers import TranslationSerializerMixin

from ..models import OptionSet, Option


class OptionSetSerializer(serializers.ModelSerializer):

    conditions = serializers.HyperlinkedRelatedField(view_name='api-v1-conditions:condition-detail', read_only=True, many=True)
    options = serializers.HyperlinkedRelatedField(view_name='api-v1-options:option-detail', read_only=True, many=True)

    class Meta:
        model = OptionSet
        fields = (
            'id',
            'uri',
            'uri_prefix',
            'key',
            'comment',
            'order',
            'conditions',
            'options',
        )


class OptionSerializer(TranslationSerializerMixin, serializers.ModelSerializer):

    optionset = serializers.HyperlinkedRelatedField(view_name='api-v1-options:optionset-detail', read_only=True)

    class Meta:
        model = Option
        fields = (
            'id',
            'uri',
            'uri_prefix',
            'key',
            'comment',
            'order',
            'additional_input',
            'optionset'
        )
        trans_fields = (
            'text',
        )
