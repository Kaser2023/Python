#!/usr/bin/env python

import subprocess
import optparse
import re


# ----------------------------------------------------------------
# Coded by: Abdullah Alqurashi.
# ----------------------------
# Git-Hub: https://github.com/Kaser2023
# Linked-In: https://www.linkedin.com/in/abdullah-alqurashi-a3777a224/
# Date: 13.Rabi'a Alakhir. 1446 -  2024.Oct.16
# ----------------------------------------------------------------



def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Change interface Mac address")
    parser.add_option("-m", "--mac", dest="new_mac", help="Add the new Mac address")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("[-] Please specify an interface, user --help for more information ")
    if not options.new_mac:
        parser.error("[-] Please specify a new mac, user --help for more information ")
    return options

def mac_change(interface, new_mac):
    print("[+] Changing Mac address for " + interface + " to " + new_mac)
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])

def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    #result = ifconfig_result.decode("utf-8")
    #result = str(ifconfig_result)
    # print(result)
    Mac_Search_Result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ifconfig_result))
    if Mac_Search_Result:
        return Mac_Search_Result.group(0)
    else:
        print("[-] Could not read Mac address.")


options = get_arguments()
#it is for getting the arguments that the user enters

current_mac = get_current_mac(options.interface)
#it is going to get the current Mac using the  Get_Current_Mac function

print("The Current Mac = " + current_mac)
#it is for printing the current Mac

mac_change(options.interface, options.new_mac)
#it is the step where the Mac_Address will get changed.

current_mac = get_current_mac(options.interface)
if current_mac == options.new_mac:
    print("[+]The Mac Address was changed successfully to: " + current_mac)
else:
    print("[-] The Mac Address was not changed!")