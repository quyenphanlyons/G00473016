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
def company_exists(company_id):
    global conn

    if not conn:
        connect()

    query = """
    SELECT companyName
    FROM company
    WHERE companyID = %s
    """
    cursor = conn.cursor()
    cursor.execute(query, (company_id,))
    result = cursor.fetchone()

    if result:
        return result[0]
    return None


# get the attendees of a company
def get_attendees(company_id):
    global conn

    if not conn:
        connect()

    query = """
    SELECT  a.attendeeName, 
            a.attendeeDOB,
            s.sessionTitle,
            s.speakerName,
            s.sessionDate,
            r.roomName
    FROM attendee a
    JOIN registration re ON a.attendeeID = re.attendeeID
    JOIN session s ON re.sessionID = s.sessionID
    JOIN room r ON s.roomID = r.roomID
    WHERE a.attendeeCompanyID = %s
    """

    cursor = conn.cursor()
    cursor.execute(query, (company_id,))
    return cursor.fetchall()



# Option 3: Add new attendee

# check if attendee exists
def attendee_exists(attendeeID):
    global conn

    if not conn:
        connect()

    query = """
    SELECT attendeeID
    FROM attendee
    WHERE attendeeID = %s
    """
    cursor = conn.cursor()
    cursor.execute(query, (attendeeID,))
    return cursor.fetchone() is not None


def new_attendee(attendeeID, attendeeName, attendeeDOB, attendeeGender, attendeeCompanyID):
    global conn

    if not conn:
        connect()

    query = """
    INSERT INTO attendee (attendeeID, attendeeName, attendeeDOB, attendeeGender, attendeeCompanyID)
    VALUES (%s, %s, %s, %s, %s)
    """

    cursor = conn.cursor()
    cursor.execute(query, (attendeeID, attendeeName, attendeeDOB, attendeeGender, attendeeCompanyID))
    conn.commit()
