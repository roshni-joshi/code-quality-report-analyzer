import React, { useState, useEffect } from 'react'
import { Bar } from 'react-chartjs-2'

function CommonChart(props) {
  const [data, setData] = useState({})
  const [selectedData, setSelectedData] = useState(props.data.full_repo);

  const users = [...new Set(Object.values(selectedData).map((category) => {
    return category.user
  }))];


  const [selectedUser, setSelectedUser] = useState(users[0]);
  const [selectedDensity, setSelectedDensity] = useState('full_repo_smell_density');

  // JSON data provided
  const jsonData = props.data

  const handleDataChange = (event) => {
    setSelectedData(props.data[event.target.value])
  }

  const handleUserChange = (event) => {
    setSelectedUser(event.target.value)
  }

  useEffect(() => {
    const prepareData = () => {
      const selectedChartData = selectedData
      const cat = [];
      Object.values(selectedChartData).map((category) => {
    
        cat.push(Object.keys(category).filter(
          (category) => category !== 'total_smells' && category !== 'user'
        ));
      })
      const categories = [...new Set(cat.flat())];
      const commits = Object.keys(selectedChartData).slice(
        0,
        props.numberOfCommits
      ) // Limit commits
      
      const totalSmells = commits.map((commit) => {
        if (
          selectedChartData &&
          selectedChartData[commit] &&
          selectedChartData[commit].user === selectedUser
        ) {
          return selectedChartData[commit].total_smells;
        }
        return 0;
      });

      const datasets = categories.map((category) => {
        const dataPoints = commits.map((commit) => {
          if (
            selectedChartData &&
            selectedChartData[commit] &&
            selectedChartData[commit][category] &&
            selectedChartData[commit].user === selectedUser
          ) {
            return selectedChartData[commit][category].total_smells
          }
          return 0
        })

        return {
          label: category,
          data: dataPoints,
          backgroundColor: '#' + ((Math.random() * 0xffffff) << 0).toString(16),
        }
      })

      datasets.push({
        type: 'line',
        label: 'Total Smells',
        data: totalSmells,
        fill: false,
        backgroundColor: '#373030',
        borderColor: 'rgb(0,0,0)',
        tension: 0.1,
      });

      setData({
        labels: commits,
        datasets: datasets,
      })
    }

    prepareData(jsonData)
  }, [selectedData, props.numberOfCommits, selectedUser, selectedDensity])

  return (
    <div>
      <div className="test">
        <div className="common-heading">
          <h2>Smell Details</h2>
        </div>
        <div className="common-dropdown">
          <select onChange={handleDataChange}>
            <option value="full_repo">Full Repository</option>
            <option value="commit_changes">Commit Changes</option>
            <option value="full_repo_smell_density">Smell Density</option>
          </select>
        </div>
        {/* Dropdown to select the user */}
        <div className="user-dropdown">
          <select onChange={handleUserChange}>
            {
              users.map((user) => {
                return <option key={user} value={user}>{user}</option>
              })
            }
          </select>
        </div>
      </div>
      <div>
        {data.labels && data.labels.length > 0 && (
          <Bar
            data={data}
            options={{
              scales: {
                x: { stacked: true, title: {
                  display: true,
                  text: 'Commit ID',
                  font: {
                    size: 20,
                  }
                } },
                y: { stacked: true,
                  title: {
                    display: true,
                    text: 'Smell Count',
                    font: {
                      size: 20,
                    }
                  } },
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
            }}
          />
        )}
      </div>
    </div>
  )
}

export default CommonChart
