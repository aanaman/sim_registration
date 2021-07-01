//document.addEventListener("DOMContentLoaded", function () {
//    var dropDownEl = document.querySelector('.dropdown-content');
//    if (dropDownEl !== undefined || dropDownEl !== null) {
//        //sending an ajax request to get products
//        var newMarkup = '<div id="menu_period" class="dropdown-content">';
//        fetch('/products/')
//            .then(function (res) {
//                return res.json();
//            })
//            .then(function (data) {
//                if (data.length) {
//                    for (var i = 0; i < data.length; i++) {
//                        newMarkup += `<a href="#" class="product" data-id=${data[i].productId} style="color: white; border: 1px;">${data[i].description}</a>`;
//                    }
//                    newMarkup += '</div>';
//                    dropDownEl.outerHTML = newMarkup;
//                }
//                var products = Array.from(document.querySelectorAll('.product'));
//                console.table(products);
//                if (products.length) {
//                    products.forEach(function (e) {
//                        e.addEventListener('click', function (event) {
//                            var productId = event.target.getAttribute('data-id');

//                        });
//                    });
//                }
//            })
//    }
//});

function ShowToast(message,type='error') {
    var Toast = Swal.mixin({
        toast: true,
        position: 'top-end',
        showConfirmButton: false,
        timer: 3000
    });

    Toast.fire({
        type: type,
        title: message
    });
}