#!/usr/bin/env python



import scapy.all as scapy


def scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    arp_request.show()
    #print(arp_request.summary())
    # scapy.ls(scapy.ARP)

    brodcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    brodcast.show()
    # scapy.ls(scapy.Ether)
    #print(brodcast.summary())

    arp_brodcast_request = brodcast / arp_request
    #arp_brodcast_request = scapy.Ether(dst="ff:ff:ff:ff:ff:ff") / scapy.ARP(pdst=ip) #This is jusy my oponion
    #print(arp_brodcast_request.summary())
    arp_brodcast_request.show()

    answered, unanswered = scapy.srp(arp_brodcast_request, timeout=1)
    print(answered.summary())


scan("192.168.1.1/24")
