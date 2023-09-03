from collections import UserDict
from datetime import datetime
import pickle


class ADDRESSBOOK(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def __iter__(self):
        self._iter_index = 0
        return self

    def __next__(self):
        if self._iter_index < len(self.data):
            keys = list(self.data.keys())
            key = keys[self._iter_index]
            self._iter_index += 1
            return self.data[key]
        else:
            raise StopIteration

    def search_by_name_or_phone(self, query):
        results = []
        for record in self.data.values():
            if isinstance(record.name.value, str) and query.lower() in record.name.value.lower():
                results.append(record)
            for phone in record.phones:
                if query == phone.value:  # Зміна тут: порівнюємо замість перевірки входження
                    results.append(record)
                    break
        return results

# Зберігання адресної книги до файлу
def save_address_book(address_book, filename):
    with open(filename, 'wb') as file:
        pickle.dump(address_book, file)

# Завантаження адресної книги з файлу
def load_address_book(filename):
    with open(filename, 'rb') as file:
        return pickle.load(file)

class Field:
    def __init__(self, value):
        self.value = value


class Phone(Field):
    def __init__(self, value):
        super().__init__(value)
        if not self.is_valid_phone(value):
            raise ValueError("Invalid phone number")

    def is_valid_phone(self, value):
        return True


class Name(Field):
    def __init__(self, value):
        super().__init__(value)


class Email(Field):
    def __init__(self, value):
        super().__init__(value)


class Record:
    def __init__(self, name, phone, email, birthday=None):
        self.name = Name(name)
        self.phones = [Phone(phone)]
        self.emails = [Email(email)]
        self.birthday = birthday

    def add_phone(self, number):
        if number not in [phone.value for phone in self.phones]:
            self.phones.append(Phone(number))

    def update_phone(self, old_number, new_number):
        for i in range(len(self.phones)):
            if self.phones[i].value == old_number:
                self.phones[i] = Phone(new_number)

    def delete_phone(self, value):
        self.phones = [phone for phone in self.phones if phone.value != value]

    def add_email(self, email):
        if email not in [e.value for e in self.emails]:
            self.emails.append(Email(email))

    def update_email(self, old_email, new_email):
        for i in range(len(self.emails)):
            if self.emails[i].value == old_email:
                self.emails[i] = Email(new_email)

    def delete_email(self, value):
        self.emails = [email for email in self.emails if email.value != value]

    def calculate_days_to_birthday(self):
        if self.birthday:
            today = datetime.today()
            next_birthday = datetime(
                today.year, self.birthday.value.month, self.birthday.value.day
            )
            if next_birthday < today:
                next_birthday = datetime(
                    today.year + 1, self.birthday.value.month, self.birthday.value.day
                )
            days_remaining = (next_birthday - today).days
            return days_remaining
        else:
            return None


class Birthday(Field):
    def __init__(self, value):
        self.value = value

    def is_valid_birthday(self, value):
        return True

    def __get__(self, instance, owner):
        return self.value

    def __set__(self, instance, value):
        if not self.is_valid_birthday(value):
            raise ValueError("Incorrect Birthday")

if __name__ == "__main__":
    # Створення декількох контактів
    name1 = Name("Art")
    phone1 = Phone("023456789")
    email1 = Email("art@gmail.com")
    birthday1 = Birthday(datetime(1997, 7, 10))

    name2 = Name("Nick")
    phone2 = Phone("987654321")
    email2 = Email("Nick@gmail.com")
    birthday2 = Birthday(datetime(1997, 8, 9))

    # Створення записів в книгу
    record1 = Record(name1, phone1, email1, birthday1)
    record2 = Record(name2, phone2, email2, birthday2)

    # Додавання та редагування контактів
    record1.add_phone("11111111")
    record2.update_email("Nick@gmail.com", "Nickdiss@gmail.com")

    # Створення адресної книги та додавання записів
    address_book = ADDRESSBOOK()
    address_book.add_record(record1)
    address_book.add_record(record2)

    # Збереження адресної книги до файлу
    save_address_book(address_book, "address_book.pkl")

    # Завантаження адресної книги
    loaded_address_book = load_address_book("address_book.pkl")

    search_str = "11111111"
    search_result = loaded_address_book.search_by_name_or_phone(search_str)
if search_result:
    print("Результати пошуку:")
    for result in search_result:
        print(f"Ім'я: {result.name.value}")
        print("Телефони:")
        for phone in result.phones:
            print(f"- {phone.value}")
        print("Електронні адреси:")
        for email in result.emails:
            print(f"- {email.value}")
        print(f"Дні до дня народження: {result.calculate_days_to_birthday()}")
        print()
else:
    print("Нічого не знайдено.")




  
