$(function () {
    $('.show-login').on("click", function () {
        $("#login-form").toggleClass("hidden")

        $(this).toggleClass("hidden");
    });

    $('.hide-login').on("click", function () {
        $("#login-form").toggleClass("hidden")
        $(".show-login").toggleClass("hidden")
    });

    $(".hide-login").on("hover", function(){
        $(".arrow").toggle(slow);
    });

    $('#myform').on('submit', function(event) {
        event.preventDefault();
        alert("the message is sent");
        var formData = $(this).serialize();
        $.ajax({
          url: 'localhost:8000/login/',
          method: 'POST',
          data: formData,
          success: function(response) {
            if (response.success) {
              // login successful, do something
              console.log("You are logged in now we will redirect to dashboards")
            } else {
              alert(response.error);
            }
          }
        });
      });
});