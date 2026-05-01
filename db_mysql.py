import pymysql

conn = None


def connect():
    global conn
    conn = pymysql.connect(
        host="localhost",
        user="root",
        password="root",
        db="appdbproj",
        ssl={'ssl':{}}
    )


def get_speakers_sessions(name):
    global conn

    if not conn:
        connect()

    query = """
    SELECT s.speakerName, s.sessionTitle, r.roomName
    FROM session s
    JOIN room r ON s.roomID = r.roomID
    WHERE s.speakerName LIKE %s
    """

    cursor = conn.cursor()
    cursor.execute(query, ("%" + name + "%",))
    return cursor.fetchall()

