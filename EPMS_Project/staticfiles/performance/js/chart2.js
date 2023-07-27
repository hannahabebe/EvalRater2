var ctx2 = document.getElementById('doughnut').getContext('2d');
var myChart2 = new Chart(ctx2, {
    type: 'doughnut',
    data: {
        labels: ['Academic', 'Non-Academic', 'Administration', 'Others'],

        datasets: [{
            label: 'Employees',
            data: [42, 12, 8, 6],
            backgroundColor: [
                'rgba(33, 140, 204, 0.6)',
                'rgba(222, 239, 252, 1)',
                'rgba(120, 245, 245, 0.6)',
                'rgba(211, 211, 211, 1)'

            ],
            borderColor: [
                'rgba(33, 140, 204, 0.6)',
                'rgba(222, 239, 252, 1)',
                'rgba(120, 245, 245, 0.6)',
                'rgba(211, 211, 211, 1)'

            ],
            borderWidth: 1
        }]

    },
    options: {
        responsive: true
    }
});