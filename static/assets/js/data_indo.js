        var ctx=document.getElementById('barPlot');        var dtx=document.getElementById('vbarPlot');        var etx=document.getElementById('piePlot');        var source = {                            labels: ['West Java', 'Central Java', 'Jakarta', 'East Java', 'Special Region of Yogyakarta', 'Banten', 'Lampung', 'North Sumatra', 'North Sulawesi', 'West Sumatra', 'Bali', 'Central Sulawesi', 'South Sumatra', 'Gorontalo', 'West Kalimantan', 'South Kalimantan', 'Papua', 'East Nusa Tenggara', 'Riau', 'Bangka Belitung Islands', 'Riau Islands', 'South Sulawesi', 'East Kalimantan', 'West Papua', 'West Nusa Tenggara', 'Bengkulu', 'Central Kalimantan', 'North Maluku', 'Jambi', 'Southeast Sulawesi', 'North Kalimantan', 'Maluku', 'West Sulawesi'],                            datasets: [{                                label:' # Active cases',                                data: [9938, 3151, 2099, 732, 705, 653, 339, 283, 216, 169, 165, 159, 155, 129, 127, 119, 118, 118, 93, 79, 77, 76, 71, 64, 62, 53, 53, 47, 47, 46, 14, 13, 12],                                backgroundColor: ['#63C755', '#3630A2', '#21EEC9', '#FA7062', '#DE6CEB', '#3219F4', '#F4B4DA', '#17F68B', '#D0E9E3', '#441B35', '#4A3790', '#8D7964', '#C9EA53', '#F773C1', '#30EDCC', '#8295C9', '#26F1F2', '#703F31', '#BA8DF3', '#BAB759', '#390FBD', '#B6F63B', '#8393F1', '#0385F7', '#E56008', '#1616C3', '#4C8C5F', '#C445FB', '#235DFB', '#BFA789', '#ECBBD9', '#14A678', '#574D1D', '#065640'],                                borderWidth:1                            }]                        };        var option={                        animation: {                        onComplete: () => {                        delayed = true;                    },                    delay: (context) => {                        let delay = 0;                        if (context.type === 'data' && context.mode === 'default' && !delayed) {                            delay = context.dataIndex * 300 + context.datasetIndex * 100;                        }                    return delay;                    },                    },                    responsive: true,                    legend: {                        position: 'right',                    },                    title: {                        display: true,                        text: 'Rank of Active Cases by Province'                    }                };                    var barPlot= new Chart(ctx, {                        type: 'horizontalBar',                        data: source,                        options: option                    });                    var vbarPlot= new Chart(dtx, {                        type: 'bar',                        data: source,                        options: option                    });                    var piePlot= new Chart(etx, {                        type: 'pie',                        data: source,                        options: option                    });    