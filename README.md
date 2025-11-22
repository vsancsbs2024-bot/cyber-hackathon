# cyber-hackathon

pip install requests streamlit pandas scapy


# TOR TRAFFIC CORRELATION & FORENSIC INTELLIGENCE SYSTEM
## Comprehensive Technical Project Report (Modules 1–5)
## Version: 1.0 — Prepared for Hackathon Submission

### Installation
pip install requests streamlit pandas scapy

# TABLE OF CONTENTS
1. Introduction
2. Problem Statement & Motivation
3. System Architecture Overview
4. Module 1: TOR Node Collector
5. Module 2: PCAP Parser
6. Module 3: Correlation Engine
7. Module 4: Interactive Dashboard
8. Module 5: Forensic Report Exporter
9. Data Formats & Schemas
10. Security, Ethics & Legal Boundaries
11. Limitations & Future Improvements
12. Conclusion

# 1. INTRODUCTION
The rise of privacy-enhancing technologies like the Tor network enables individuals to browse the internet without revealing their identity. While this promotes privacy and protects journalists, activists, and normal users, it also provides opportunities for criminals to hide behind anonymity layers.
When investigators seize a suspect’s computer or capture network logs, they rarely have tools to:
* Analyze whether Tor was used
* Understand which Tor nodes were contacted
* Reconstruct a probable Tor path
* Automatically correlate traffic metadata
* Produce structured forensic reports
This project solves that gap.

# 2. PROBLEM STATEMENT & MOTIVATION
Law enforcement, cyber forensic teams, and security analysts often obtain **PCAP files** from compromised devices or network monitors. These captures may contain **encrypted Tor traffic**. Although Tor securely hides the user’s identity, investigators still require:
* Confirmation whether Tor was used
* Which exit nodes were involved
* Time correlation between device activity and Tor relay availability
* Patterns and leads for further investigation
* Legally defensible documentation
However, there is **no public tool** that:
* Collects all global Tor nodes
* Parses network captures
* Performs multi-stage correlation
* Predicts likely Tor hops
* Visualizes paths
* Generates final forensic reports
This project fills that gap with a **complete end-to-end forensic analysis system**.

# 3. SYSTEM ARCHITECTURE OVERVIEW
## High-Level Pipeline


# 4. MODULE 1 — TOR NODE COLLECTOR (Highly Detailed)
## 4.1 Purpose
This module collects the **latest Tor relay information** from the official Tor directories and classifies them into relay roles: Entry, Middle, and Exit.
This data will later be used to compare the PCAP’s IP addresses with known Tor relays.

## 4.2 Data Source: Onionoo API
We use:
`https://onionoo.torproject.org/details?type=relay`
This provides **100% public** and **legal** metadata.
It includes:
* Relay **IP addresses**
* Relay **fingerprints**
* Flags (Guard, Exit, HSDir, Running)
* Bandwidth
* Country
* Timestamps (`published`, `last_seen`)

## 4.3 Classification Logic
All relays fall into one of the categories:
| Type | Rule | Purpose in Tor |
|---|---|---|
| **Entry (Guard)** | `guard == True` | First relay – sees user’s real IP |
| **Middle** | Neither Guard nor Exit | Middle hop – encrypted |
| **Exit** | `exit == True` | Final hop – contacts internet |
Note: Middle relays cannot be directly identified as “middle” but are inferred by absence of guard/exit flags.

## 4.4 Data Cleaning & Normalization
Each relay entry is normalized to:
`{ "ip": "185.220.101.31", "role": "exit", "fingerprint": "ABCDEF123456", "published": "2025-02-10T05:00:00Z", "last_seen": "2025-02-11T09:20:00Z", "country": "DE", "bandwidth": 320000 }`

## 4.5 Why Module 1 is Important
When the user supplies a PCAP, the system tries to find matches between PCAP IPs and Tor relays.
Without this module, no correlation is possible.

