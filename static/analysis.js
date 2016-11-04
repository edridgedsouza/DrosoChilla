// Default values for date inputs
function defaultInputs() {
    var today = new Date();
    var dd = today.getDate();
    var yesterdd = dd - 1;
    var mm = today.getMonth() + 1; //January is 0!
    var yyyy = today.getFullYear();

    if (dd < 10) {
        dd = '0' + dd;
    }

    if (yesterdd < 10) {
        yesterdd = '0' + yesterdd;
    }

    if (mm < 10) {
        mm = '0' + mm;
    }

    currentday = mm + '/' + dd + '/' + yyyy;
    yesterday = mm + '/' + yesterdd + '/' + yyyy;

    document.getElementById("datepicker1").value = yesterday;
    document.getElementById("datepicker2").value = currentday;
}
defaultInputs();



var df; // Global var. Main df gets loaded once, while scaleDates() returns subsets

function getData() { // Async data loading
    Plotly.d3.tsv("/log", function(data) {
        process(data);
    });
}



function process(rows) { // Parse inputs into arrays
    var time = [],
        temp = [],
        hum = [],
        timesort = [],
        tempsort = [],
        humsort = [];

    for (var i = 0; i < rows.length; i++) {
        currentRow = rows[i];
        time.push(currentRow['time']);
        temp.push(parseFloat(currentRow['temp']));
        hum.push(parseFloat(currentRow['hum']));
    }

    // Remove outlier values where temp and humidity sensor don't work
    while (temp.indexOf(-999) != -1) {
        outlier = temp.indexOf(-999);
        /* Uncomment if you just want to discard these data points
        time.splice(outlier,1)
        temp.splice(outlier,1)
        hum.splice(outlier,1) */
        temp[outlier] = null;
        hum[outlier] = null;
    }

    // Part where we sort time, temp, and hum according to time. For whatever reason, the alternative is Plotly improperly connecting the splines.
    // http://stackoverflow.com/a/13960306
    // We build a list of indices, then rearrange them however `time` will be when fully sorted. Then re-index `time`, `temp`, and `hum` according to the new index order.


    var idx = [];
    for (var j = 0; j < time.length; j++) {
        idx.push(j);
    }
    var comparator = function(arr) {
        return function(a, b) {
            return ((arr[a] < arr[b]) ? -1 : ((arr[a] > arr[b]) ? 1 : 0));
        };
    };
    idx = idx.sort(comparator(time)); // Proper order of indices

    console.log(idx.length, time.length); // Make sure this sort is working as intended

    for (var k = 0; k < time.length; k++) {
        timesort.push(time[idx[k]]);
        tempsort.push(temp[idx[k]]);
        humsort.push(hum[idx[k]]);
    }


    // For debugging purposes
    console.log('Time:', time, time.length, 'Temp:', temp, temp.length, 'Humidity:', hum, hum.length);

    df = [timesort, tempsort, humsort]; // Global, accessible externally from getMostRecent() and graphIt()
    getMostRecent();
}


function getMostRecent() { //Display most recent temperature readings.
    var paragraph = document.getElementById("mostRecent");
    var lastMatch = df[1].length - 1;

    if (df[1][lastMatch] != null) {
        var results = "<span style='color:black'>Date:</span> <b>" + df[0][lastMatch] +
            "</b>; <span style='color:black'>Temperature:</span> <b style='color:rgb(255,122,105)'>" + df[1][lastMatch] +
            "</b>; <span style='color:black'>Humidity:</span> <b style='color:rgba(85,159,255, 0.7)'>" + df[2][lastMatch] + "</b>";
        paragraph.innerHTML = "<span style='color:rgb(150,150,150); font-size:10pt;'>Most recent results:</span> &nbsp;&nbsp;&nbsp;" + results;
    } else {
        paragraph.innerHTML = "<span style='color:rgb(150,150,150);'>Your sensor is returning null measurements. Please ensure that it is properly connected and try again.</span>";
    }


    // Rendering the Download buttons here because we don't want people to click until the data is loaded.

    var buttonHTML = "<button class=\"pure-button pure-button-primary\" style=\"background: rgb(105, 167, 216);\" onclick=\"$('#graph').html(''); graphIt(scaleDates());\">Generate graph</button>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<a id=\"downloader\"><button class=\"pure-button pure-button-primary\" style=\"background: rgb(105, 167, 216);\" onclick=\"downloadify(scaleDates());\">Download data</button></a>";
    document.getElementById("buttons").innerHTML = buttonHTML;
}


