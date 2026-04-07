"""Reporter pool for ticket generation.

Provides diverse names, emails, and departments for Contoso Financial Services.
"""

from dataclasses import dataclass


@dataclass
class Reporter:
    """A ticket reporter."""

    name: str
    email: str
    department: str
    is_vip: bool = False


# ── Departments at Contoso Financial Services ─────────────────────────────

DEPARTMENTS = [
    "Engineering",
    "Wealth Management",
    "Executive Operations",
    "Risk & Compliance",
    "Trading",
    "Finance",
    "Human Resources",
    "Legal",
    "Marketing",
    "Client Services",
    "Operations",
    "Research & Analytics",
    "Product Management",
    "Infrastructure",
    "Security",
    "Data Science",
    "Accounting",
    "Treasury",
    "Internal Audit",
    "Corporate Strategy",
    "Facilities",
    "Procurement",
    "Investor Relations",
    "Private Banking",
    "Commercial Banking",
    "Asset Management",
    "Quantitative Research",
    "Regulatory Affairs",
    "Business Development",
    "IT Support",
]


# ── Reporter Pool ─────────────────────────────────────────────────────────

REPORTERS: list[Reporter] = [
    # VIP reporters (C-suite, SVP+)
    Reporter("James Harrison", "james.harrison@contoso.com", "Executive Operations", True),
    Reporter("Victoria Chen", "victoria.chen@contoso.com", "Executive Operations", True),
    Reporter("Robert Blackwell", "robert.blackwell@contoso.com", "Executive Operations", True),
    Reporter("Catherine Okafor", "catherine.okafor@contoso.com", "Finance", True),
    Reporter("Michael Strauss", "michael.strauss@contoso.com", "Trading", True),
    Reporter("Elena Marchetti", "elena.marchetti@contoso.com", "Wealth Management", True),
    Reporter("David Kim", "david.kim@contoso.com", "Corporate Strategy", True),
    Reporter("Sandra Williams", "sandra.williams@contoso.com", "Legal", True),
    Reporter("Thomas Anderson", "thomas.anderson@contoso.com", "Risk & Compliance", True),
    Reporter("Priya Sharma", "priya.sharma@contoso.com", "Asset Management", True),
    # Regular reporters — diverse pool
    Reporter("Sarah Chen", "sarah.chen@contoso.com", "Engineering"),
    Reporter("Marcus Rodriguez", "marcus.rodriguez@contoso.com", "Wealth Management"),
    Reporter("Diana Marsh", "diana.marsh@contoso.com", "Client Services"),
    Reporter("Kevin O'Brien", "kevin.obrien@contoso.com", "Trading"),
    Reporter("Aisha Patel", "aisha.patel@contoso.com", "Risk & Compliance"),
    Reporter("Jorge Mendoza", "jorge.mendoza@contoso.com", "Finance"),
    Reporter("Yuki Tanaka", "yuki.tanaka@contoso.com", "Research & Analytics"),
    Reporter("Fatima Al-Hassan", "fatima.alhassan@contoso.com", "Operations"),
    Reporter("Brian Murphy", "brian.murphy@contoso.com", "Infrastructure"),
    Reporter("Lena Johansson", "lena.johansson@contoso.com", "Marketing"),
    Reporter("Raj Mehta", "raj.mehta@contoso.com", "IT Support"),
    Reporter("Grace Nwosu", "grace.nwosu@contoso.com", "Human Resources"),
    Reporter("Chris Park", "chris.park@contoso.com", "Product Management"),
    Reporter("Olga Petrov", "olga.petrov@contoso.com", "Accounting"),
    Reporter("Samuel Osei", "samuel.osei@contoso.com", "Data Science"),
    Reporter("Lisa Bergmann", "lisa.bergmann@contoso.com", "Legal"),
    Reporter("Ahmed El-Sayed", "ahmed.elsayed@contoso.com", "Security"),
    Reporter("Jessica Liu", "jessica.liu@contoso.com", "Quantitative Research"),
    Reporter("Patrick Dunn", "patrick.dunn@contoso.com", "Commercial Banking"),
    Reporter("Maria Santos", "maria.santos@contoso.com", "Private Banking"),
    Reporter("Wei Zhang", "wei.zhang@contoso.com", "Engineering"),
    Reporter("Natasha Volkov", "natasha.volkov@contoso.com", "Treasury"),
    Reporter("Tyler Brooks", "tyler.brooks@contoso.com", "Business Development"),
    Reporter("Ingrid Nilsson", "ingrid.nilsson@contoso.com", "Internal Audit"),
    Reporter("Hassan Diallo", "hassan.diallo@contoso.com", "Regulatory Affairs"),
    Reporter("Emily Watson", "emily.watson@contoso.com", "Client Services"),
    Reporter("Daniel Kim", "daniel.kim@contoso.com", "Facilities"),
    Reporter("Sofia Reyes", "sofia.reyes@contoso.com", "Procurement"),
    Reporter("Nathan Greene", "nathan.greene@contoso.com", "Investor Relations"),
    Reporter("Olivia Thompson", "olivia.thompson@contoso.com", "Marketing"),
    Reporter("Ryan Mitchell", "ryan.mitchell@contoso.com", "Infrastructure"),
    Reporter("Ava Nguyen", "ava.nguyen@contoso.com", "Research & Analytics"),
    Reporter("Carlos Gutierrez", "carlos.gutierrez@contoso.com", "Operations"),
    Reporter("Hannah Lee", "hannah.lee@contoso.com", "Finance"),
    Reporter("Jack Robinson", "jack.robinson@contoso.com", "Engineering"),
    Reporter("Mei Lin", "mei.lin@contoso.com", "Data Science"),
    Reporter("Oscar Fernandez", "oscar.fernandez@contoso.com", "Trading"),
    Reporter("Anna Kowalski", "anna.kowalski@contoso.com", "Risk & Compliance"),
    Reporter("James Wright", "james.wright@contoso.com", "Wealth Management"),
    Reporter("Zara Ahmad", "zara.ahmad@contoso.com", "Product Management"),
    Reporter("Derek Johnson", "derek.johnson@contoso.com", "IT Support"),
    Reporter("Isabelle Martin", "isabelle.martin@contoso.com", "Human Resources"),
    Reporter("Leo Chang", "leo.chang@contoso.com", "Accounting"),
    Reporter("Nina Popov", "nina.popov@contoso.com", "Legal"),
    Reporter("Alex Rivera", "alex.rivera@contoso.com", "Security"),
    Reporter("Rachel Green", "rachel.green@contoso.com", "Client Services"),
    Reporter("Simon Park", "simon.park@contoso.com", "Commercial Banking"),
    Reporter("Tanya Ivanova", "tanya.ivanova@contoso.com", "Private Banking"),
    Reporter("Usama Malik", "usama.malik@contoso.com", "Engineering"),
    Reporter("Valerie Dubois", "valerie.dubois@contoso.com", "Corporate Strategy"),
    Reporter("William Chen", "william.chen@contoso.com", "Infrastructure"),
    Reporter("Xena Torres", "xena.torres@contoso.com", "Operations"),
    Reporter("Yusuf Osman", "yusuf.osman@contoso.com", "Trading"),
    Reporter("Zoe Campbell", "zoe.campbell@contoso.com", "Finance"),
    Reporter("Adam Novak", "adam.novak@contoso.com", "Research & Analytics"),
    Reporter("Bianca Russo", "bianca.russo@contoso.com", "Marketing"),
    Reporter("Charles Wang", "charles.wang@contoso.com", "Quantitative Research"),
    Reporter("Daniela Silva", "daniela.silva@contoso.com", "Treasury"),
    Reporter("Ethan Brown", "ethan.brown@contoso.com", "Regulatory Affairs"),
    Reporter("Fiona O'Connell", "fiona.oconnell@contoso.com", "Internal Audit"),
    Reporter("George Nakamura", "george.nakamura@contoso.com", "Data Science"),
    Reporter("Holly Andrews", "holly.andrews@contoso.com", "Facilities"),
    Reporter("Ivan Kravchenko", "ivan.kravchenko@contoso.com", "Procurement"),
    Reporter("Julia Hoffman", "julia.hoffman@contoso.com", "Business Development"),
    Reporter("Khalid Basri", "khalid.basri@contoso.com", "Investor Relations"),
    Reporter("Laura Mendez", "laura.mendez@contoso.com", "Wealth Management"),
    Reporter("Mohammed Ali", "mohammed.ali@contoso.com", "Asset Management"),
    Reporter("Nadia Cheung", "nadia.cheung@contoso.com", "Client Services"),
    Reporter("Owen Phillips", "owen.phillips@contoso.com", "Engineering"),
    Reporter("Penelope Gray", "penelope.gray@contoso.com", "Human Resources"),
]

VIP_REPORTERS = [r for r in REPORTERS if r.is_vip]
REGULAR_REPORTERS = [r for r in REPORTERS if not r.is_vip]
