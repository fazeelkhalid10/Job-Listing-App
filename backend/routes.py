# routes.py

from flask import Blueprint, request, jsonify
from models import db, Job

job_bp = Blueprint("job_bp", __name__)

# Get all jobs (with optional filters/sorting)
@job_bp.route("/jobs", methods=["GET"])
def get_jobs():
    query = Job.query

    # Filters
    location = request.args.get("location")
    job_type = request.args.get("job_type")
    tag = request.args.get("tag")
    keyword = request.args.get("keyword")
    sort = request.args.get("sort")

    if location:
        query = query.filter(Job.location.ilike(f"%{location}%"))
    if job_type:
        query = query.filter_by(job_type=job_type)
    if tag:
        query = query.filter(Job.tags.ilike(f"%{tag}%"))
    if keyword:
        keyword = f"%{keyword}%"
        query = query.filter(
            (Job.title.ilike(keyword)) |
            (Job.company.ilike(keyword)) |
            (Job.description.ilike(keyword))
        )

    # Sorting
    if sort == "date_asc":
        query = query.order_by(Job.posting_date.asc())
    else:  # default to newest first
        query = query.order_by(Job.posting_date.desc())

    jobs = query.all()
    return jsonify([serialize_job(job) for job in jobs]), 200


# Get single job by ID
@job_bp.route("/jobs/<int:job_id>", methods=["GET"])
def get_job(job_id):
    job = Job.query.get_or_404(job_id)
    return jsonify(serialize_job(job)), 200


# Create a new job
@job_bp.route("/jobs", methods=["POST"])
def create_job():
    data = request.get_json()
    required_fields = ["title", "company", "location"]

    if not all(field in data and data[field] for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    # ✅ Check for existing job (title + company + location)
    existing = Job.query.filter_by(
        title=data["title"],
        company=data["company"],
        location=data["location"]
    ).first()

    if existing:
        return jsonify({"message": "Duplicate job exists"}), 409

    job = Job(
        title=data["title"],
        company=data["company"],
        location=data["location"],
        job_type=data.get("jobType", ""),
        posting_date=data.get("posting_date", ""),
        tags=data.get("tags", ""),
        description=data.get("description", ""),
    )

    db.session.add(job)
    db.session.commit()

    return jsonify(serialize_job(job)), 201


# Update a job
@job_bp.route("/jobs/<int:job_id>", methods=["PUT"])
def update_job(job_id):
    job = Job.query.get_or_404(job_id)
    data = request.get_json()

    job.title = data.get("title", job.title)
    job.company = data.get("company", job.company)
    job.location = data.get("location", job.location)
    job.job_type = data.get("jobType", job.job_type)
    job.posting_date = data.get("posting_date", job.posting_date)
    job.tags = data.get("tags", job.tags)
    job.description = data.get("description", job.description)

    db.session.commit()

    return jsonify(serialize_job(job)), 200


# Delete a job
@job_bp.route("/jobs/<int:job_id>", methods=["DELETE"])
def delete_job(job_id):
    job = Job.query.get_or_404(job_id)
    db.session.delete(job)
    db.session.commit()
    return jsonify({"message": "Job deleted"}), 200


# Helper function
def serialize_job(job):
    return {
        "id": job.id,
        "title": job.title,
        "company": job.company,
        "location": job.location,
        "jobType": job.job_type,
        "tags": job.tags.split(",") if job.tags else [],
        "datePosted": job.posting_date,
        "description": job.description,
    }
