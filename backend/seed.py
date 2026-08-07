"""Seed script for generating realistic GraphHire AI graph data."""

from __future__ import annotations

import logging
import os
import random
import re
import sys
from datetime import datetime, timedelta
from typing import Any

from faker import Faker
from flask import Flask

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from backend.config import Config
from backend.database import db

logger = logging.getLogger(__name__)


def _init_db() -> None:
    """Initialize the database connection using the Flask app config."""
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)


def _create_constraints(session: Any) -> None:
    """Create uniqueness constraints for the graph seed data."""
    statements = [
        "CREATE CONSTRAINT developer_email_unique IF NOT EXISTS FOR (d:Developer) REQUIRE d.email IS UNIQUE",
        "CREATE CONSTRAINT company_name_unique IF NOT EXISTS FOR (c:Company) REQUIRE c.name IS UNIQUE",
        "CREATE CONSTRAINT project_name_unique IF NOT EXISTS FOR (p:Project) REQUIRE p.name IS UNIQUE",
        "CREATE CONSTRAINT skill_name_unique IF NOT EXISTS FOR (s:Skill) REQUIRE s.name IS UNIQUE",
        "CREATE CONSTRAINT technology_name_unique IF NOT EXISTS FOR (t:Technology) REQUIRE t.name IS UNIQUE",
        "CREATE CONSTRAINT certification_name_unique IF NOT EXISTS FOR (c:Certification) REQUIRE c.name IS UNIQUE",
        "CREATE CONSTRAINT location_city_country_unique IF NOT EXISTS FOR (l:Location) REQUIRE (l.city, l.country) IS UNIQUE",
    ]

    for statement in statements:
        session.run(statement)


def _batch_upsert(session: Any, query: str, rows: list[dict[str, Any]], batch_size: int = 50) -> None:
    """Insert a list of row dictionaries in batches using parameterized Cypher."""
    for start in range(0, len(rows), batch_size):
        batch = rows[start : start + batch_size]
        session.run(query, {"rows": batch})


def _slugify(value: str) -> str:
    """Convert a string into a GitHub/LinkedIn friendly slug."""
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "developer"


