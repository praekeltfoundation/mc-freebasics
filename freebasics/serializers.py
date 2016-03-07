from rest_framework import serializers
from freebasics.models import FreeBasicsTemplateData


class FreeBasicsDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = FreeBasicsTemplateData
        fields = (
            'site_name', 'site_name_url', 'body_background_color',
            'body_color', 'body_font_family', 'accent1',
            'accent2', 'header_position', 'article_position',
            'banner_position', 'category_position', 'poll_position',
            'footer_position', 'controller')
