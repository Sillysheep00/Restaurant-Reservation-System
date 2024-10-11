import os
import random
from datetime import datetime, timedelta


# Open to read file
def read_file(file_path):
    with open(file_path, 'r') as files:
        my_reservation_list = files.readlines()
        return my_reservation_list


# Open to write file
def write_file(file_path, my_reservation_list):
    with open(file_path, 'w') as file:
        for line in my_reservation_list:
            file.write(line.rstrip() + '\n')

        # Clear screen for better presentation


def clear_screen():
    os.system('cls')


# Get reservation date in a correct format
def is_valid_date(date_input):
    try:
        reservation_date = datetime.strptime(date_input, "%Y-%m-%d").date()
        current_date = datetime.now().date()
        time_diff = reservation_date - current_date
        return time_diff >= timedelta(days=5)
    except ValueError:
        return False


# Get user phone number in correct format
def is_valid_phone(phone_input):
    if len(phone_input) not in (10, 11):
        return False

    if phone_input.startswith('01') and phone_input.isdigit():
        return True

    return False


# Get user email address in correct format
def is_valid_email(email_input):
    if '@' in email_input and '.' in email_input:
        return True

    return False


# Allow user to choose the time slot they want. Time slot above 8 reservations are required to change the time slot
def validate_time_slot(date_input, slot_input, my_reservation_list):
    matching_bookings = [
        reservation for reservation in my_reservation_list if reservation.startswith(f"{date_input.ljust(10)} | Slot {str(slot_input)}")
    ]
    remaining_slots = 8 - len(matching_bookings)
    if remaining_slots <= 0:
        return False
    else:
        return True


# Call the function to run the program for adding reservation
def add_reservation():
    global my_reservation_list
    print("\n--- Add Reservation ---")
    while True:
        date = input("Enter the date (YYYY-MM-DD): ")
        if is_valid_date(date):
            break
        else:
            print("\nPlease enter a valid date format and book 5 days in advance. Sorry for the inconvenience.\n")

    while True:
        existing_slots = [line.split('|')[1].strip() for line in my_reservation_list if line.split('|')[0].strip() == date]
        slot_counts = {slot: existing_slots.count(slot) for slot in existing_slots}

        # Update the available_slots list to include only available slots
        available_slots = [slot_num for slot_num in range(1, 5) if validate_time_slot(date, slot_num, my_reservation_list)]

        if not available_slots:
            print("\nNo available time slots for this date. Please choose another date.")
            return
        print(" [1]12.00pm - 02.00pm\n [2]02.00pm - 04.00pm\n [3]06.00pm - 08.00pm\n [4]08.00pm - 10.00pm")
        print("\nAvailable Time Slots:")
        for slot_num in available_slots:
            slot_key = f"Slot {slot_num}"
            remaining_slots = 8 - slot_counts.get(slot_key, 0)
            print(f"Slot {slot_num}: {remaining_slots} remaining")

        while True:
            slot = input(f"\nEnter slot ({', '.join(map(str, available_slots))}) ".ljust(37) + ": ")

            if slot not in map(str, available_slots):
                print("Please enter a valid slot.")
            elif not validate_time_slot(date, int(slot), my_reservation_list):
                print("Slot is fully booked, please choose another slot.")
            else:
                break

        name = input(("Enter name ").ljust(36) + ": ").upper()

        while True:
            email = input(("Enter email ").ljust(36) + ": ")
            if is_valid_email(email):
                break
            else:
                print("Please enter a valid email address.")

        while True:
            phone = input(("Enter phone (10 digits/ 11 digits) ").ljust(36) + ": ")
            if is_valid_phone(phone):
                break
            else:
                print("Please enter a valid Malaysia 10 or 11 digit phone number starting with '01'.")

        while True:
            pax = input(("Enter pax (max 4) ").ljust(36) + ": ")
            if pax in {"1", "2", "3", "4"}:
                break
            else:
                print("Only 4 pax in a group for a single reservation. Please enter a valid pax.")

        new_reservation = f"{date} | Slot {slot} | {name.ljust(15)} | {email.ljust(29)} | {phone.ljust(15)} | {pax}\n"
        my_reservation_list.append(new_reservation)
        print("\nReservation added successfully!")
        return


# Prompt user to enter their reservation detail for confirmation
def find_reservation(name):
    for index, reservation in enumerate(my_reservation_list):
        if reservation.split('|')[2].strip().upper() == name:  # Assuming name is the 3rd element
            return index, reservation
    return -1, None


def get_continue_input():
    while True:
        try:
            user_input = input("Would you like to continue updating reservations? (Y/N): ").upper()
            if user_input == 'N':
                print("Quitting reservation update.")
                main_program()
                break

            elif user_input == 'Y':
                update_reservation()
                break
            else:
                print("Invalid input.Please enter'Y' to continue or 'N' to quit")

        except Exception as e :
            print("Invalid input. Please enter 'Y' to continue or 'N' to quit.",str(e))