def _build_seed_data(faker: Faker | None = None) -> dict[str, list[dict[str, Any]]]:
    """Generate a compact, well-connected Indian-only graph for the application."""
    if faker is None:
        faker = Faker("en_US")

    rng = random.Random(42)

    skill_names = [
        "Python",
        "JavaScript",
        "TypeScript",
        "React",
        "Node.js",
        "GraphQL",
        "Neo4j",
        "Django",
        "Flask",
        "FastAPI",
        "Kubernetes",
        "Docker",
        "AWS",
        "Azure",
        "GCP",
        "Machine Learning",
        "Data Engineering",
        "Microservices",
        "Cybersecurity",
        "DevOps",
        "Product Design",
        "UI/UX",
        "System Design",
        "Go",
        "Java",
        "C#",
        "Rust",
        "Elixir",
        "Scala",
        "PostgreSQL",
        "Redis",
        "Apache Kafka",
        "TensorFlow",
        "PyTorch",
        "OpenAI",
        "LangChain",
        "Prompt Engineering",
        "ETL",
        "Data Visualization",
        "CI/CD",
        "Observability",
        "Cloud Native",
        "Serverless",
        "Test Automation",
        "Security Auditing",
        "API Design",
        "Frontend Architecture",
        "Backend Architecture",
        "Mobile Development",
        "React Native",
        "Swift",
        "Kotlin",
        "Flutter",
    ]
    skills = [
        {"name": name, "category": rng.choice(["Programming", "Data", "Cloud", "Product", "Operations", "Security", "Design"])}
        for name in skill_names[:50]
    ]

    technologies = [
        {"name": name, "type": tech_type}
        for name, tech_type in [
            ("Python", "Language"),
            ("JavaScript", "Language"),
            ("TypeScript", "Language"),
            ("React", "Framework"),
            ("Node.js", "Runtime"),
            ("Neo4j", "Database"),
            ("PostgreSQL", "Database"),
            ("Docker", "Tool"),
            ("Kubernetes", "Platform"),
            ("AWS", "Cloud"),
            ("Azure", "Cloud"),
            ("GCP", "Cloud"),
            ("Kafka", "Messaging"),
            ("Redis", "Database"),
            ("TensorFlow", "Library"),
            ("PyTorch", "Library"),
            ("LangChain", "Library"),
            ("OpenAI API", "API"),
            ("GraphQL", "API"),
            ("FastAPI", "Framework"),
            ("Django", "Framework"),
            ("Flask", "Framework"),
        ]
    ][:20]

    certifications = [
        {"name": name, "provider": provider}
        for name, provider in [
            ("AWS Certified Solutions Architect", "Amazon Web Services"),
            ("Google Cloud Professional Engineer", "Google Cloud"),
            ("Azure Fundamentals", "Microsoft"),
            ("Certified Kubernetes Administrator", "Cloud Native Computing Foundation"),
            ("Certified Scrum Master", "Scrum Alliance"),
            ("Project Management Professional", "Project Management Institute"),
            ("Oracle Certified Java Programmer", "Oracle"),
            ("Certified Information Systems Security Professional", "(ISC)²"),
            ("AWS Certified Machine Learning", "Amazon Web Services"),
            ("Neo4j Certified Professional", "Neo4j"),
            ("Databricks Certified Data Engineer", "Databricks"),
            ("HashiCorp Certified Terraform Associate", "HashiCorp"),
        ]
    ]

    indian_cities = [
        "Bengaluru",
        "Hyderabad",
        "Pune",
        "Mumbai",
        "Delhi",
        "Chennai",
        "Kolkata",
        "Ahmedabad",
        "Noida",
        "Gurugram",
    ]

    locations = [{"city": city, "country": "India"} for city in indian_cities]

    companies = [
        {
            "name": name,
            "industry": "Technology",
            "founded_year": 1990 + index,
            "headquarters": indian_cities[index % len(indian_cities)],
            "website": f"https://www.{_slugify(name)}.com",
        }
        for index, name in enumerate([
            "Infosys",
            "TCS",
            "Wipro",
            "Tech Mahindra",
            "HCLTech",
            "Zoho",
            "Freshworks",
            "Razorpay",
            "PhonePe",
            "Flipkart",
            "CRED",
            "Swiggy",
            "Zomato",
            "Paytm",
        ])
    ]

    developer_profiles = [
        ("Apeksha Vishwasrao", "Bengaluru", "Infosys", 8),
        ("Aarav Mehta", "Hyderabad", "TCS", 6),
        ("Ananya Gupta", "Pune", "Wipro", 7),
        ("Aditya Joshi", "Mumbai", "Tech Mahindra", 9),
        ("Priya Patil", "Delhi", "HCLTech", 5),
        ("Rahul Sharma", "Chennai", "Zoho", 10),
        ("Sneha Kulkarni", "Kolkata", "Freshworks", 7),
        ("Rohan Deshmukh", "Ahmedabad", "Razorpay", 8),
        ("Isha Nair", "Noida", "PhonePe", 6),
        ("Arjun Reddy", "Gurugram", "Flipkart", 9),
        ("Riya Shah", "Bengaluru", "CRED", 5),
        ("Kunal Verma", "Hyderabad", "Swiggy", 7),
        ("Neha Singh", "Pune", "Zomato", 8),
        ("Amit Singh", "Mumbai", "Paytm", 11),
        ("Kavya Iyer", "Delhi", "Infosys", 6),
        ("Siddharth Joshi", "Chennai", "TCS", 10),
        ("Anjali Joshi", "Kolkata", "Wipro", 7),
        ("Aman Agarwal", "Ahmedabad", "Tech Mahindra", 5),
        ("Sanjay Malhotra", "Noida", "HCLTech", 12),
        ("Shreya Gupta", "Gurugram", "Zoho", 8),
    ]

    def _build_bio(name: str, current_company: str, years: int, skill_names_for_profile: list[str], city: str) -> str:
        skill_list = ", ".join(skill_names_for_profile[:3])
        return (
            f"{name} is a {years}-year software engineer based in {city}, India. "
            f"At {current_company}, they build reliable products using {skill_list} and cloud-native engineering practices. "
            "They enjoy mentoring peers, simplifying distributed systems, and delivering quality software at scale."
        )

    developers = []
    for index, (full_name, city, company_name, years_experience) in enumerate(developer_profiles):
        developer_skills = rng.sample([skill["name"] for skill in skills], k=6)
        slug = _slugify(full_name)
        developers.append(
            {
                "full_name": full_name,
                "email": f"{slug}@{_slugify(company_name)}.com",
                "profile_image_url": f"https://i.pravatar.cc/300?img={(index % 70) + 1}",
                "github_url": f"https://github.com/{slug}",
                "linkedin_url": f"https://www.linkedin.com/in/{slug}",
                "bio": _build_bio(full_name, company_name, years_experience, developer_skills, city),
                "years_of_experience": years_experience,
                "current_company": company_name,
                "country": "India",
                "city": city,
                "skills": developer_skills,
            }
        )

    projects = []
    statuses = ["Planning", "In Progress", "Completed", "On Hold"]
    project_prefixes = ["Analytics", "Payments", "Customer", "Collaboration", "Marketplace", "Insights", "Compliance", "Platform"]
    project_suffixes = ["Hub", "Suite", "Engine", "Portal", "Studio", "Network", "Platform", "Dashboard"]

    for index in range(24):
        start_date = faker.date_between(start_date="-5y", end_date="-1y")
        end_date = start_date + timedelta(days=rng.randint(120, 900))
        tech_stack = rng.sample([technology["name"] for technology in technologies], k=4)
        project_name = f"{project_prefixes[index % len(project_prefixes)]} {project_suffixes[index % len(project_suffixes)]} {index + 1}"
        projects.append(
            {
                "name": project_name,
                "description": (
                    f"A {rng.choice(['data-driven', 'high-performance', 'customer-focused', 'enterprise-grade'])} solution built to improve business outcomes "
                    f"using {', '.join(tech_stack[:-1])}, and {tech_stack[-1]}."
                ),
                "status": rng.choice(statuses),
                "github_repository": f"https://github.com/{_slugify(project_name)}/{_slugify(project_prefixes[index % len(project_prefixes)])}",
                "start_date": start_date.strftime("%Y-%m-%d"),
                "end_date": end_date.strftime("%Y-%m-%d"),
                "technology_stack": tech_stack,
            }
        )

    return {
        "developers": developers,
        "companies": companies,
        "projects": projects,
        "skills": skills,
        "technologies": technologies,
        "certifications": certifications,
        "locations": locations,
    }


