import pymysql

conn = None

# Connect to MySQL database
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

    # Run query
    cursor.execute(query, ("%" + name + "%",))
    # Return all matching rows
    return cursor.fetchall()


# Option 2: Get attendees by company

# the companyId exists?
def company_exists(company_id):
    global conn

    if not conn:
        connect()

    # check if companyID exists and get company name
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


# get the attendees in a specific company
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
    # Run query and return all matching rows
    cursor.execute(query, (company_id,))
    return cursor.fetchall()



# Option 3: Add new attendee

# check if attendee exists
def attendee_exists(attendeeID):
    global conn

    if not conn:
        connect()

    # check if attendeeID exists
    query = """
    SELECT attendeeID
    FROM attendee
    WHERE attendeeID = %s
    """
    cursor = conn.cursor()
    cursor.execute(query, (attendeeID,))
    return cursor.fetchone() is not None

# Insert new attendee into the database
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


# Option 4: Get connected attendees
def get_attendee_name(attendeeID):
    global conn

    if not conn:
        connect()

    # Get attendee's name
    query = """
    SELECT attendeeName
    FROM attendee
    WHERE attendeeID = %s
    """
    cursor = conn.cursor()
    cursor.execute(query, (attendeeID,))
    result = cursor.fetchone()

    # Return attendee's name if found, otherwise return None
    return result[0] if result else None

# Option 6: Get rooms information
def get_room_info():
    global conn

    if not conn:
        connect()

    # Get room details
    query = """
    SELECT roomID,roomName, capacity
    FROM room
    """
    cursor = conn.cursor()
    # Run query and return all room details
    cursor.execute(query)
    return cursor.fetchall()