# Allow user to edit the reservation details chosen by them
def update_reservation():
    print("\n--- Update Reservation ---")
    user_confirmation = input("Enter reservation NAME to update: ").strip().upper()
    index, reservation_line = find_reservation(user_confirmation)

    if index == -1:
        print("Reservation not found. Please enter a valid name.")
        return

    else:
        print("Current Details:")
        print(reservation_line)

        date = reservation_line.split('|')[0].strip()

        rl = reservation_line.split('|')
        rl = list(map(lambda p: p.strip(), rl))

        day_reservations = dict()
        for mr in my_reservation_list:
            parts = mr.split('|')
            parts = list(map(lambda p: p.strip(), parts))

            if parts == rl:
                continue

            rdata = parts[0]
            slot = parts[1]
            dataslot = '|'.join([rdata, slot])
            if dataslot not in day_reservations:
                day_reservations[dataslot] = 1
            else:
                day_reservations[dataslot] += 1

        # Prompt user to enter(1,2,3,4,5,6,7) for the detail that they want to edit
        while True:
            print("\nPlease enter the selection that you would like to edit.")
            print("[1] Reservation Date\n[2] Reservation Time Slot\n[3] Reservation Name")
            print("[4] Reservation Email\n[5] Reservation Phone Number\n[6] Reservation Pax")
            print("[7] Done Editing Reservation")
            selected_details = input("Selections: ").split(',')

            updated_details = reservation_line.split('|')
            date = updated_details[0]
            try:
                for select_edit in selected_details:
                    select_edit = int(select_edit.strip())

                    if select_edit == 1:
                        while True:
                            new_date_input = input("Enter the new date (YYYY-MM-DD): ")
                            if is_valid_date(new_date_input):
                                updated_details[0] = new_date_input
                                reservation_line = ' | '.join(updated_details)  # Update reservation_line with new date
                                break
                            else:
                                print("ERROR: Invalid date format or date not at least 5 days in advance.")

                    elif select_edit == 2:
                        for s in range(1, 5):
                            slot = f"Slot {s}"
                            dataslot = '|'.join([date.strip(), slot])
                            print('Slot', s, ':', 8 - day_reservations.get(dataslot, 0))

                        while True:
                            new_time_chosen = input("Enter the new time slot [1, 2, 3, 4]: ")

                            if new_time_chosen in ['1', '2', '3', '4']:
                                new_time_slot = f"Slot {new_time_chosen}"
                                dataslot = '|'.join([date, slot])
                                if day_reservations.get(dataslot, 0) < 8:
                                    updated_details[1] = new_time_slot
                                    reservation_line = ' | '.join(
                                        updated_details)  # Update reservation_line with new slot
                                    break
                                else:
                                    print("Time slot is fully booked. Please choose another time slot.")

                            else:
                                print("Invalid input. Please enter according to the format [1,2,3,4].")

                    elif select_edit == 3:
                        new_name = input("Enter the new name: ")
                        updated_details[2] = new_name
                        reservation_line = ' | '.join(updated_details)  # Update reservation_line with new name

                    elif select_edit == 4:
                        while True:
                            new_email = input("Enter the new email: ")
                            if is_valid_email(new_email):
                                updated_details[3] = new_email
                                reservation_line = ' | '.join(updated_details)  # Update reservation_line with new email
                                break
                            else:
                                print(
                                    "Invalid email address. Please enter your email in a valid form (example@xxxxx.com).")

                    elif select_edit == 5:
                        while True:
                            new_phone_number = input("Phone Number (eg. 0123456789): ")
                            if is_valid_phone(new_phone_number):
                                updated_details[4] = new_phone_number
                                reservation_line = ' | '.join(updated_details)  # Update reservation_line with new phone
                                break
                            else:
                                print("Invalid input. Please enter a valid phone number. (Example: 0123456789)")

                    elif select_edit == 6:
                        while True:
                            new_pax = input("Enter the new number of people (1-4): ")
                            if new_pax in {"1", "2", "3", "4"}:
                                updated_details[5] = new_pax
                                reservation_line = ' | '.join(updated_details)  # Update reservation_line with new pax
                                break
                            else:
                                print(
                                    "Only 4 pax in a group for a single reservation. Please enter a valid number (1-4).")

                    elif select_edit == 7:
                        print("\nDone updating reservation.")
                        return  # Return to exit the function
                    else:
                        print("Invalid choice. Choose 1, 2, 3, 4, 5, 6, or 7.")

            except ValueError:
                print("Invalid choice. Please verified again")
                break
            
            
            print("\nUpdated Details:")
            print(reservation_line)
            
            my_reservation_list[index] = reservation_line
            my_reservation_list.reverse()

            
           
            # Write the updated reservations back to the file
    return get_continue_input()



