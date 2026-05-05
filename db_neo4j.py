from neo4j import GraphDatabase

driver = None

def connect():
    global driver
    uri = "neo4j://localhost:7687"
    username = "neo4j"      
    password = "neo4jneo4j"

    driver = GraphDatabase.driver(uri, auth=(username, password))

# Option 4: Get connected attendees
def get_connected_attendees(attendeeID):
    global driver

    if not driver:
        connect()

    query = """
    MATCH (a:Attendee {attendeeID: $attendeeID})-[:CONNECTED_TO]->(b:Attendee)
    RETURN b.attendeeID AS ID, b.attendeeName AS name
    """

    with driver.session() as session:
        result = session.run(query, attendee_id=attendeeID)
        return result.data()