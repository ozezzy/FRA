(function () {
    $('#features-table').DataTable();

    // prevent selection of past date as target-date
    $("#target-date").attr("min", todayDate());

    // set priority based on selected client
    $('#client').change(function () {
        $.getJSON('/c_priority', {
            client: this.value
        }, function (data) {

            const sel = $("#client-priority").empty() // remove current options 
            $("<option />", { value: `[${data.length + 1}]`, text: data.length + 1 }).appendTo(sel);
            for (var i in data) {
                $("<option />", { value: JSON.stringify([data[i][0], data[i][1]]), text: `(${data[i][0]},  ${data[i][1]})` }).appendTo(sel);
            }
        })
        return false
    })

    // populate modal with details 
    $('#details-modal').on('show.bs.modal', function (e) {
        const targetRow = $(e.relatedTarget); // Row that triggered the modal
        var feature = targetRow.data('feature'); // Extract info from data-* attributes
        feature = JSON.parse(feature.replace(/\'/g, '"'))
        for (var key in feature) {
            console.log(`#${key}`)
            $(`#${key}`).html(feature[key]);
        }

    });
}());

// returns date format for html5 date min
function todayDate() {
    var today = new Date();
    var dd = today.getDate();
    var mm = today.getMonth() + 1; //January is 0!
    var yyyy = today.getFullYear();
    if (dd < 10) {
        dd = '0' + dd
    }
    if (mm < 10) {
        mm = '0' + mm
    }
    return today = yyyy + '-' + mm + '-' + dd;
}