def clear_database() -> None:
    """Clear all graph data for a development-only seed reset."""
    if db.get_driver() is None:
        _init_db()

    try:
        with db.get_driver().session() as session:
            session.run("MATCH (n) DETACH DELETE n")
    except Exception as exc:  # pragma: no cover - defensive fallback for missing services
        print(f"Database clear failed: {exc}")
        raise

    print("Cleared existing graph data")


def seed_database() -> None:
    """Create indexes and seed graph data if the database is reachable."""
    print("Initializing database connection...")
    _init_db()

    try:
        if not db.ping():
            print("Database is offline; skipping seed import")
            return
    except Exception as exc:  # pragma: no cover - defensive fallback for missing services
        print(f"Database is unavailable: {exc}")
        return

    print("Clearing existing graph data...")
    clear_database()

    print("Generating realistic graph data...")
    seed_data = _build_seed_data()

    with db.get_driver().session() as session:
        print("Creating graph constraints...")
        _create_constraints(session)

        print("Inserting developers...")
        developer_query = """
        UNWIND $rows AS row
        MERGE (d:Developer {email: row.email})
        ON CREATE SET d += row
        """
        _batch_upsert(session, developer_query, seed_data["developers"])

        print("Inserting companies...")
        company_query = """
        UNWIND $rows AS row
        MERGE (c:Company {name: row.name})
        ON CREATE SET c += row
        """
        _batch_upsert(session, company_query, seed_data["companies"])

        print("Inserting projects...")
        project_query = """
        UNWIND $rows AS row
        MERGE (p:Project {name: row.name})
        ON CREATE SET p += row
        """
        _batch_upsert(session, project_query, seed_data["projects"])

        print("Inserting skills...")
        skill_query = """
        UNWIND $rows AS row
        MERGE (s:Skill {name: row.name})
        ON CREATE SET s += row
        """
        _batch_upsert(session, skill_query, seed_data["skills"])

        print("Inserting technologies...")
        technology_query = """
        UNWIND $rows AS row
        MERGE (t:Technology {name: row.name})
        ON CREATE SET t += row
        """
        _batch_upsert(session, technology_query, seed_data["technologies"])

        print("Inserting certifications...")
        certification_query = """
        UNWIND $rows AS row
        MERGE (c:Certification {name: row.name})
        ON CREATE SET c += row
        """
        _batch_upsert(session, certification_query, seed_data["certifications"])

        print("Inserting locations...")
        location_query = """
        UNWIND $rows AS row
        MERGE (l:Location {city: row.city, country: row.country})
        ON CREATE SET l += row
        """
        _batch_upsert(session, location_query, seed_data["locations"])

        print("Creating relationships...")
        relationship_rows: list[dict[str, Any]] = []
        developer_emails = [developer["email"] for developer in seed_data["developers"]]
        developer_names = [developer["full_name"] for developer in seed_data["developers"]]
        company_names = [company["name"] for company in seed_data["companies"]]
        project_names = [project["name"] for project in seed_data["projects"]]
        skill_names = [skill["name"] for skill in seed_data["skills"]]
        technology_names = [technology["name"] for technology in seed_data["technologies"]]
        certification_names = [certification["name"] for certification in seed_data["certifications"]]
        location_keys = [f"{location['city']}|{location['country']}" for location in seed_data["locations"]]

        for index, developer in enumerate(seed_data["developers"]):
            for skill_name in developer.get("skills", []):
                relationship_rows.append({"developer_email": developer["email"], "skill_name": skill_name})

            current_company = developer["current_company"]
            relationship_rows.append({"developer_email": developer["email"], "company_name": current_company})

            for _ in range(random.randint(1, 2)):
                relationship_rows.append({"developer_email": developer["email"], "project_name": random.choice(project_names)})

            for certification_name in random.sample(certification_names, k=random.randint(1, 2)):
                relationship_rows.append({"developer_email": developer["email"], "certification_name": certification_name})

            relationship_rows.append({"developer_email": developer["email"], "location_key": random.choice(location_keys)})

            for collaborator in random.sample(developer_emails, k=random.randint(2, 4)):
                if collaborator != developer["email"]:
                    relationship_rows.append({"developer_email": developer["email"], "collaborator_email": collaborator})

            if index % 3 == 0:
                mentor_email = developer_emails[(index + 1) % len(developer_emails)]
                relationship_rows.append({"developer_email": developer["email"], "mentor_email": mentor_email})

        for project in seed_data["projects"]:
            relationship_rows.append({"project_name": project["name"], "company_name": random.choice(company_names)})
            for technology_name in project.get("technology_stack", []):
                relationship_rows.append({"project_name": project["name"], "technology_name": technology_name})

        for company in seed_data["companies"]:
            for technology_name in random.sample(technology_names, k=random.randint(3, 5)):
                relationship_rows.append({"company_name": company["name"], "technology_name": technology_name})

        print(f"Generated {len(relationship_rows)} relationships")

        relationship_query = """
        UNWIND $rows AS row
        MATCH (d:Developer {email: row.developer_email})
        MATCH (s:Skill {name: row.skill_name})
        MERGE (d)-[:HAS_SKILL]->(s)
        """
        # Relationship queries are split into targeted batches for readability and performance.
        skill_relationships = [row for row in relationship_rows if "skill_name" in row and "developer_email" in row]
        _batch_upsert(session, relationship_query, skill_relationships)

        work_query = """
        UNWIND $rows AS row
        MATCH (d:Developer {email: row.developer_email})
        MATCH (c:Company {name: row.company_name})
        MERGE (d)-[:WORKED_AT]->(c)
        """
        work_relationships = [row for row in relationship_rows if "company_name" in row and "developer_email" in row]
        _batch_upsert(session, work_query, work_relationships)

        project_query = """
        UNWIND $rows AS row
        MATCH (d:Developer {email: row.developer_email})
        MATCH (p:Project {name: row.project_name})
        MERGE (d)-[:BUILT]->(p)
        """
        build_relationships = [row for row in relationship_rows if "project_name" in row and "developer_email" in row]
        _batch_upsert(session, project_query, build_relationships)

        certification_query = """
        UNWIND $rows AS row
        MATCH (d:Developer {email: row.developer_email})
        MATCH (c:Certification {name: row.certification_name})
        MERGE (d)-[:CERTIFIED_IN]->(c)
        """
        certification_relationships = [row for row in relationship_rows if "certification_name" in row and "developer_email" in row]
        _batch_upsert(session, certification_query, certification_relationships)

        location_query = """
        UNWIND $rows AS row
        MATCH (d:Developer {email: row.developer_email})
        MATCH (l:Location {city: row.location_city, country: row.location_country})
        MERGE (d)-[:LOCATED_IN]->(l)
        """
        location_relationships = []
        for row in relationship_rows:
            if "location_key" in row and "developer_email" in row:
                city, country = row["location_key"].split("|", 1)
                location_relationships.append({"developer_email": row["developer_email"], "location_city": city, "location_country": country})
        _batch_upsert(session, location_query, location_relationships)

        collaboration_query = """
        UNWIND $rows AS row
        MATCH (d1:Developer {email: row.developer_email})
        MATCH (d2:Developer {email: row.collaborator_email})
        MERGE (d1)-[:COLLABORATED_WITH]->(d2)
        """
        collaboration_relationships = [row for row in relationship_rows if "collaborator_email" in row and "developer_email" in row]
        _batch_upsert(session, collaboration_query, collaboration_relationships)

        mentorship_query = """
        UNWIND $rows AS row
        MATCH (d1:Developer {email: row.developer_email})
        MATCH (d2:Developer {email: row.mentor_email})
        MERGE (d1)-[:MENTORS]->(d2)
        """
        mentorship_relationships = [row for row in relationship_rows if "mentor_email" in row and "developer_email" in row]
        _batch_upsert(session, mentorship_query, mentorship_relationships)

        project_owner_query = """
        UNWIND $rows AS row
        MATCH (p:Project {name: row.project_name})
        MATCH (c:Company {name: row.company_name})
        MERGE (p)-[:OWNED_BY]->(c)
        """
        project_owner_relationships = [row for row in relationship_rows if "project_name" in row and "company_name" in row and "developer_email" not in row]
        _batch_upsert(session, project_owner_query, project_owner_relationships)

        company_technology_query = """
        UNWIND $rows AS row
        MATCH (c:Company {name: row.company_name})
        MATCH (t:Technology {name: row.technology_name})
        MERGE (c)-[:USES]->(t)
        """
        company_technology_relationships = [row for row in relationship_rows if "company_name" in row and "technology_name" in row and "developer_email" not in row and "project_name" not in row]
        _batch_upsert(session, company_technology_query, company_technology_relationships)

        project_technology_query = """
        UNWIND $rows AS row
        MATCH (p:Project {name: row.project_name})
        MATCH (t:Technology {name: row.technology_name})
        MERGE (p)-[:USES]->(t)
        """
        project_technology_relationships = [row for row in relationship_rows if "project_name" in row and "technology_name" in row and "company_name" not in row]
        _batch_upsert(session, project_technology_query, project_technology_relationships)

    print("Seed operations completed")
    print(f"Developers: {len(seed_data['developers'])}")
    print(f"Companies: {len(seed_data['companies'])}")
    print(f"Skills: {len(seed_data['skills'])}")
    print(f"Technologies: {len(seed_data['technologies'])}")
    print(f"Projects: {len(seed_data['projects'])}")
    print(f"Certifications: {len(seed_data['certifications'])}")
    print(f"Relationships: {len(relationship_rows)}")


if __name__ == "__main__":
    seed_database()
