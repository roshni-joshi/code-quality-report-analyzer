import React from 'react';
import Logo from '../../assets/images/logo.png';
import './sidebar.css';
import { Link, useLocation } from 'react-router-dom';

function Sidebar() {
  const location = useLocation();

  const isActive = (path) => {
    return location.pathname.includes(path) ? 'active' : '';
  };

  return (
    <div className="sidebar">
      <div className="logo">
        <Link to={'/'}>
          <img src={Logo} alt="" />
        </Link>
      </div>
      <div className="sidebar-menu-items">
        <Link to={'/dashboard/oneCommit'} className={`oneCommit common-item ${isActive('oneCommit')}`}>
          One Commit
        </Link>
        <Link to={'/dashboard/trend'} className={`trendAnalysis common-item ${isActive('trend')}`}>
          Trend Analysis
        </Link>
        <Link to={'/dashboard/hotspot'} className={`hotspotAnalysis common-item ${isActive('hotspot')}`}>
          Hotspot Analysis
        </Link>
      </div>
    </div>
  );
}

export default Sidebar;
