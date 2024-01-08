import React, { createContext, useState, useEffect } from 'react'

export const HotspotAnalysisContext = createContext()

export const HotspotAnalysisProvider = ({ children }) => {
  const localData = localStorage.getItem('hotspotAnalysisData')
  const [hotspotAnalysisData, setHotspotAnalysisData] = useState(
    localData ? JSON.parse(localData) : null
  )

  useEffect(() => {
    if (hotspotAnalysisData) {
      localStorage.setItem('hotspotAnalysisData', JSON.stringify(hotspotAnalysisData))
    }
  }, [hotspotAnalysisData])

  return (
    <HotspotAnalysisContext.Provider
      value={{ hotspotAnalysisData, setHotspotAnalysisData }}
    >
      {children}
    </HotspotAnalysisContext.Provider>
  )
}