# 5. MODULE 2 — PCAP PARSER (Detailed Forensic Extraction)
This module transforms the raw network capture into structured, analyzable datasets.

## 5.1 What the Parser Extracts
### Packet-Level Extraction
* Timestamp (Epoch + ISO)
* Source IP, Destination IP
* Source port, Destination port
* Packet length
* TCP flags
* Protocol
* Flow ID (5-Tuple hash)

## 5.2 Flow-Level Extraction
A “flow” = a session based on:
`(srcIP, dstIP, srcPort, dstPort, protocol)`
Each flow logs:
* `flow_start`
* `flow_end`
* of packets
* bytes sent/received
This makes the correlation engine faster and more accurate.

## 5.3 Output Files (Important)
### 1. parsed_pcap.csv
Contains ALL packets.
### 2. parsed_pcap_tor_candidates.csv
Filtered packets that match Tor IPs.
### 3. parsed_flows.csv (optional)
Aggregated flow-level data.
### 4. parsed_pcap.metadata.json
Contains:
* Original PCAP SHA-256 hash
* Packets scanned
* Candidate packets
* Parse timestamp
* Tool version
This acts as **chain-of-custody evidence**.

# 6. MODULE 3 — CORRELATION ENGINE (Deep Technical Explanation)
This is the core logic that reconstructs _probable_ Tor paths.

## 6.1 Core Idea
Tor works like:
`User → Entry → Middle → Exit → Internet`
We cannot see middle hops directly, but we can:
* detect PCAP packets going to **Tor relays**
* match them to timestamps
* reconstruct a chain based on **sequence + timing + relay role**

## 6.2 Step-by-Step Correlation Process
### STEP 1 — Match Packets to Tor Nodes
From `parsed_pcap_tor_candidates.csv`, each row is checked:
`if dst_ip in tor_ip_set → matched as node`
Creates records like:
`pkt #55 → exit node 185.220.101.31 → 2025-11-19 10:15:22`

### STEP 2 — Time Window Linking
Tor circuit creation has very tight timing patterns.
We use windows (e.g., ±1.5 seconds):
`Exit event at t=10.0s Middle event around t=9.5–10.5s Entry event around t=9.0–10.0s`
Packets are grouped by temporal proximity.

### STEP 3 — Build Candidate Paths
For each exit event:
* Look backwards to find a matching middle-relay packet
* Then find a matching entry-relay packet
This creates possible chains like:
`Entry (ip1) → Middle (ip2) → Exit (ip3)`
Each with timestamps and packet support.

### STEP 4 — Feature-Based Scoring Model
To score each chain, we compute:
#### 1. Time Gap Score
Small time difference = more likely.
#### 2. Flow Overlap Score
If many packets belong to same flow.
#### 3. Packet Support
Total number of matched packets.
#### 4. Repetition Score
If pattern repeats (evidence strengthens).
#### 5. Node Reliability Score
Relay uptime & publish timestamp alignment.

### STEP 5 — Composite Score Calculation
`score = normalize( 0.40*time_score + 0.25*flow_overlap + 0.20*packet_support + 0.10*repetition + 0.05*node_reliability )`

### STEP 6 — Output
Top-scoring chains saved to:
`candidates.json`

### STEP 7 — Complete Evidence Log
All matches stored in:
`correlation_log.csv`

# 7. MODULE 4 — INTERACTIVE DASHBOARD (Detailed UX)
A complete web-based visualization tool.

## 7.1 Key UI Features
### 1. Case Upload Panel
* Upload PCAP
* Show PCAP hash
* Store case metadata

### 2. Summary Panel
Contains:
| Item | Description |
|---|---|
| Top predicted path | Entry → Middle → Exit |
| Confidence Score | High/Medium/Low |
| Packets scanned | From PCAP |
| Tor matches found | Candidate packets |
| Case timestamp | Report time |

