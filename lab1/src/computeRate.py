from scapy.config import conf
conf.ipv6_enabled = False
from scapy.all import *
from scapy.layers.inet import IP, TCP, UDP
import sys
import time

# read pcap
packets_TCP_h3 = rdpcap('../out/TCP_h3.pcap') 
packets_TCP_h4 = rdpcap('../out/TCP_h4.pcap') 
packets_UDP_h3 = rdpcap('../out/UDP_h3.pcap') 
packets_UDP_h4 = rdpcap('../out/UDP_h4.pcap') 

flow_TCP_h3_1 = {'proto': TCP, 'dst_port': 7777}
flow_TCP_h3_2 = {'proto': TCP, 'dst_port': 8888}
flow_TCP_h4 = {'proto': TCP,  'dst_port': 7777}

flow_UDP_h3_1 = {'proto': UDP, 'dst_port': 7777}
flow_UDP_h3_2 = {'proto': UDP, 'dst_port': 8888}
flow_UDP_h4 = {'proto': UDP, 'dst_port': 7777}


def calculate_flow_rate(packets, flow_info):
    proto = flow_info['proto']
    startTime = 0
    endTime = 0
    count = 0
    packet_size_sum = 0
    for packet in packets[proto]:
        # Check if the packet matches the flow criteria
        if (packet.dport == flow_info['dst_port'] or packet.sport == flow_info['dst_port']):
            if count == 0:
                startTime = packet.time
            count += 1
            packet_size_sum += len(packet)
            endTime = packet.time
    packet_size = packet_size_sum / count
    duration = endTime - startTime
    # print (count, packet_size)
    # print (duration)
    rate = float(count) / float(duration) * packet_size * 8 / 1000000
    return rate

print (f"--- TCP ---")
rate = calculate_flow_rate(packets_TCP_h3, flow_TCP_h3_1)
print (f"Flow1(h1->h3): {rate} Mbps")
rate = calculate_flow_rate(packets_TCP_h3, flow_TCP_h3_2)
print (f"Flow2(h1->h3): {rate} Mbps")
rate = calculate_flow_rate(packets_TCP_h4, flow_TCP_h4)
print(f"Flow3(h2->h4): {rate} Mbps")

print (f"--- UDP ---")
rate = calculate_flow_rate(packets_UDP_h3, flow_UDP_h3_1)
print (f"Flow1(h1->h3): {rate} Mbps")
rate = calculate_flow_rate(packets_UDP_h3, flow_UDP_h3_2)
print (f"Flow2(h1->h3): {rate} Mbps")
rate = calculate_flow_rate(packets_UDP_h4, flow_UDP_h4)
print (f"Flow3(h2->h4): {rate} Mbps")
