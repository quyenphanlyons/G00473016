

import db_mysql
import db_neo4j

def menu():
    print("\nConference Management")
    print("----------------------")
    print("1 - View Speakers & Sessions")
    print("2 - View Attendees by Company")
    print("3 - Add New Attendee")
    print("4 - View Connected Attendees")
    print("5 - Add Attendee Connection")
    print("6 - View Rooms")
    print("x - Exit")


def main():
    while True:
        menu()
        choice = input("Choice: ")

        if choice == "1":
            op1()
        elif choice =="2":
            op2()
        elif choice =="3":
            op3()
        elif choice =="4":
            op4()
        elif choice =="5":
            op5()
        elif choice =="x":
            break

# Option 1: Get speakers, their sessions and rooms
def op1():
    name = input("Enter speaker name: ")
    results = db_mysql.get_speakers_sessions(name)

    print(f"Session Details For : {name}")

    if not results:
        print("No speakers found of that name")
        return

    for row in results:
        speaker, session, room = row
        print(f"{speaker} | {session} | {room}")
          

# Option 2: Get attendees by company
def op2():
    while True:
        try:
            type_in = input("Enter company ID or 'x' to exit request:")
            if type_in.lower() == 'x':
                return 
            
            comId = int(type_in)

            # companyId must be valid
            if comId <= 0:
                raise ValueError
            
            if not db_mysql.company_exists(comId):
                print(f"Company with Id {comId} does not exist.")
                continue

            results = db_mysql.get_attendees(comId)
            company_name = db_mysql.company_exists(comId)

            print(f"{company_name} Attendees")

            if not results:
                print(f"No attendees found for {company_name}")
                return

            for row in results:
                name, dob, session, speaker, date, room = row
                print(f"{name} | {dob} | {session} | {speaker} | {date}  | {room}")
            return
        except ValueError:
            print("Invalid company Id")


# Option 3: Add new attendee
def op3():
    try:
        attendeeID = int(input("Enter Attendee ID: "))
        attendeeName = input("Enter Attendee Name: ")
        attendeeDOB = input("Enter Attendee Date of Birth: ")
        attendeeGender = input("Enter Attendee Gender: ")
        attendeeCompanyID = int(input("Enter Attendee Company ID: "))
        
        # Send an Error message if attendeeID already exists
        if db_mysql.attendee_exists(attendeeID):
            print(f"*** ERROR *** Attendee ID already exists")
            return

        # Send an Error message for invalid gender
        if attendeeGender not in ['Male', 'Female']:
            print(f"*** ERROR *** Invalid gender")
            return
        
        # Send an Error message for invalid company ID
        if not db_mysql.company_exists(attendeeCompanyID):
            print(f"*** ERROR *** Company ID does not exist")
            return
        
        # Insert the new attendee into the database
        db_mysql.new_attendee(attendeeID, attendeeName, attendeeDOB, attendeeGender, attendeeCompanyID)
        print("Attendee successfully added.")

    except Exception as e:
        print(f"*** ERROR *** {e}")
        

# Option 4: View connected attendees
def op4():
    
    while True:
        try:
            attendeeID = int(input("Enter Attendee ID: "))
            
            # Get attendee's name from mysql
            attendeeName = db_mysql.get_attendee_name(attendeeID)

            if not attendeeName:
                print("*** ERROR *** Attendee does not exist")
                continue
            
            # print attendee's name if found
            print(f"Attendee Name: {attendeeName}")
            print("------------------------------")

            # Get connected attendees
            connect = db_neo4j.get_connected_attendees(attendeeID)

            if not connect:
                print("No connections")
                return
            
            # print connections
            for c in connect:
                name = db_mysql.get_attendee_name(c['ID'])
                print("These attendees are connected:")
                print(f"{c['ID']} | {name}")
            return
        except ValueError:
            print("*** ERROR *** Invalid Attendee ID")


# Option 5: Add attendee connection
# For the moment, the option will keep running until 
# I enter the right combination of attendees so it can create a connection. 
# I should be able to quit this option when I want

def op5():
    while True:
    
        try:
            attendee1 = int(input("Enter Attendee 1 ID: "))
            attendee2 = int(input("Enter Attendee 2 ID: "))

            # Check if both attendees exist
            a1 = db_mysql.attendee_exists(attendee1)
            a2 = db_mysql.attendee_exists(attendee2)

            if not a1 or not a2:
                print("*** ERROR *** One or both attendee IDs do not exist")
                continue
            
            if attendee1==attendee2:
                print("*** ERROR *** An attendee cannot connect to him/herself")
                continue
            
            # check if any attendee already has a connection
            if db_neo4j.connection_exists(attendee1,attendee2):
                print("*** ERROR *** These attendees are already connected")
                continue

            # Add connection in Neo4j
            db_neo4j.add_connection(attendee1, attendee2)
            print(f"Attendee {attendee1} is now connected to Attendee {attendee2}")
            return
        
        except ValueError:
            print("*** ERROR *** Attendee IDs must be numbers")

# Option 6: Get room information
def op6():
    try:
        rooms = db_mysql.get_room_info()
        print("Room ID | RoomName | Capacity")
        for room in rooms:
            print(f"{room[0]} | {room[1]} | {room[2]}")
    except Exception as e:
        print(f"*** ERROR *** {e}")

if __name__ == "__main__":
    main()