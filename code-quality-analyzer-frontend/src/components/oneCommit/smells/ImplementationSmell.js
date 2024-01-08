import React, { useEffect, useState } from 'react'
import 'chart.js/auto'
import { Doughnut } from 'react-chartjs-2'
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

function ImplementationSmell({implementationSmellData}) {
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
    if (implementationSmellData && implementationSmellData['Implementation Smell']) {
    const labels = Object.keys(
      implementationSmellData['Implementation Smell']?.[
        'smell_distribution'
      ]
    )

    const values = Object.values(
      implementationSmellData['Implementation Smell']?.[
        'smell_distribution'
      ]
    )

    const backgroundColor = labels.map(() => getRandomColor());

    setChartData({
      labels,
      datasets: [
        {
          label: 'Smells',
          data: values,
          backgroundColor,
          hoverOffset: 4,
        },
      ],
    })
  }
  }, [implementationSmellData])

  const doughnutOptions = {
    plugins: {
      title: {
        display: true,
        text: 'Implementation Smells',
        font: {
          size: 20,
        },
      },
      legend: {
        display: true,
        position: 'left',
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
        <Doughnut
          height={'500px'}
          width={'500px'}
          data={chartData}
          options={doughnutOptions}
        />
      </div>
    </>
  )
}

export default ImplementationSmell
