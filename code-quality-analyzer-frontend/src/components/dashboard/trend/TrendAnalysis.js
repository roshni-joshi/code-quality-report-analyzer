import React, { useContext, useEffect, useState } from 'react'
import './trend-analysis.css'
import Architechture from '../../trendAnalysis/Architechture'
import Design from '../../trendAnalysis/Design'
import Implementation from '../../trendAnalysis/Implementation'
import Test from '../../trendAnalysis/Test'
import Testability from '../../trendAnalysis/Testability'
import CommonChart from '../../trendAnalysis/CommonChart'
import { TrendAnalysisContext } from '../../../TrendAnalysisContext'
import { OneCommitAnalysisContext } from '../../../OneCommitAnalysisContext'
import axios from 'axios'
import api from '../../../utils/api'
import Select from 'react-select'
import Loader from '../../loader/Loader'

const TrendAnalysis = (props) => {
  const { trendAnalysisData, setTrendAnalysisData } =
    useContext(TrendAnalysisContext)
  const { analysisData } = useContext(OneCommitAnalysisContext)
  const [isLoading, setIsLoading] = useState(false)
  const [repoLink, setRepoLink] = useState(localStorage.getItem('repoLink'))
  const [branch, setBranch] = useState()
  const { fetchBranches, fetchCommits } = api()
  const Sbranch = JSON.parse(localStorage.getItem('trendBranch') || '{}')
  const [errorMessage, setErrorMessage] = useState('')
  const commits = trendAnalysisData?.commit_changes
    ? Object.keys(trendAnalysisData.commit_changes)
    : []

  useEffect(() => {
    const currentRepoLink = localStorage.getItem('repoLink')
    const currentBranchString = localStorage.getItem('trendBranch')
    const currentBranchObject = currentBranchString
      ? JSON.parse(currentBranchString)
      : null
    const currentBranchValue = currentBranchObject
      ? currentBranchObject.value
      : ''
    const currentMaxCommits = localStorage.getItem('maxCommits')

    if (!trendAnalysisData || currentRepoLink !== repoLink) {
      setIsLoading(true)

      const requestData = {
        gitRepoLink: currentRepoLink,
        branch: currentBranchValue,
        noOfCommits: currentMaxCommits,
      }

      axios
        .post(
          process.env.REACT_APP_BACKEND_URL + '/trend/getanalysis',
          requestData,
          {
            headers: {
              'Content-Type': 'application/json',
            },
          }
        )
        .then((response) => {
          setIsLoading(false)
          if (response.status === 200) {
            setTrendAnalysisData(response.data)
            if (!analysisData) {
              fetchLatestCommit(currentBranchObject)
            }
          }
        })
        .catch((error) => {
          console.error('Failed to fetch trend analysis data:', error)
        })

      setRepoLink(currentRepoLink)
    } else {
      if (!analysisData) {
        fetchLatestCommit(currentBranchObject)
      }
    }
    setSelectedBranch(Sbranch)
    fetchB()
  }, [trendAnalysisData, setTrendAnalysisData, repoLink])
  const fetchB = async () => {
    var B = await fetchBranches(repoLink)
    setBranch(B)
  }

  const fetchLatestCommit = async (branchSelected) => {
    if (branchSelected) {
      const commits = await fetchCommits(repoLink, branchSelected)
      localStorage.setItem('oneCommitBranch', JSON.stringify(branchSelected))
      localStorage.setItem('commit', JSON.stringify(commits[0]))
    }
  }

  const [selectedBranch, setSelectedBranch] = useState(null)
  const [numberOfCommits, setNumberOfCommits] = useState(10)
  const [selectedUser, setSelectedUser] = useState('')

  const handleBranchChange = (event) => {
    setSelectedBranch(event.target.value)
  }

  const handleUserChange = (event) => {
    setSelectedUser(event.target.value)
  }

  const handleCommitsChange = (event) => {
    setNumberOfCommits(parseInt(event.target.value))
  }

  const handleExecuteQuery = () => {
    setIsLoading(true)
    const requestData = {
      gitRepoLink: repoLink,
      branch: selectedBranch.value,
      noOfCommits: numberOfCommits,
    }
    console.log(requestData)
    axios
      .post(
        process.env.REACT_APP_BACKEND_URL + '/trend/getanalysis',
        requestData,
        {
          headers: {
            'Content-Type': 'application/json',
          },
        }
      )
      .then((response) => {
        console.log(response.data)
        if (response.status === 200) {
          setIsLoading(false)
          setTrendAnalysisData(response.data)
          localStorage.setItem('trendBranch', JSON.stringify(selectedBranch))
          if (!analysisData) {
            fetchLatestCommit(selectedBranch)
          }
        }
      })
      .catch((error) => {
        setErrorMessage('Failed to load analysis. Try again later.')
      })
  }
  return (
    <>
      {isLoading && (
        <div className="loading-overlay">
          <div className="loading-spinner"></div>
          <div className="loading-content">
            <p>Updating Analysis</p>
          </div>
        </div>
      )}
      {!isLoading ? (
        trendAnalysisData && (
          <div className="trend-analysis-container">
            <div className="trend-heading">
              <h1>Code Smell Trend Analysis</h1>
            </div>
            <div className="branch commits-dropdown dropdown-container">
              <div className="branch-container">
                <h4>Branches:</h4>
                <Select
                  value={selectedBranch}
                  onChange={(option) => {
                    setSelectedBranch(option)
                  }}
                  options={branch}
                  isSearchable={true}
                  placeholder=" Branch..."
                />

                <button
                  className={`trend_button ${isLoading ? 'loading' : ''}`}
                  onClick={handleExecuteQuery}
                  disabled={isLoading}
                >
                  Update Analysis
                </button>
              </div>
              <div className="commits-container">
                <h4>Number of Commits:</h4>
                <select
                  name=""
                  id=""
                  onChange={handleCommitsChange}
                  defaultValue={10}
                >
                  {[...Array(10)].map((_, index) => (
                    <option key={index} value={index + 1}>
                      {index + 1}
                    </option>
                  ))}
                </select>
              </div>
            </div>
            <div className="trend-smell-charts">
              <CommonChart
                data={trendAnalysisData}
                numberOfCommits={numberOfCommits}
              />
              <Architechture
                data={trendAnalysisData}
                commits={commits}
                numberOfCommits={numberOfCommits}
              />
              <Design
                data={trendAnalysisData}
                commits={commits}
                numberOfCommits={numberOfCommits}
              />
              <Implementation
                data={trendAnalysisData}
                commits={commits}
                numberOfCommits={numberOfCommits}
              />
              <Test
                data={trendAnalysisData}
                commits={commits}
                numberOfCommits={numberOfCommits}
              />
              <Testability
                data={trendAnalysisData}
                commits={commits}
                numberOfCommits={numberOfCommits}
              />
            </div>
          </div>
        )
      ) : (
        <div className="loading">
          <h2></h2>
        </div>
      )}
    </>
  )
}

export default TrendAnalysis
