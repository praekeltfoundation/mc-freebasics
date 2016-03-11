from freebasics import the_celery_app


@the_celery_app.task(serializer='json')
def update_marathon_app(project_id):
    from mc2.controllers.base.models import Controller

    controller = Controller.objects.get(pk=project_id)
    controller.update_marathon_app()
