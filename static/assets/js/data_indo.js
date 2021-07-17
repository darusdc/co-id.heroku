var ctx=document.getElementById('barPlot');
                    var barPlot= new Chart(ctx, {
                        type: 'horizontalBar',
                        data: {
                            labels: ['Jakarta', 'West Java', 'Central Java', 'East Java', 'Banten', 'Special Region of Yogyakarta', 'East Kalimantan', 'Papua', 'East Nusa Tenggara', 'West Sumatra', 'Central Kalimantan', 'Riau', 'Riau Islands', 'North Sumatra', 'South Sulawesi', 'Bali', 'South Sumatra', 'Lampung', 'West Kalimantan', 'West Papua', 'Maluku', 'Bangka Belitung Islands', 'Bengkulu', 'Jambi', 'North Sulawesi', 'South Kalimantan', 'North Kalimantan', 'North Maluku', 'Central Sulawesi', 'West Nusa Tenggara', 'Southeast Sulawesi', 'West Sulawesi', 'Gorontalo'],
                            datasets: [{
                                label:' # Active cases',
                                data: [113082, 110834, 56943, 38288, 25019, 24614, 14036, 11070, 8912, 7849, 7409, 7196, 6886, 6469, 5805, 5803, 5225, 5107, 4278, 4217, 3951, 3609, 2828, 2823, 2709, 2616, 2580, 2532, 2201, 2187, 2143, 838, 660],
                                backgroundColor: ['#3DB40F', '#E8F51C', '#0E9873', '#9F1CB4', '#CDF3EC', '#D68544', '#D7FDEB', '#55D152', '#CA840D', '#501A87', '#6DF551', '#61CDF5', '#CA3752', '#1C3A38', '#1A977E', '#A49345', '#12A1BF', '#AD9F7C', '#629DC7', '#2BD0F4', '#ED32EE', '#4B7C71', '#6D016C', '#DB3CC8', '#9DAFDE', '#44B49E', '#045BBC', '#2F3100', '#95AFE0', '#C449D7', '#9F891C', '#37350F', '#3F078C', '#E7796A'],
                                borderWidth:1
                            }]
                        },
                        options:{
                            elements: {
                            rectangle: {
                                borderWidth: 2,
                            }
                        },
                        responsive: true,
                        legend: {
                            position: 'right',
                        },
                        title: {
                            display: true,
                            text: 'Rank of Active Cases by Province'
                        }
                    }
                    }
                    )