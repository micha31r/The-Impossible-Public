// Like button ajax
function comment_ajax(pk) {
    $(document).ready(
        function() {
            $.ajax(
                {
                    url: `/idea/comment/get`,
                    data: {
                        'pk':pk,
                        'comment_num':comment_num,
                    },
                    dataType: 'json',
                    success: function(data) {
                        if (data.failed) {
                            console.log("Getting Comments Failed");
                        } else {
                            comment_num = data.new_comment_num;
                            data.comments = JSON.parse(data.comments);
                            for (var i=0; i<data.comments.length; i++) {
                                var comment = data.comments[i];
                                var author = data.authors[i];
                                var last_edit = data.timestamps[i];
                                var delete_link = "";
                                var delete_link_class = "";
                                if (author == username) {
                                    delete_link = `/idea/comment/delete/${comment.pk}/${idea_pk}`
                                    delete_link_class = "delete-link";
                                }
                                $("#append-target2").append(
                                    `<div class="comment-wrapper">
                                    <h6>${comment.fields.content}</h6>
                                    <p class="small">${author}</p>
                                    <a class="small ${delete_link_class}" href="${delete_link}">
                                    <span>Last Edited <span class="time">${last_edit}</span></span></a>`
                                );
                            }
                            hide_button();
                            // Auto scrolling with Jquery
                            // https://stackoverflow.com/questions/10503606/scroll-to-bottom-of-div-on-page-load-jquery
                            $(".comment-container").animate({ scrollTop: $('.comment-container').prop("scrollHeight")}, 1000);
                        }
                    }
                }
            );
        }
    );
}

auto_run.queue( 
    hide_button
);

function hide_button() {
    if (total_comments_num <= comment_num) {
        $(".more-comment-btn").css("display","none");
    }
}
