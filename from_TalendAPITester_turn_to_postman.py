import json


# -*- coding: utf-8 -*-

# turn the env setting
def turn_the_env(old_file_path, new_file_path):
    new_json = {}
    with open(old_file_path, 'r', encoding="utf-8") as old_file:
        with open(new_file_path, 'w+', encoding="utf-8") as new_file:
            old_json = json.load(old_file)
            json_name = old_json['environments'][0]['name']
            new_json['name'] = json_name
            new_json['values'] = []
            values = old_json['environments'][0]['variables']
            for each_value in values.items():
                key = each_value[1]['name']
                value = each_value[1]['value']
                enabled = each_value[1]['enabled']
                new_json['values'].append(
                    {
                        "key": key,
                        "value": value,
                        "enabled": enabled
                    }
                )
            json.dump(new_json, new_file)


# turn the API setting
def turn_the_API(old_file_path: str, new_file_path: str):
    new_json = {}
    with open(old_file_path, 'r', encoding="utf-8") as old_file:
        with open(new_file_path, 'w+', encoding="utf-8") as new_file:
            old_json = json.load(old_file)
            name = old_json['entities'][0]['children'][0]['entity']['name']
            description = old_json['entities'][0]['children'][0]['entity']['description']
            new_json["info"] = {
                "name": name,
                "description": description,
                "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
            }
            new_json["item"] = []
            item_base = old_json['entities'][0]['children'][0]['children']
            # TODO fix the json_api turn
            for each_item in item_base:
                each_item = each_item['entity']
                new_json["item"].append(turn_api_request(each_item))
            json.dump(new_json, new_file, ensure_ascii=False)


# turn the request(POST, GET) ok
def turn_api_request(item: dict):
    name = item['name']
    request_method = item['method']['name']
    request_header = [{
        "key": x['name'],
        "value": x['value'],
        "type": "text",
        "disabled": not x['enabled']
    } for x in item['headers']]
    request_body = {
        "mode": 'row',
        "row": item['body']['textBody']
    }
    request_description = item['description'] if 'description' in item else ""
    url_host = [item['uri']['host'].replace('$', '{', 1) + "}"]
    url_path = [x for x in item['uri']['path'].split('/') if x != '']
    url_query = [{
        "key": x['name'],
        "value": x['value'].replace('$', '{', 1) + '}' if "$" in x['value'] else x['value'],
        "disabled": not x["enabled"]
    } for x in item['uri']['query']['items']]
    url_raw = '/'.join(tuple(url_host)) + '/' + '/'.join(url_path) + "?" + '&'.join(
        [x['key'].format() + '=' + x['value'].format() for x in url_query])
    return {
        'name': name,
        'request': {
            "description": request_description,
            "method": request_method,
            "header": request_header,
            "body": request_body,
            "url": {
                "raw": url_raw,
                "host": url_host,
                "path": url_path,
                "query": url_query
            }
        },
        "response": []
    }


if __name__ == '__main__':
    turn_the_env("test.json", "test_new.json")
    turn_the_API("test2.json", "test2_new.json")
