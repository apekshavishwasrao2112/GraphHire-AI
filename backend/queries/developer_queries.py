"""Parameterized Cypher query templates for developer-related graph operations."""


SEARCH_DEVELOPERS = """
MATCH (d:Developer)
WHERE toLower(d.full_name) CONTAINS toLower($query)
   OR toLower(d.email) CONTAINS toLower($query)
RETURN d.email AS email,
       d.full_name AS name,
       d.bio AS bio,
       d.years_of_experience AS experience,
       d.current_company AS current_company,
       d.country AS country,
       d.city AS city,
       d.profile_image_url AS profile_image_url,
       d.github_url AS github_url,
       d.linkedin_url AS linkedin_url
ORDER BY d.full_name
LIMIT $limit
"""


RECOMMENDATIONS = """
MATCH (d:Developer {email: $developer_email})-[:HAS_SKILL]->(s:Skill)<-[:HAS_SKILL]-(other:Developer)
WHERE other.email <> $developer_email
RETURN other, collect(s) AS shared_skills
ORDER BY size(shared_skills) DESC
LIMIT $limit
"""


GRAPH_PATH = """
MATCH p = shortestPath(
    (start:Developer {email: $from_email})-[*]-(end:Developer {email: $to_email})
)
RETURN p
"""


TOP_SKILLS = """
MATCH (s:Skill)<-[:HAS_SKILL]-(d:Developer)
RETURN s.name AS skill, count(d) AS developers
ORDER BY developers DESC
LIMIT $limit
"""


TOP_COMPANIES = """
MATCH (c:Company)<-[:WORKED_AT]-(d:Developer)
RETURN c.name AS company, count(d) AS employees
ORDER BY employees DESC
LIMIT $limit
"""


DASHBOARD_METRICS = """
MATCH (d:Developer)
WITH count(d) AS active_developers

MATCH (c:Company)
WITH active_developers, count(c) AS companies

MATCH (t:Technology)
WITH active_developers, companies, count(t) AS tech_domains

MATCH ()-[r]-()
WITH active_developers,
     companies,
     tech_domains,
     count(r) AS total_relationships

RETURN active_developers,
       companies,
       tech_domains,
       total_relationships
"""


COMPANY_EMPLOYEES = """
MATCH (d:Developer)-[:WORKED_AT]->(c:Company {name: $company_name})
RETURN d
ORDER BY d.full_name
"""


PROJECT_TECHNOLOGIES = """
MATCH (p:Project {name: $project_name})-[:USES]->(t:Technology)
RETURN t.name AS technology
"""


DEVELOPER_CAREER = """
MATCH (d:Developer {email: $developer_email})-[:WORKED_AT]->(c:Company)
RETURN d.full_name AS developer,
       collect(c.name) AS companies
"""


SIMILARITY = """
MATCH (d1:Developer {email: $from_email})-[:HAS_SKILL]->(s:Skill)<-[:HAS_SKILL]-(d2:Developer {email: $to_email})
RETURN count(s) AS shared_skills
"""


GRAPH_EXPLORER = """
MATCH (start)
WHERE
(
    start:Developer
    AND (
        toLower(coalesce(start.full_name, '')) CONTAINS toLower($query)
        OR toLower(coalesce(start.email, '')) CONTAINS toLower($query)
    )
)
OR (
    start:Skill
    AND toLower(coalesce(start.name, '')) CONTAINS toLower($query)
)
OR (
    start:Company
    AND toLower(coalesce(start.name, '')) CONTAINS toLower($query)
)
OR (
    start:Project
    AND toLower(coalesce(start.name, '')) CONTAINS toLower($query)
)
OR (
    start:Technology
    AND toLower(coalesce(start.name, '')) CONTAINS toLower($query)
)
OR (
    start:Certification
    AND toLower(coalesce(start.name, '')) CONTAINS toLower($query)
)
OR (
    start:Location
    AND (
        toLower(coalesce(start.city, '')) CONTAINS toLower($query)
        OR toLower(coalesce(start.country, '')) CONTAINS toLower($query)
    )
)

MATCH p = (start)-[*1..2]-(connected)

WITH start, collect(p)[0..50] AS paths

UNWIND paths AS path

UNWIND nodes(path) AS node

WITH
    start,
    collect(DISTINCT node) AS graph_nodes,
    paths

UNWIND paths AS path

UNWIND relationships(path) AS relationship

WITH
    graph_nodes,
    collect(DISTINCT relationship) AS graph_relationships

RETURN
[
    node IN graph_nodes |
    {
        id: toString(id(node)),
        labels: labels(node),
        properties: properties(node)
    }
] AS nodes,

[
    relationship IN graph_relationships |
    {
        id: toString(id(relationship)),
        source: toString(id(startNode(relationship))),
        target: toString(id(endNode(relationship))),
        type: type(relationship),
        properties: properties(relationship)
    }
] AS relationships
"""