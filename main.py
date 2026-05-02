

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

    print(f"Session details for : {name}")

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
            type_in = input("Enter company ID or 'x' to exit request")
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
            company_name = db_mysql.get_company_name(comId)

            print(f"{company_name} Attendees")

            if not results:
                print(f"No attendees found for {company_name}")
                return

            for row in results:
                name, dob, session, speaker, room = row
                print(f"{name} | {dob} | {session} | {speaker} | {room}")
            return
        except:
            print("Invalid company Id")


if __name__ == "__main__":
    main()