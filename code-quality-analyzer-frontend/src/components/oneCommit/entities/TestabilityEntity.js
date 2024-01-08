import React, { useEffect, useState } from 'react'
import 'chart.js/auto'
import { Bar } from 'react-chartjs-2'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js'
ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend)

function TestabilityEntity(props) {
  const [chartData, setChartData] = useState({
    labels: [],
    datasets: [
      {
        label: 'Loading Data',
        data: [],
      },
    ],
  })

  function getRandomColor() {
    const r = Math.floor(Math.random() * 256);
    const g = Math.floor(Math.random() * 256);
    const b = Math.floor(Math.random() * 256);
    const opacity = 0.5; // Set any value between 0 and 1
    return `rgba(${r}, ${g}, ${b}, ${opacity})`;
  }

  useEffect(() => {
    const topEntities =
      props.testabilityEntityData?.['Testability Smell']?.['top_entities']
    const values = topEntities ? Object.values(topEntities) : null;

    const labels = topEntities ? Object.keys(topEntities).map((key) => {
      const parts = key.split('||')
      const lastPart = parts[parts.length - 1]
      return lastPart
    }) : null;

    const backgroundColor = labels?.map(() => getRandomColor())

    setChartData({
      labels,
      datasets: [
        {
          label: "Testability Entity",
          data: values,
          backgroundColor: backgroundColor,
        },
      ],
    })
  }, [props.testabilityEntityData])

  const doughnutOptions = {
    scales: {
      x: {
        title: {
          display: true,
          text: 'Package',
          font: {
            size: 16,
          },
        },
      },
      y: {
        title: {
          display: true,
          text: 'Number of Entities',
          font: {
            size: 16,
          },
        },
      },
    },
    plugins: {
      title: {
        display: true,
        text: 'Testability Entities',
        font: {
          size: 20,
        },
      },
      legend: {
        display: true,
        position: 'top',
        labels: {
          font: {
            size: 12,
          },
        },
      },
    },
  }
  return (
    <>
      <div>
        <Bar
          height={'500px'}
          width={'500px'}
          data={chartData}
          options={doughnutOptions}
        />
      </div>
    </>
  )
}

export default TestabilityEntity
