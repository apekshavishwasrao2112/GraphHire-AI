"""Service layer for developer and graph analytics operations."""

from __future__ import annotations

import logging

from backend.database import db
from backend.queries.developer_queries import (
    COMPANY_EMPLOYEES,
    DEVELOPER_CAREER,
    GRAPH_PATH,
    GRAPH_EXPLORER,
    PROJECT_TECHNOLOGIES,
    RECOMMENDATIONS,
    SEARCH_DEVELOPERS,
    SIMILARITY,
    TOP_COMPANIES,
    TOP_SKILLS,
    DASHBOARD_METRICS,
)

logger = logging.getLogger(__name__)


class DeveloperService:
    """Encapsulates graph queries for developer-facing APIs."""

    def _safe_query(
        self,
        query: str,
        parameters: dict | None = None,
    ) -> list[dict]:
        """Execute graph queries safely."""

        try:
            return db.run_query(
                query,
                parameters or {},
            )

        except Exception:
            logger.exception("Database query failed")
            return []

    def get_graph(self, query: str) -> dict:
   
        if not query or not query.strip():
            return {
                "nodes": [],
                "edges": [],
            }

        records = self._safe_query(
            GRAPH_EXPLORER,
            {"query": query.strip()},
        )

        if not records:
            return {
                "nodes": [],
                "edges": [],
            }

        record = records[0]

        return {
            "nodes": record.get("nodes", []),
            "edges": record.get("relationships", []),
        }

    # ------------------------------------------------------------------
    # Developer search
    # ------------------------------------------------------------------

    def search_developers(
        self,
        query: str,
        limit: int = 10,
    ) -> list[dict]:
        """Search developers by name or email."""

        records = self._safe_query(
            SEARCH_DEVELOPERS,
            {
                "query": query,
                "limit": limit,
            },
        )

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
                    "profile_image_url": record.get(
                        "profile_image_url"
                    ),
                    "github_url": record.get("github_url"),
                    "linkedin_url": record.get(
                        "linkedin_url"
                    ),
                }
            }
            for record in records
        ]

    # ------------------------------------------------------------------
    # Recommendations
    # ------------------------------------------------------------------

    def get_recommendations(
        self,
        developer_email: str,
        limit: int = 10,
    ) -> list[dict]:
        """Recommend developers based on shared skills."""

        records = self._safe_query(
            RECOMMENDATIONS,
            {
                "developer_email": developer_email,
                "limit": limit,
            },
        )

        return [
            {
                "developer": record.get("other"),
                "shared_skills": [
                    skill
                    for skill in record.get(
                        "shared_skills",
                        [],
                    )
                ],
            }
            for record in records
        ]

    # ------------------------------------------------------------------
    # Shortest path
    # ------------------------------------------------------------------

    def get_shortest_path(
        self,
        from_email: str,
        to_email: str,
    ) -> list[dict]:
        """Return the shortest path between two developers."""

        records = self._safe_query(
            GRAPH_PATH,
            {
                "from_email": from_email,
                "to_email": to_email,
            },
        )

        return [
            {
                "path": record.get("p"),
            }
            for record in records
        ]

    # ------------------------------------------------------------------
    # Company employees
    # ------------------------------------------------------------------

    def get_company_employees(
        self,
        company_name: str,
    ) -> list[dict]:
        """Return employees for a company."""

        records = self._safe_query(
            COMPANY_EMPLOYEES,
            {
                "company_name": company_name,
            },
        )

        return [
            {
                "developer": record.get("d"),
            }
            for record in records
        ]

    # ------------------------------------------------------------------
    # Project technologies
    # ------------------------------------------------------------------

    def get_project_technologies(
        self,
        project_name: str,
    ) -> list[dict]:
        """Return technologies used by a project."""

        records = self._safe_query(
            PROJECT_TECHNOLOGIES,
            {
                "project_name": project_name,
            },
        )

        return [
            {
                "technology": record.get("technology"),
            }
            for record in records
        ]

    # ------------------------------------------------------------------
    # Dashboard
    # ------------------------------------------------------------------

    def get_top_skills(
        self,
        limit: int = 10,
    ) -> list[dict]:
        """Return the most-used skills."""

        records = self._safe_query(
            TOP_SKILLS,
            {
                "limit": limit,
            },
        )

        return [
            {
                "skill": record.get("skill"),
                "developers": record.get(
                    "developers"
                ),
            }
            for record in records
        ]

    def get_top_companies(
        self,
        limit: int = 10,
    ) -> list[dict]:
        """Return the most-populated companies."""

        records = self._safe_query(
            TOP_COMPANIES,
            {
                "limit": limit,
            },
        )

        return [
            {
                "company": record.get("company"),
                "employees": record.get(
                    "employees"
                ),
            }
            for record in records
        ]

    def get_dashboard(
        self,
        limit: int = 10,
    ) -> dict:
        """Return dashboard analytics."""

        top_skills = self.get_top_skills(
            limit=limit
        )

        top_companies = self.get_top_companies(
            limit=limit
        )

        metrics_records = self._safe_query(
            DASHBOARD_METRICS
        )

        metrics = {}

        if metrics_records:
            record = metrics_records[0]

            metrics = {
                "active_developers": (
                    record.get(
                        "active_developers"
                    )
                    or 0
                ),
                "companies": (
                    record.get("companies")
                    or 0
                ),
                "tech_domains": (
                    record.get("tech_domains")
                    or 0
                ),
                "total_relationships": (
                    record.get(
                        "total_relationships"
                    )
                    or 0
                ),
            }

        return {
            "top_skills": top_skills,
            "top_companies": top_companies,
            "metrics": metrics,
        }

    # ------------------------------------------------------------------
    # Career
    # ------------------------------------------------------------------

    def get_developer_career(
        self,
        developer_email: str,
    ) -> list[dict]:
        """Return the companies associated with a developer."""

        records = self._safe_query(
            DEVELOPER_CAREER,
            {
                "developer_email": developer_email,
            },
        )

        return [
            {
                "developer": record.get(
                    "developer"
                ),
                "companies": record.get(
                    "companies"
                ),
            }
            for record in records
        ]

    # ------------------------------------------------------------------
    # Global search
    # ------------------------------------------------------------------

    def search_all(
        self,
        query: str,
        limit: int = 10,
    ) -> dict:
        """
        Search across multiple graph entity types.

        All Cypher values are passed as parameters.
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
            """
            MATCH (d:Developer)
            WHERE
                toLower(d.full_name)
                    CONTAINS toLower($q)
                OR
                toLower(d.email)
                    CONTAINS toLower($q)

            RETURN
                d.full_name AS name,
                d.email AS email,
                d.years_of_experience AS experience

            LIMIT $limit
            """,
            {
                "q": query,
                "limit": limit,
            },
        )

        results["developers"] = [
            {
                "name": record.get("name"),
                "email": record.get("email"),
                "experience": record.get(
                    "experience"
                ),
            }
            for record in dev_records
        ]

        # Skills
        skill_records = self._safe_query(
            """
            MATCH (s:Skill)
            WHERE toLower(s.name)
                CONTAINS toLower($q)

            RETURN s.name AS name

            LIMIT $limit
            """,
            {
                "q": query,
                "limit": limit,
            },
        )

        results["skills"] = [
            record.get("name")
            for record in skill_records
        ]

        # Companies
        company_records = self._safe_query(
            """
            MATCH (c:Company)
            WHERE toLower(c.name)
                CONTAINS toLower($q)

            RETURN c.name AS name

            LIMIT $limit
            """,
            {
                "q": query,
                "limit": limit,
            },
        )

        results["companies"] = [
            record.get("name")
            for record in company_records
        ]

        # Projects
        project_records = self._safe_query(
            """
            MATCH (p:Project)
            WHERE
                toLower(p.name)
                    CONTAINS toLower($q)
                OR
                toLower(coalesce(p.description, ""))
                    CONTAINS toLower($q)

            RETURN p.name AS name

            LIMIT $limit
            """,
            {
                "q": query,
                "limit": limit,
            },
        )

        results["projects"] = [
            record.get("name")
            for record in project_records
        ]

        # Technologies
        technology_records = self._safe_query(
            """
            MATCH (t:Technology)
            WHERE toLower(t.name)
                CONTAINS toLower($q)

            RETURN t.name AS name

            LIMIT $limit
            """,
            {
                "q": query,
                "limit": limit,
            },
        )

        results["technologies"] = [
            record.get("name")
            for record in technology_records
        ]

        # Certifications
        certification_records = self._safe_query(
            """
            MATCH (c:Certification)
            WHERE toLower(c.name)
                CONTAINS toLower($q)

            RETURN c.name AS name

            LIMIT $limit
            """,
            {
                "q": query,
                "limit": limit,
            },
        )

        results["certifications"] = [
            record.get("name")
            for record in certification_records
        ]

        # Locations
        location_records = self._safe_query(
            """
            MATCH (l:Location)
            WHERE
                toLower(coalesce(l.city, ""))
                    CONTAINS toLower($q)
                OR
                toLower(coalesce(l.country, ""))
                    CONTAINS toLower($q)

            RETURN
                l.city AS city,
                l.country AS country

            LIMIT $limit
            """,
            {
                "q": query,
                "limit": limit,
            },
        )

        results["locations"] = [
            {
                "city": record.get("city"),
                "country": record.get(
                    "country"
                ),
            }
            for record in location_records
        ]

        return results

    # ------------------------------------------------------------------
    # Similarity
    # ------------------------------------------------------------------

    def get_similarity(
        self,
        from_email: str,
        to_email: str,
    ) -> list[dict]:
        """Return shared-skill similarity between developers."""

        records = self._safe_query(
            SIMILARITY,
            {
                "from_email": from_email,
                "to_email": to_email,
            },
        )

        return [
            {
                "shared_skills": record.get(
                    "shared_skills"
                ),
            }
            for record in records
        ]

    # ------------------------------------------------------------------
    # LIVE GRAPH
    # ------------------------------------------------------------------

    def get_developer_graph(
        self,
        developer_email: str,
    ) -> dict:
        """
        Build a graph around one developer.

        The query traverses up to two relationship hops so the
        frontend can display a useful connected network.

        Example:

            Developer
                |
                +-- HAS_SKILL --> Skill
                |
                +-- WORKED_AT --> Company
                |
                +-- BUILT -----> Project
        """

        query = """
        MATCH (center:Developer)
        WHERE toLower(center.email) = toLower($email)

        MATCH path = (center)-[*1..2]-(connected)

        WITH
            center,
            collect(DISTINCT path) AS paths

        UNWIND paths AS path

        UNWIND nodes(path) AS node
        WITH
            center,
            collect(DISTINCT node) AS all_nodes,
            paths

        UNWIND paths AS path

        UNWIND relationships(path) AS relationship
        WITH
            center,
            all_nodes,
            collect(DISTINCT relationship) AS all_relationships

        RETURN
            elementId(center) AS center_id,
            [
                node IN all_nodes |
                {
                    id: elementId(node),
                    labels: labels(node),
                    properties: properties(node)
                }
            ] AS nodes,
            [
                relationship IN all_relationships |
                {
                    id: elementId(relationship),
                    type: type(relationship),
                    source: elementId(startNode(relationship)),
                    target: elementId(endNode(relationship)),
                    properties: properties(relationship)
                }
            ] AS edges
        """

        records = self._safe_query(
            query,
            {
                "email": developer_email,
            },
        )

        if not records:
            return {
                "center": None,
                "nodes": [],
                "edges": [],
            }

        record = records[0]

        return {
            "center": record.get(
                "center_id"
            ),
            "nodes": record.get(
                "nodes",
                [],
            ),
            "edges": record.get(
                "edges",
                [],
            ),
        }

    # ------------------------------------------------------------------
    # LIVE GRAPH SEARCH
    # ------------------------------------------------------------------

    def search_graph(
        self,
        query: str,
    ) -> dict:
        """
        Search any graph entity and return its connected network.

        Examples:

            Python
            Infosys
            Apeksha
            React
            Bengaluru

        The matching entity becomes the center of the graph.
        """

        graph_query = """
        MATCH (center)
        WHERE
            (
                "Developer" IN labels(center)
                AND (
                    toLower(coalesce(center.full_name, ""))
                        CONTAINS toLower($q)
                    OR
                    toLower(coalesce(center.name, ""))
                        CONTAINS toLower($q)
                    OR
                    toLower(coalesce(center.email, ""))
                        CONTAINS toLower($q)
                )
            )
            OR
            (
                "Skill" IN labels(center)
                AND toLower(coalesce(center.name, ""))
                    CONTAINS toLower($q)
            )
            OR
            (
                "Company" IN labels(center)
                AND toLower(coalesce(center.name, ""))
                    CONTAINS toLower($q)
            )
            OR
            (
                "Project" IN labels(center)
                AND toLower(coalesce(center.name, ""))
                    CONTAINS toLower($q)
            )
            OR
            (
                "Technology" IN labels(center)
                AND toLower(coalesce(center.name, ""))
                    CONTAINS toLower($q)
            )
            OR
            (
                "Certification" IN labels(center)
                AND toLower(coalesce(center.name, ""))
                    CONTAINS toLower($q)
            )
            OR
            (
                "Location" IN labels(center)
                AND (
                    toLower(coalesce(center.city, ""))
                        CONTAINS toLower($q)
                    OR
                    toLower(coalesce(center.country, ""))
                        CONTAINS toLower($q)
                )
            )

        WITH center
        ORDER BY
            CASE
                WHEN "Developer" IN labels(center)
                    THEN 1
                WHEN "Company" IN labels(center)
                    THEN 2
                WHEN "Skill" IN labels(center)
                    THEN 3
                ELSE 4
            END

        LIMIT 1

        OPTIONAL MATCH path =
            (center)-[*1..2]-(connected)

        WITH
            center,
            collect(DISTINCT path) AS paths

        UNWIND paths AS path

        UNWIND nodes(path) AS node

        WITH
            center,
            collect(DISTINCT node) AS all_nodes,
            paths

        UNWIND paths AS path

        UNWIND relationships(path) AS relationship

        WITH
            center,
            all_nodes,
            collect(DISTINCT relationship) AS all_relationships

        RETURN
            elementId(center) AS center_id,

            [
                node IN all_nodes |
                {
                    id: elementId(node),
                    labels: labels(node),
                    properties: properties(node)
                }
            ] AS nodes,

            [
                relationship IN all_relationships |
                {
                    id: elementId(relationship),
                    type: type(relationship),
                    source: elementId(startNode(relationship)),
                    target: elementId(endNode(relationship)),
                    properties: properties(relationship)
                }
            ] AS edges
        """

        records = self._safe_query(
            graph_query,
            {
                "q": query,
            },
        )

        if not records:
            return {
                "center": None,
                "nodes": [],
                "edges": [],
            }

        record = records[0]

        return {
            "center": record.get(
                "center_id"
            ),
            "nodes": record.get(
                "nodes",
                [],
            ),
            "edges": record.get(
                "edges",
                [],
            ),
        }

