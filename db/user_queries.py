def insert_user(con, name, apartment, phone, password):
    try:
        cur = con.cursor()
        query = "INSERT INTO users (name, apartment, phone, password) VALUES (%s, %s, %s, %s)"
        cur.execute(query, (name, apartment, phone, password))
        con.commit()
        return True
    except Exception as e:
        print(f"Error during user registration: {e}")
        return False

def login_user(con, phone, password):
    try:
        cur = con.cursor()
        query = "SELECT * FROM users WHERE phone=%s AND password=%s"
        cur.execute(query, (phone, password))
        user = cur.fetchone()
        return user is not None
    except Exception as e:
        print(f"Error during login: {e}")
        return False
