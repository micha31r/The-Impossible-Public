// Like button ajax
function like_idea_ajax(pk) {
    $(document).ready(
        function() {
            $.ajax(
                {
                    url: `/idea/like`,
                    data: {
                        'pk':pk,
                    },
                    dataType: 'json',
                    success: function(data) {
                        if (data.failed) {
                            console.log("Like Failed");
                        } else {
                            $(`#like-svg-${pk}`).attr('name', data.action);
                        }
                    }
                }
            );
        }
    );
}

// Star button ajax
function star_idea_ajax(pk) {
    $(document).ready(
        function() {
            $.ajax(
                {
                    url: `/idea/star`,
                    data: {
                        'pk':pk,
                    },
                    dataType: 'json',
                    success: function(data) {
                        if (data.failed) {
                            console.log("Star Failed");
                        } else {
                            $(`#star-svg-${pk}`).attr('name', data.action);
                        }
                    }
                }
            );
        }
    );
} 
