from django.db import models
from mc2.controllers.docker.models import DockerController


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
    siteName = models.CharField(max_length=100, blank=True, null=True)
    siteNameUrl = models.CharField(
        unique=True, max_length=100, blank=True, null=True)
    bodyBackgroundColor = models.CharField(
        max_length=100, blank=True, null=True)
    bodyColor = models.CharField(max_length=100, blank=True, null=True)
    bodyFontFamily = models.CharField(max_length=100, blank=True, null=True)
    accent1 = models.CharField(max_length=100, blank=True, null=True)
    accent2 = models.CharField(max_length=100, blank=True, null=True)
    headerPosition = models.IntegerField(default=1)
    articlePosition = models.IntegerField(default=2)
    bannerPosition = models.IntegerField(default=3)
    categoryPosition = models.IntegerField(default=4)
    pollPosition = models.IntegerField(default=5)
    footerPosition = models.IntegerField(default=6)
