/**
 * tables.js
 *
 * This script is used to style tables.
 * It adds the .alt class to every other <tr> element in all tables.
*/


lwpcms_tables = document.querySelectorAll('.lwpcms-table');

for(var i = 0; i < lwpcms_tables.length; i++) {
    table = lwpcms_tables[i];
    table_rows = table.querySelectorAll('tr');

    alt = false;
    for(var ii = 0; ii < table_rows.length; ii++) {
        row = table_rows[ii];
        
        if(alt) {
            row.className += ' ' + 'alt';
            
            alt = false;
        }else {
            alt = true;
        }
    }
}
