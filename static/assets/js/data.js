var ctx=document.getElementById('linePlot');
    var linePlot= new Chart(ctx, {
        type: 'line',
        data: {
            labels: [{%for i in month%} '{{i}}',{%endfor%}],
            datasets: [{
                label: 'New Deaths',
                data: {{deaths}},
                backgroundColor: '#fc0703',fill: true
            }, {
                label: 'New Cases',
                data: {{cases}},
                backgroundColor: '#fcd303',fill: true
            }]
        },
        options:{
            responsive: true,
            tooltips: {mode: 'index',intersect: false,},
            hover: {mode:'nearest',intersect:true},
            scales:{
                xAxes: [{
                    scaleLabel:{
                        display:true,
                        labelString:'Month'
                    }
                }],
                yAxes:[{
                    display: true,
                    scaleLabel:{
                        display: true,
                        labelString:'# Cases'
                    }
                }]
            }
        }
    });
    var data_base= {
    {%for i in country%}
    "{{i}}" : {
        data_m: [{%for y in data.get_group(i).resample('M').mean()['New_deaths']%} {{y|round}},{%endfor%}],
        data_h:[{%for v in data.get_group(i).resample('M').mean()['New_cases']%} {{v|round}},{%endfor%}]
    },
    {%endfor%}
    };
    document.getElementById('negara').onchange= function(){
        var plot=linePlot.config.data;
        var neg=document.getElementById('negara').value;
        plot.datasets[0].data=data_base[neg]['data_m'];
        plot.datasets[1].data=data_base[neg]['data_h'];
        document.getElementById('judul').innerHTML=neg;
        linePlot.update()
    };