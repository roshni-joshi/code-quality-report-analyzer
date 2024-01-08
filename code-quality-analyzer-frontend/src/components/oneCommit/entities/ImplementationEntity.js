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

function ImplementationEntity({implementationEntityData}) {
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
    const topEntities = implementationEntityData?.['Implementation Smell']?.['top_entities'];
  
    // Check if topEntities is defined and not null
    if (topEntities) {
      const labels = Object.keys(topEntities).map((key) => {
        const parts = key.split('||');
        const lastPart = parts[parts.length - 1];
        return lastPart;
      });
  
      const values = Object.values(topEntities);
      
      // Ensure labels is an array before using map
      if (Array.isArray(labels)) {
        const backgroundColor = labels.map(() => getRandomColor());
  
        setChartData({
          labels: labels,
          datasets: [
            {
              label: 'Design Entity',
              data: values,
              backgroundColor,
            },
          ],
        });
      }
    }
  }, [implementationEntityData]);

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
        text: 'Implementation Entities',
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

export default ImplementationEntity
