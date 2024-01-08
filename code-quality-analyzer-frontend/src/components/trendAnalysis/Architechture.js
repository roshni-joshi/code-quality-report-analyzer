import React, { useState, useEffect } from 'react';
import { Line } from 'react-chartjs-2';
import PropTypes from 'prop-types';

const Architechture = ({ data, commits, numberOfCommits }) => {
  const selectedSmell = 'Architecture Smell'; // Keep this as a constant
  const [selectedDataSource, setSelectedDataSource] = useState('full_repo'); // State for selecting data source

  const subtypes = Object.keys(
    data[selectedDataSource][commits[0]][selectedSmell].smell_distribution
  );

  const chartDataForSubtype = {
    labels: commits.slice(-numberOfCommits),
    datasets: subtypes.map((subtype) => ({
      label: subtype,
      data: commits
        .slice(-numberOfCommits)
        .map((commit) =>
          selectedSmell
            ? data[selectedDataSource][commit][selectedSmell].smell_distribution[subtype]
            : 0
        ),
      fill: false,
      backgroundColor: getRandomColor(),
    })),
  };

  const options = {
    scales: {
      x: {
        beginAtZero: true,
        title: {
          display: true,
          text: 'Commit Id',
          font: {
            size: 20,
          }
        }
      },
      y: {
        beginAtZero: true,
        title: {
          display: true,
          text: 'Number of Smells',
          font: {
            size: 20,
          }
        }
      },
    },
    plugins: {
      legend: {
        position: 'right',
        labels: {
          font: {
            size: 14
          }
        }
      }
    }
  }

  function getRandomColor() {
    const letters = '0123456789ABCDEF'
    let color = '#'
    for (let i = 0; i < 6; i++) {
      color += letters[Math.floor(Math.random() * 16)]
    }
    return color
  }

  const handleDataSourceChange = (event) => {
    setSelectedDataSource(event.target.value)
  }

  useEffect(() => {
    // This block will re-run whenever numberOfCommits changes
  }, [numberOfCommits]);

  return (
    <div className="chart-container">
      <div className="test">
        <h2>Architecture Smell</h2>

        {/* Dropdown to select the data source (full_repo or commit_changes) */}
        <div className="dropdowns-container">
          <div className="dropdown-container">
            <select
              value={selectedDataSource}
              onChange={handleDataSourceChange}
            >
              <option value="commit_changes">Commit Changes</option>
              <option value="full_repo">Full Repository</option>
            </select>
          </div>
        </div>
      </div>

      {/* Render the Line chart for all subtypes */}
      <Line data={chartDataForSubtype} options={options} />
    </div>
  );
}

Architechture.propTypes = {
  data: PropTypes.object.isRequired,
  commits: PropTypes.array.isRequired,
  numberOfCommits: PropTypes.number.isRequired,
}

export default Architechture;
