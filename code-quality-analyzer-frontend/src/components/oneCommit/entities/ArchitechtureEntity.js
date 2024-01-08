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

function ArchitechtureEntity({ architectureEntityData }) {
  const [chartData, setChartData] = useState({
    labels: [],
    datasets: [
      {
        label: 'Loading Data',
        data: [],
      },
    ],
  })

  // function getRandomColor() {
  //   const letters = '0123456789ABCDEF';
  //   let color = '#';
  //   for (let i = 0; i < 6; i++) {
  //     color += letters[Math.floor(Math.random() * 16)];
  //   }
  //   return color;
  //  }

  function getRandomColor() {
    const r = Math.floor(Math.random() * 256);
    const g = Math.floor(Math.random() * 256);
    const b = Math.floor(Math.random() * 256);
    const opacity = 0.5; // Set any value between 0 and 1
    return `rgba(${r}, ${g}, ${b}, ${opacity})`;
  }
   
  useEffect(() => {
    if (architectureEntityData && architectureEntityData['Architecture Smell']) {
    const labels = Object.keys(
      architectureEntityData['Architecture Smell']?.['top_entities']
    )

    const values = Object.values(
      architectureEntityData['Architecture Smell']?.['top_entities']
    )

    const backgroundColor = labels.map(() => getRandomColor());

    setChartData({
      labels: labels.map((label) => {
        const splitLabel = label.split('||')
        return splitLabel[splitLabel.length - 1]
      }),
      datasets: [
        {
          label: 'Architecture Entities',
          data: values,
          backgroundColor
        },
      ],
    })
  }
  }, [architectureEntityData])

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
        text: 'Architecture Entities',
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

export default ArchitechtureEntity
