"""Service layer for developer and graph analytics operations."""

from __future__ import annotations

from backend.database import db
from backend.queries.developer_queries import (
    COMPANY_EMPLOYEES,
    DEVELOPER_CAREER,
    GRAPH_PATH,
    PROJECT_TECHNOLOGIES,
    RECOMMENDATIONS,
    SEARCH_DEVELOPERS,
    SIMILARITY,
    TOP_COMPANIES,
    TOP_SKILLS,
    DASHBOARD_METRICS,
)


class DeveloperService:
    """Encapsulates graph queries for developer-facing APIs."""

    def _safe_query(self, query: str, parameters: dict | None = None) -> list[dict]:
        """Execute graph queries safely and return an empty list if the database is unavailable."""
        try:
            return db.run_query(query, parameters or {})
        except (RuntimeError, Exception):
            # Log the full exception for debugging in the server logs
            import logging

            logging.getLogger(__name__).exception("Database query failed")
            return []

    def search_developers(self, query: str, limit: int = 10) -> list[dict]:
        """Search developers by name or email."""
        records = self._safe_query(SEARCH_DEVELOPERS, {"query": query, "limit": limit})
        return [
            {
                "developer": {
                    "email": record.get("email"),
                    "name": record.get("name"),
                    "bio": record.get("bio"),
                    "experience": record.get("experience"),
                    "current_company": record.get("current_company"),
                    "country": record.get("country"),
                    "city": record.get("city"),
                    "skills": record.get("skills", []),
                    "profile_image_url": record.get("profile_image_url"),
                    "github_url": record.get("github_url"),
                    "linkedin_url": record.get("linkedin_url"),
                }
            }
            for record in records
        ]

    def get_recommendations(self, developer_email: str, limit: int = 10) -> list[dict]:
        """Recommend developers based on shared skills."""
        records = self._safe_query(RECOMMENDATIONS, {"developer_email": developer_email, "limit": limit})
        return [
            {"developer": record.get("other"), "shared_skills": [skill for skill in record.get("shared_skills", [])]}
            for record in records
        ]

    def get_shortest_path(self, from_email: str, to_email: str) -> list[dict]:
        """Return the shortest path between two developers."""
        records = self._safe_query(GRAPH_PATH, {"from_email": from_email, "to_email": to_email})
        return [{"path": record.get("p")} for record in records]

    def get_company_employees(self, company_name: str) -> list[dict]:
        """Return employees for a company."""
        records = self._safe_query(COMPANY_EMPLOYEES, {"company_name": company_name})
        return [{"developer": record.get("d")} for record in records]

    def get_project_technologies(self, project_name: str) -> list[dict]:
        """Return technologies used by a project."""
        records = self._safe_query(PROJECT_TECHNOLOGIES, {"project_name": project_name})
        return [{"technology": record.get("technology")} for record in records]

    def get_top_skills(self, limit: int = 10) -> list[dict]:
        """Return the most-used skills."""
        records = self._safe_query(TOP_SKILLS, {"limit": limit})
        return [{"skill": record.get("skill"), "developers": record.get("developers")} for record in records]

    def get_top_companies(self, limit: int = 10) -> list[dict]:
        """Return the most-populated companies."""
        records = self._safe_query(TOP_COMPANIES, {"limit": limit})
        return [{"company": record.get("company"), "employees": record.get("employees")} for record in records]

    def get_dashboard(self, limit: int = 10) -> dict:
        """Return dashboard payload with top skills, companies and high-level metrics."""
        top_skills = self.get_top_skills(limit=limit)
        top_companies = self.get_top_companies(limit=limit)

        # Dashboard metrics: active developers, companies, tech domains, total relationships
        metrics_records = self._safe_query(DASHBOARD_METRICS)
        metrics = {}
        if metrics_records:
            rec = metrics_records[0]
            metrics = {
                "active_developers": rec.get("active_developers") or 0,
                "companies": rec.get("companies") or 0,
                "tech_domains": rec.get("tech_domains") or 0,
                "total_relationships": rec.get("total_relationships") or 0,
            }

        return {"top_skills": top_skills, "top_companies": top_companies, "metrics": metrics}

    def get_developer_career(self, developer_email: str) -> list[dict]:
        """Return the companies associated with the developer journey."""
        records = self._safe_query(DEVELOPER_CAREER, {"developer_email": developer_email})
        return [{"developer": record.get("developer"), "companies": record.get("companies")} for record in records]

    def search_all(self, query: str, limit: int = 10) -> dict:
        """Search across multiple entity types and return categorized results.

        Uses parameterized Cypher for each category to avoid injection.
        Returns a dict with keys: developers, skills, companies, projects, technologies, certifications, locations
        """
        results = {
            "developers": [],
            "skills": [],
            "companies": [],
            "projects": [],
            "technologies": [],
            "certifications": [],
            "locations": [],
        }

        # Developers
        dev_records = self._safe_query(
            "MATCH (d:Developer) WHERE toLower(d.full_name) CONTAINS toLower($q) OR toLower(d.email) CONTAINS toLower($q) RETURN d.full_name AS name, d.email AS email, d.years_of_experience AS experience LIMIT $limit",
            {"q": query, "limit": limit},
        )
        results["developers"] = [{"name": r.get("name"), "email": r.get("email"), "experience": r.get("experience")} for r in dev_records]

        # Skills
        skill_records = self._safe_query("MATCH (s:Skill) WHERE toLower(s.name) CONTAINS toLower($q) RETURN s.name AS name LIMIT $limit", {"q": query, "limit": limit})
        results["skills"] = [r.get("name") for r in skill_records]

        # Companies
        comp_records = self._safe_query("MATCH (c:Company) WHERE toLower(c.name) CONTAINS toLower($q) RETURN c.name AS name LIMIT $limit", {"q": query, "limit": limit})
        results["companies"] = [r.get("name") for r in comp_records]

        # Projects
        proj_records = self._safe_query("MATCH (p:Project) WHERE toLower(p.name) CONTAINS toLower($q) OR toLower(p.description) CONTAINS toLower($q) RETURN p.name AS name LIMIT $limit", {"q": query, "limit": limit})
        results["projects"] = [r.get("name") for r in proj_records]

        # Technologies
        tech_records = self._safe_query("MATCH (t:Technology) WHERE toLower(t.name) CONTAINS toLower($q) RETURN t.name AS name LIMIT $limit", {"q": query, "limit": limit})
        results["technologies"] = [r.get("name") for r in tech_records]

        # Certifications
        cert_records = self._safe_query("MATCH (c:Certification) WHERE toLower(c.name) CONTAINS toLower($q) RETURN c.name AS name LIMIT $limit", {"q": query, "limit": limit})
        results["certifications"] = [r.get("name") for r in cert_records]

        # Locations
        loc_records = self._safe_query("MATCH (l:Location) WHERE toLower(l.city) CONTAINS toLower($q) OR toLower(l.country) CONTAINS toLower($q) RETURN l.city AS city, l.country AS country LIMIT $limit", {"q": query, "limit": limit})
        results["locations"] = [{"city": r.get("city"), "country": r.get("country")} for r in loc_records]

        return results

    def get_similarity(self, from_email: str, to_email: str) -> list[dict]:
        """Return shared-skill similarity between developers."""
        records = self._safe_query(SIMILARITY, {"from_email": from_email, "to_email": to_email})
        return [{"shared_skills": record.get("shared_skills")} for record in records]