from address_book import *  #<-- Імпортуємо всі класи та їх методи з файлу address_book.py 

import time #<-- Імпортуємо модуль time для функції search_contact, щоб був гарний вивід
import difflib #<-- Імпортуємо бібліотеку defflib, вона має в собі алгоритм Левенштейна(за допоміж якого ми виконали завдання з *)

#Список commands містить усі команди по яким працює алгоритм Леванштейна
commands = ["hello", "add contact", "change contact", "get number contact", "show all contacts", "delete contact", "search contact", "goodbye", "close", "exit"]

#Декоратор 'input_error' обробляє вийнятки 'KeyError', 'IndexError', 'ValueError'
def input_error(func):
    def wrapper(name, phone):
        try:
            result = func(name, phone)
            return result
        except KeyError:
            print("The contact is missing. ")
        except IndexError:
            print("Enter the name and number separated by a space. ")
        except ValueError:
            print("ValueError. Please try again. ")
    return wrapper

#Функція повертає привітальне повідомлення
def hello():
    return "How i can help you?"


#Функція add_contact(name, phone) додає новий контакт до адресної книги, зберігає його у файлі "phonebook.csv" і повертає підтвердження.
@input_error
def add_contact(name, phone):
    ab = AddressBook()
    ab.load_to_file('phonebook.csv')
    record = Record(Name(name))
    record.phones.append(Phone(phone))
    ab.add_record(record)
    ab.save_to_file('phonebook.csv')
    return f"Contact {name} with phone number {phone} has been added."


#Функція change_contact(name, phone) змінює номер телефону існуючого контакту в адресній книзі, зберігає зміни у файлі "phonebook.csv" і повертає підтвердження.
@input_error
def change_contact(name, phone):
    ab = AddressBook()
    ab.load_to_file('phonebook.csv')
    if name in ab.data:
        record = ab.data[name]
        record.phones = [Phone(phone)]
        ab.save_to_file('phonebook.csv')
        return f"Contact {name}'s phone number has been update to {phone}. "
    else:
        return f"Contact {name}'s does not exist"
    

#Функція get_number_contact(name) повертає номер телефону контакту за вказаним іменем.
def get_number_contact(name):
    ab = AddressBook()
    ab.load_to_file('phonebook.csv')
    if name in ab.data:
        return f"The phone number of {name} is {ab.data[name].phones[0].value}. "
    else:
        return f"Contact {name} does not exist. "
    

#Функція show_all_contact() виводіть всі контакти з адресної книги
def show_all_contact():
    ab = AddressBook()
    ab.load_to_file('phonebook.csv')
    contacts_all = ""
    for name, record in ab.data.items():
        phones = [phone.value for phone in record.phones]
        contacts_all += f"| {name}: {', '.join(phones)} |\n"
    return contacts_all


#Функція delete_contact() видаляє контакт з адресної книги
def delete_contact(name):
    ab = AddressBook()
    ab.load_to_file('phonebook.csv')
    if name in ab.data:
        del ab.data[name]
        ab.save_to_file('phonebook.csv')
        return f"Contact with name {name} has been deleted."
    else:
        return f"Contact with name {name} not found."


#Функція exit_program() зберігає зміни у файлі "phonebook.csv" і повертає прощальне повідомлення.
def exit_program():
    ab = AddressBook()
    ab.load_to_file('phonebook.csv')
    ab.save_to_file('phonebook.csv')
    return "Goodbye!"


#Функція find_closest_command(user_input) знаходить найближчу команду до введеної користувачем, за допомогою алгоритму Левенштейну.
def find_closest_command(user_input):
    closest_command = difflib.get_close_matches(user_input, commands, n=1)
    if closest_command:
        return closest_command[0]
    else:
        return None


#Основна функція main() містить цикл, в якому відбувається взаємодія з користувачем. В залежності від введеної команди виконуються відповідні функції.
def main():
    print("Welcome to the Assistant bot! ")
    while True:
        user_input = input("Enter a command: ")
        if user_input.lower() in ["goodbye", "close", "exit"]:
            print(exit_program())
            break
        elif user_input.lower() == "hello":
            print(hello())
        elif user_input.lower() == "delete contact":
            name = input("Enter a contact to delete: ")
            print(delete_contact(name))
        elif user_input.lower() == "show all contacts":
             print(show_all_contact())
        elif user_input.lower() == "add contact":
            name = input("Enter the name: ")
            phone = input("Enter the phone number: ")
            print(add_contact(name, phone))
        elif user_input.lower() == "change contact":
            contact_info = input("Enter the name and new phone number separated by a space: ")
            name, phone = contact_info.split()
            print(change_contact(name, phone))
        elif user_input.lower() == "get number contact":
            name = input("Enter the name: ")
            print(get_number_contact(name))
        elif user_input.lower() == "search contact":
            ab = AddressBook()
            ab.load_to_file('phonebook.csv')
            search_query = input("Enter the search query: ")
            result = ab.search_contact(search_query)
            if len(result) > 0:
                print("Searching similarities, please wait..")
                time.sleep(2)
                print("Succsessfully completed :D \n ↓ ↓ INFO ↓ ↓")
                time.sleep(1.5)
                for record in result:
                    print(f"Contact found: {record.name.value}")
                    for phone in record.phones:
                        print(f"Phone number: {phone.value}")
            else:
                print("Searching similarities, please wait..")
                time.sleep(2)
                print(f"No contacts found with the provided search query. ")
        
        else:
            closest_command = find_closest_command(user_input)
            if closest_command:
                print(f"Did you mean '{closest_command}'? ")
            else:
                print("Invalid command. ")
        

if __name__ == "__main__":
    main()