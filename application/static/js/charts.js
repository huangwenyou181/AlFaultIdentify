var testJson = {
    "length": "2",
    "results": [
        {
            "len": "2",
            "user": "admin",
            "src": "test.jpg",
            "result": [
                {
                    "class": "zhang_wu",
                    "score": "0.999",
                    "max_x": "1",
                    "min_x": "2",
                    "max_y": "3",
                    "min_y": "4"
                },
                {
                    "class": "zhang_wu",
                    "score": "0.999",
                    "max_x": "1",
                    "min_x": "2",
                    "max_y": "3",
                    "min_y": "4"
                }
            ]
        },
        {
            "len": "2",
            "user": "admin",
            "src": "test.jpg",
            "result": [
                {
                    "class": "zhang_wu",
                    "score": "0.999",
                    "max_x": "1",
                    "min_x": "2",
                    "max_y": "3",
                    "min_y": "4"
                },
                {
                    "class": "zhang_wu",
                    "score": "0.999",
                    "max_x": "1",
                    "min_x": "2",
                    "max_y": "3",
                    "min_y": "4"
                }
            ]
        }
    ]
}

function getResultTab(obj) {
    reTabInner = '<h4 class="tittle-w3-agileits mb-4">Result</h4>';
    console.log(obj)
    for (let i in obj.results) {
        var num = parseInt(i) + 1;
        var colid = 'collapse' + num;
        reTabInner += '<div class="reWrapper container-fluid"><div><div class="inline-box">' +
            '<img src="' + obj.results[i]["src"] + '" style="height: 120px; width: 160px;" class="reimg"></div>' +
            '<div class="inline-box reTabWrapper"><table class="table reTab"><tbody><tr class="tabFirstLine">' +
            '<th>No.</th>' + '<td class="text-center">' + num + '</td></tr>' +
            '<tr><th>Num</th>' + '<td class="text-center">' + obj.results[i]["len"] + '</td></tr>' +
            '<tr class="tabLastLine"><th>User</th><td class="text-center">' + obj.results[i]["user"] + '</td></tr></tbody></table></div>' +
            '<div class="text-center"><a data-toggle="collapse" href="' + '#' + colid + '">details</a></div></div>' +
            '<div id="' + colid + '" class="panel-collapse collapse">';

        var reNum = parseInt(obj.results[i].len) - 1;
        for (let j in obj.results[i].result) {
            reTabInner += '<div class="detailTab"><div style="border-bottom: 1px solid #d8d8d8;" class="deTabReWarp row';
            reTabInner += j == 0 ? ' top-border-radius">' : '">';
            reTabInner += '<div class="col text-center" >坐标:</div><div class="col text-center" >' +
                '(' + obj.results[i].result[j]["min_x"] + ',' + obj.results[i].result[j]["min_y"] + '),' + '(' + obj.results[i].result[j]["max_x"] + ',' + obj.results[i].result[j]["max_y"] + ')' + '</div></div>';
            reTabInner += j == reNum ? '<div class="deTabReWarp row bottom-botder-radius">' : '<div class="deTabReWarp row">';
            reTabInner += '<div class="col text-center">种类:</div>' +
                '<div class="col text-center">' + obj.results[i].result[j]["class"] + '</div></div></div>';
        }
        reTabInner += '</div></div>';
    }
    document.getElementById('resultTable').innerHTML = reTabInner;
}

function tableInit(data) {
    var barWidth = document.getElementById('summary').offsetWidth;
    barWidth = document.getElementsByTagName('body')[0].offsetWidth < 667 ? barWidth - 30 : (barWidth - 45) / 2;
    document.getElementById('chartBar').style.width = barWidth;
    var myBar = echarts.init(document.getElementById("chartBar"));
    var optionBar = {
        dataset: {
            source: [
                ['product', '脏\n污', '褶\n皱', '针\n孔', "擦\n伤"],
                ['amount', data[0], data[1], data[2], data[3]]
            ]
        },
        xAxis: {},
        yAxis: { type: 'category', axisLabel: { fontSize: 15 } },
        series: [
            {
                type: 'bar',
                seriesLayoutBy: 'row',
                label: {
                    fontSize: 16
                }
            },
        ]
    };
    optionBar && myBar.setOption(optionBar);

    var pieWidth = document.getElementById('summary').offsetWidth;
    pieWidth = document.getElementsByTagName('body')[0].offsetWidth < 667 ? pieWidth - 45 : (pieWidth - 45) / 2;
    var myPie = echarts.init(document.getElementById("chartPie"), null, { height: 350, width: pieWidth });
    var optionPie = {
        series: [
            {
                type: 'pie',
                data: [
                    { value: data[0], name: '脏\n污' },
                    { value: data[1], name: '褶\n皱' },
                    { value: data[2], name: '针\n孔' },
                    { value: data[3], name: '擦\n伤' }
                ],
                label: { fontSize: 15 }
            }
        ]
    };
    optionPie && myPie.setOption(optionPie);
}

window.onload = function () {
    returnTab = $.ajax({
        url: '/charts',
        type: 'POST',
        async: false,
        data: "",
        processData: false,
        success: function (data) {
        },
        error: function (data) {
        }
    });
    getResultTab(returnTab.responseJSON);
    tableInit(returnTab.responseJSON.data);
}