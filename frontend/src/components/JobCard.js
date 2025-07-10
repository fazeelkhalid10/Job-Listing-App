"use client"

const JobCard = ({ job, onEdit, onDelete }) => {
  const formatDate = (dateString) => {
    const date = new Date(dateString)
    return date.toLocaleDateString("en-US", {
      year: "numeric",
      month: "short",
      day: "numeric",
    })
  }

  return (
    <div className="job-card">
      <div className="job-header">
        <div className="job-title-section">
          <h3 className="job-title">{job.title}</h3>
          <p className="job-company">{job.company}</p>
        </div>
        <div className="job-actions">
          <button className="btn-edit" onClick={() => onEdit(job)}>
            Edit
          </button>
          <button className="btn-delete" onClick={() => onDelete(job.id)}>
            Delete
          </button>
        </div>
      </div>

      <div className="job-details">
        <div className="job-info">
          <span className="job-location">📍 {job.location}</span>
          <span className="job-type">{job.jobType}</span>
          <span className="job-date">📅 {formatDate(job.datePosted)}</span>
        </div>
      </div>

      <div className="job-description">
        {/* <p>{job.description}</p> */}
      </div>

      <div className="job-tags">
        {job.tags.map((tag, index) => (
          <span key={index} className="job-tag">
            {tag}
          </span>
        ))}
      </div>
    </div>
  )
}

export default JobCard
