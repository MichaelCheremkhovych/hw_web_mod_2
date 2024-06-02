from collections import UserDict
from datetime import datetime, timedelta
import pickle

class AddressBook(UserDict):
    
    def __init__(self):
        super().__init__()
        
    def load_data(self, filename = 'address_book.pkl'):
        try:
            with open(filename, 'rb') as file:
                return pickle.load(file)
        except FileNotFoundError:
            return AddressBook()  # Повертаємо новий екземпляр адресної книги, якщо файл не знайдено

    def save_data(self, filename = 'address_book.pkl'):
        with open(filename, 'wb') as file:
            pickle.dump(self, file)

        
    def add_contact(self, record):
        # Додає контакт до книги адрес
        self.data[record.name.value] = record

    def remove_contact(self, name):
        # Видаляє контакт за ім'ям з книги адрес
        if name in self.data:
            del self.data[name]
    
    def change_contact_name(self, name):
        # Змінює ім'я контакту за ім'ям
        if name in self.data:
            record = self.data.pop(name)
            new_name = input("Enter new name for the contact: ")
            record.name.value = new_name
            self.data[new_name] = record

    def change_contact_phone(self, name):
        # Змінює номер телефону контакту за ім'ям
        if name in self.data:
            record = self.data[name]
            old_phone_number = input("Enter the old phone number: ")
            new_phone_number = input("Enter the new phone number: ")
            record.edit_phone(old_phone_number, new_phone_number)
            print("Phone number changed.")
        else:
            print("Contact not found.")    
    
    @staticmethod
    def birthday_contact(users):
        # Обробляє дні народження контактів і повертає список користувачів з наступними днями народження
        prepared_users = []  # Оголошення порожнього списку для підготовлених користувачів
        for user in users:
            try:
                birthday_str = user.birthday.strftime('%d.%m.%Y')
                birthday = datetime.strptime(birthday_str, '%d.%m.%Y').date()
                prepared_users.append({"name": user.name.value, 'birthday': birthday})
            except ValueError:
                print(f'Некоректна дата народження для користувача {user.name.value}')
        return prepared_users    

    def get_upcoming_birthdays(self, prepared_users, days=7):   
        today = datetime.today().date() #поточна дата
        upcoming_birthdays = [] #список майбутніх днів народження
        for user in prepared_users: #ітерація по підготовленим користувачам
            birthday_this_year = user["birthday"].replace(year=today.year) #заміна року на поточний для дня народження цього року
            if birthday_this_year < today: #якщо дата народження вже пройшла цього року
                birthday_this_year = birthday_this_year.replace(year=today.year + 1) #переносимо наступний рік
            if 0 <= (birthday_this_year - today).days <= days: #якщо день народження в межах вказаного періоду
                if birthday_this_year.weekday() >= 5: #якщо день народження випадає на суботу або неділю
                   birthday_this_year = self.find_next_weekday(birthday_this_year, 0) #знаходимо наступний понеділок
                congratulation_date_str = birthday_this_year.strftime('%d.%m.%Y') #форматуємо дату у рядок
                upcoming_birthdays.append({                           #додаємо дані про майбутній день народження
                    "name": user["name"],
                    "congratulation_date": congratulation_date_str
                })
        return upcoming_birthdays #повертаємо список словників із даними про майбутні дні народження    
    
    @staticmethod
    def find_next_weekday(d, weekday: int):
        days_ahead = weekday - d.weekday()  #різниця між заданим днем тижня та днем тижня заданої дати
        if days_ahead <= 0:  #якщо день народження вже минув
            days_ahead += 7  #додаємо 7 днів, щоб отримати наступний тиждень
        return d + timedelta(days=days_ahead)  #повертаємо нову дату

    def show_phone(self, name):
        # Показує номер телефону за ім'ям контакту
        if name in self.data:
            print(self.data[name])

    def get_contact(self, name):
        # Повертає контакт за ім'ям
        return self.data.get(name)

    def get_all_contacts(self):
        # Повертає всі контакти з книги адрес
        return self.data.values()

# Клас, що представляє базове поле (значення)
class Field:
    
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

# Клас, який наслідується від базового поля для збереження імені
class Name(Field):
    pass

