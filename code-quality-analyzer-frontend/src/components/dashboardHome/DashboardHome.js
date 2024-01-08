import React from 'react'
import './dashboard-home.css'
import Sidebar from '../sidebar/Sidebar'
import OneCommitDashboard from '../dashboard/oneCommit/OneCommitDashboard'
import HotspotAnalysis from '../dashboard/hotspot/HotspotAnalysis'
import TrendAnalysis from '../dashboard/trend/TrendAnalysis'
import { useParams } from 'react-router'

function DashboardHome(props) {
  const { chartType } = useParams()
  let chart
  if (chartType === 'oneCommit') {
    chart = <OneCommitDashboard />
  } else if (chartType === 'trend') {
    chart = <TrendAnalysis />
  } else if (chartType === 'hotspot') {
    chart = <HotspotAnalysis />
  } 
  else {
    chart = <OneCommitDashboard />
  }
  return (
    <>
      <div className="dashboardHome">
        <Sidebar />
        {chart}
      </div>
    </>
  )
}

export default DashboardHome
