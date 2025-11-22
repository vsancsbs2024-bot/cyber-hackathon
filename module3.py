# We are importing the tool you made in Module 2!
# Make sure your previous file is named 'module2.py'
from module2 import parse_pcap

def load_wanted_list():
    print("📂 Loading the list of bad guy hideouts...")
    wanted_ips = set() # A 'set' is a magic bag that is SUPER fast to search
    
    try:
        with open("tor_nodes.txt", "r") as file:
            for line in file:
                # .strip() cuts off the invisible \n we added earlier!
                ip = line.strip()
                wanted_ips.add(ip)
        print(f"✅ Loaded {len(wanted_ips)} suspect addresses into memory.")
        return wanted_ips
    except FileNotFoundError:
        print("❌ Error: Run Module 1 first! I can't find 'tor_nodes.txt'")
        return set()

def hunt_for_spies(pcap_file):
    # 1. Get the Wanted List (from Module 1's text file)
    tor_nodes = load_wanted_list()
    
    # 2. Get the Traffic Data (using Module 2's tool)
    traffic_data = parse_pcap(pcap_file)
    
    print("\n🕵️‍♂️ STARTING CORRELATION SCAN...")
    print("---------------------------------")
    
    matches_found = []
    
    # 3. The Comparison Loop
    for packet in traffic_data:
        src = packet['src']
        dst = packet['dst']
        
        # THE BIG MOMENT: Is the destination in our Wanted List?
        if dst in tor_nodes:
            print(f"🚨 ALERT! Traffic detected to TOR NODE!")
            print(f"   User: {src}  -->  Tor Node: {dst}")
            matches_found.append(packet)
        else:
            # Optional: print safe traffic just to see it
            # print(f"   [Safe] {src} -> {dst}")
            pass
            
    print("---------------------------------")
    if len(matches_found) > 0:
        print(f"🔥 RESULTS: Found {len(matches_found)} suspicious connections!")
    else:
        print("✅ CLEAN: No Tor traffic found.")

# Run the machine
if __name__ == "__main__":
    hunt_for_spies("test_traffic.pcap")
