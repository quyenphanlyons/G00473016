from neo4j import GraphDatabase

driver = None

def connect():
    global driver
    uri = "neo4j://localhost:7687"
    username = "neo4j"      
    password = "neo4jneo4j"

    driver = GraphDatabase.driver(uri, auth=(username, password))
