from neo4j import GraphDatabase

driver = None

def connect():
    global driver
    uri = "bolt://localhost:7687"
    username = "neo4j"      
    password = "neo4jneo4j"

    driver = GraphDatabase.driver(uri, auth=(username, password))

if __name__ == "__main__":
    connect()
    print("Connected to Neo4j")

# Option 4: Get connected attendees
def get_connected_attendees(attendeeID):
    global driver

    if not driver:
        connect()

    query = """
    MATCH (a:Attendee {AttendeeID: $attendeeID})-[:CONNECTED_TO]-(b:Attendee)
    RETURN b.AttendeeID AS ID
    """

    with driver.session(database="attendeenetwork") as session:
        result = session.run(query, attendeeID=attendeeID)
        return result.data()
    

# Option 5: Connect two attendees
def add_connection(attendee1, attendee2):
    global driver

    if not driver:
        connect()

    query = """
    MERGE (a:Attendee {AttendeeID: $ID1})
    MERGE (b:Attendee {AttendeeID: $ID2})
    CREATE (a)-[:CONNECTED_TO]->(b)
    CREATE (b)-[:CONNECTED_TO]->(a)
    """

    with driver.session(database="attendeenetwork") as session:
        session.run(query, ID1=attendee1, ID2=attendee2)


# check if attendee connection exists
def connection_exists(attendee1, attendee2):
    global driver

    if not driver:
        connect()

    query = """
    MATCH (a:Attendee {AttendeeID: $ID1})
    -[:CONNECTED_TO]- 
    (b:Attendee {AttendeeID: $ID2})
    RETURN 1
    """

    with driver.session(database="attendeenetwork") as session:
        result = session.run(query, ID1=attendee1, ID2=attendee2)
        return result.single() is not None