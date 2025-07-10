"use client"

const FilterBar = ({ filters, onFilterChange }) => {
  const handleFilterChange = (filterType, value) => {
    onFilterChange({
      ...filters,
      [filterType]: value,
    })
  }

  const clearFilters = () => {
    onFilterChange({
      location: "",
      jobType: "",
      tag: "",
      keyword: "",
    })
  }

  return (
    <div className="filter-bar">
      <div className="filter-title">
        <h3>Filter Jobs</h3>
        <button className="clear-filters" onClick={clearFilters}>
          Clear All
        </button>
      </div>

      <div className="filters-row">
        <div className="filter-group">
          <label>Search</label>
          <input
            type="text"
            placeholder="Search jobs, companies..."
            value={filters.keyword}
            onChange={(e) => handleFilterChange("keyword", e.target.value)}
          />
        </div>

        <div className="filter-group">
          <label>Location</label>
          <input
            type="text"
            placeholder="City, State"
            value={filters.location}
            onChange={(e) => handleFilterChange("location", e.target.value)}
          />
        </div>

        <div className="filter-group">
          <label>Job Type</label>
          <select value={filters.jobType} onChange={(e) => handleFilterChange("jobType", e.target.value)}>
            <option value="">All Types</option>
            <option value="Full-time">Full-time</option>
            <option value="Part-time">Part-time</option>
            <option value="Contract">Contract</option>
            <option value="Remote">Remote</option>
            <option value="Internship">Internship</option>
          </select>
        </div>

        <div className="filter-group">
          <label>Skills</label>
          <input
            type="text"
            placeholder="React, Python, etc."
            value={filters.tag}
            onChange={(e) => handleFilterChange("tag", e.target.value)}
          />
        </div>
      </div>
    </div>
  )
}

export default FilterBar
