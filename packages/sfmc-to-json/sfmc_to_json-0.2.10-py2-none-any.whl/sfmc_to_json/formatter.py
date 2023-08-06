import json

'''
Salesforce API will return two different payloads:
    - for SOAP it will be a SUDS object
    - for REST it will be a REST object

This library will help jsonify the salesforce response
no matter SOAP or REST
'''

def sfmc_to_json(obj=None, object_name='element'):
    """Take an object and drop it into JSON, the object_name parameter is used
        to prefex the JSON package"""
    if isinstance(obj, dict):
        data = obj["items"]
    elif isinstance(obj, list):
        data = _list_of_suds_to_json(object_name, obj)
    else:
        data = _suds_to_json(obj)
    key_prefix = (object_name+"s").lower()
    return { key_prefix : data }
    #return data

def _recursive_asdict(d):
    """Convert Suds object (What API returns) into serializable format."""
    out = {}
    for k, v in _asdict(d).items():
        if hasattr(v, "__keylist__"):
            out[k] = _recursive_asdict(v)
        elif isinstance(v, list):
            out[k] = []
            for item in v:
                if hasattr(item, "__keylist__"):
                    out[k].append(_recursive_asdict(item))
                else:
                    out[k].append(item)
        else:
            out[k] = v
    return out

def _suds_to_json(data):
    """Takes a suds object to a json object, will recurse and hand date objects"""
    json_string = json.dumps(_recursive_asdict(data), indent=4, sort_keys=True, default=str)
    return json.loads(json_string)

def _list_of_suds_to_json(object_name, list):
    """Processes a list of suds objects (can be nested) and turns in to json object"""
    data = []
    for item in list:
        my_json =  _suds_to_json(item)
        data.append(my_json)
    return data

def _items(sobject):
    """
    Extract the I{items} from a suds object much like the
    items() method works on I{dict}.
    @param sobject: A suds object
    @type sobject: L{Object}
    @return: A list of items contained in I{sobject}.
    @rtype: [(key, value),...]
    """
    for item in sobject:
       #print(item)
        yield item

def _asdict(sobject):
    """
    Convert a sudsobject into a dictionary.
    @param sobject: A suds object
    @type sobject: L{Object}
    @return: A python dictionary containing the
        items contained in I{sobject}.
    @rtype: dict
    """
    items = _items(sobject)
    #if len(list(items)) == 0:
    #    items.append("Null")
    return dict(items)
