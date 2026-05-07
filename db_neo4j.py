from neo4j import GraphDatabase

driver = None

# Connect to Neo4j database
def connect():
    global driver
    uri = "bolt://localhost:7687"
    username = "neo4j"      
    password = "neo4jneo4j"

    driver = GraphDatabase.driver(uri, auth=(username, password))

# Option 4: Get connected attendees of a given attendeeID
def get_connected_attendees(attendeeID):
    global driver

    # Make sure to connect to the database
    if not driver:
        connect()

    # Find an attendee node with the given attendeeID
    # Find all attendees connected to that node
    query = """
    MATCH (a:Attendee {AttendeeID: $attendeeID})-[:CONNECTED_TO]-(b:Attendee)
    RETURN b.AttendeeID AS ID
    """

    # Run query and return results
    with driver.session(database="attendeenetwork") as session:
        result = session.run(query, attendeeID=attendeeID)
        return result.data()
    

# Option 5: Connect two attendees
def add_connection(attendee1, attendee2):
    global driver

    if not driver:
        connect()

    # Create attendees nodes if they don't already exist
    # Create a connection between 2 attendees
    query = """
    MERGE (a:Attendee {AttendeeID: $ID1})
    MERGE (b:Attendee {AttendeeID: $ID2})
    CREATE (a)-[:CONNECTED_TO]->(b)
    CREATE (b)-[:CONNECTED_TO]->(a)
    """
    # Run query
    with driver.session(database="attendeenetwork") as session:
        session.run(query, ID1=attendee1, ID2=attendee2)


# check if attendees connection exists
def connection_exists(attendee1, attendee2):
    global driver

    if not driver:
        connect()

    # check if there is any connection between 2 attendees
    query = """
    MATCH (a:Attendee {AttendeeID: $ID1})
    -[:CONNECTED_TO]- 
    (b:Attendee {AttendeeID: $ID2})
    RETURN 1
    """
    # Run query
    with driver.session(database="attendeenetwork") as session:
        result = session.run(query, ID1=attendee1, ID2=attendee2)
        return result.single() is not None