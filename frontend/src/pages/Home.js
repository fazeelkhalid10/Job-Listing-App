"use client"

import { useState, useEffect } from "react"
import Navbar from "../components/Navbar"
import JobList from "../components/JobList"
import JobForm from "../components/JobForm"
import FilterBar from "../components/FilterBar"
import SortDropdown from "../components/SortDropdown"
import api from "../api" // Axios instance
import "../App.css"

function Home() {
  const [jobs, setJobs] = useState([])
  const [filteredJobs, setFilteredJobs] = useState([])
  const [showForm, setShowForm] = useState(false)
  const [editingJob, setEditingJob] = useState(null)
  const [filters, setFilters] = useState({
    location: "",
    jobType: "",
    tag: "",
    keyword: "",
  })
  const [sortOrder, setSortOrder] = useState("newest")

  // Fetch jobs from backend
  useEffect(() => {
    api.get("/jobs")
      .then((res) => setJobs(res.data))
      .catch((err) => console.error("Error fetching jobs:", err))
  }, [])

  // Filter and sort jobs
  useEffect(() => {
    const filtered = jobs.filter((job) => {
      return (
        (filters.location === "" || job.location.toLowerCase().includes(filters.location.toLowerCase())) &&
        (filters.jobType === "" || job.jobType === filters.jobType) &&
        (filters.tag === "" || job.tags.some((tag) => tag.toLowerCase().includes(filters.tag.toLowerCase()))) &&
        (filters.keyword === "" ||
          job.title.toLowerCase().includes(filters.keyword.toLowerCase()) ||
          job.company.toLowerCase().includes(filters.keyword.toLowerCase()) ||
          job.description.toLowerCase().includes(filters.keyword.toLowerCase()))
      )
    })

    filtered.sort((a, b) => {
      const dateA = new Date(a.datePosted)
      const dateB = new Date(b.datePosted)
      return sortOrder === "newest" ? dateB - dateA : dateA - dateB
    })

    setFilteredJobs(filtered)
  }, [jobs, filters, sortOrder])

  // Add Job
  const handleAddJob = (jobData) => {
    const payload = {
      ...jobData,
      posting_date: new Date().toISOString().split("T")[0],
      tags: jobData.tags.join(","),
    }

    api.post("/jobs", payload)
      .then((res) => {
        setJobs((prev) => [...prev, res.data])
        setShowForm(false)
      })
      .catch((err) => alert("Error adding job"))
  }

  // Edit Job
  const handleEditJob = (jobData) => {
    const payload = {
      ...jobData,
      posting_date: new Date().toISOString().split("T")[0],
      tags: jobData.tags.join(","),
    }

    api.put(`/jobs/${editingJob.id}`, payload)
      .then((res) => {
        setJobs((prev) =>
          prev.map((job) => (job.id === editingJob.id ? res.data : job))
        )
        setEditingJob(null)
        setShowForm(false)
      })
      .catch((err) => alert("Error updating job"))
  }

  // Delete Job
  const handleDeleteJob = (id) => {
    if (!window.confirm("Are you sure?")) return

    api.delete(`/jobs/${id}`)
      .then(() => {
        setJobs((prev) => prev.filter((job) => job.id !== id))
      })
      .catch((err) => alert("Error deleting job"))
  }

  const startEditing = (job) => {
    setEditingJob(job)
    setShowForm(true)
  }

  return (
    <div className="App">
      <Navbar />

      <div className="container">
        <div className="header-section">
          <h1>Find Your Dream Job</h1>
          <p>Discover amazing opportunities with top companies</p>
          <button
            className="btn-primary"
            onClick={() => {
              setShowForm(true)
              setEditingJob(null)
            }}
          >
            Post a Job
          </button>
        </div>

        {showForm && (
          <div className="modal-overlay">
            <div className="modal">
              <JobForm
                job={editingJob}
                onSubmit={editingJob ? handleEditJob : handleAddJob}
                onCancel={() => {
                  setShowForm(false)
                  setEditingJob(null)
                }}
              />
            </div>
          </div>
        )}

        <div className="controls-section">
          <FilterBar filters={filters} onFilterChange={setFilters} />
          <SortDropdown sortOrder={sortOrder} onSortChange={setSortOrder} />
        </div>

        <JobList jobs={filteredJobs} onEdit={startEditing} onDelete={handleDeleteJob} />
      </div>
    </div>
  )
}

export default Home
