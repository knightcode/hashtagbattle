//
// Handler for sanitizing and sending new battles to the server. 
//
(function ($) {
    $('#create-battle-form').submit(function (event) {
        var first_tag = $('#left-hashtag').val(),
            second_tag = $('#right-hashtag').val()
        console.log("hello");
        event.preventDefault();

        // Sanitize inputs
        if (first_tag.length === 0 || second_tag.length === 0) {
            alert("Hashtag fields can't be empty");
            return;
        }
        first_tag = first_tag.trim();
        second_tag = second_tag.trim();
        if (first_tag.charAt(0) !== '#') {
            first_tag = "#" + first_tag;
        }
        if (second_tag.charAt(0) !== '#') {
            second_tag = "#" + second_tag;
        }
        $.ajax({
            method: 'get',
            dataType: 'json',
            url: '/create/',
            data: {
                left: first_tag,
                right: second_tag
            },
            success: function (data) {
                if (data.success){ 
                    $('.messages').append("<div class=message>Success!</div>");
                    $('.battles').append("<article class=battle><div class=hashtag><span class=text>" +
                            data.left_hashtag +
                            ":</span> 0</div><div class=hashtag><span class=text>" +
                            data.right_hashtag +
                            ":</span> 0</div></article>");
                }
            },
            error: function () {
                alert("There was a problem submitting your battle!!");
            }
        });
    });
    
    timeout = setTimeout(function () {
        console.log("refreshing");
        window.location.reload();
    }, 60000);
})(jQuery)