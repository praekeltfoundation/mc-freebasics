from django.db import models
from mc2.controllers.docker.models import DockerController
from django.db.models.signals import pre_save


class FreeBasicsController(DockerController):
    TEMPLATE_CHOICES = (
        ("option1", "molo-tuneme"),
        ("option2", "molo-ndohyep"),
    )
    TEMPLATE_MARATHON_CMD = {
        "option1": "./deploy/docker-entrypoint.sh tuneme tuneme.wsgi 8000",
        "option2": "./deploy/docker-entrypoint.sh bwise ndohyep.wsgi 8000"
    }
    DEFAULT_PORT = 8000
    selected_template = models.CharField(
        default=TEMPLATE_CHOICES[0][1], max_length=100, blank=False,
        null=False)

    @property
    def app_id(self):
        """
        The app id to use for marathon
        """
        return 'freebasics-%s' % self.slug


class FreeBasicsTemplateData(models.Model):
    site_name = models.CharField(
        unique=True, max_length=100, blank=True, null=True)
    site_name_url = models.URLField(
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

    @staticmethod
    def pre_save(sender, instance, **kwargs):
        instance.controller = FreeBasicsController.objects.create()

pre_save.connect(
    FreeBasicsTemplateData.pre_save, FreeBasicsTemplateData,
    dispatch_uid="freebasics.models.FreeBasicsTemplateData")
