import re

SQL_TERMS = {
    "student",
    "students",
    "course",
    "courses",
    "doctor",
    "doctors",
    "department",
    "departments",
    "grade",
    "grades",
    "exam",
    "exams",
    "faculty",
    "university",
    "enrollment",
    "semester",
    "database",
    "sql"
}

DOCUMENT_TERMS = {
    "pdf",
    "document",
    "manual",
    "rules",
    "guide"
}


def route_question(question: str):
    words = set(re.findall(r"\w+", question.lower()))

    has_sql = bool(words & SQL_TERMS)
    has_docs = bool(words & DOCUMENT_TERMS)

    if has_sql and has_docs:
        return "hybrid"

    if has_sql:
        return "sql"

    return "document"