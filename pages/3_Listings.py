import streamlit as st
import psycopg2

st.set_page_config(page_title="Listings", page_icon="🛍️")

def get_connection():
    return psycopg2.connect(st.secrets["DB_URL"])

st.title("🛍️ Listings")

# --- Add Listing Form ---
st.subheader("➕ Add New Listing")

try:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, item_name, brand FROM items ORDER BY item_name;")
    all_items = cur.fetchall()
    cur.close()
    conn.close()
except Exception as e:
    st.error(f"Error loading items: {e}")
    all_items = []

item_options = {f"{item[1]} — {item[2] or 'No brand'}": item[0] for item in all_items}

with st.form("add_listing_form"):
    if not item_options:
        st.warning("No items in your closet yet. Add some items first.")
        st.form_submit_button("Add Listing", disabled=True)
    else:
        selected_item = st.selectbox("Select Item *", options=list(item_options.keys()))
        asking_price = st.number_input("Asking Price *", min_value=0.0, step=0.01, format="%.2f")
        platform = st.selectbox("Platform", ["", "Depop", "Poshmark", "eBay", "Mercari", "Grailed", "Other"])
        status = st.selectbox("Status *", ["available", "pending", "sold"])
        submitted = st.form_submit_button("Add Listing")

        if submitted:
            errors = []

            if not selected_item:
                errors.append("Please select an item.")
            if asking_price <= 0:
                errors.append("Asking price must be greater than zero.")

            if errors:
                for err in errors:
                    st.error(err)
            else:
                try:
                    conn = get_connection()
                    cur = conn.cursor()
                    cur.execute("""
                        INSERT INTO listings (item_id, asking_price, platform, status)
                        VALUES (%s, %s, %s, %s);
                    """, (
                        item_options[selected_item],
                        asking_price,
                        platform or None,
                        status
                    ))
                    conn.commit()
                    cur.close()
                    conn.close()
                    st.success(f"✅ Listing added successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")

st.markdown("---")

# --- Filter ---
st.subheader("🔍 Filter Listings")
status_filter = st.selectbox("Filter by status", ["All", "available", "pending", "sold"])

st.markdown("---")

# --- Display Listings ---
try:
    conn = get_connection()
    cur = conn.cursor()

    query = """
        SELECT l.id, i.item_name, i.brand, l.asking_price, l.platform, l.status, l.listed_date
        FROM listings l
        JOIN items i ON l.item_id = i.id
        WHERE 1=1
    """
    params = []

    if status_filter != "All":
        query += " AND l.status = %s"
        params.append(status_filter)

    query += " ORDER BY l.listed_date DESC;"

    cur.execute(query, params)
    rows = cur.fetchall()
    cur.close()
    conn.close()

except Exception as e:
    st.error(f"Database connection error: {e}")
    rows = []

if not rows:
    st.info("No listings found.")
else:
    st.subheader(f"📋 {len(rows)} listing(s) found")

    for row in rows:
        listing_id, item_name, brand, asking_price, platform, status, listed_date = row

        with st.container():
            col1, col2, col3 = st.columns([4, 1, 1])

            with col1:
                st.markdown(f"**{item_name}** — {brand or 'No brand'} | ${asking_price} | {platform or 'No platform'} | Status: **{status}** | Listed: {listed_date.strftime('%Y-%m-%d')}")

            with col2:
                if st.button("✏️ Edit", key=f"edit_{listing_id}"):
                    st.session_state[f"editing_{listing_id}"] = True

            with col3:
                if st.button("🗑️ Delete", key=f"delete_{listing_id}"):
                    st.session_state[f"confirm_delete_{listing_id}"] = True

        # --- Confirm delete ---
        if st.session_state.get(f"confirm_delete_{listing_id}"):
            st.warning(f"Are you sure you want to delete the listing for **{item_name}**?")
            col_yes, col_no = st.columns([1, 1])
            with col_yes:
                if st.button("Yes, delete", key=f"yes_{listing_id}"):
                    try:
                        conn = get_connection()
                        cur = conn.cursor()
                        cur.execute("DELETE FROM listings WHERE id = %s;", (listing_id,))
                        conn.commit()
                        cur.close()
                        conn.close()
                        st.success(f"✅ Listing deleted.")
                        st.session_state[f"confirm_delete_{listing_id}"] = False
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error: {e}")
            with col_no:
                if st.button("Cancel", key=f"cancel_{listing_id}"):
                    st.session_state[f"confirm_delete_{listing_id}"] = False
                    st.rerun()

        # --- Edit form ---
        if st.session_state.get(f"editing_{listing_id}"):
            with st.form(key=f"edit_form_{listing_id}"):
                st.subheader(f"Edit Listing — {item_name}")
                new_price = st.number_input("Asking Price *", min_value=0.0, step=0.01, format="%.2f", value=float(asking_price))
                new_platform = st.selectbox("Platform", ["", "Depop", "Poshmark", "eBay", "Mercari", "Grailed", "Other"],
                    index=["", "Depop", "Poshmark", "eBay", "Mercari", "Grailed", "Other"].index(platform) if platform in ["", "Depop", "Poshmark", "eBay", "Mercari", "Grailed", "Other"] else 0)
                new_status = st.selectbox("Status *", ["available", "pending", "sold"],
                    index=["available", "pending", "sold"].index(status))
                submitted = st.form_submit_button("Save Changes")

                if submitted:
                    errors = []
                    if new_price <= 0:
                        errors.append("Asking price must be greater than zero.")
                    if errors:
                        for err in errors:
                            st.error(err)
                    else:
                        try:
                            conn = get_connection()
                            cur = conn.cursor()
                            cur.execute("""
                                UPDATE listings
                                SET asking_price = %s, platform = %s, status = %s
                                WHERE id = %s;
                            """, (new_price, new_platform or None, new_status, listing_id))
                            conn.commit()
                            cur.close()
                            conn.close()
                            st.success("✅ Listing updated successfully!")
                            st.session_state[f"editing_{listing_id}"] = False
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error: {e}")

            if st.button("Cancel Edit", key=f"cancel_edit_{listing_id}"):
                st.session_state[f"editing_{listing_id}"] = False
                st.rerun()

        st.markdown("---")