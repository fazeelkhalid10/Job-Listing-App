import JobCard from "./JobCard"

const JobList = ({ jobs, onEdit, onDelete }) => {
  if (jobs.length === 0) {
    return (
      <div className="no-jobs">
        <h3>No jobs found</h3>
        <p>Try adjusting your filters or search criteria</p>
      </div>
    )
  }

  return (
    <div className="job-list">
      <div className="jobs-count">
        <h3>
          {jobs.length} Job{jobs.length !== 1 ? "s" : ""} Found
        </h3>
      </div>
      <div className="jobs-grid">
        {jobs.map((job) => (
          <JobCard key={job.id} job={job} onEdit={onEdit} onDelete={onDelete} />
        ))}
      </div>
    </div>
  )
}

export default JobList
