# Copyright (c) Microsoft. All rights reserved.
"""Pool of reporter profiles for ticket generation."""

# ── Name pools ────────────────────────────────────────────────────────────────

FIRST_NAMES = [
    "Sarah", "Marcus", "Priya", "James", "Lisa", "Carlos", "Yuki", "David",
    "Fatima", "Ryan", "Angela", "Wei", "Mohammed", "Jennifer", "Patrick",
    "Svetlana", "Tomás", "Aisha", "Daniel", "Mei", "Roberto", "Hannah",
    "Kwame", "Elena", "Nathan", "Sunita", "Gregory", "Zara", "Brandon",
    "Olivia", "Ahmed", "Sophia", "Derek", "Amara", "Kevin", "Isabella",
    "Jamal", "Chloe", "Raj", "Maya", "Liam", "Nadia", "Oscar", "Freya",
    "Victor", "Leila", "Simon", "Aaliyah", "Thomas", "Ingrid", "Alex",
    "Kira", "Martin", "Jing", "Trevor", "Amelia", "Hassan", "Bianca",
    "Franklin", "Camille", "Arjun", "Dorothy", "Ethan", "Nina", "Sergei",
    "Paula", "Jerome", "Mika", "Conrad", "Tanya", "Felix", "Vera",
    "Diego", "Helen", "Ravi", "Stella", "Keith", "Yara", "Bruce",
    "Natasha", "Gene", "Rosa", "Adrian", "Greta", "Hugh", "Ines",
    "Lloyd", "Tamara", "Philip", "Uma", "Scott", "Wendy", "Ivan",
    "Xiomara", "Ralph", "Dina", "Warren", "Celeste", "Owen", "Lily",
]

LAST_NAMES = [
    "Chen", "Rodriguez", "Patel", "Johnson", "Kim", "Martinez", "Tanaka",
    "Williams", "Hassan", "Foster", "Müller", "Zhang", "Al-Rashid", "Thompson",
    "O'Brien", "Petrov", "García", "Okafor", "Lewis", "Nakamura", "Santos",
    "Wright", "Adeyemi", "Volkov", "Cooper", "Sharma", "Blackwell", "Farsi",
    "Henderson", "Liu", "Morales", "Fischer", "Kovacs", "Park", "Bennett",
    "Ibrahim", "Dixon", "Johansson", "Torres", "Campbell", "Nguyen", "Grant",
    "Da Silva", "Morton", "Kuznetsov", "Reeves", "Gupta", "Lindberg", "Wells",
    "Osei", "Vasquez", "Hoffman", "Mitchell", "Sato", "Crawford", "Malik",
    "Barnes", "Fernandez", "Stone", "Chandra", "Walsh", "Yamamoto", "Holt",
    "Almeida", "Fletcher", "Svensson", "Herrera", "Prasad", "Caldwell", "Li",
    "Abbott", "Ramirez", "Durham", "Singh", "Brandt", "Quinn", "Nair",
    "Dalton", "Romero", "Pierce", "Mehta", "Cross", "Wagner", "James",
    "Ortiz", "Douglas", "Akhtar", "Shaw", "Tran", "Holland", "Bakshi",
    "Price", "Novak", "Fields", "Desai", "Chambers", "Berg", "Logan", "Ray",
]

# ── Department pools ──────────────────────────────────────────────────────────

DEPARTMENTS = [
    "Engineering", "Wealth Management", "Trading", "Compliance", "HR",
    "IT", "Finance", "Legal", "Operations", "Investor Relations",
    "Risk Management", "Marketing", "Executive Office", "Research",
    "Client Services", "Internal Audit", "Treasury", "Retail Banking",
    "Corporate Banking", "Insurance", "Asset Management",
]

# ── VIP departments (C-suite, SVP+) ──────────────────────────────────────────

VIP_DEPARTMENTS = frozenset({"Executive Office"})

# ── Attachment pools by category context ──────────────────────────────────────

COMMON_ATTACHMENTS: dict[str, list[list[str]]] = {
    "screenshot": [
        ["screenshot.png"],
        ["error_screenshot.png"],
        ["screen_capture.jpg"],
        ["issue_screenshot.png"],
    ],
    "log_file": [
        ["debug.log"],
        ["error_log.txt"],
        ["system_log.txt"],
        ["application.log"],
    ],
    "document": [
        ["details.docx"],
        ["notes.txt"],
        ["request_form.pdf"],
        ["approval.pdf"],
    ],
    "email": [
        ["forwarded_email.eml"],
        ["original_message.msg"],
        ["email_thread.eml"],
    ],
    "config": [
        ["config.xml"],
        ["settings.json"],
        ["network_config.txt"],
    ],
    "none": [[]],
}
