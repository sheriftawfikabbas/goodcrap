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
    "Basem",
    "Basim",
    "Ibrahim",
    "Ismael",
    "Ismail",
    "Idris",
    "Loai",
    "Labib",
    "Mohamed",
    "Mahmoud",
    "Mehmed",
    "Mounir",
    "Moneer",
    "Mazen",
    "Mazin",
    "Mamdouh",
    "Tamir",
    "Tahir",
    "Taher",
    "Zayn",
    "Zain",
    "Zakaria",
    "Zaki",
    "Zekri",
    "Zaker"
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
]

class Faker(Unfairker): 
    def first_name_male(self):
        if random.random()>0.5:
            return random.sample(names_male,1)[0]
        else:
            return super().first_name_male()
    def first_name_female(self):
        if random.random()>0.5:
            return random.sample(names_female,1)[0]
        else:
            return super().first_name_female()
    def first_name(self):
        if random.random()>0.5:
            return self.first_name_male()
        else:
            return super().first_name_female()
        
        