# Allow user to delete reservation
def delete_reservation():
    global my_reservation_list
    count = 0

    print("\n--- Delete Reservation ---")
    print("\nCurrent Reservations:")
    for i, line in enumerate(my_reservation_list, start=1):
        print(f"{i}. {line.strip()}")

    # Prompt user to enter the number of line that they want to delete
    while True:
        try:
            line_to_delete_in_list = int(
                input("\nEnter the line number to delete (e.g., '1' to delete the first line): "))
            line_to_delete_index = line_to_delete_in_list - 1
            if 0 <= line_to_delete_index < len(my_reservation_list):
                deleted_reservation = my_reservation_list.pop(line_to_delete_index)
                print(f"\nDelete Reservation '{deleted_reservation.strip()}'\nReservation successfully cancelled!")
                break
            else:
                print("ERROR: Invalid Line Number!")

        except ValueError:
            print("ERROR: Invalid Line Number!")


# defining read_menu_file() function to open restaurant menu and read the content (dishes) inside
def read_menu_file():
    with open('menuItems.txt', 'r') as files:
        my_menu_list = files.readlines()
    return my_menu_list


def get_random_food():
    count = 0
    # calling read_menu_file() function to read the contents of the file and print out the contents
    my_menu_list = read_menu_file()
    print("\nMenu Items:")
    for item in my_menu_list:
        print(item.strip())
        # Using strip() to remove leading and trailing whitespaces
    while True:
        recommended_food = random.choice(my_menu_list)
        # using random.choice() to recommend dishes (choice) to customer randomly
        my_menu_list.remove(recommended_food)
        # remove the recommended food recently to avoid recommending same dishes to customers
        print("\n---Taste Sensations: Chef's Special Recommendations---")
        print(f"Chef's Daily Picks: {recommended_food}")
        # display the first recommended food

        print('Would you like more food recommendations?\n[1] Yes\n[2] No')
        # ask to make sure the customer is satisfied with the food recommended recently
        selection = int(input('Enter your selection [1 or 2]: '))
        print()
        try:
            if selection == 1:
                count += 1

            elif selection == 2:
                print(
                    "We're happy that we could assist in finding the perfect food for you."
                    "\nYour satisfaction means a lot to us!")
                break

        except ValueError:
            # Handle non-integer inputs
            print('\nERROR: Invalid Input!\nPlease enter [1] for Yes or [2] for No.\n')

        if count == 10:
            # only recommend 10 dishes
            print(
                "\nSORRY!"
                "\nPlease accept our apologies for not having any specific recommendation."
                "\nHowever, we would like to extend an invitation to explore our menu once again."
                "\nWe apologize for any disappointment and hope you'll find something delightful among our diverse offerings.")
            break



column_widths = [12, 10, 20, 35, 20, 5]


def print_subheading():
    subheading = f"{'Date'.ljust(column_widths[0])} | {'Slot'.ljust(column_widths[1])} | {'Name'.ljust(column_widths[2])} | {'Email'.ljust(column_widths[3])} | {'Mobile No.'.ljust(column_widths[4])} | {'Pax'.ljust(column_widths[5])}"
    print(subheading)


# Display main menu of the restaurant reservation system which prompt user to enter (1,2,3,4,5) for the relevant service
def print_reservations(reservation_list):
    print_subheading()  # Print the subheading first
    for line in reservation_list:
        formatted_line = line.strip().split('|')

        for i in range(len(formatted_line)):
            formatted_line[i] = formatted_line[i].strip().ljust(column_widths[i])

        print(" | ".join(formatted_line))


def main_program():
    clear_screen()
    print('- Welcome to Charming Thyme Trattoria! -\n')
    file_path = "reservation.txt"
    global my_reservation_list
    my_reservation_list = read_file(file_path)
    print("All Bookings:\n")
    print_reservations(my_reservation_list)

    while True:
        try:  # User are asked to enter correct input to continue the program; program will loop if it's an invalid input
            print('\nWhat service would you like to choose?\n')
            print(
                '[1] Add Reservation\n[2] Delete Reservation\n[3] Update Reservation\n[4] Food Recommendation\n[5] Exit\n')
            choice = int(input('Choice: '))
            if choice == 1:
                add_reservation()
                print("\nUpdated All Bookings:")
                print_reservations(my_reservation_list)
                write_file(file_path, my_reservation_list)

            elif choice == 2:
                delete_reservation()
                print("\nUpdated All Bookings:")
                print_reservations(my_reservation_list)
                write_file(file_path, my_reservation_list)

            elif choice == 3:
                update_reservation()
                print("\nUpdated All Bookings:")
                print_reservations(my_reservation_list)
                write_file(file_path, my_reservation_list)

            elif choice == 4:
                get_random_food()

            elif choice == 5:
                print("All Bookings:")
                print_reservations(my_reservation_list)
                print("\nThank you!")
                print(
                    "May your time at our restaurant be filled with delightful moments and unparalleled satisfaction.")
                print("\nHave a nice day!!")
                exit()

            else:
                print("ERROR! Please enter a valid service [1-5].")

        except ValueError:
            print("ERROR! Please enter a valid choice [1-5].")


main_program()
