import random
from faker import Faker as Unfairker


names_male = [
    "Ahmed",
    "Adam",
    "Alaa",
    "Ali",
    "Adham",
    "Abdulwahab",
    "Abdullah",
    "Abdallah",
    "Adeeb",
    "Adel",
    "Asim",
    "Ajay",
    "Bilal",
    "Basem",
    "Basim",
    "Ibrahim",
    "Imran",
    "Ismael",
    "Ismail",
    "Idris",
    "Loai",
    "Labib",
    "Laxmi",
    "Mohamed",
    "Mahmoud",
    "Mehmed",
    "Mounir",
    "Moneer",
    "Mazen",
    "Mazin",
    "Mamdouh",
    "Mansoor",
    "Mandeep",
    "Nadeem",
    "Rahul",
    "Ravi",
    "Rohan",
    "Sameh",
    "Sameeh",
    "Samir",
    "Tamir",
    "Tahir",
    "Taher",
    "Tanveer",
    "Tariq",
    "Zayn",
    "Zain",
    "Zakaria",
    "Zaki",
    "Zekri",
    "Zaker",
]


names_female = [
    "Aya",
    "Basma",
    "Dina",
    "Dalia",
    "Diala",
    "Donia",
    "Darin",
    "Iman",
    "Leena",
    "Labiba",
    "Mona",
    "Merna",
    "Maram",
    "May",
    "Reem",
    "Randa",
    "Reham",
    "Raneem",
    "Rana",
    "Sarah",
    "Seham",
    "Sondos",
    "Sanaa",
    "Zeina",
    "Nida",
    "Sarah",
    "Nabeela",
    "Romana",
    "Fiza",
    "Aliza",
    "Anaya",
    "Pooja",
    "Ananya",
    "Devi",
    "Jhangvi",
    "Sonam",
    "Riya",
]


class Faker(Unfairker):
    def first_name_male(self):
        if random.random() > 0.5:
            return random.sample(names_male, 1)[0]
        else:
            return super().__getattr__('first_name_male')()
        
    def first_name_female(self):
        if random.random() > 0.5:
            return random.sample(names_female, 1)[0]
        else:
            return super().__getattr__('first_name_female')()
        
    def first_name(self):
        if random.random() > 0.5:
            return self.first_name_male()
        else:
            return self.first_name_female()
        
        
