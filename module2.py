from scapy.all import rdpcap, IP

def parse_pcap(pcap_filename):
    print(f"📼 Loading the replay tape: {pcap_filename}...")
    
    try:
        # 1. rdpcap reads the file all at once
        packets = rdpcap(pcap_filename)
        print(f"🔎 I found {len(packets)} packets (digital envelopes) in this file.")
        
        parsed_data = []

        # 2. Loop through every single packet
        for packet in packets:
            # We only care about packets that have IP addresses (Internet Protocol)
            if IP in packet:
                source_ip = packet[IP].src      # The sender
                destination_ip = packet[IP].dst # The receiver
                
                # Store this info nicely
                packet_info = {
                    "src": source_ip,
                    "dst": destination_ip,
                }
                parsed_data.append(packet_info)

        print(f"✅ Finished reading! Extracted {len(parsed_data)} conversations.")
        return parsed_data

    except FileNotFoundError:
        print("❌ Oops! I can't find that PCAP file. Did you type the name right?")
        return []
    except Exception as e:
        print(f"💥 Crash! {e}")
        return []

# Testing the code
if __name__ == "__main__":
    # Ideally, you need a file named 'test_traffic.pcap' in the same folder
    # If you don't have one, this will just say "File not found", which is okay for now!
    data = parse_pcap("test_traffic.pcap")
    
    # Let's print the first 3 conversations just to see if it worked
    if len(data) > 0:
        print("--- PREVIEW OF DATA ---")
        for i in range(min(3, len(data))):
            print(data[i])
