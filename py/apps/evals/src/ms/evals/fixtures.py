# Copyright (c) Microsoft. All rights reserved.
"""Fixture data for realistic ticket generation.

Provides pools of names, departments, email patterns, systems, error messages,
and other parameterizable elements used to populate scenario templates.
"""

import random

# Diverse set of reporter names covering various cultural backgrounds
FIRST_NAMES = [
    "Sarah", "Marcus", "Diana", "Jordan", "Priya", "Thomas", "Raj", "Elena",
    "Wei", "Alex", "Fatima", "James", "Yuki", "Aisha", "Carlos", "Nina",
    "David", "Mei", "Oliver", "Zara", "Hassan", "Sophie", "Ravi", "Emma",
    "Takeshi", "Grace", "Mohamed", "Laura", "Andrei", "Kim", "Deepika",
    "Michael", "Chiara", "Luis", "Nadia", "Sanjay", "Hannah", "Kofi",
    "Maria", "Derek", "Anya", "Bryan", "Chloe", "Dimitri", "Fiona",
    "George", "Helen", "Ivan", "Julia", "Kevin", "Lena", "Nathan",
    "Olivia", "Patrick", "Quinn", "Rita", "Sam", "Tina", "Uma",
    "Vincent", "Wendy", "Xavier", "Yara", "Zachary", "Aaliya", "Boris",
    "Camilla", "Dante", "Esther", "Felix", "Greta", "Hugo", "Ingrid",
    "Jake", "Kiran", "Lucia", "Martin", "Naomi", "Oscar", "Paula",
    "Rafael", "Simone", "Tony", "Ursula", "Victor", "Wanda", "Xiomara",
    "Yusuf", "Zoe", "Adam", "Bianca", "Cyrus", "Dina", "Erik",
    "Francisca", "Gordon", "Hana", "Igor", "Jasmine", "Kyle", "Linh",
    "Max", "Noelle", "Omar", "Petra", "Rami", "Selena", "Troy",
    "Ulrike", "Vera", "Warren", "Ximena", "Yasmine", "Zach", "Amara",
    "Brendan", "Catalina", "Donovan", "Eva", "Finn", "Gloria",
    "Henrik", "Isabelle", "Jensen", "Karla", "Leo", "Miriam",
    "Nikolai", "Ophelia", "Paulo", "Rosie", "Stefan", "Tamara",
]

LAST_NAMES = [
    "Chen", "Rodriguez", "Marsh", "Lee", "Kapoor", "Wright", "Patel",
    "Volkov", "Zhang", "Kim", "Al-Rashid", "O'Brien", "Tanaka", "Hassan",
    "Santos", "Novak", "Fischer", "Wang", "Thompson", "Begum", "Muller",
    "Johansson", "Nakamura", "Okafor", "Anderson", "Petrov", "Morales",
    "Kumar", "Larsen", "Yamamoto", "Ibrahim", "Garcia", "Williams",
    "Brown", "Taylor", "Wilson", "Johnson", "White", "Martin", "Clark",
    "Moore", "Hall", "Allen", "Young", "King", "Hill", "Baker",
    "Green", "Adams", "Nelson", "Carter", "Mitchell", "Roberts",
    "Turner", "Phillips", "Campbell", "Parker", "Evans", "Edwards",
    "Collins", "Stewart", "Morris", "Murphy", "Rivera", "Cook",
    "Rogers", "Morgan", "Peterson", "Cooper", "Reed", "Bailey",
    "Bell", "Howard", "Ward", "Torres", "Sanders", "Price",
    "Bennett", "Wood", "Barnes", "Ross", "Henderson", "Coleman",
    "Jenkins", "Perry", "Powell", "Sullivan", "Russell", "Gray",
    "Watson", "Brooks", "Kelly", "Ramirez", "Gonzalez", "Hernandez",
    "Diaz", "Reyes", "Cruz", "Flores", "Singh", "Sharma", "Gupta",
    "Chopra", "Reddy", "Rao", "Nair", "Bhat", "Mehta", "Shah",
    "Liu", "Sun", "Huang", "Lin", "Yang", "Wu", "Zhou", "Xu",
    "Cheng", "Ma", "Park", "Choi", "Kang", "Yoon", "Jeon",
    "Sato", "Suzuki", "Watanabe", "Ito", "Kobayashi", "Takahashi",
]

DEPARTMENTS = [
    "Wealth Management", "Institutional Trading", "Retail Banking",
    "Compliance", "Legal", "HR", "IT", "Finance", "Engineering",
    "Data Engineering", "Data Science", "Marketing", "Operations",
    "Executive Operations", "Risk Management", "Treasury",
    "Client Services", "Product Management", "Research",
    "Internal Audit", "Facilities", "Procurement",
    "Backend Engineering", "Frontend Engineering", "Cloud Infrastructure",
    "DevOps", "Security Engineering", "Business Intelligence",
    "Corporate Strategy", "Investor Relations",
]

