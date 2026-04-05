"""Domain constants for the Contoso IT support triage system."""

from enum import StrEnum


class Category(StrEnum):
    """Ticket categories matching the output schema."""

    ACCESS_AUTH = "Access & Authentication"
    HARDWARE = "Hardware & Peripherals"
    NETWORK = "Network & Connectivity"
    SOFTWARE = "Software & Applications"
    SECURITY = "Security & Compliance"
    DATA_STORAGE = "Data & Storage"
    GENERAL_INQUIRY = "General Inquiry"
    NOT_SUPPORT = "Not a Support Ticket"


class Priority(StrEnum):
    """Priority levels matching the output schema."""

    P1 = "P1"
    P2 = "P2"
    P3 = "P3"
    P4 = "P4"


class Team(StrEnum):
    """Specialist teams matching the output schema."""

    IAM = "Identity & Access Management"
    ENDPOINT = "Endpoint Engineering"
    NETWORK_OPS = "Network Operations"
    ENTERPRISE_APPS = "Enterprise Applications"
    SECURITY_OPS = "Security Operations"
    DATA_PLATFORM = "Data Platform"
    NONE = "None"


class Channel(StrEnum):
    """Ticket submission channels."""

    EMAIL = "email"
    CHAT = "chat"
    PORTAL = "portal"
    PHONE = "phone"


class MissingInfo(StrEnum):
    """Constrained vocabulary for missing information fields."""

    AFFECTED_SYSTEM = "affected_system"
    ERROR_MESSAGE = "error_message"
    STEPS_TO_REPRODUCE = "steps_to_reproduce"
    AFFECTED_USERS = "affected_users"
    ENVIRONMENT_DETAILS = "environment_details"
    TIMESTAMP = "timestamp"
    PREVIOUS_TICKET_ID = "previous_ticket_id"
    CONTACT_INFO = "contact_info"
    DEVICE_INFO = "device_info"
    APPLICATION_VERSION = "application_version"
    NETWORK_LOCATION = "network_location"
    BUSINESS_IMPACT = "business_impact"
    REPRODUCTION_FREQUENCY = "reproduction_frequency"
    SCREENSHOT_OR_ATTACHMENT = "screenshot_or_attachment"
    AUTHENTICATION_METHOD = "authentication_method"
    CONFIGURATION_DETAILS = "configuration_details"


DEPARTMENTS: list[str] = [
    "Engineering",
    "Wealth Management",
    "Trading",
    "Compliance",
    "Legal",
    "Finance",
    "HR",
    "Marketing",
    "Operations",
    "Retail Banking",
    "Institutional Trading",
    "Data Engineering",
    "Data Science",
    "Cloud Infrastructure",
    "Executive Operations",
    "Backend Engineering",
    "Frontend Engineering",
    "Product Management",
    "Risk Management",
    "Internal Audit",
    "Investor Relations",
    "Client Services",
    "Consulting",
    "Research",
    "Quantitative Analysis",
    "Portfolio Management",
    "Treasury",
    "Corporate Strategy",
    "Business Development",
    "Facilities",
    "Procurement",
    "IT Security",
    "DevOps",
    "Quality Assurance",
    "Customer Success",
    "Private Banking",
    "Asset Management",
    "Fixed Income",
    "Equity Trading",
    "Derivatives",
    "Settlements",
    "Middle Office",
    "Fund Administration",
    "Regulatory Affairs",
    "Tax",
    "Payroll",
    "Learning & Development",
    "Corporate Communications",
    "Public Relations",
    "ESG & Sustainability",
]

OFFICES: list[str] = ["New York", "London", "Singapore"]

BUILDINGS: list[str] = [
    "Building 1",
    "Building 2",
    "Building 3",
    "Building 4",
    "Building 5",
    "Building 6",
    "Building 7",
    "Building 8",
]

FLOORS: list[str] = [
    "1st floor",
    "2nd floor",
    "3rd floor",
    "4th floor",
    "5th floor",
    "6th floor",
    "7th floor",
    "8th floor",
    "9th floor",
    "10th floor",
]

# Alias for test compatibility — same enum, different name.
MissingInfoField = MissingInfo
