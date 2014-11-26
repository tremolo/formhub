import httplib2
import json
from celery import task
from odk_viewer.models import ParsedInstance
from restservice.models import RestServiceAnswer
from httplib2 import RelativeURIError, ServerNotFoundError
import time

from django.conf import settings

#If we ever want to use it uncomment
#from utils.bamboo import get_new_bamboo_dataset, get_bamboo_url


def get_network_data(method, url, headers, post_data, parsed_instance, services):
    http = httplib2.Http()

    for i in range(3):
        try:
            
            if method == "GET":
                requ, content =  http.request(url, 'GET')
            elif method == "POST":
                requ, content = http.request(uri=url, method=method,
                                     headers=headers,
                                     body=post_data)
        except RelativeURIError:
            status = "500"
            content = "RelativeURIError"
        except ServerNotFoundError:
            status = "500"
            content = "ServerNotFoundError"
        except Exception as e:
            status = "500"
            content = unicode( type(e) )
        else:
            status = requ["status"]
            
        response = RestServiceAnswer()
        response.service = services
        response.instance = parsed_instance
        response.returnCode = status 
        response.returnText = content
        response.iteration = i
        response.save()

        #Also add it to Mongo
        record = {}
        record["url"] = unicode(url)
        record["status"] = unicode(status)
        record["content"] = unicode(content)
        record["try"] = i
        record["timestamp"] = unicode(response.date)
        
        mongo_instance = settings.MONGO_DB.instances
        
        mongo_instance.update({"_id":parsed_instance.pk}, { '$push': { "webhooks" :record } })
        
        #If the status is 200 everything is fine
        if status == '200':
            break
        
        #So we give the service some time to recover, if that is the problem
        time.sleep(60)
    
    


@task()
def generic_json(url, parsed_instance_pk, services):
    
    parsed_instance = ParsedInstance.objects.get(pk=parsed_instance_pk)
    
    post_data = json.dumps(parsed_instance.to_dict_for_mongo())
    headers = {"Content-Type": "application/json"}
    
    return get_network_data("POST", url, headers, post_data, parsed_instance, services)

    
    
@task()
def generic_xml(url, parsed_instance_pk, services):

    parsed_instance = ParsedInstance.objects.get(pk=parsed_instance_pk)

    instance = parsed_instance.instance
    headers = {"Content-Type": "application/xml"}

    return get_network_data("POST", url, headers, instance.xml, parsed_instance, services)

@task()
def f2dhis2(url, parsed_instance_pk, services):
    parsed_instance = ParsedInstance.objects.get(pk=parsed_instance_pk)

    instance = parsed_instance.instance
    info = {"id_string": instance.xform.id_string, "uuid": instance.uuid}
    valid_url = url % info
    
    return get_network_data("GET", valid_url, None, None, parsed_instance, services)
    
# For now we don't need this. 
# But should work as a dropin replacement
# def bamboo(self, url, parsed_instance):
# 
#     xform = parsed_instance.instance.xform
#     rows = [parsed_instance.to_dict_for_mongo()]
# 
#     # prefix meta columns names for bamboo
#     prefix = (u'%(id_string)s_%(id)s'
#               % {'id_string': xform.id_string, 'id': xform.id})
# 
#     for row in rows:
#         for col, value in row.items():
#             if col.startswith('_') or col.startswith('meta_') \
#                 or col.startswith('meta/'):
#                 new_col = (u'%(prefix)s%(col)s'
#                            % {'prefix': prefix, 'col': col})
#                 row.update({new_col: value})
#                 del(row[col])
# 
#     # create dataset on bamboo first (including current submission)
#     if not xform.bamboo_dataset:
#         dataset_id = get_new_bamboo_dataset(xform, force_last=True)
#         xform.bamboo_dataset = dataset_id
#         xform.save()
#     else:
#         dataset = Dataset(connection=Connection(url=get_bamboo_url(xform)),
#                           dataset_id=xform.bamboo_dataset)
#         dataset.update_data(rows=rows)
#         
#     return