# NYC, London, Singapore offices
OFFICE_LOCATIONS = [
    "NYC office, Floor 2", "NYC office, Floor 3", "NYC office, Floor 4",
    "NYC office, Floor 5", "NYC office, Floor 6",
    "London office, Floor 1", "London office, Floor 2", "London office, Floor 3",
    "Singapore office, Floor 1", "Singapore office, Floor 2",
    "Remote — home office", "Remote — coworking space", "Remote — traveling",
]

SYSTEMS_AND_APPS = [
    "SAP ERP", "Salesforce CRM", "Bloomberg Terminal", "Microsoft Teams",
    "Outlook", "OneDrive", "SharePoint", "Azure DevOps", "ServiceNow",
    "Jira", "Confluence", "Power BI", "Azure Data Factory",
    "SQL Server", "PostgreSQL", "Cosmos DB", "Azure Blob Storage",
    "Intune", "Entra ID", "Defender for Endpoint", "GlobalProtect VPN",
    "Cisco AnyConnect", "Zscaler", "Citrix Workspace", "VMware Horizon",
    "Adobe Acrobat", "DocuSign", "Workday", "Concur", "Slack",
    "Zoom", "WebEx", "CrowdStrike", "Splunk", "Datadog",
    "GitHub Enterprise", "Terraform", "Kubernetes", "Docker",
    "Excel", "Word", "PowerPoint", "OneNote", "Visio",
    "AutoCAD", "Tableau", "Snowflake", "Databricks",
    "Azure SQL Database", "Azure Key Vault", "Azure Functions",
    "Logic Apps", "API Management", "Azure Monitor",
]

ERROR_MESSAGES = [
    "Error 403: Access Denied",
    "Connection timed out after 30 seconds",
    "AADSTS50076: MFA required but not completed",
    "SSL_ERROR_HANDSHAKE_FAILURE_ALERT",
    "SQLSTATE[HY000] [2002] Connection refused",
    "HTTP 500: Internal Server Error",
    "ERROR: permission denied for table client_data",
    "The RPC server is unavailable",
    "Your account has been locked due to multiple failed sign-in attempts",
    "Certificate expired: CN=client-api.contoso.com",
    "NTLM authentication failed for user CONTOSO\\\\{name}",
    "Kerberos pre-authentication failed",
    "Token refresh failed: invalid_grant",
    "Error 0x80070005: Access is denied",
    "DNS resolution failed for internal.contoso.com",
    "VPN tunnel establishment failed: peer not responding",
    "Application crash: APPCRASH in msedge.exe",
    "Blue screen: DRIVER_IRQL_NOT_LESS_OR_EQUAL",
    "Disk I/O error: sector read failure",
    "Out of memory: Java heap space",
    "Service principal authentication failed: client secret expired",
    "RBAC role assignment not found for subscription",
    "Pipeline failed: ADF_PIPELINE_RUN_FAILED",
    "Sync conflict detected: 3 files could not be synced",
]

ATTACHMENT_NAMES = [
    "screenshot.png", "error_log.txt", "crash_dump.dmp",
    "network_trace.pcap", "config_export.xml", "audit_report.pdf",
    "email_headers.txt", "system_info.txt", "event_log.evtx",
    "performance_report.html", "login_alert_screenshot.png",
    "adf_error_log.txt", "browser_console.log", "vpn_diagnostics.zip",
    "teams_log.txt", "intune_report.csv", "defender_alert.json",
    "azure_activity_log.json", "sql_query_plan.xml",
    "sharepoint_error.png", "outlook_trace.etl", "device_report.pdf",
    "compliance_scan.pdf", "vulnerability_report.csv",
    "patch_list.xlsx", "firmware_version.txt", "wireshark_capture.pcapng",
    "memory_dump.hdmp", "app_trace.nettrace",
]


def generate_reporter(rng: random.Random) -> tuple[str, str, str]:
    """Generate a random reporter with name, email, and department.

    Returns:
        Tuple of (full_name, email, department).
    """
    first = rng.choice(FIRST_NAMES)
    last = rng.choice(LAST_NAMES)
    name = f"{first} {last}"
    email = f"{first.lower()}.{last.lower()}@contoso.com"
    department = rng.choice(DEPARTMENTS)
    return name, email, department


def pick_attachments(rng: random.Random, max_count: int = 3) -> list[str]:
    """Select random attachment filenames.

    Args:
        rng: Random number generator.
        max_count: Maximum number of attachments to include.

    Returns:
        List of attachment filenames (may be empty).
    """
    if rng.random() < 0.6:
        return []
    count = rng.randint(1, max_count)
    return rng.sample(ATTACHMENT_NAMES, min(count, len(ATTACHMENT_NAMES)))
