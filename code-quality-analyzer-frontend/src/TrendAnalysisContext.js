// TrendAnalysisContext.js
import React, { createContext, useState, useEffect } from 'react';

export const TrendAnalysisContext = createContext();

export const TrendAnalysisProvider = ({ children }) => {
  const localData = localStorage.getItem('trendAnalysisData');
  const [trendAnalysisData, setTrendAnalysisData] = useState(
    localData ? JSON.parse(localData) : null
  );

  useEffect(() => {
    if (trendAnalysisData) {
      localStorage.setItem('trendAnalysisData', JSON.stringify(trendAnalysisData));
    }
  }, [trendAnalysisData]);

  return (
    <TrendAnalysisContext.Provider value={{ trendAnalysisData, setTrendAnalysisData }}>
      {children}
    </TrendAnalysisContext.Provider>
  );
};
