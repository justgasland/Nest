


console.log("Working Fine");

$(document).ready(function () {
    $('#commentForm').submit(function (e) {
        e.preventDefault();

        $.ajax({
            data: $(this).serialize(),
            method: $(this).attr("method"),
            url: $(this).attr("action"),
            dataType: "json",

            success: function (res) {
                if (res.bool === true) {
                    console.log("Comment Saved to Db");
                    $('#reviewss').html("Review Added Successfully");

                    // ✅ Correct class selector instead of wrong ID
                    $('.hide-comment-form').hide();

                    // ✅ Build stars
                    let stars = '';
                    for (let i = 1; i <= res.context.rating; i++) {
                        stars += '<i class="fas fa-star text-warning"></i>';
                    }

                    // ✅ Dynamic HTML (no Django tags!)
                    let _html = `
                        <div class="single-comment justify-content-between d-flex mb-30">
                        <div class="user justify-content-between d-flex">
                            <div class="thumb text-center">
                                <img src="/static/assets/imgs/blog/author-2.png" alt="">
                                <a href="#" class="font-heading text-brand">${res.context.user}</a>
                            </div>
                            <div class="desc">
                                <div class="d-flex justify-content-between mb-10">
                                    <div class="d-flex align-items-center">
                                        <span class="font-xs text-muted">Just now</span>
                                    </div>
                                    <div class="product-rate d-inline-block">
                                        ${stars}
                                    </div>
                                </div>
                                <p class="mb-10">${res.context.review} <a href="#" class="reply">Reply</a></p>
                            </div>
                        </div>
                    `;

                    // ✅ Find correct container and prepend
                    $('.comment-list').prepend(_html);
                }
            }
        });
    });
});



$(document).ready(function () {
    $(".filter-checkbox, #price-filter-btn").on("click", function () {
        console.log("Checkbox clicked!")

        let min_price = $('#max_price').attr("min")
        let max_price = $('#max_price').val()

        let filter_object = {}


        filter_object.min_price = min_price;
        filter_object.max_price = max_price; 

        
        $(".filter-checkbox").each(function () {
            let filter_value = $(this).val()
            let filter_key = $(this).data("filter")

            // console.log(filter_value, filter_key)
            // console.log("filter value", filter_value)
            // console.log("filter key", filter_key)
            filter_object[filter_key] = Array.from(document.querySelectorAll('input[data-filter=' + filter_key + ']:checked')).map(function (element) {
                return element.value
            })
            console.log(filter_object)
        });

        console.log("Filter Object is: ", filter_object);
        $.ajax({
            url: '/filter-products/',
            data: filter_object,
            dataType: 'json',
            beforeSend: function () {
                console.log("Trying to filter data");
            },
            
            success: function (response) {
                console.log("Data filtered successfully!");
                $("#filteredproducts").html(response.data); 
            }
            
        });

    });
    $('#max_price').onblur('change', function () {
        let max_price = $(this).attr()
        let min_price = $(this).attr()
        let current_price = $(this).val()
        console.log("Max Price: ", max_price)
        console.log("Min Price: ", min_price)
        console.log("Current Price: ", current_price)   

        if (current_price < parseInt(min_price) || current_price > parseInt(max_price)) {
            console.log("Price is out of range")

        
            min_price=Math.round(min_price* 100) / 100
            max_price=Math.round(max_price* 100) / 100

            alert("Price should be between " + min_price + " and " + max_price)
            $(this).val(min_price)
            $('#range').val(min)
            $(this).focus()

            return false
        
        }
        
        
    });
});

// Add to cart functionality

$("#add-to-btn").on("click", function () {
    let quantity = $("product-quantity").val();
    let product_title = $("#product-title").val();
    let product_id = $("#product-id").val();
    let product_price = $("#product-price").text();

    let this_val = $(this);

    console.log("Product ID: ", product_id);    
    console.log("Product Title: ", product_title);
    console.log("Product Price: ", product_price);
    console.log("Quantity: ", quantity);
    console.log("Button clicked: ", this_val);

});