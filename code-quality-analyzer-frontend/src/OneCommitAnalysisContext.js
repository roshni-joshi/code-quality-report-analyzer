import React, { createContext, useState, useEffect } from 'react'

export const OneCommitAnalysisContext = createContext()

export const OneCommitAnalysisProvider = ({ children }) => {
  const localData = localStorage.getItem('analysisData')
  const [analysisData, setAnalysisData] = useState(
    localData ? JSON.parse(localData) : null
  )

  useEffect(() => {
    if (analysisData) {
      localStorage.setItem('analysisData', JSON.stringify(analysisData))
    }
  }, [analysisData])

  return (
    <OneCommitAnalysisContext.Provider
      value={{ analysisData, setAnalysisData }}
    >
      {children}
    </OneCommitAnalysisContext.Provider>
  )
}
