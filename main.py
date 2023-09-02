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
                if query in phone.value:
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
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.phones = []
        self.emails = []
        self.birthday = birthday

    def add_phone(self, number: Phone):
        phone_number = Phone(number)
        if phone_number not in self.phones:
            self.phones.append(phone_number)

    def update_phone(self, old_number, new_number):
        old_phone = Phone(old_number)
        for i in range(len(self.phones)):
            if self.phones[i] == old_phone:
                self.phones[i] = Phone(new_number)

    def delete_phone(self, value):
        self.phones = [phone for phone in self.phones if phone.value != value]

    def add_email(self, email: Email):
        email_address = Email(email)
        if email_address not in self.emails:
            self.emails.append(email_address)

    def update_email(self, old_email, new_email):
        index = self.emails.index(old_email)
        self.emails[index] = new_email

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
    try:
        restored_address_book = load_address_book('address_book.pkl')
    except FileNotFoundError:
        restored_address_book = ADDRESSBOOK()

    name = Name('Nick')
    phone = Phone('987654321')
    rec = Record(name, phone)
    ab = ADDRESSBOOK()
    ab.add_record(rec)
    ab['Nick'] = rec
    ab['Nick'].add_phone('987654321')

    assert isinstance(ab['Nick'], Record)
    assert isinstance(ab['Nick'].name, Name)
    assert isinstance(ab['Nick'].phones, list)
    assert len(ab['Nick'].phones) > 0
    assert isinstance(ab['Nick'].phones[0], Phone)
    assert ab['Nick'].phones[0].value == '987654321'
    print('Test 1 : OK')

    name = Name('Art')
    phone = Phone('023456789')
    rec = Record(name, phone)
    ab = ADDRESSBOOK()
    ab.add_record(rec)
    ab['Art'] = rec
    ab['Art'].add_phone('023456789')

    assert isinstance(ab['Art'], Record)
    assert isinstance(ab['Art'].name, Name)
    assert isinstance(ab['Art'].phones, list)
    assert len(ab['Art'].phones) > 0
    assert isinstance(ab['Art'].phones[0], Phone)
    assert ab['Art'].phones[0].value == '023456789'
    print('Test 2 : OK')

    name = Name('Alice')
    phone = Phone('555555555')
    rec = Record(name, phone)
    ab = ADDRESSBOOK()
    ab.add_record(rec)
    ab['Alice'] = rec
    ab['Alice'].add_phone('555555555')

    assert isinstance(ab['Alice'], Record)
    assert isinstance(ab['Alice'].name, Name)
    assert isinstance(ab['Alice'].phones, list)
    assert len(ab['Alice'].phones) > 0
    assert isinstance(ab['Alice'].phones[0], Phone)
    assert ab['Alice'].phones[0].value == '555555555'
    print('Test 3 : OK')
    
    save_address_book(ab, 'address_book.pkl')

    print("Записи в адресній книзі:")
    for record in restored_address_book:
        print(f"Ім'я: {record.name.value}")
        print(f"Телефони: {', '.join(phone.value for phone in record.phones)}")
        print(f"Електронні адреси: {', '.join(email.value for email in record.emails)}")
        print(f"День народження: {record.birthday.value if record.birthday else 'Немає'}")
        print()

    # search_query = input("Введіть ім'я або номер телефону для пошуку: ")
    # search_results = ab.search_by_name_or_phone(search_query)

    # if search_results:
    #     print("Результати пошуку:")
    #     for result in search_results:
    #         print(f"Ім'я: {result.name.value}")
    #         print(f"Телефони: {', '.join(phone.value for phone in result.phones)}")
    #         print(f"Електронні адреси: {', '.join(email.value for email in result.emails)}")
    #         print(f"Дні до дня народження: {result.calculate_days_to_birthday()}")
    #         print()
    # else:
    #     print("Нічого не знайдено.")


