

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


def main():
    while True:
        menu()
        choice = input("Choice: ")

        if choice == "1":
            op1()
        elif choice =="2":
            op2()
        elif choice =="x":
            break

# Option 1: Get speakers, their sessions and rooms
def op1():
    name = input("Enter speaker name: ")
    results = db_mysql.get_speakers_sessions(name)

    print("Session details for speakers:", name)

    if not results:
        print("No speakers found")
        return

    for row in results:
        speaker, session, room = row
        print(f"{speaker} | {session} | {room}")
          

# Option 2: Get attendees by company
def op2():
    comId = int(input("Enter company ID: "))

    # companyId must be valid
    if comId <= 0:
        raise ValueError("Company ID must be a positive integer")
    
    if not db_mysql.company_exists(comId):
        print(f"Company with Id {comId} does not exist.")
        return

    results = db_mysql.get_attendees(comId)
    company_name = db_mysql.get_company_name(comId)

    print(f"{company_name} Attendees")

    if not results:
        print(f"No attendees found for {company_name}")
        return

    for row in results:
        name, dob, session, speaker, room = row
        print(f"{name} | {dob} | {session} | {speaker} | {room}")



if __name__ == "__main__":
    main()