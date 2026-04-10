import streamlit as st
import psycopg2

st.set_page_config(page_title="My Closet", page_icon="👗")

def get_connection():
    return psycopg2.connect(st.secrets["DB_URL"])

st.title("👗 My Closet")

# --- Filters ---
st.subheader("🔍 Search & Filter")

search = st.text_input("Search by name or brand")

col1, col2 = st.columns(2)
with col1:
    category_filter = st.selectbox("Filter by category", ["All", "Sneakers", "Clothing", "Handbag", "Accessory", "Outerwear", "Jewelry", "Other"])
with col2:
    condition_filter = st.selectbox("Filter by condition", ["All", "New", "Like New", "Good", "Fair"])

st.markdown("---")

# --- Build query based on filters ---
try:
    conn = get_connection()
    cur = conn.cursor()

    query = "SELECT id, item_name, brand, category, size, condition, notes FROM items WHERE 1=1"
    params = []

    if search.strip():
        query += " AND (item_name ILIKE %s OR brand ILIKE %s)"
        params.extend([f"%{search.strip()}%", f"%{search.strip()}%"])

    if category_filter != "All":
        query += " AND category = %s"
        params.append(category_filter)

    if condition_filter != "All":
        query += " AND condition = %s"
        params.append(condition_filter)

    query += " ORDER BY id DESC;"

    cur.execute(query, params)
    rows = cur.fetchall()
    cur.close()
    conn.close()

except Exception as e:
    st.error(f"Database connection error: {e}")
    rows = []

# --- Display items ---
if not rows:
    st.info("No items found.")
else:
    st.subheader(f"📦 {len(rows)} item(s) found")

    for row in rows:
        item_id, item_name, brand, category, size, condition, notes = row

        with st.container():
            col1, col2, col3 = st.columns([4, 1, 1])

            with col1:
                st.markdown(f"**{item_name}** — {brand or 'No brand'} | {category} | Size: {size or 'N/A'} | Condition: {condition or 'N/A'}")

            with col2:
                if st.button("✏️ Edit", key=f"edit_{item_id}"):
                    st.session_state[f"editing_{item_id}"] = True

            with col3:
                if st.button("🗑️ Delete", key=f"delete_{item_id}"):
                    st.session_state[f"confirm_delete_{item_id}"] = True

        # --- Confirm delete ---
        if st.session_state.get(f"confirm_delete_{item_id}"):
            st.warning(f"Are you sure you want to delete **{item_name}**?")
            col_yes, col_no = st.columns([1, 1])
            with col_yes:
                if st.button("Yes, delete", key=f"yes_{item_id}"):
                    try:
                        conn = get_connection()
                        cur = conn.cursor()
                        cur.execute("DELETE FROM items WHERE id = %s;", (item_id,))
                        conn.commit()
                        cur.close()
                        conn.close()
                        st.success(f"✅ '{item_name}' deleted.")
                        st.session_state[f"confirm_delete_{item_id}"] = False
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error: {e}")
            with col_no:
                if st.button("Cancel", key=f"cancel_{item_id}"):
                    st.session_state[f"confirm_delete_{item_id}"] = False
                    st.rerun()

        # --- Edit form ---
        if st.session_state.get(f"editing_{item_id}"):
            with st.form(key=f"edit_form_{item_id}"):
                st.subheader(f"Edit — {item_name}")
                new_name = st.text_input("Item Name", value=item_name)
                new_brand = st.text_input("Brand", value=brand or "")
                new_category = st.selectbox("Category", ["Sneakers", "Clothing", "Handbag", "Accessory", "Outerwear", "Jewelry", "Other"],
                    index=["Sneakers", "Clothing", "Handbag", "Accessory", "Outerwear", "Jewelry", "Other"].index(category) if category in ["Sneakers", "Clothing", "Handbag", "Accessory", "Outerwear", "Jewelry", "Other"] else 0)
                new_size = st.text_input("Size", value=size or "")
                new_condition = st.selectbox("Condition", ["New", "Like New", "Good", "Fair"],
                    index=["New", "Like New", "Good", "Fair"].index(condition) if condition in ["New", "Like New", "Good", "Fair"] else 0)
                new_notes = st.text_area("Notes", value=notes or "")
                submitted = st.form_submit_button("Save Changes")

                if submitted:
                    errors = []
                    if not new_name.strip():
                        errors.append("Item name is required.")
                    if errors:
                        for err in errors:
                            st.error(err)
                    else:
                        try:
                            conn = get_connection()
                            cur = conn.cursor()
                            cur.execute("""
                                UPDATE items
                                SET item_name = %s, brand = %s, category = %s, size = %s, condition = %s, notes = %s
                                WHERE id = %s;
                            """, (new_name.strip(), new_brand.strip(), new_category, new_size.strip(), new_condition, new_notes.strip(), item_id))
                            conn.commit()
                            cur.close()
                            conn.close()
                            st.success(f"✅ '{new_name}' updated successfully!")
                            st.session_state[f"editing_{item_id}"] = False
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error: {e}")

            if st.button("Cancel Edit", key=f"cancel_edit_{item_id}"):
                st.session_state[f"editing_{item_id}"] = False
                st.rerun()

        st.markdown("---")