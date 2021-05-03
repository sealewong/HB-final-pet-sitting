"use strict";

const deletePet = (petName) => {
    $('#cart-items').append()
}

const button = document.querySelector('#delete-button');

button.addEventListener('click', () => {
  alert('Deleted Pet');
});

$('#calEvents').DataTable( {
    "processing": true,
    "serverSide": false,
    "order": [[ 3, "asc" ]],
    "ajax": "/api/v1/calendar/get",
    'columnDefs': [
        {
           targets: 2, render: function(data1){ return moment(data1).format('dddd')},
           defaultContent: '<button class="btn-view" type="button">Edit</button>'
             + '<button class="btn-delete" type="button">Delete</button>'
        },
        { targets: 3, render: function(data2){ return moment(data2).format('YYYY-MM-DD')}},
    ]
} );`