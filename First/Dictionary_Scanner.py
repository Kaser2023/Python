#!/usr/bin/env python

import scapy.all as scapy
import subprocess



def scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="00:11:00:22:00:33")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1,              verbose=False)[0]


    kaser_clients = []
    for kaser_element in answered_list:
        kaser_client_dictionary = {"ip": kaser_element[1].psrc, "mac": kaser_element[1].hwsrc}
        kaser_clients.append(kaser_client_dictionary)
        #print(kaser_element[1].psrc + "\t" + kaser_element[1].hwsrc)

    return kaser_clients


def print_results(results):
    print("---------------------------------------------")
    print("IP\t\tAt MAC Address\t")
    print("- - - - - - - - - - - - - - - - - - - - - - -")

    for client in results:
        print(client["ip"] + "\t\t" + client["mac"])


scan_result = scan("192.168.1.1/24")
print_results(scan_result)
