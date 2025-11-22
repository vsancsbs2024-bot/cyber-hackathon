import streamlit as st # The Magic Wand
import pandas as pd     # The Table Organizer

# --- 1. SET UP THE COMMAND CENTER ---
st.set_page_config(layout="wide") # Makes the dashboard fill the screen
st.title("🚨 TOR TRAFFIC FORENSIC COMMAND CENTER 🚨")
st.caption("Tracking bad guys using the Secret Door (Tor) network.")

# --- 2. THE INPUT DATA (Pretend this came from Module 3) ---
# We have a list of all the suspicious conversations we found!
suspect_data = {
    'Suspect_IP': ['192.168.1.5', '10.0.0.2', '172.16.0.8'],
    'Tor_Node_Contacted': ['185.220.101.1', '192.42.116.16', '94.140.15.5'],
    'Location': ['Chennai', 'Coimbatore', 'Madurai'],
    'Time_of_Contact': ['10:00:15', '10:00:30', '10:01:05'],
    # Streamlit can map latitude/longitude, so let's add coordinates for the IPs!
    'lat': [13.0827, 11.0168, 9.9252],  # Fake Latitude for Tamil Nadu cities
    'lon': [80.2707, 76.9558, 78.1198]   # Fake Longitude
}

# Turn the list into a neat table (Pandas DataFrame)
df = pd.DataFrame(suspect_data)

# --- 3. DISPLAY THE RESULTS ---
st.subheader("📊 Intelligence Summary")
total_spies = len(df)

# Show a big number counter!
st.metric(label="Suspect Connections Detected", value=total_spies)

# --- 4. THE EVIDENCE TABLE ---
st.subheader("🕵️‍♂️ Correlated Traffic Log (RED ALERT!)")
st.dataframe(df, use_container_width=True) # Show the table nicely

# --- 5. THE MAP VISUALIZATION (This looks super cool!) ---
st.subheader("🗺️ Geographic Location of Suspects (Map View)")
# Streamlit knows how to plot 'lat' and 'lon' on a map automatically!
st.map(df, latitude='lat', longitude='lon', zoom=6)
