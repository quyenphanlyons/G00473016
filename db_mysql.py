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
    SELECT s.speakerName, sess.sessionTitle, r.roomName
    FROM speaker s
    JOIN session sess ON s.speakerID = sess.speakerID
    JOIN room r ON sess.roomID = r.roomID
    WHERE s.speakerName LIKE %s
    """

    cursor = conn.cursor()
    cursor.execute(query, ("%" + name + "%",))
    return cursor.fetchall()

