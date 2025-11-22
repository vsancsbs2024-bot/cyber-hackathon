import requests  # This is our Robot Butler

def fetch_tor_nodes():
    print("🤖 BEEP BOOP... Robot Butler is starting...")
    print("🌏 Going to the internet to find the list of Secret Doors...")

    # This is the website URL that keeps the official list of Tor Exit Nodes
    # It updates automatically!
    url = "https://check.torproject.org/torbulkexitlist"

    try:
        # 1. Send the Robot Butler to get the list
        response = requests.get(url)

        # 2. Check if the Robot came back successfully (Code 200 means 'OK!')
        if response.status_code == 200:
            print("✅ Success! I found the list!")
            
            # 3. The list is just one big chunk of text. Let's split it line by line.
            tor_ips = response.text.splitlines()
            print(tor_ips)
            print(f"😲 Wow! We found {len(tor_ips)} Tor nodes active right now.")
            
            # 4. Let's save this list to a file so we can use it later
            with open("tor_nodes.txt", "w") as file:
                for ip in tor_ips:
                    file.write(ip + "\n")
            
            print("📁 I saved all the addresses into 'tor_nodes.txt' for you.")
            
        else:
            print("❌ Oh no! The website didn't let us in.")

    except Exception as e:
        print(f"💥 Crash! Something went wrong: {e}")

# This line tells the computer to actually run the function above
if __name__ == "__main__":
    fetch_tor_nodes()
