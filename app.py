import streamlit as st
import json
import time
from pathlib import Path
import uuid

st.set_page_config(
    page_title="Smart Coffee Kiosk",
    page_icon="",
    layout="centered"
)

json_file = Path("inventory.json")


if json_file.exists():
    with json_file.open("r", encoding="utf-8") as f:
        inventory = json.load(f)
else:
    inventory = []


if "orders" not in st.session_state:
    st.session_state.orders = []

orders = st.session_state.orders


tab1, tab2, tab3, tab4 = st.tabs([
    "Place Order",
    "View Inventory",
    "Restock",
    "Manage Orders"
])


# PLACE ORDER

with tab1:

    st.header("Place Order")

    item_names = []
    for item in inventory:
        item_names.append(item["name"])

    selected_item = st.selectbox("Select Drink", item_names)
    quantity = st.number_input("Quantity", min_value=1)
    customer = st.text_input("Customer Name")
    btn_order = st.button("Place Order", use_container_width=True)

    if btn_order:

        for item in inventory:

            if item["name"] == selected_item:

                if item["stock"] >= quantity:

                    item["stock"] -= quantity

                    total_price = item["price"] * quantity

                    order = {
                        "order_id": str(uuid.uuid4())[:8],
                        "customer": customer,
                        "item": selected_item,
                        "quantity": quantity,
                        "total": total_price,
                        "status": "Placed"
                    }

                    orders.append(order)

                    with json_file.open("w", encoding="utf-8") as f:
                        json.dump(inventory, f, indent=4)

                    st.success("Order Placed!")

                    with st.expander("Receipt", expanded=True):
                        st.write(order)

                else:
                    st.error("Out of Stock")


# VIEW INVENTORY

with tab2:

    st.header("View Inventory")
    search = st.text_input("Search Item")
    if search:
        filtered_inventory = []
        for item in inventory:
            if search.lower() in item["name"].lower():
                filtered_inventory.append(item)

        st.dataframe(filtered_inventory)

    else:
        st.dataframe(inventory)

    total_stock = 0

    for item in inventory:
        total_stock += item["stock"]

    st.metric("Total Items in Stock", total_stock)


# RESTOCK

with tab3:

    st.header("Restock Item")
    item_names = []
    for item in inventory:
        item_names.append(item["name"])
    selected_item = st.selectbox("Select Item", item_names)
    add_stock = st.number_input("Add Quantity", min_value=1)
    btn_restock = st.button("Restock", use_container_width=True)
    if btn_restock:

        for item in inventory:

            if item["name"] == selected_item:
                item["stock"] += add_stock

        with json_file.open("w", encoding="utf-8") as f:
            json.dump(inventory, f, indent=4)

        st.success("Stock Updated!")

        time.sleep(2)

        st.rerun()


# MANAGE ORDERS
with tab4:
    st.header("Manage Orders")
    if len(orders) == 0:
        st.info("No orders placed yet.")
    else:
        st.dataframe(orders)
        order_ids = []
        for order in orders:
            order_ids.append(order["order_id"])
        selected_order = st.selectbox("Select Order to Cancel", order_ids)
        btn_cancel = st.button("Cancel Order", use_container_width=True)
        if btn_cancel:
            for order in orders:
                if order["order_id"] == selected_order:
                    order["status"] = "Cancelled"
                    for item in inventory:
                        if item["name"] == order["item"]:
                            item["stock"] += order["quantity"]

            with json_file.open("w", encoding="utf-8") as f:
                json.dump(inventory, f, indent=4)

            st.success("Order Cancelled and Stock Refunded!")
            time.sleep(2)
            st.rerun()