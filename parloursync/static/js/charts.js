/* charts.js - Chart.js configurations for business intelligence & analytics dashboard */

document.addEventListener('DOMContentLoaded', () => {
    // Helper to format currency
    const formatCurrency = (val) => {
        return new Intl.NumberFormat('en-US', {
            style: 'currency',
            currency: 'USD',
            maximumFractionDigits: 0
        }).format(val);
    };

    // 1. Monthly Revenue Chart (Bar/Line Chart)
    const revCtx = document.getElementById('revenueChart');
    if (revCtx) {
        new Chart(revCtx, {
            type: 'line',
            data: {
                labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
                datasets: [{
                    label: 'Revenue',
                    data: [1200, 1900, 3000, 5000, 4800, 6200, 7500, 7200, 8100, 9500, 11000, 14200],
                    borderColor: '#4f46e5', // Indigo-600
                    backgroundColor: 'rgba(79, 70, 229, 0.05)',
                    fill: true,
                    tension: 0.4,
                    borderWidth: 2,
                    pointRadius: 4,
                    pointBackgroundColor: '#4f46e5'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return 'Revenue: ' + formatCurrency(context.raw);
                            }
                        }
                    }
                },
                scales: {
                    y: {
                        grid: {
                            color: 'rgba(148, 163, 184, 0.08)'
                        },
                        ticks: {
                            callback: function(value) {
                                return formatCurrency(value);
                            }
                        }
                    },
                    x: {
                        grid: {
                            display: false
                        }
                    }
                }
            }
        });
    }

    // 2. Booking Status Chart (Doughnut Chart)
    const statusCtx = document.getElementById('bookingStatusChart');
    if (statusCtx) {
        // Read data attributes or defaults
        const pending = parseInt(statusCtx.getAttribute('data-pending') || '0', 10);
        const confirmed = parseInt(statusCtx.getAttribute('data-confirmed') || '0', 10);
        const completed = parseInt(statusCtx.getAttribute('data-completed') || '0', 10);
        const cancelled = parseInt(statusCtx.getAttribute('data-cancelled') || '0', 10);

        new Chart(statusCtx, {
            type: 'doughnut',
            data: {
                labels: ['Pending', 'Confirmed', 'Completed', 'Cancelled'],
                datasets: [{
                    data: [
                        pending || 5, 
                        confirmed || 12, 
                        completed || 28, 
                        cancelled || 3
                    ],
                    backgroundColor: [
                        '#f59e0b', // Yellow-500
                        '#3b82f6', // Blue-500
                        '#10b981', // Emerald-500
                        '#ef4444'  // Red-500
                    ],
                    borderWidth: 0,
                    hoverOffset: 4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            boxWidth: 12,
                            padding: 15,
                            font: {
                                size: 11
                            }
                        }
                    }
                },
                cutout: '70%'
            }
        });
    }

    // 3. Service Distribution Chart
    const serviceCtx = document.getElementById('serviceDistributionChart');
    if (serviceCtx) {
        new Chart(serviceCtx, {
            type: 'bar',
            data: {
                labels: ['Haircut', 'Coloring', 'Styling', 'Facial', 'Massage', 'Manicure'],
                datasets: [{
                    data: [42, 28, 19, 15, 12, 8],
                    backgroundColor: '#dfac6c', // Gold/Warm color
                    borderRadius: 6,
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    }
                },
                scales: {
                    y: {
                        grid: {
                            color: 'rgba(148, 163, 184, 0.08)'
                        }
                    },
                    x: {
                        grid: {
                            display: false
                        }
                    }
                }
            }
        });
    }
});
