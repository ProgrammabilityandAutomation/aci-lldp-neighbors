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
URL mapping of the application
"""

from django.conf.urls import url

from . import views

urlpatterns = [

    url(r'^$', views.index),

    # Angular mappings
    url(r'^home/?$', views.index),
    url(r'^ng/home/?$', views.home),
    url(r'^devices/?$', views.index),
    url(r'^ng/devices/?$', views.devices),
    url(r'^configuration/?$', views.index),
    url(r'^ng/configuration/?$', views.configuration),
    url(r'^upgrade/?$', views.index),
    url(r'^ng/upgrade/?$', views.upgrade),

    # APIs Mappings
    url(r'^api/neighbors/?$', views.api_get_neighbors),
    url(r'^api/login/?$', views.api_login),
    url(r'^api/upgrade/?$', views.api_upgrade_device),
    url(r'^api/groups/?$', views.api_group),
]
