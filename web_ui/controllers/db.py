"""
Copyright (c) 2018 Cisco and/or its affiliates.

This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.0 (the "License"). You may obtain a copy of the
License at

               https://developer.cisco.com/docs/licenses

All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.

"""
"""
Database controller the application. All DB functions must be implement within this file
"""
from web_ui.models import *

"""******** Generics ********"""


def save_entity(entity):
    entity.save()


"""******** Groups ********"""


def getGroups(**db_filter):
    return Group.objects.all().filter(**db_filter)

def addGroup(**kwargs):
    return Group(**kwargs).save()


"""******** Devices ********"""

def getDevices(**db_filter):
    return Device.objects.all().filter(**db_filter)

def addDevice(**kwargs):
    return Device(**kwargs).save()