import requests
#import csv
import json
#import re

#class WebphoneInfo():
def call_webphone(uid):
    request_url = "http://tabularasa.web.att.com/api/webphone/json/{}".format(uid)
    full_profile = json.loads(str(requests.get(request_url).text))
    return full_profile

#print(call_webphone("dl268k"))

def get_profile(uid):
    full_profile = call_webphone(uid)
    profile_dict = {}
    profile_dict['name'] = full_profile['first_name'].title() + " " + full_profile['last_name'].title()
    profile_dict['job_title'] = full_profile['jt_name'].title()
    profile_dict['department'] = full_profile['dept_name'].title()
    profile_dict['bus_unit'] = full_profile['bus_unit_name']
    profile_dict['location'] = full_profile['city'].title() +" "+full_profile['state']

    return profile_dict


def get_manager_name(uid):
    full_profile = call_webphone(uid)
    manager_uid = full_profile['supervisor_id']
    manager_profile = call_webphone(manager_uid)
    manager_name = manager_profile['first_name'].title()+" "+manager_profile['last_name'].title()
    return manager_name


def get_report_chain(uid):
    report_chain_list = [get_profile(uid)['name']]
    while call_webphone(uid)['supervisor_id']:
        report_chain_list.append(get_manager_name(uid))
        uid = call_webphone(uid)['supervisor_id']

    report_chain = ""
    t = 0
    for name in reversed(report_chain_list):
        report_chain += ("  "*t+name+"\n")
        t+=1
    return report_chain


print(get_report_chain("dl268k"))
