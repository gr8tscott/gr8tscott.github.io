$(document).ready(function() {
    $('#refresh-button').click(function() {
        $.ajax({
            url: '/stock_data',
            method: 'GET',
            success: function(data) {
                var tableBody = $('#stock-predictions-table tbody');
                tableBody.empty();
                data.forEach(function(stock) {
                    var row = '<tr>' +
                        '<td>' + stock.ticker + '</td>' +
                        '<td>' + stock.current_price + '</td>' +
                        '<td>' + stock.traded_price + '</td>' +
                        '<td>' + stock.ai_response + '</td>' +
                        '<td>' + stock.date + '</td>' +
                        '</tr>';
                    tableBody.append(row);
                });
            },
            error: function(error) {
                console.log('Error fetching stock data:', error);
            }
        });
    });
});
