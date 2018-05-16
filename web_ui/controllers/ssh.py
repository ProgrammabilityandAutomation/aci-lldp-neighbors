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
import pexpect
import sys
import time


class SSHController:
    def __init__(self):
        self.child = None

    def connect(self, ip, username):
        """
        Spawns a connection to the given IP
        :param ip:
        :return:
        """

        try:
            self.child = pexpect.spawn(
                'ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null ' + username + '@' + ip)
            return True
        except ImportError:
            print("Error connecting to device " + ip + " with username " + username)
            return False

    def upgradeIE4000Switch(self, ip, username, password, tftpUrl):
        try:
            self.connect(ip, username)
            done = False
            imageName = tftpUrl.split("/")[len(tftpUrl.split("/")) - 1]
            while not done:
                status = self.child.expect(['\(yes\/no\)\?',
                                            '[Pp]assword:',
                                            '#', pexpect.TIMEOUT])
                if status == 0:
                    self.child.sendline("yes")
                elif status == 1:
                    self.child.sendline(password)
                elif status == 2:
                    print(self.child.before)
                    copyDone = False
                    self.child.sendline(
                        "copy tftp://" + tftpUrl + " flash:" + imageName)
                    while not copyDone:
                        statusTftp = self.child.expect(
                            ['Destination filename \[' + imageName + '\]?',
                             'Do you want to over write? \[confirm\]',
                             '#',
                             pexpect.TIMEOUT])
                        if statusTftp == 0 or statusTftp == 1:
                            self.child.sendline("\n")
                        elif statusTftp == 2:
                            copyDone = True
                            print("Done!")
                        print(self.child.before)
                    break
        except:
            raise
        finally:
            print(self.child.before)
