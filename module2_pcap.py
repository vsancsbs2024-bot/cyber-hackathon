from scapy.all import IP, wrpcap
# This is a setup script to create a FAKE pcap file for testing

print("🛠️ Creating a fake traffic recording...")

# Create 2 fake packets
# Packet 1: Normal traffic (Google DNS)
pkt1 = IP(src="192.168.1.5", dst="8.8.8.8")

# Packet 2: SUSPICIOUS traffic (One of the Tor Nodes from your list!)
# (Check your tor_nodes.txt for a real IP to put here to test later)
pkt2 = IP(src="192.168.1.5", dst="185.220.101.1") 

# Save them to a file
wrpcap("test_traffic.pcap", [pkt1, pkt2])

print("✅ 'test_traffic.pcap' created! Now run module2_parser.py")
