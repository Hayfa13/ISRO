import streamlit as st
import json
import pandas as pd
import requests
from datetime import datetime

# ---------- Load JSON Data ----------
with open("placement_input.json") as f:
    data = json.load(f)
items = data["items"]
containers = data["containers"]

with open("waste_output.json") as f:
    waste_data = json.load(f)

# Load placement output
with open("placement_output.json") as f:
    placement_output = json.load(f)

# ---------- Sidebar Navigation ----------
st.sidebar.title("🚀 ISS Cargo Dashboard")
section = st.sidebar.radio("Navigate", [
    "Overview",
    "Items & Containers",
    "Run Placement",
    "3D Visualization",
    "Waste Detection",
    "Simulate Time",
    "Search Item",
    "Export & Logs"
])

# ---------- Overview ----------
if section == "Overview":
    st.title("🛰️ ISS Cargo Optimization")
    st.markdown("Welcome, astronaut logistics assistant! This dashboard lets you organize, track, and simulate cargo management on the ISS.")
    st.markdown("- 📦 View items & containers")
    st.markdown("- 🤖 Run smart placement algorithm")
    st.markdown("- 🧹 Detect waste and expired items")
    st.markdown("- ⏩ Simulate days in space")
    st.markdown("- 🔍 Search for any item")
    st.markdown("- 📊 View 3D cargo arrangement")

# ---------- Items & Containers ----------
elif section == "Items & Containers":
    st.header("📦 Items and Containers Overview")
    st.subheader("Items")
    st.dataframe(pd.DataFrame(items))
    st.subheader("Containers")
    st.dataframe(pd.DataFrame(containers))

# ---------- Run Placement ----------
elif section == "Run Placement":
    st.header("🧠 Smart Placement Results")

    if placement_output["success"]:
        st.success("Placement data loaded!")
        df = pd.DataFrame(placement_output["placements"])
        st.subheader("Placement Table")
        st.dataframe(df)
    else:
        st.error("Failed to load placement data.")

# ---------- 3D Visualization ----------
elif section == "3D Visualization":
    st.header("📊 3D Cargo Visualization")
    if st.button("Show 3D View"):
        from visualize_placement_3d import visualize_placement
        visualize_placement("placement_output.json")

# ---------- Waste Detection ----------
elif section == "Waste Detection":
    st.header("🧹 Expired/Waste Item Detection")
    st.write(f"**Note:** {waste_data['note']}")
    if waste_data["wasteItems"]:
        st.subheader("Detected Waste Items:")
        df_waste = pd.DataFrame(waste_data["wasteItems"])
        st.dataframe(df_waste)
    else:
        st.success("No expired items currently!")

# ---------- Simulate Time ----------
elif section == "Simulate Time":
    st.header("⏩ Simulate Time Passage")

    num_days = st.number_input("Number of days to simulate", min_value=1, max_value=365, value=1)
    st.markdown("📝 Optional: Specify usage per item")
    usage_text = st.text_area("Format: item_id:count (one per line)", value="")

    items_used_dict = {}
    if usage_text.strip():
        try:
            for line in usage_text.strip().splitlines():
                item_id, count = line.split(":")
                items_used_dict[item_id.strip()] = int(count.strip())
        except Exception as e:
            st.error(f"Invalid format: {e}")

    if st.button("Run Simulation"):
        from simulate_time import simulate_time_passage
        result = simulate_time_passage(items, num_days=num_days, items_used_per_day=items_used_dict)
        st.success("Simulation completed!")

        st.write(f"📅 New Simulated Date: `{result['newDate']}`")
        st.subheader("Items Used")
        st.json(result["changes"]["itemsUsed"])
        st.subheader("Items Expired")
        st.json(result["changes"]["itemsExpired"])
        st.subheader("Items Depleted Today")
        st.json(result["changes"]["itemsDepletedToday"])

# ---------- Search Item ----------
elif section == "Search Item":
    st.header("🔍 Search for Item")

    item_id = st.text_input("Enter Item ID")
    item_name = st.text_input("Or Enter Item Name")

    if st.button("Search"):
        if item_id or item_name:
            result = requests.get("http://localhost:8000/api/search", params={"itemId": item_id, "itemName": item_name})
            if result.status_code == 200:
                st.success("Item Found:")
                st.json(result.json())
            else:
                st.error("Item not found or invalid input")
        else:
            st.warning("Please enter an Item ID or Name")

# ---------- Export & Logs ----------
elif section == "Export & Logs":
    st.header("📤 Export & Logs")

    if st.button("Download Arrangement CSV"):
        response = requests.get("http://localhost:8000/api/export/arrangement")
        st.download_button("Download", response.text, file_name="arrangement.csv")

    if st.button("View Logs"):
        logs = requests.get("http://localhost:8000/api/logs").json()
        st.json(logs)
