import React, { useState, useEffect, useRef } from 'react'
import { Bar } from 'react-chartjs-2'

function HotspotChart(props) {
  const [data, setData] = useState({})
  const [selectedData, setSelectedData] = useState(
    props.hotspotAnalysisData.top_classes_list
  )
  const packagesRef = useRef([])
  const selectedDataRef = useRef(selectedData)

  useEffect(() => {
    const prepareData = () => {
      const selectedChartData = selectedData

      const packages = selectedChartData.map((item) => {
        return Object.keys(item)[0]
      })
      packagesRef.current = packages // Use useRef to store the packages

      const datasets = [
        {
          label: 'Total Smells',
          data: selectedChartData.map((item) => item[Object.keys(item)[0]]),
          backgroundColor: '#' + ((Math.random() * 0xffffff) << 0).toString(16),
        },
      ]

      let totalSmells = datasets.reduce((acc, dataset) => {
        dataset.data.forEach((item, index) => {
          let totalSmellForItem = Object.values(item.smell_distribution).reduce(
            (a, b) => a + b,
            0
          )
          acc[index] = (acc[index] || 0) + totalSmellForItem
        })
        return acc
      }, [])

      datasets.push({
        type: 'line',
        label: 'Total Smell',
        data: totalSmells,
        fill: false,
        backgroundColor: '#373030',
        borderColor: 'rgb(0,0,0)',
      })

      // Extract smell distribution labels
      const smellDistributionLabels = Object.keys(
        selectedChartData[0][packages[0]].smell_distribution
      )

      // Create a dataset for each smell distribution label

      smellDistributionLabels.forEach((label) => {
        const smellDistributionData = selectedChartData.map(
          (item) => item[Object.keys(item)[0]].smell_distribution[label]
        )
        datasets.push({
          label: label,
          data: smellDistributionData,
          // backgroundColor: '#' + ((Math.random() * 0xffffff) << 0).toString(16),
          backgroundColor: `rgba(${Math.random() * 255},${
            Math.random() * 255
          },${Math.random() * 255},0.5)`,
        })
      })

      setData({
        labels: packages.map((label) => {
          // Truncate the labels for display
          const parts = label.split('||')
          return parts[parts.length - 1] // Display the last part
        }),

        // I want to remove the label of "Total Smells" from the data
        datasets: datasets.filter(
          (dataset) => dataset.label !== 'Total Smells'
        ),
      })
    }
    selectedDataRef.current = selectedData
    prepareData()
  }, [selectedData])

  return (
    <div className="hotspot-container">
      <div className="test">
        <div className="common-heading">
          <h2>
            {selectedData === props.hotspotAnalysisData.top_classes_list
              ? 'Classes'
              : 'Methods'}{' '}
            Smell Details
          </h2>
        </div>
        {/* Dropdown to select the user */}
        <div className="user-dropdown">
          <select
            onChange={(event) =>
              setSelectedData(props.hotspotAnalysisData[event.target.value])
            }
          >
            {props.hotspotAnalysisData &&
              Object.keys(props.hotspotAnalysisData).map((item, index) => (
                <option key={index} value={item}>
                  {item}
                </option>
              ))}
          </select>
        </div>
      </div>

      <div
        style={{
          display: 'flex',
          justifyContent: 'center0',
          alignItems: 'center',
          width: '1200px',
          marginLeft: '20px',
          height: '100%',
        }}
      >
        {data.labels && data.labels.length > 0 && (
          <Bar
            data={data}
            options={{
              scales: {
                x: {
                  stacked: true,
                  title: {
                    display: true,
                    text:
                      selectedData ===
                      props.hotspotAnalysisData.top_classes_list
                        ? 'Classes'
                        : 'Methods',
                    font: {
                      size: 20,
                    },
                  },
                },
                y: {
                  stacked: true,
                  title: {
                    display: true,
                    text: 'Number of Smells',
                    font: {
                      size: 20,
                    },
                  },
                },
              },
              plugins: {
                title: {
                  display: true,
                  font: {
                    size: 20,
                  },
                },
                legend: {
                  position: 'right',
                },
                tooltip: {
                  callbacks: {
                    label: function (context) {
                      const labelIndex = context.dataIndex
                      const datasetLabel = context.dataset.label
                      const originalLabel = packagesRef.current[labelIndex]
                      const splitLabel = originalLabel.split('||')
                      const isClass =
                        selectedDataRef.current ===
                        props.hotspotAnalysisData.top_classes_list
                      const classOrMethodLabel = isClass ? 'Class' : 'Method'
                      const classNameOrMethodName = isClass
                        ? splitLabel[2]
                        : splitLabel[splitLabel.length - 1]
                      return [
                        `${datasetLabel}: ${context.parsed.y}`,
                        `Project: ${splitLabel[0]}`,
                        `Package: ${splitLabel[1]}`,
                        `${classOrMethodLabel}: ${classNameOrMethodName}`,
                      ]
                    },
                  },
                },
              },
            }}
            height={window.innerHeight}
            width={window.innerWidth}
          />
        )}
      </div>
    </div>
  )
}

export default HotspotChart