### 3. Network Graph Visualization
Displays Tor path like a map:
`Client → Entry → Middle → Exit → Target`
Features:
* Hover shows relay info
* Click highlights nodes
* Zoom/pan
* Color-coded nodes (entry=green, middle=blue, exit=red)

### 4. Timeline Player
Allows investigators to:
* Scroll through packet events
* Watch Tor path being reconstructed
* Replay traffic behavior

### 5. Candidate List
Ranked candidate paths:
`#1 score 0.814 #2 score 0.702 #3 score 0.511`
Click to show details.

### 6. Evidence Table
Shows:
* Packet index
* Timestamp
* IP pair
* Packet size
* Protocol
Allows investigators to verify findings in Wireshark.

### 7. Report Export Button
Triggers Module 5 processing.

# 8. MODULE 5 — FORENSIC REPORT EXPORTER (Detailed Report Design)
Generates a **legally defensible** forensic PDF report.

## 8.1 Report Sections (expanded)
### 1. Cover Page
* Project name
* Case ID
* Organization
* Timestamp
* Tool version

### 2. Executive Summary
A short 4–6 sentence explanation of:
* Whether Tor was detected
* Top predicted relay chain
* Confidence of the findings
* Summary of matched evidence

### 3. Chain-of-Custody Metadata
Includes:
* Original PCAP SHA-256
* Parsed CSV SHA-256
* Report SHA-256
* Parsing timestamp
* Operator name
This assures integrity.

### 4. Methodology
Explains:
* What data was used
* No Tor logs
* Only public metadata
* How packets were parsed
* How candidate chains were built

### 5. Top Candidate Paths (Tables)
Displayed in nice tabular format:

### 6. Graph and Timeline Images
* Node graph snapshot
* Timeline of packet events
* Color-coded legend

### 7. Evidence Section
Contains:
* Matched packets
* Packet indices
* Flow IDs
* Event times
* Links to CSV evidence

### 8. Limitations
States:
* No deanonymization
* Correlation is _probabilistic_
* Requires investigator judgement

### 9. Appendix
* Full candidates.json
* Full correlation_log.csv
* Node metadata
* All file hashes

# 9. DATA FORMATS & SCHEMAS
### nodes.json
List of all Tor nodes w/ metadata.
### parsed_pcap.csv
Packet rows (detailed fields).
### parsed_flows.csv
Flow aggregated rows.
### candidates.json
Predicted paths + scores.
### correlation_log.csv
Evidence audit log.
### report.pdf
Final export.

# 10. SECURITY, ETHICS & LEGAL BOUNDARIES
### This tool:
* Does **NOT** break Tor
* Does **NOT** reveal user identity
* Does **NOT** access hidden Tor logs
* Only uses **public nodes** + **local PCAP**
* Provides **investigative leads**, not certainty
All analysis is compliant with:
* Ethical guidelines
* Forensic principles
* Privacy responsibility

# 11. LIMITATIONS
### Technical:
* Cannot deanonymize Tor
* Middle nodes are inferred
* Scoring is probabilistic
* Relies on accuracy of investigator’s PCAP
### Legal:
* Must be used only on authorized data
* Investigators must combine results with other evidence

# 12. FUTURE IMPROVEMENTS
* AI-based Tor traffic fingerprinting
* Multi-incident linking engine
* Tor node risk scoring
* Pluggable transport detection
* Multi-format report exports (PPTX, DOCX)
* Live monitoring integration

# 13. CONCLUSION
This project provides:
* A **complete modular pipeline**
* A **powerful correlation engine**
* A **professional forensic dashboard**
* A **legally defensible reporting system**
* A **unique, innovative solution** not available elsewhere
It is a standout, comprehensive hackathon project demonstrating:
* Networking knowledge
* Forensic analysis
* Data engineering
* Metadata intelligence
* UI/UX design
* Ethical cybersecurity practices

[main_project.py]
