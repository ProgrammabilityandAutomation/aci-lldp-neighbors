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
# Create your models here.
from __future__ import unicode_literals

from django.db import models


# Create your models here.

class Group(models.Model):
    name = models.CharField(max_length=200)


class Device(models.Model):
    name = models.CharField(max_length=200)
    ip = models.CharField(max_length=200)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
