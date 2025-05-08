import sqlite3

def verify_admin_credentials(username, password):
    conn = sqlite3.connect('reservations.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM admins WHERE username=? AND password=?", (username, password))
    result = cur.fetchone()
    conn.close()
    return result is not None

def verify_reservation_information(seat_row, seat_col):
    if seat_row < 0 or seat_row > 11 or seat_col < 0 or seat_col > 3:
        return False
    conn = sqlite3.connect('reservations.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM reservations WHERE seatRow=? AND seatColumn=?", (seat_row, seat_col))
    reservation = cur.fetchone()
    conn.close()
    if reservation:
        return False
    return True