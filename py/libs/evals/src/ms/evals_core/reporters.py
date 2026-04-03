"""Reporter pool generation for eval tickets."""

import random

from ms.evals_core.constants import DEPARTMENTS

FIRST_NAMES: list[str] = [
    "James", "Mary", "Robert", "Patricia", "John", "Jennifer", "Michael", "Linda",
    "David", "Elizabeth", "William", "Barbara", "Richard", "Susan", "Joseph", "Jessica",
    "Thomas", "Sarah", "Christopher", "Karen", "Charles", "Lisa", "Daniel", "Nancy",
    "Matthew", "Betty", "Anthony", "Margaret", "Mark", "Sandra", "Steven", "Ashley",
    "Paul", "Dorothy", "Andrew", "Kimberly", "Joshua", "Emily", "Kenneth", "Donna",
    "Kevin", "Michelle", "Brian", "Carol", "George", "Amanda", "Timothy", "Melissa",
    "Ronald", "Deborah", "Edward", "Stephanie", "Jason", "Rebecca", "Jeffrey", "Sharon",
    "Ryan", "Laura", "Jacob", "Cynthia", "Gary", "Kathleen", "Nicholas", "Amy",
    "Eric", "Angela", "Jonathan", "Shirley", "Stephen", "Anna", "Larry", "Brenda",
    "Justin", "Pamela", "Scott", "Emma", "Brandon", "Nicole", "Benjamin", "Helen",
    "Samuel", "Samantha", "Raymond", "Katherine", "Gregory", "Christine", "Frank", "Debra",
    "Alexander", "Rachel", "Patrick", "Carolyn", "Jack", "Janet", "Dennis", "Catherine",
    "Jerry", "Maria", "Tyler", "Heather", "Aaron", "Diane", "Jose", "Ruth",
    "Nathan", "Julie", "Henry", "Olivia", "Douglas", "Joyce", "Peter", "Virginia",
    "Wei", "Mei", "Raj", "Priya", "Yuki", "Aiko", "Carlos", "Sofia",
    "Mohammed", "Fatima", "Dmitri", "Natasha", "Hans", "Elena", "Pierre", "Marie",
    "Satoshi", "Yui", "Jin", "Min-Ji", "Arjun", "Deepa", "Sven", "Ingrid",
    "Kofi", "Amara", "Omar", "Leila", "Chen", "Mei-Lin", "Vikram", "Ananya",
    "Marco", "Giulia", "Andre", "Claudia", "Leo", "Isabella", "Hugo", "Camille",
    "Ravi", "Neha", "Kenji", "Sakura", "Ali", "Zara", "Oscar", "Valentina",
    "Felix", "Clara", "Luca", "Sophia", "Noah", "Mia", "Ethan", "Ava",
    "Adrian", "Luna", "Diego", "Catalina", "Ivan", "Anastasia", "Niko", "Eleni",
    "Lars", "Freya", "Kwame", "Ama", "Jamal", "Aisha", "Miguel", "Carmen",
    "Tomas", "Petra", "Andrei", "Irina", "Yousef", "Noor", "Tariq", "Hana",
    "Amit", "Kavita", "Sanjay", "Meera", "Hiroshi", "Haruki", "Takeshi", "Emiko",
]

LAST_NAMES: list[str] = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
    "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson",
    "Thomas", "Taylor", "Moore", "Jackson", "Martin", "Lee", "Perez", "Thompson",
    "White", "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson", "Walker",
    "Young", "Allen", "King", "Wright", "Scott", "Torres", "Nguyen", "Hill",
    "Flores", "Green", "Adams", "Nelson", "Baker", "Hall", "Rivera", "Campbell",
    "Mitchell", "Carter", "Roberts", "Chen", "Wu", "Li", "Zhang", "Wang",
    "Liu", "Yang", "Huang", "Zhao", "Kim", "Park", "Choi", "Tanaka",
    "Patel", "Shah", "Singh", "Kumar", "Gupta", "Sharma", "Joshi", "Kapoor",
    "Muller", "Schmidt", "Schneider", "Fischer", "Weber", "Meyer", "Wagner", "Becker",
    "Rossi", "Russo", "Ferrari", "Esposito", "Romano", "Colombo", "Silva", "Santos",
    "Oliveira", "Nakamura", "Sato", "Suzuki", "Watanabe", "Ito", "Yamamoto", "Osei",
    "Mensah", "Addo", "Asante", "Owusu", "Petrov", "Volkov", "Sokolov", "Fedorov",
    "Ivanov", "Johansson", "Lindberg", "Eriksson", "Andersen", "Jensen", "Nielsen",
    "O'Brien", "O'Sullivan", "Murphy", "Kelly", "Byrne", "Ali", "Hassan", "Ibrahim",
    "Ahmed", "Khan", "Begum", "Rahman", "Chowdhury", "Tan", "Lim", "Koh",
    "Ng", "Ong", "Reyes", "Cruz", "Ramos", "Morales", "Vargas", "Mendoza",
    "Kowalski", "Nowak", "Wozniak", "Dubois", "Moreau", "Laurent", "Vasquez", "Diaz",
]

VIP_TITLES: list[str] = [
    "CEO", "CFO", "CTO", "COO", "CIO", "CISO",
    "SVP", "Executive Vice President", "Managing Director",
]


def generate_reporter(rng: random.Random, *, is_vip: bool = False) -> tuple[str, str, str]:
    """Generate a random reporter (name, email, department).

    Returns:
        Tuple of (full_name, email, department).
    """
    first = rng.choice(FIRST_NAMES)
    last = rng.choice(LAST_NAMES)
    full_name = f"{first} {last}"

    email_base = f"{first.lower()}.{last.lower()}"
    # Add suffix for potential duplicates
    suffix = rng.randint(1, 99) if rng.random() < 0.15 else 0
    email = f"{email_base}{suffix if suffix else ''}@contoso.com"

    if is_vip:
        department = rng.choice(["Executive Operations", "Corporate Strategy", "Institutional Trading"])
    else:
        department = rng.choice(DEPARTMENTS)

    return full_name, email, department


def generate_vip_name(rng: random.Random) -> tuple[str, str, str, str]:
    """Generate a VIP reporter with title.

    Returns:
        Tuple of (full_name, email, department, title).
    """
    name, email, department = generate_reporter(rng, is_vip=True)
    title = rng.choice(VIP_TITLES)
    return name, email, department, title
