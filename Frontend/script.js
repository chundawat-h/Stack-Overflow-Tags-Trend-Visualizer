async function renderChart() {
    const response = await fetch("http://127.0.0.1:5000/top-tags");
    const data = await response.json();
  
    const ctx = document.getElementById('lineChart').getContext('2d');
    new Chart(ctx, {
      type: 'line',
      data: {
        labels: data.labels,
        datasets: data.datasets
      },
      options: {
        responsive: true,
        plugins: {
          title: {
            display: true,
            text: 'Relative Popularity of Top 10 Tags (%)'
          }
        },
        scales: {
          y: {
            beginAtZero: true,
            title: {
              display: true,
              text: 'Popularity (%)'
            }
          },
          x: {
            title: {
              display: true,
              text: 'Year'
            }
          }
        }
      }
    });
  }
  
  renderChart();
  