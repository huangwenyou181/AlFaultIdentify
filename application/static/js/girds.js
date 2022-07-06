window.onload = function () {
    initGraph("Select ALL");
    createListNode();
    listHeightAdapt();
}

window.onresize = function () {
    var temp = document.getElementsByClassName("selectListSpan");
    var w = document.getElementsByClassName("selectList")[0].offsetHeight;
    for (let sp of temp)
        sp.style.lineHeight = w + "px";
    echarts.init(document.getElementById("graph")).resize();
}

function listHeightAdapt() {
    var temp = document.getElementsByClassName("selectListSpan");
    var w = document.getElementsByClassName("selectList")[0].offsetHeight;
    for (let sp of temp)
        sp.style.lineHeight = w + "px";
}

function selectListChg(obj) {
    var objs = document.getElementsByClassName("selectList");
    var flag = obj.style.backgroundColor == '#ffffff';
    if (flag == 1) return;
    for (let item of objs) {
        if (obj == item)
            item.style.backgroundColor = "#ffffff";
        else
            item.style.backgroundColor = "#cfcfcf";
    }
    var uname = obj.getElementsByTagName("span")[0].innerHTML;
    console.log(uname);
    var postData = {
        "name": uname
    }
    var ReData = $.ajax({
        url: '/getGraphData',
        type: 'POST',
        async: false,
        data: uname,
        processData: false,
        //contentType: "application/json",
        success: function (data) {
        },
        error: function (data) {
        }
    }).responseJSON;
}


//test data
let base = new Date(2022, 2, 1, 0, 0, 0, 1);
let oneDay = 24 * 3600 * 1000;
let onems = 1;
let date = [];
let data = [[], [], [], []];
let dateStr = base.toJSON();
for (let i = 1; i < 200; i++) {
    base.setDate(base.getDate() + 1);
    date.push([base.getFullYear(), base.getMonth(), base.getDate()].join('/'));
    data[0].push(Math.round(Math.random() * 20));
    data[1].push(Math.round(Math.random() * 20));
    data[2].push(Math.round(Math.random() * 20));
    data[3].push(Math.round(Math.random() * 20));
}

var testJson = {
    length: 2,
    
}

function initGraph(uname) {
    
    var ReData = $.ajax({
        url: '/getGraphData',
        type: 'POST',
        async: false,
        data: uname,
        processData: false,
        //contentType: "application/json",
        success: function (data) {
        },
        error: function (data) {
        }
    }).responseJSON;

    data = ReData['data']
    date = ReData['date']
    console.log(date)
    console.log(data)

    var mychart = echarts.init(document.getElementById("graph"));
    var option = {
        tooltip: {
            trigger: 'axis',
            position: function (pt) {
                return [pt[0], '10%'];
            }
        },
        toolbox: {
            feature: {
                dataZoom: { yAxisIndex: 'none' },
                restore: {},
                saveAsImage: {}
            }
        },
        xAxis: { type: 'category', boundaryGap: false, data: date },
        yAxis: { type: 'value', boundaryGap: [0, '100%'] },
        dataZoom: [{ start: 0, end: 10 }],
        series: [
            { name: '脏污', type: 'line', symbol: 'none', sampling: 'lttb', areaStyle: {}, data: data[0] },
            { name: '针孔', type: 'line', symbol: 'none', sampling: 'lttb', areaStyle: {}, data: data[1] },
            { name: '褶皱', type: 'line', symbol: 'none', sampling: 'lttb', areaStyle: {}, data: data[2] },
            { name: '擦伤', type: 'line', symbol: 'none', sampling: 'lttb', areaStyle: {}, data: data[3] },
        ]
    };
    option && mychart.setOption(option);
}

function createListNode() {
    var ul = document.getElementById("selectUL");
    var topli = document.createElement("li");
    var lidav = document.createElement("div");
    var liSp = document.createElement("span");
    liSp.innerHTML = "Select ALL";
    lidav.appendChild(liSp);
    lidav.setAttribute("class", "selectListSpan");
    topli.appendChild(lidav);
    topli.setAttribute("class", "selectList");
    topli.setAttribute("onclick", "selectListChg(this)");
    topli.setAttribute("style", "background-color: #ffffff;")
    ul.appendChild(topli);
    var nameList = $.ajax({
        url: '/grids',
        type: 'POST',
        async: false,
        data: "",
        processData: false,
        success: function (data) {
            
        },
        error: function (data) {
            
        }
    }).responseJSON;
    for (let item of nameList['namelist'])
    {
        topli = document.createElement("li");
        lidav = document.createElement("div");
        liSp = document.createElement("span");
        liSp.innerHTML = item;
        lidav.appendChild(liSp);
        lidav.setAttribute("class", "selectListSpan");
        topli.appendChild(lidav);
        topli.setAttribute("class", "selectList");
        topli.setAttribute("onclick", "selectListChg(this)");
        ul.appendChild(topli);
    }
}