from restservice.models import RestService

def call_service(parsed_instance):
    # lookup service
    instance = parsed_instance.instance
    services = RestService.objects.filter(xform=instance.xform)
    # call service send with url and instance id
    for sv in services:
        service = sv.get_service_definition()
        service.delay(sv.service_url, parsed_instance.pk, sv)
