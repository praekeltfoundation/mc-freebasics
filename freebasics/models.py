from django.db import models
from mc2.controllers.docker.models import DockerController


class FreeBasicsController(DockerController):

    def get_marathon_app_data(self):
        data = super(FreeBasicsController, self).get_marathon_app_data()

        env_data = {}
        if self.env_variables.exists():
            env_data.update(dict([
                (env.key, env.value)
                for env in self.env_variables.all()]))

        if self.freebasicstemplatedata:
            env_data.update(self.freebasicstemplatedata.to_env_dict())
        data.update({'env': env_data})
        return data

    @property
    def app_id(self):
        """
        The app id to use for marathon
        """
        return 'freebasics-%s' % self.slug


class FreeBasicsTemplateData(models.Model):
    site_name = models.CharField(
        unique=True, max_length=100, blank=True, null=True)
    site_name_url = models.CharField(
        unique=True, max_length=255, blank=True, null=True)
    body_background_color = models.CharField(
        max_length=100, blank=True, null=True)
    body_color = models.CharField(max_length=100, blank=True, null=True)
    body_font_family = models.CharField(max_length=100, blank=True, null=True)
    accent1 = models.CharField(max_length=100, blank=True, null=True)
    accent2 = models.CharField(max_length=100, blank=True, null=True)
    header_position = models.IntegerField(default=1)
    article_position = models.IntegerField(default=2)
    banner_position = models.IntegerField(default=3)
    category_position = models.IntegerField(default=4)
    poll_position = models.IntegerField(default=5)
    footer_position = models.IntegerField(default=6)
    controller = models.OneToOneField(
        FreeBasicsController, on_delete=models.CASCADE)

    def to_env_dict(self):
        return {
            'CUSTOM_CSS_BODY_BACKGROUND_COLOR': self.body_background_color,
            'CUSTOM_CSS_BODY_FONT_COLOR': self.body_color,
            'CUSTOM_CSS_BODY_FONT': self.body_font_family,
            'CUSTOM_CSS_ACCENT_1': self.body_font_family,
            'CUSTOM_CSS_ACCENT_2': self.body_font_family,
            'BLOCK_POSITION_BANNER': self.banner_position,
            'BLOCK_POSITION_LATEST': self.article_position,
            'BLOCK_POSITION_QUESTIONS': self.poll_position,
            'BLOCK_POSITION_SECTIONS': self.category_position}
