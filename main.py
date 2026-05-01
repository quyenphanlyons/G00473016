

import db_mysql

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

def op1():
    name = input("Enter speaker name: ")
    results = db_mysql.get_speakers_sessions(name)

    print("Session details for speakers:", name)

    if not results:
        print("No speakers found")
        return

    for row in results:
        speaker, session, room = row
        print(f"{speaker}, {session}, {room}")
          

def main():

    while True:
        menu()
        choice = input("Choice: ")

        if choice == "1":
            op1()
        elif choice =="x":
            break

if __name__ == "__main__":
    main()