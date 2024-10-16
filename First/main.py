#!/usr/bin/env python



import scapy.all as scapy


def scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    # arp_request.show()
    #print(arp_request.summary())
    # scapy.ls(scapy.ARP)

    brodcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
   # brodcast.show()
    # scapy.ls(scapy.Ether)
    #print(brodcast.summary())

    arp_brodcast_request = brodcast / arp_request


    answered_list= scapy.srp(arp_brodcast_request, timeout=1, verbose=False)[0]
    #print(answered.summary())



    print("\n++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print("    IP\t\t\t\t    MAC Address      +")
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++")

    for element in answered_list:
        print(element[1].psrc, "\t\t\t", element[1].hwsrc, "  +")
        # print(element[1].psrc)
        # to print the (IP) of the target
        # print(element[1].hwsrc)
        #   to print the mac address   the target
        # print("++++++++++++++++++++++++++++")

    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++")


scan("192.168.1.1/24")
