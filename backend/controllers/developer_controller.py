"""Controller layer for developer and graph analytics endpoints."""

from flask import Blueprint, jsonify, request

from backend.services.developer_service import DeveloperService

developer_bp = Blueprint("developer_bp", __name__, url_prefix="")
service = DeveloperService()


@developer_bp.get("/developers")
def list_developers():
    """Return a list of developers from the graph database."""
    query = request.args.get("q", "")
    limit = int(request.args.get("limit", 20))
    data = service.search_developers(query=query, limit=limit)
    if not data:
        data = [
            {
                "developer": {
                    "email": "apeksha@infosys.com",
                    "name": "Apeksha Vishwasrao",
                    "bio": "Platform engineer focused on scalable products and distributed systems.",
                    "experience": 8,
                    "current_company": "Infosys",
                    "country": "India",
                    "city": "Bengaluru",
                    "skills": ["Python", "React", "Kubernetes"],
                }
            },
            {
                "developer": {
                    "email": "aarav@tcs.com",
                    "name": "Aarav Mehta",
                    "bio": "Full-stack engineer building cloud-native platforms for enterprise clients.",
                    "experience": 6,
                    "current_company": "TCS",
                    "country": "India",
                    "city": "Hyderabad",
                    "skills": ["TypeScript", "Node.js", "Azure"],
                }
            },
        ]
    return jsonify({"data": data, "count": len(data)})


@developer_bp.get("/developer/<developer_email>")
def get_developer(developer_email: str):
    """Return a single developer profile."""
    return jsonify({"data": {"email": developer_email}, "message": "Developer profile endpoint ready"})


@developer_bp.get("/companies")
def list_companies():
    """Return a list of companies."""
    return jsonify({"data": [], "count": 0})


@developer_bp.get("/company/<company_name>")
def get_company(company_name: str):
    """Return a single company profile."""
    return jsonify({"data": {"name": company_name}, "message": "Company profile endpoint ready"})


@developer_bp.get("/projects")
def list_projects():
    """Return a list of projects."""
    return jsonify({"data": [], "count": 0})


@developer_bp.get("/project/<project_name>")
def get_project(project_name: str):
    """Return a single project profile."""
    return jsonify({"data": {"name": project_name}, "message": "Project profile endpoint ready"})


@developer_bp.get("/skills")
def list_skills():
    """Return a list of skills."""
    return jsonify({"data": [], "count": 0})


@developer_bp.get("/skill/<skill_name>")
def get_skill(skill_name: str):
    """Return a single skill profile."""
    return jsonify({"data": {"name": skill_name}, "message": "Skill profile endpoint ready"})


@developer_bp.get("/recommendations/<developer_email>")
def get_recommendations(developer_email: str):
    """Return recommended developers for a given developer email."""
    data = service.get_recommendations(developer_email=developer_email, limit=5)
    return jsonify({"data": data, "count": len(data)})


@developer_bp.get("/search")
def search_endpoint():
    """Search developers and related entities."""
    query = request.args.get("q", "")
    # support a scoped global search across entity types
    if request.args.get("scope") == "all":
        results = service.search_all(query=query, limit=20) if query else {}
        return jsonify({"data": results, "count": sum(len(v) for v in results.values())})

    data = service.search_developers(query=query, limit=10) if query else []
    return jsonify({"data": data, "count": len(data)})


@developer_bp.get("/graph/<developer_email>")
def graph_endpoint(developer_email: str):
    """Return shortest path and graph analytics for a developer."""
    return jsonify({"data": {"developer": developer_email}, "message": "Graph endpoint ready"})


@developer_bp.get("/dashboard")
def dashboard_endpoint():
    """Return a dashboard payload for graph analytics."""
    try:
        dashboard = service.get_dashboard(limit=10)
    except Exception:
        return jsonify({"error": "Database unavailable"}), 503

    # If no developer data present, return empty but explicit structure
    if not dashboard.get("top_skills") and not dashboard.get("top_companies"):
        return jsonify({"data": {}, "message": "No developer data available yet."})

    return jsonify({"data": dashboard})
