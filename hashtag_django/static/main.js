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
            }
        });
    });
    
    timeout = setTimeout(function () {
        console.log("refreshing");
        window.location.reload();
    }, 60000);
})(jQuery)