#!/usr/bin/env python3
# This is my first Python script.*
import subprocess
from optparse import OptionParser
import re
import random


# Disclaimer
print("############### Simple MAC_CHANGER by Wolchara000 ###############")


# Random MAC generator
def mac_generator():
    mac = [0x00, 0x24, 0x81,
           random.randint(0x00, 0x7f),
           random.randint(0x00, 0xff),
           random.randint(0x00, 0xff)]

    var = ':'.join(map(lambda x: "%02x" % x, mac))
    return var


# Parser
def get_args():
    parser = OptionParser()
    parser.add_option("-i", "--interface", dest="inter", help="Interface to change MAC on", metavar="INTERFACE")
    (options, arguments) = parser.parse_args()
    if not options.inter:
        parser.error("[-] No Interface were specified. Use -h for help.")
    return options


# MAC change function
def changer(interface1, mac1):
    subprocess.run(["ifconfig", interface1, "down"])
    subprocess.run(["ifconfig", interface1, "hw", "ether", mac1])
    subprocess.run(["ifconfig", interface1, "up"])


# Checker code
def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    mac_search = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ifconfig_result))
    if mac_search:
        return mac_search.group(0)
    else:
        print("[-] Could not read mac address. Check if interface you've entered have one.")


# Main code
new_mac = mac_generator()
options = get_args()
print("[+] Changing MAC on " + str(options.inter) + " to " + str(new_mac))
changer(options.inter, new_mac)
current_mac = get_current_mac(options.inter)
if current_mac == new_mac:
    print("[+] MAC address changed!!!")
else:
    print("[-] Could not change MAC address. Try again.")
