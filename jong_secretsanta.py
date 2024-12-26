# -*- coding: utf-8 -*-
"""JONG_SecretSanta.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1jTPIHJMZEhH-6yhv9UO0iJHVYbraulLI
"""

import streamlit as st
import pandas as pd
import random

# Store participant data
if "participants" not in st.session_state:
    st.session_state.participants = []

if "assigned_pairs" not in st.session_state:
    st.session_state.assigned_pairs = {}

# Admin Panel
def admin_panel():
    st.header("Admin Panel - Manage Participants")
    name = st.text_input("Enter Participant Name")
    add_participant = st.button("Add Participant")
    if add_participant and name:
        st.session_state.participants.append({"name": name, "assigned": False})
        st.success(f"Added {name} to the list!")

    st.write("Current Participants:")
    st.write(pd.DataFrame(st.session_state.participants))

    if st.button("Reset Participant List"):
        st.session_state.participants = []
        st.session_state.assigned_pairs = {}
        st.success("Participant list reset!")

# Participant UI
def participant_ui():
    st.header("Welcome to Secret Santa 🎅")
    st.write("Select your name and find out who you’ll be gifting this year!")

    if not st.session_state.participants:
        st.warning("No participants available yet. Please wait for the admin to add names.")
        return

    names = [p["name"] for p in st.session_state.participants if not p["assigned"]]
    if not names:
        st.warning("All participants have already picked names!")
        return

    selected_name = st.selectbox("Select Your Name", options=names)
    pick_button = st.button("Pick a Name to be Gifted")

    if pick_button:
        # Randomly assign a name (ensure it's not the participant's own name)
        remaining_names = [p["name"] for p in st.session_state.participants if p["name"] != selected_name and not p["assigned"]]
        if not remaining_names:
            st.warning("No names left to assign!")
            return

        recipient_name = random.choice(remaining_names)
        st.session_state.assigned_pairs[selected_name] = recipient_name

        # Mark both as assigned
        for p in st.session_state.participants:
            if p["name"] == recipient_name:
                p["assigned"] = True

        st.success(f"You’ve been assigned to gift: **{recipient_name}** 🎁")
        st.write("Please keep it a secret!")

# App Mode Selector
mode = st.sidebar.selectbox("Choose Mode", ["Admin", "Participant"])

if mode == "Admin":
    admin_password = st.sidebar.text_input("Enter Admin Password", type="password")
    if admin_password == "your_password":  # Replace with a strong password
        admin_panel()
    else:
        st.error("Incorrect password!")
else:
    participant_ui()