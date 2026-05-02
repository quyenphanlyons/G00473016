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

# Option 1: Get speakers, their sessions and rooms
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

# Option 2: Get attendees by company

# the companyId exists?
def company_exists(companyId):
    global conn

    if not conn:
        connect()

    query = """
    "SELECT companyName
    "FROM company
    "WHERE companyId = %s
    """
    cursor = conn.cursor()
    cursor.execute(query, (companyId,))
    return cursor.fetchone() is not None

# get the attendees of a company
def get_attendees(companyId):
    global conn

    if not conn:
        connect()

    query = """
    SELECT  c.companyName,
            a.attendeeName, 
            a.attendeeDOB,
            a.attendeeTitle,
            s.speakerName,
            r.roomName
    FROM attendee a
    JOIN company c ON a.attendeeCompanyId = c.companyId
    JOIN registration re ON a.attendeeID = re.attendeeID
    JOIN session s ON re.sessionID = s.sessionID
    JOIN room r ON s.roomID = r.roomID
    WHERE a.attendeeCompanyId = %s
    """

    cursor = conn.cursor()
    cursor.execute(query, (companyId,))
    return cursor.fetchall()