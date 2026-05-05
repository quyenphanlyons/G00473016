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
    MATCH (a:Attendee {AttendeeID: $attendeeID})-[:CONNECTED_TO]->(b:Attendee)
    RETURN b.AttendeeID AS ID
    """

    with driver.session(database="attendeeNetwork") as session:
        result = session.run(query, attendeeID=attendeeID)
        return result.data()