function graphIt(dt) { // Not called until button pushed; prevents mishaps with async data loading
    var datetime = dt[0],
        temperature = dt[1],
        humidity = dt[2];
    var plotDiv = document.getElementById("plot"); // Doesn't seem to be used but it was in the tutorial so I'm keeping it.
    var tempTrace = {
        x: datetime,
        y: temperature,
        name: "Temperature",
        type: 'scatter',
        //mode: 'lines+markers',
        line: { shape: 'spline', width: 4 },
        marker: { color: 'rgb(255,122,105)' }
    };

    var humTrace = {
        x: datetime,
        y: humidity,
        name: "Humidity",
        yaxis: 'y2',
        type: 'scatter',
        //mode: 'lines+markers',
        line: { shape: 'spline', width: 2 },
        marker: { color: 'rgba(85,159,255, 0.7)' }
    };

    var combined = [tempTrace, humTrace];

    /*
    var temp_nonnull = temperature.filter(function(y) { return (y != null)});
    var hum_nonnull = humidity.filter(function(y) { return (y != null)});

    // Find min and max points. May not be totally necessary but no harm
    var tempMax = Math.max.apply(null, temp_nonnull),
    tempMin = Math.min.apply(null, temp_nonnull), // Ignore null values
    humMax = Math.max.apply(null, hum_nonnull),
    humMin = Math.min.apply(null, hum_nonnull); // Ignore null values
    */

    var aesthetics = {
        title: 'Temperature and Humidity Monitoring',
        plot_bgcolor: 'rgba(240,240,240,1)',
        paper_bgcolor: 'rgba(0,0,0,0)',
        xaxis: {
            title: 'Time',
            showgrid: true,
            gridcolor: 'rgba(255,255,255,1)',
            zeroline: true
        },
        yaxis: {
            title: 'Temperature (Celsius)',
            color: 'rgb(255,122,105)',
            showline: true,
            showgrid: true,
            gridcolor: 'rgba(255,255,255,1)'
                //range: [tempMin - 0.5, tempMax + 0.5]
        },

        yaxis2: {
            title: 'Humidity (percent)',
            color: 'rgba(85,159,255, 0.7)',
            showline: true,
            showgrid: true,
            gridcolor: 'rgba(255,255,255,0)', // Don't want confusing double grids
            overlaying: 'y',
            side: 'right'
                //range: [humMin - 0.5, humMax + 0.5]
        }

    };
    Plotly.newPlot('graph', combined, aesthetics)
}

getData(); // Call the chain of events to get the data. Asynchronous, so we'll wait for user to call graphIt()
console.log(Plotly.BUILD);


// Section where we reshape dataframe according to date picker

function scaleDates() {

    var box1 = document.getElementById("datepicker1").value,
        box2 = document.getElementById("datepicker2").value;

    function convertDates(datestring) {
        var splitdate = datestring.split("/"),
            plotlyForm = splitdate[2] + "-" + splitdate[0] + "-" + splitdate[1];
        return plotlyForm;
    }

    var startDate = convertDates(box1),
        endDate = convertDates(box2);

    function matchRange(re, array) {
        truthIndex = [];

        function getAllIndexes(arr, val) { // http://stackoverflow.com/questions/20798477/how-to-find-index-of-all-occurrences-of-element-in-array
            var indexes = [],
                i = -1;
            while ((i = arr.indexOf(val, i + 1)) != -1) {
                indexes.push(i);
            }
            return indexes;
        }

        for (i in array) {
            truthIndex[i] = (re.test(array[i]));
        }


        trueIndices = getAllIndexes(truthIndex, true);
        firstMatch = Math.min.apply(null, trueIndices);
        lastMatch = Math.max.apply(null, trueIndices);

        return ([firstMatch, lastMatch]);
    }

    var startRe = new RegExp(startDate),
        stopRe = new RegExp(endDate);

    var startIndex = Math.min.apply(null, matchRange(startRe, df[0]));
    var stopIndex = Math.max.apply(null, matchRange(stopRe, df[0]));

    if (startIndex > stopIndex) {
        var temporary = startIndex,
            startIndex = stopIndex,
            stopIndex = temporary;
    }

    var Datetime = df[0].slice(startIndex, stopIndex);
    var Temperature = df[1].slice(startIndex, stopIndex);
    var Humidity = df[2].slice(startIndex, stopIndex);

    return [Datetime, Temperature, Humidity];
}


// Given scaled date range from scaleDates(), open a window to download TSV format file.
function downloadify(arr) {
    var separator = "\t";
    var content = "data:text/tab-separated-values;charset=utf-8,";
    content += "Time" + separator + "Temperature" + separator + "Humidity\n"
    for (var row = 0; row < arr[0].length; row++) {
        content = content + arr[0][row] + separator + arr[1][row] + separator + arr[2][row] + "\n";
    }

    var encodedUri = encodeURI(content)
        //window.open(encodedUri)

    link = document.getElementById("downloader")
    link.setAttribute("href", encodedUri);
    link.setAttribute("download", "my_data.tsv");
}
