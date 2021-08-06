function myFunction() {
    var rowIndex = 2;
    var cellIndex = getTableCellIndexByHeaderName("Бележки");
    console.log(document.getElementById('orders-table').rows[rowIndex].cells[cellIndex]);
}

function getTableCellIndexByHeaderName(headerName) {
    var result = -1;
    var cellsCount = document.getElementById("orders-table").rows[0].cells.length;
    for (i = 0; i < cellsCount; i++) {
        if (document.getElementById("orders-table").rows[0].cells[i].innerHTML === headerName) {
            result = i;
            break;
        }
    }
    return result;
}

function addRowHandlers() {
    var table = document.getElementById("orders-table");
    var rows = table.getElementsByTagName("tr");
    for (i = 0; i < rows.length; i++) {
        var currentRow = table.rows[i];
        var createClickHandler =
            function (row) {
                return function () {
                    var cellIndex = getTableCellIndexByHeaderName("Бележки");
                    var cell = row.getElementsByTagName("td")[cellIndex];
                    var id = cell.innerHTML;
                    alert(id);
                };
            };
        currentRow.onclick = createClickHandler(currentRow);
    }
}

function hide () {
    var column = getTableCellIndexByHeaderName("Бележки");
    var tbl = document.getElementById("orders-table");
    var i;
    for ( i = 0; i < tbl.rows.length; i++ )
      tbl.rows[i].cells[column].style.display = "none";
    }

function start()
{
    hide();
    addRowHandlers();
}

window.onload = start();