# Клас, який наслідується від базового поля для збереження номера телефону з валідацією
class Phone(Field):
    
    def __init__(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Phone number must be a 10-digit number.")
        super().__init__(value)

# Клас Дати народження
class Birthday(Field):
    pass
    
    


# Клас, що представляє запис у книзі контактів
class Record:
    
    def __init__(self, name, phone_number, birthday = None):
        self.name = Name(name)  # Записуємо ім'я як об'єкт класу Name
        self.phones = [Phone(phone_number)]  # Список для збереження номерів телефонів
        self.birthday = birthday

    def add_phone(self, phone_number):
        self.phones.append(Phone(phone_number))  # Додаємо новий номер телефону

    def remove_phone(self, phone_number):
        # Видаляємо номер телефону зі списку
        for phone in self.phones:
            if phone.value == phone_number:
                self.phones.remove(phone)
                break

    def edit_phone(self, old_phone_number, new_phone_number):
        # Редагуємо номер телефону у списку
        for phone in self.phones:
            if phone.value == old_phone_number:
                phone.value = new_phone_number
                break

    def add_birthday(self, birthday): # Додає нову дату народження
        self.birthday = birthday
    
    def edit_birthday(self, new_birthday): # Редагуємо дату народження
        self.birthday = new_birthday
    
    def find_phone(self, phone_number):
        # Пошук номера телефону у записі
        for phone in self.phones:
            if phone.value == phone_number:
                return phone
        return None

    def __str__(self):
        # Перевизначений метод для зручного виводу інформації про запис
        return f"Contact name: {self.name.value}, phones: {'; '.join(str(p) for p in self.phones)}, birthday: {self.birthday}"


def input_error(func):
    """
    Декоратор для обробки помилок введення користувача.
    Обробляє винятки KeyError, ValueError, IndexError.
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (KeyError, ValueError, IndexError) as e:
            print(f"Error: {e}")
            return None
    return wrapper    

@input_error
# Функція для додавання контакту
def add_contact(address_book):
    name = input("Enter contact name: ")
    phone_number = input("Enter contact phone number: ")
    record = Record(name, phone_number)
    address_book.add_contact(record)
    print("Contact added.")

@input_error
# Функція для видалення контакту
def remove_contact(address_book):
    name = input("Enter the name of the contact you want to remove: ")
    address_book.remove_contact(name)
    print("Contact removed.")

@input_error
# Функція для зміни імені контакту
def change_contact_name(address_book):
    name = input("Enter the name of the contact you want to change: ")
    address_book.change_contact_name(name)
    print("Contact name changed.")

@input_error
# Функція для зміни номеру телефону контакту
def change_contact_phone(address_book):
    name = input("Enter the name of the contact whose phone number you want to change: ")
    address_book.change_contact_phone(name)
    print("Phone number changed.")

@input_error
# Функція для відображення конкретного контакту
def show_phone(address_book):
    name = input("Enter the name of the contact you want to show: ")
    address_book.show_phone(name)

@input_error
# Функція для відображення всіх контактів
def show_all_contacts(address_book):
    print("All contacts:")
    for record in address_book.get_all_contacts():
        print(record)

@input_error
# Функція для відображення всіх контактів з датою народження
def show_birthday(address_book):
    for record in address_book.get_all_contacts():
        print(f"Name: {record.name.value}, Birthday: {record.birthday}")


@input_error
# Функція для додавання дня народження контакта
def add_contact_birthday(address_book):
    name = input("Enter contact name: ")
    existing_record = address_book.get_contact(name)
    if existing_record:
        birthday_str = input("Enter contact's birthday (DD.MM.YYYY): ")
        birthday = datetime.strptime(birthday_str, '%d.%m.%Y').date()
        existing_record.add_birthday(birthday)
        print("Birthday added.")
    else:    
        print("Contact added with birthday.")

@input_error
# Функція для зміни дня народження контакта
def edit_birthday(address_book):
    name = input("Enter the name of the contact whose birthday you want to change: ")
    record = address_book.get_contact(name)
    if record:
        new_birthday_str = input("Enter the new birthday (DD.MM.YYYY): ")
        new_birthday = datetime.strptime(new_birthday_str, '%d.%m.%Y').date()
        record.edit_birthday(new_birthday)
        print("Contact birthday changed.")
    else:
        print("Contact not found.")


def parse_input(command):
    """
    Функція для розбору введеної команди.
    """
    parts = command.split()
    if len(parts) < 1:
        return None, []
    action = parts[0].lower()
    if action == "exit" or action == "close":
        return action, []
    elif action in ["hello", "add", "remove", "change_name", "change_phone", "show", "all", "add_birthday", "edit_birthday", "show_birthday", "upcoming_birthdays"]:
        return action, parts[1:]
    else:
        return "Unknown command.", []

#блок виводу інформації від бота
def main():
    print("Welcome to the assistant bot!")
    address_book = AddressBook()

    address_book = address_book.load_data() # Завантажуємо збережені дані при запуску програми

    while True:
        command = input("Enter command: ")
        action, args = parse_input(command)
        if action == "exit" or command == "close":
            print("Good bye!")
            address_book.save_data()
            break
        elif action == "hello":
            print("How can I help you?")
        elif action == "add":
            add_contact(address_book)
        elif action == "remove":
            remove_contact(address_book)
        elif action == "change_name":
            change_contact_name(address_book)
        elif action == "change_phone":
            change_contact_phone(address_book)
        elif action == "add_birthday":
            add_contact_birthday(address_book)
        elif action == "edit_birthday":
            edit_birthday(address_book)
        elif action == "show_birthday":
            show_birthday(address_book)    
        elif action == "show":
            show_phone(address_book)
        elif action == "upcoming_birthdays":
            list_of_contacts = list(address_book.get_all_contacts())
            prepared_users = AddressBook.birthday_contact(list_of_contacts)
            upcoming = address_book.get_upcoming_birthdays(prepared_users)
            if upcoming:
                print("Upcoming birthdays this week:")
                for contact in upcoming:
                    print(f"{contact['name']}: {contact['congratulation_date']}")
            else:
                print("No upcoming birthdays this week.")    
        elif action == "all":
            show_all_contacts(address_book)
        else:
            print(action)
            print("Unknown command.")

if __name__ == "__main__":
    main()
   
