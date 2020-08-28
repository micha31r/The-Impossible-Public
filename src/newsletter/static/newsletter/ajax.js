// Subscribe to mailing list ajax
function join_newsletter_ajax(email) {
    $(document).ready(
        function() {
            $.ajax(
                {
                    url: `/newsletter/join/`,
                    data: {
                        'email':email,
                    },
                    dataType: 'json',
                    success: function(data) {
                        var msg;
                        $("#join-status").attr("class","alert alert-black-outline bold");
                        if (data.exist) {
                                msg = "Email already exist";
                        } else if (data.failed) {
                            msg = "Join Failed";
                        } else {
                            $("#join-form").css("display","none");
                            msg = "You have successfully subscribed!";
                        }
                        $("#join-status").html(msg);
                        $("#join-status").css("display","block");

                        // Resize form
                        newsletter_resize();
                    }
                }
            );
        }
    );
}