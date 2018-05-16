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
from __future__ import unicode_literals
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
import json
import traceback
from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer
from web_ui.controllers.apic import ApicController
from web_ui.controllers.ssh import SSHController
from web_ui.controllers import db
from django.forms.models import model_to_dict
from django.core import serializers


# ====================>>>>>>>> Utils <<<<<<<<====================
class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """

    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


# ====================>>>>>>>> Templates <<<<<<<<====================

def login(request):
    return render(request, 'web_app/login.html')


def index(request):
    return render(request, 'web_app/index.html')


def home(request):
    return render(request, 'web_app/home.html')


def devices(request):
    return render(request, 'web_app/devices.html')


def configuration(request):
    return render(request, 'web_app/config.html')


def upgrade(request):
    return render(request, 'web_app/upgrade.html')


# ====================>>>>>>>> APIs <<<<<<<<====================
@csrf_exempt
def api_get_neighbors(request):
    """
    Return an apic neighbors
    :param request:
    :return:
    """
    if request.method == 'GET':
        try:
            # return JSONResponse([{'fabricLooseNode': {'attributes': {'childAction': '', 'dn': 'topology/lsnode-10.0.226.249', 'id': '10.0.226.249', 'lcOwn': 'local', 'modTs': '2018-01-04T20:45:13.803-05:00', 'monPolDn': 'uni/fabric/monfab-default', 'name': '', 'nameAlias': '', 'operIssues': '', 'status': '', 'sysDesc': 'Cisco Nexus Operating System (NX-OS) Software\nTAC support: http://www.cisco.com/tac\nCopyright (c) 2002-2016, Cisco Systems, Inc. All rights reserved.', 'sysName': 'ucs-TT14-B', 'lldpNodes': ['topology/pod-1/node-203/']}}}, {'fabricLooseNode': {'attributes': {'childAction': '', 'dn': 'topology/lsnode-10.0.243.14', 'id': '10.0.243.14', 'lcOwn': 'local', 'modTs': '2017-06-18T20:26:46.416-05:00', 'monPolDn': 'uni/fabric/monfab-default', 'name': '', 'nameAlias': '', 'operIssues': '', 'status': '', 'sysDesc': 'Cisco Nexus Operating System (NX-OS) Software 6.0(2)U3(7)\nTAC support: http://www.cisco.com/tac\nCopyright (c) 2002-2015, Cisco Systems, Inc. All rights reserved.', 'sysName': 'n3k-top'}}}, {'fabricLooseNode': {'attributes': {'childAction': '', 'dn': 'topology/lsnode-10.0.226.248', 'id': '10.0.226.248', 'lcOwn': 'local', 'modTs': '2018-01-04T20:45:14.239-05:00', 'monPolDn': 'uni/fabric/monfab-default', 'name': '', 'nameAlias': '', 'operIssues': '', 'status': '', 'sysDesc': 'Cisco Nexus Operating System (NX-OS) Software\nTAC support: http://www.cisco.com/tac\nCopyright (c) 2002-2016, Cisco Systems, Inc. All rights reserved.', 'sysName': 'ucs-TT14-A', 'lldpNodes': ['topology/pod-1/node-203/']}}}, {'fabricLooseNode': {'attributes': {'childAction': '', 'dn': 'topology/lsnode-10.0.243.15', 'id': '10.0.243.15', 'lcOwn': 'local', 'modTs': '2018-01-04T20:45:49.470-05:00', 'monPolDn': 'uni/fabric/monfab-default', 'name': '', 'nameAlias': '', 'operIssues': '', 'status': '', 'sysDesc': 'Cisco Nexus Operating System (NX-OS) Software 6.0(2)U3(7)\nTAC support: http://www.cisco.com/tac\nCopyright (c) 2002-2015, Cisco Systems, Inc. All rights reserved.', 'sysName': 'n3k-bottom', 'lldpNodes': ['topology/pod-1/node-203/']}}}, {'fabricLooseNode': {'attributes': {'childAction': '', 'dn': 'topology/lsnode-10.0.243.38', 'id': '10.0.243.38', 'lcOwn': 'local', 'modTs': '2017-05-18T13:10:10.629-05:00', 'monPolDn': 'uni/fabric/monfab-default', 'name': '', 'nameAlias': '', 'operIssues': '', 'status': '', 'sysDesc': 'Red Hat Enterprise Linux Server 7.3 (Maipo) Linux 3.10.0-514.el7.x86_64 #1 SMP Wed Oct 19 11:24:13 EDT 2016 x86_64', 'sysName': 'os-getsvs-1', 'lldpNodes': ['topology/pod-1/node-203/']}}}, {'fabricLooseNode': {'attributes': {'childAction': '', 'dn': 'topology/lsnode-10.0.243.39', 'id': '10.0.243.39', 'lcOwn': 'local', 'modTs': '2017-05-26T12:41:54.352-05:00', 'monPolDn': 'uni/fabric/monfab-default', 'name': '', 'nameAlias': '', 'operIssues': '', 'status': '', 'sysDesc': 'Red Hat Enterprise Linux Server 7.3 (Maipo) Linux 3.10.0-514.el7.x86_64 #1 SMP Wed Oct 19 11:24:13 EDT 2016 x86_64', 'sysName': 'os-getsvs-2'}}}])
            # Parse the json
            apic = ApicController()
            apic.url = request.session["url"]
            apic.token = request.session["token"]
            pods = apic.getPods()
            lldpNodes = []
            manageByACI = False
            present = False

            for pod in apic.getPods():
                podInventory = apic.getSwitches(pod_dn=pod["fabricPod"]["attributes"]["dn"])
                for leaf in apic.getLeafs(pod_dn=pod["fabricPod"]["attributes"]["dn"]):
                    print("Checking switch " + leaf["fabricNode"]["attributes"]["dn"])
                    for neighborItfc in apic.getLldpNeighbors(switch_dn=leaf["fabricNode"]["attributes"]["dn"]):
                        # Check that neighbor is not part of the inventory
                        for neighbor in neighborItfc["lldpIf"]["children"]:
                            manageByACI = False
                            for switch in podInventory:
                                if switch["fabricNode"]["attributes"]["dn"] == \
                                        neighbor["lldpAdjEp"]["attributes"]["sysDesc"]:
                                    manageByACI = True
                                    break
                            if not manageByACI:
                                if neighbor["lldpAdjEp"]["attributes"]["sysName"] != "" and "apic" not in \
                                        neighbor["lldpAdjEp"]["attributes"]["sysName"]:
                                    # Neighbor found
                                    # Getting name
                                    for switch_in in podInventory:
                                        if neighborItfc["lldpIf"]["attributes"]["sysDesc"] == \
                                                switch_in["fabricNode"]["attributes"]["dn"]:
                                            neighborName = switch_in["fabricNode"]["attributes"]["name"]
                                            break

                                    present = False

                                    for item in lldpNodes:
                                        if item["name"] == neighbor["lldpAdjEp"]["attributes"]["sysName"]:
                                            item["neighbors"].append("Device " + neighborName + " port " +
                                                                     neighborItfc["lldpIf"]["attributes"]["id"])
                                            present = True
                                            break
                                    if not present:
                                        lldpNodes.append({"name": neighbor["lldpAdjEp"]["attributes"]["sysName"],
                                                          "mgmtIp": neighbor["lldpAdjEp"]["attributes"]["mgmtIp"],
                                                          "neighbors": ["Device " + neighborName + " port " +
                                                                        neighborItfc["lldpIf"]["attributes"]["id"]]})

            return JSONResponse(lldpNodes)
        except Exception as e:
            print(traceback.print_exc())
            # return the error to web client
            return JSONResponse({'error': e.__class__.__name__, 'message': str(e)}, status=500)
    else:
        return JSONResponse("Bad request. " + request.method + " is not supported", status=400)


@csrf_exempt
def api_login(request):
    """
    Return an apic neighbors
    :param request:
    :return:
    """
    if request.method == 'POST':
        try:
            payload = json.loads(request.body)
            apic = ApicController()
            apic.url = payload["url"]
            request.session['apic_url'] = payload["url"]
            token = apic.get_token(username=payload["username"],
                                   password=payload["password"])
            request.session["token"] = token
            request.session["url"] = apic.url
            return JSONResponse("ok")
        except Exception as e:
            print(traceback.print_exc())
            # return the error to web client
            return JSONResponse({'error': e.__class__.__name__, 'message': str(e)}, status=500)
    else:
        return JSONResponse("Bad request. " + request.method + " is not supported", status=400)


@csrf_exempt
def api_upgrade_device(request):
    """
    Opens a ssh connection to manually copy and upgrade device
    :param request:
    :return:
    """
    if request.method == 'POST':
        try:
            payload = json.loads(request.body)
            sshCtrl = SSHController()
            sshCtrl.upgradeIE4000Switch(ip=payload["mgmtIp"],
                                        username=payload["username"],
                                        password=payload["password"],
                                        tftpUrl=payload["upgradeURL"])
            return JSONResponse("ok")
        except Exception as e:
            print(traceback.print_exc())
            # return the error to web client
            return JSONResponse({'error': e.__class__.__name__, 'message': str(e)}, status=500)
    else:
        return JSONResponse("Bad request. " + request.method + " is not supported", status=400)


@csrf_exempt
def api_group(request):
    """
    Creates and retrieves groups
    :param request:
    :return:
    """
    if request.method == 'POST':
        # Create a group
        try:
            payload = json.loads(request.body)
            db.addGroup(name=payload["name"])
            group = db.getGroups(name=payload["name"])[0]
            for device in payload["devices"]:
                db.addDevice(group=group, name=device["name"], ip=device["mgmtIp"])
            return JSONResponse("ok")
        except Exception as e:
            print(traceback.print_exc())
            # return the error to web client
            return JSONResponse({'error': e.__class__.__name__, 'message': str(e)}, status=500)
    elif request.method == 'GET':
        # Get all groups
        try:
            groupsQS = db.getGroups()
            groups = []
            for group in groupsQS:
                groupDict = model_to_dict(group)
                groupDict["devices"] = []
                devicesQS = db.getDevices(group=group)
                for device in devicesQS:
                    groupDict["devices"].append(model_to_dict(device))
                groups.append(groupDict)
            return JSONResponse(groups)
        except Exception as e:
            print(traceback.print_exc())
            # return the error to web client
            return JSONResponse({'error': e.__class__.__name__, 'message': str(e)}, status=500)
    else:
        return JSONResponse("Bad request. " + request.method + " is not supported", status=400)
