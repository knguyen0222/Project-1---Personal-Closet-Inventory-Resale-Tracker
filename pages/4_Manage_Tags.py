import streamlit as st
import psycopg2

st.set_page_config(page_title="Manage Tags", page_icon="🏷️")

def get_connection():
    return psycopg2.connect(st.secrets["DB_URL"])

st.title("🏷️ Manage Tags")

# --- Add Tag Form ---
with st.expander("➕ Add New Tag", expanded=False):
    with st.form("add_tag_form"):
        tag_name = st.text_input("Tag Name *")
        submitted = st.form_submit_button("Add Tag")

        if submitted:
            errors = []

            if not tag_name.strip():
                errors.append("Tag name is required.")

            if errors:
                for err in errors:
                    st.error(err)
            else:
                try:
                    conn = get_connection()
                    cur = conn.cursor()
                    cur.execute("""
                        INSERT INTO tags (tag_name)
                        VALUES (%s);
                    """, (tag_name.strip(),))
                    conn.commit()
                    cur.close()
                    conn.close()
                    st.success(f"✅ Tag '{tag_name}' added successfully!")
                    st.rerun()
                except psycopg2.errors.UniqueViolation:
                    st.error(f"⚠️ A tag named '{tag_name}' already exists.")
                except Exception as e:
                    st.error(f"Error: {e}")

st.markdown("---")

# --- Display Tags ---
st.subheader("🏷️ All Tags")

try:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, tag_name, created_at FROM tags ORDER BY tag_name;")
    rows = cur.fetchall()
    cur.close()
    conn.close()
except Exception as e:
    st.error(f"Database connection error: {e}")
    rows = []

if not rows:
    st.info("No tags yet. Add your first tag above!")
else:
    st.caption(f"{len(rows)} tag(s) total")

    for row in rows:
        tag_id, tag_name, created_at = row

        with st.container():
            col1, col2 = st.columns([5, 1])

            with col1:
                st.markdown(f"**{tag_name}** — added {created_at.strftime('%Y-%m-%d')}")

            with col2:
                if st.button("🗑️ Delete", key=f"delete_{tag_id}"):
                    st.session_state[f"confirm_delete_{tag_id}"] = True

        # --- Confirm delete ---
        if st.session_state.get(f"confirm_delete_{tag_id}"):
            st.warning(f"Are you sure you want to delete the tag **'{tag_name}'**? It will be removed from all items.")
            col_yes, col_no = st.columns([1, 1])
            with col_yes:
                if st.button("Yes, delete", key=f"yes_{tag_id}"):
                    try:
                        conn = get_connection()
                        cur = conn.cursor()
                        cur.execute("DELETE FROM tags WHERE id = %s;", (tag_id,))
                        conn.commit()
                        cur.close()
                        conn.close()
                        st.success(f"✅ Tag '{tag_name}' deleted.")
                        st.session_state[f"confirm_delete_{tag_id}"] = False
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error: {e}")
            with col_no:
                if st.button("Cancel", key=f"cancel_{tag_id}"):
                    st.session_state[f"confirm_delete_{tag_id}"] = False
                    st.rerun()

        st.markdown("---")