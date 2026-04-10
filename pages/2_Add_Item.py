import streamlit as st
import psycopg2

st.set_page_config(page_title="Add Item", page_icon="➕")

def get_connection():
    return psycopg2.connect(st.secrets["DB_URL"])

st.title("➕ Add Item")

# --- Pull tags from database for multi-select ---
try:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, tag_name FROM tags ORDER BY tag_name;")
    all_tags = cur.fetchall()
    cur.close()
    conn.close()
except Exception as e:
    st.error(f"Error loading tags: {e}")
    all_tags = []

tag_options = {tag[1]: tag[0] for tag in all_tags}

# --- Add Item Form ---
with st.form("add_item_form"):
    item_name = st.text_input("Item Name *")
    brand = st.text_input("Brand")
    category = st.selectbox("Category *", ["", "Shoes", "Clothing", "Handbag", "Accessory", "Outerwear", "Jewelry", "Other"])
    size = st.text_input("Size")
    condition = st.selectbox("Condition", ["", "New", "Like New", "Good", "Fair"])
    notes = st.text_area("Notes")
    selected_tags = st.multiselect("Tags", options=list(tag_options.keys()))
    submitted = st.form_submit_button("Add Item")

    if submitted:
        errors = []

        if not item_name.strip():
            errors.append("Item name is required.")
        if not category:
            errors.append("Category is required.")

        if errors:
            for err in errors:
                st.error(err)
        else:
            try:
                conn = get_connection()
                cur = conn.cursor()

                # Insert item
                cur.execute("""
                    INSERT INTO items (item_name, brand, category, size, condition, notes)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    RETURNING id;
                """, (
                    item_name.strip(),
                    brand.strip() or None,
                    category,
                    size.strip() or None,
                    condition or None,
                    notes.strip() or None
                ))

                new_item_id = cur.fetchone()[0]

                # Insert tags into item_tags
                for tag_name in selected_tags:
                    tag_id = tag_options[tag_name]
                    cur.execute("""
                        INSERT INTO item_tags (item_id, tag_id)
                        VALUES (%s, %s);
                    """, (new_item_id, tag_id))

                conn.commit()
                cur.close()
                conn.close()
                st.success(f"✅ '{item_name}' added to your closet!")

            except Exception as e:
                st.error(f"Error: {e}")

st.markdown("---")

# --- Recently added items ---
st.subheader("🕐 Recently Added")

try:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT item_name, brand, category, size, condition
        FROM items
        ORDER BY id DESC
        LIMIT 5;
    """)
    rows = cur.fetchall()
    cur.close()
    conn.close()

    if rows:
        st.table([{"Name": r[0], "Brand": r[1], "Category": r[2], "Size": r[3], "Condition": r[4]} for r in rows])
    else:
        st.info("No items yet.")

except Exception as e:
    st.error(f"Error: {e}")