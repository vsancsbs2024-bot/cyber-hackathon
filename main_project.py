# =================================================================
# TOR TRAFFIC CORRELATION & FORENSIC INTELLIGENCE SYSTEM
# (Full, Final Version with Timestamp Fix)
# =================================================================

# 1. --- IMPORTS (The entire toolkit) ---
import requests
import streamlit as st
import pandas as pd
from scapy.all import rdpcap, IP
import os

# --- Configuration ---
TOR_NODES_FILE = "tor_nodes.txt"
PCAP_TARGET = "test_traffic.pcap" 

# =================================================================
# MODULE 1: TOR NODE COLLECTOR (The List of Secret Doors)
# =================================================================

def fetch_tor_nodes_and_save():
    """Fetches the list of Tor Exit Nodes and saves them to a file."""
    if os.path.exists(TOR_NODES_FILE):
        return # Skip if file already exists for fast demoing
        
    st.sidebar.write("🤖 Module 1: Fetching Tor Node List...")
    url = "https://check.torproject.org/torbulkexitlist"
    
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            tor_ips = response.text.splitlines()
            with open(TOR_NODES_FILE, "w") as file:
                for ip in tor_ips:
                    file.write(ip + "\n")
            st.sidebar.success(f"✅ Found and saved {len(tor_ips)} Tor nodes!")
        else:
            st.sidebar.error(f"❌ Failed to fetch list (Status: {response.status_code})")
    except Exception as e:
        st.sidebar.error(f"💥 Crash fetching Tor list: {e}")

def load_wanted_list():
    """Loads the Tor Node IPs from file into a fast-search Set."""
    wanted_ips = set()
    try:
        with open(TOR_NODES_FILE, "r") as file:
            for line in file:
                wanted_ips.add(line.strip())
        return wanted_ips
    except FileNotFoundError:
        st.sidebar.error("❌ Error: tor_nodes.txt not found. Run collector first!")
        return set()

# =================================================================
# MODULE 2: PCAP PARSER (The Time Traveler) - UPDATED with time_stamp
# =================================================================

def parse_pcap(pcap_filename):
    """Reads a PCAP file and extracts SRC, DST, and Time."""
    st.sidebar.write(f"📼 Module 2: Reading {pcap_filename}...")
    try:
        packets = rdpcap(pcap_filename)
        parsed_data = []

        for packet in packets:
            if IP in packet:
                # CRITICAL UPDATE: Grabbing the raw Unix timestamp
                time_stamp = packet.time
                
                packet_info = {
                    "src": packet[IP].src,
                    "dst": packet[IP].dst,
                    "time_stamp": time_stamp  # Time clue included!
                }
                parsed_data.append(packet_info)
        
        st.sidebar.success(f"🔎 Extracted {len(parsed_data)} conversations!")
        return parsed_data

    except FileNotFoundError:
        st.sidebar.error(f"❌ PCAP file '{pcap_filename}' not found!")
        return []
    except Exception as e:
        st.sidebar.error(f"💥 Crash parsing PCAP: {e}")
        return []

# =================================================================
# MODULE 3: CORRELATION ENGINE (The Gotcha! Machine)
# =================================================================

def hunt_for_spies(pcap_filename):
    """Correlates traffic data against the Tor node list."""
    st.sidebar.write("\n🧠 Module 3: Starting Correlation Scan...")
    
    tor_nodes = load_wanted_list()
    traffic_data = parse_pcap(pcap_filename)
    
    matches_found = []
    
    for packet in traffic_data:
        dst = packet['dst']
        
        # CORE LOGIC: Check destination against the Magic Index
        if dst in tor_nodes:
            matches_found.append(packet)
            
    st.sidebar.success(f"🔥 Found {len(matches_found)} suspicious connections!")
    return matches_found

# =================================================================
# MODULE 4: INTERACTIVE DASHBOARD (The Command Center) - UPDATED with error fix
# =================================================================

def create_dashboard(correlated_data):
    """Creates and displays the Streamlit dashboard."""
    
    st.set_page_config(layout="wide")
    st.title("🚨 TOR FORENSIC SPY HQ 🚨")
    st.caption("Correlation Intelligence System (TN Govt. Hackathon)")
    
    if not correlated_data:
        st.warning("No suspicious traffic found, or check the status panel on the left.")
        return

    # 1. Convert to DataFrame
    df = pd.DataFrame(correlated_data)

    # 2. CRITICAL FIX: Ensure timestamp column is numeric before conversion
    try:
        df['time_stamp'] = pd.to_numeric(df['time_stamp'])
    except ValueError as e:
        st.error("Pandas conversion failed. Timestamps might be corrupted or missing.")
        return

    # 3. Format the time (Making computer time human-readable!)
    df['Time_of_Contact'] = pd.to_datetime(df['time_stamp'], unit='s')
    
    # 4. Clean and Prepare for Display
    
    # Add fake location data for the map (Placeholder for GeoIP lookup)
    df['lat'] = df['src'].apply(lambda x: 13.0827 + (hash(x) % 1000) * 0.0005) # Fake Lat based on IP hash
    df['lon'] = df['src'].apply(lambda x: 80.2707 + (hash(x) % 1000) * 0.0005) # Fake Lon based on IP hash
    
    df = df.rename(columns={'src': 'Suspect_IP', 'dst': 'Tor_Node_Contacted'})
    df = df[['Time_of_Contact', 'Suspect_IP', 'Tor_Node_Contacted', 'lat', 'lon']] # Select final columns

    # Display Widgets
    st.subheader("📊 Intelligence Summary")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Total Tor Connections Detected", value=len(df))
    with col2:
        st.metric(label="Unique Suspect IPs", value=df['Suspect_IP'].nunique())
    
    st.subheader("🕵️‍♂️ Correlated Traffic Log (Evidence Table)")
    st.dataframe(df.drop(columns=['lat', 'lon']), use_container_width=True) # Hide lat/lon in main table

    st.subheader("🗺️ Suspect Origin Map View")
    st.map(df, latitude='lat', longitude='lon', zoom=10)

# =================================================================
# MAIN EXECUTION
# =================================================================

if __name__ == "__main__":
    
    st.sidebar.title("System Status")
    
    # 1. Run Module 1 to get the list
    fetch_tor_nodes_and_save()
    
    # 2. Run Modules 2 & 3 (The Hunt!)
    final_matches = hunt_for_spies(PCAP_TARGET)
    
    # 3. Run Module 4 (The Display)
    create_dashboard(final_matches)
