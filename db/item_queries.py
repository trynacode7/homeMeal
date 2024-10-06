def fetch_items(con):
    try:
        cur = con.cursor()
        query = "SELECT * FROM items"
        cur.execute(query)
        items = cur.fetchall()
        return items
    except Exception as e:
        print(f"Error fetching items: {e}")
        return []
