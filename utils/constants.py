"""
Constants used throughout the Recruitment CRM application.
"""

# User Roles
ROLE_ADMIN = "admin"
ROLE_RECRUITER = "recruiter"
ROLE_VIEWER = "viewer"

ROLES = [ROLE_ADMIN, ROLE_RECRUITER, ROLE_VIEWER]

# Candidate Status Options
STATUS_APPLIED = "Applied"
STATUS_SCREENING = "Screening"
STATUS_INTERVIEW = "Interview"
STATUS_OFFER = "Offer"
STATUS_HIRED = "Hired"
STATUS_REJECTED = "Rejected"

CANDIDATE_STATUSES = [
    STATUS_APPLIED,
    STATUS_SCREENING,
    STATUS_INTERVIEW,
    STATUS_OFFER,
    STATUS_HIRED,
    STATUS_REJECTED
]

# Call Types
CALL_TYPE_PHONE = "Phone"
CALL_TYPE_VIDEO = "Video"
CALL_TYPE_IN_PERSON = "In-Person"
CALL_TYPE_EMAIL = "Email"

CALL_TYPES = [
    CALL_TYPE_PHONE,
    CALL_TYPE_VIDEO,
    CALL_TYPE_IN_PERSON,
    CALL_TYPE_EMAIL
]

# Call Outcomes
OUTCOME_INTERESTED = "Interested"
OUTCOME_NOT_INTERESTED = "Not Interested"
OUTCOME_FOLLOW_UP_REQUIRED = "Follow-up Required"
OUTCOME_NO_RESPONSE = "No Response"
OUTCOME_SCHEDULED_INTERVIEW = "Scheduled Interview"
OUTCOME_OFFER_ACCEPTED = "Offer Accepted"
OUTCOME_OFFER_DECLINED = "Offer Declined"

CALL_OUTCOMES = [
    OUTCOME_INTERESTED,
    OUTCOME_NOT_INTERESTED,
    OUTCOME_FOLLOW_UP_REQUIRED,
    OUTCOME_NO_RESPONSE,
    OUTCOME_SCHEDULED_INTERVIEW,
    OUTCOME_OFFER_ACCEPTED,
    OUTCOME_OFFER_DECLINED
]

# Candidate Sources
SOURCE_LINKEDIN = "LinkedIn"
SOURCE_REFERRAL = "Referral"
SOURCE_JOB_BOARD = "Job Board"
SOURCE_COMPANY_WEBSITE = "Company Website"
SOURCE_RECRUITMENT_AGENCY = "Recruitment Agency"
SOURCE_DIRECT_APPLICATION = "Direct Application"
SOURCE_OTHER = "Other"

CANDIDATE_SOURCES = [
    SOURCE_LINKEDIN,
    SOURCE_REFERRAL,
    SOURCE_JOB_BOARD,
    SOURCE_COMPANY_WEBSITE,
    SOURCE_RECRUITMENT_AGENCY,
    SOURCE_DIRECT_APPLICATION,
    SOURCE_OTHER
]

# Activity Log Action Types
ACTION_CREATE = "CREATE"
ACTION_UPDATE = "UPDATE"
ACTION_DELETE = "DELETE"
ACTION_EXPORT = "EXPORT"
ACTION_LOGIN = "LOGIN"
ACTION_LOGOUT = "LOGOUT"

# Experience Ranges (in years)
EXPERIENCE_RANGES = [
    "0-1 years",
    "1-3 years",
    "3-5 years",
    "5-7 years",
    "7-10 years",
    "10+ years"
]

# Notice Period Options
NOTICE_PERIODS = [
    "Immediate",
    "15 days",
    "30 days",
    "60 days",
    "90 days",
    "Serving notice"
]

# Common Job Positions (can be customized)
COMMON_POSITIONS = [
    "Software Engineer",
    "Senior Software Engineer",
    "Frontend Developer",
    "Backend Developer",
    "Full Stack Developer",
    "DevOps Engineer",
    "Data Scientist",
    "Data Analyst",
    "Product Manager",
    "Project Manager",
    "UI/UX Designer",
    "QA Engineer",
    "Business Analyst",
    "System Administrator",
    "Other"
]

# Education Levels
EDUCATION_LEVELS = [
    "High School",
    "Associate Degree",
    "Bachelor's Degree",
    "Master's Degree",
    "PhD",
    "Certification",
    "Other"
]
