import streamlit as st
import psycopg2

st.set_page_config(page_title="Closet Tracker", page_icon="👗")

def get_connection():
    return psycopg2.connect(st.secrets["DB_URL"])

st.title("👗 Closet Tracker")
st.write("Welcome! Use the sidebar to navigate between pages.")

st.markdown("---")
st.subheader("📊 Overview")

try:
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM items;")
    item_count = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM listings WHERE status IN ('available', 'pending');")
    active_listings = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM listings WHERE status = 'sold';")
    sold_count = cur.fetchone()[0]

    cur.execute("SELECT COALESCE(SUM(purchase_price), 0) FROM items;")
    total_spent = cur.fetchone()[0]

    if total_spent >= 1000000:
        spent_display = f"${total_spent/1000000:,.1f}M"
    elif total_spent >= 10000:
        spent_display = f"${total_spent/1000:,.1f}k"
    else:
        spent_display = f"${total_spent:,.2f}"

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Items", item_count)
    col2.metric("Active Listings", active_listings)
    col3.metric("Items Sold", sold_count)
    col4.metric("Total Spent", spent_display)

    st.markdown("---")
    st.subheader("🕐 Recently Added Items")

    cur.execute("""
        SELECT item_name, brand, category, size, color, condition, purchase_price, acquired_date
        FROM items
        ORDER BY id DESC
        LIMIT 5;
    """)
    rows = cur.fetchall()

    if rows:
        st.table(
            [{"Name": r[0], "Brand": r[1], "Category": r[2], "Size": r[3], "Color": r[4], "Condition": r[5], "Paid": f"${r[6]:,.2f}" if r[6] else "N/A", "Acquired": r[7].strftime("%Y-%m-%d") if r[7] else "N/A"} for r in rows]
        )
    else:
        st.info("No items yet. Head to Add Item to log your first piece!")

    st.markdown("---")
    st.subheader("🛍️ Active Listings")

    cur.execute("""
        SELECT i.item_name, i.brand, i.category, i.size, i.color, i.condition, l.asking_price, l.platform, l.status, l.listed_date
        FROM listings l
        JOIN items i ON l.item_id = i.id
        WHERE l.status IN ('available', 'pending')
        ORDER BY l.listed_date DESC;
    """)
    listings = cur.fetchall()

    if listings:
        st.table(
            [{"Name": r[0], "Brand": r[1], "Category": r[2], "Size": r[3], "Color": r[4], "Condition": r[5], "Asking Price": f"${r[6]:,.2f}", "Platform": r[7] or "N/A", "Status": r[8], "Listed": r[9].strftime("%Y-%m-%d")} for r in listings]
        )
    else:
        st.info("No active listings yet. Head to Listings to post something for sale!")

    st.markdown("---")
    st.subheader("💰 Items Sold")

    cur.execute("""
        SELECT i.item_name, i.brand, i.category, i.size, i.color, i.condition, l.asking_price, l.platform, l.listed_date
        FROM listings l
        JOIN items i ON l.item_id = i.id
        WHERE l.status = 'sold'
        ORDER BY l.listed_date DESC;
    """)
    sold = cur.fetchall()

    if sold:
        st.table(
            [{"Name": r[0], "Brand": r[1], "Category": r[2], "Size": r[3], "Color": r[4], "Condition": r[5], "Sold For": f"${r[6]:,.2f}", "Platform": r[7] or "N/A", "Listed": r[8].strftime("%Y-%m-%d")} for r in sold]
        )
    else:
        st.info("No items sold yet.")

    cur.close()
    conn.close()

except Exception as e:
    st.error(f"Database connection error: {e}")