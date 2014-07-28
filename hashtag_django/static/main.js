//
// Handler for sanitizing and sending new battles to the server. 
//
(function ($) {

    var socket,
        timeout,
        battles = {},
        showing_form = false,
        battle_template = function (context) {
            return "<article class='battle battle-" +
                context.battle_id +
                "'><div class=hashtag><div class=text>" +
                context.left_hashtag.substring(1) +
                "</div> <div class=count>" +
                context.left_count +
                "</div></div><div class=hashtag><div class=text>" +
                context.right_hashtag.substring(1) +
                "</div> <div class=count>" +
                context.right_count +
                "</div></div></article>";
        };
    $('.add-battle').on('click', function(evt) {
        if (showing_form) {
            $('#create-battle-form').slideUp();
            $('.add-battle').text('+');
        } else {
            $('#create-battle-form').slideDown();
            $('.add-battle').html('&ndash;');
        }
        showing_form = !showing_form;
    });
    $('#create-battle-form').submit(function (event) {
        var first_tag = $('#left-hashtag').val(),
            second_tag = $('#right-hashtag').val()
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
                if (data.success) {
                    battles[data.battle_id] = true;
                    $('.messages').append("<div class=message>Success!</div>");
                    $('.battles').append(battle_template(data));
                }
            },
            error: function () {
                alert("There was a problem submitting your battle!!");
            }
        });
    });

    socket = io.connect("/battles");

    socket.on('connect', function () {
        console.log("connected");
        socket.emit('getAllBattles');
    });
    socket.on('allBattles', function (data) {
        var i = 0, len = data.battles.length,
            $battles = $('.battles'),
            bid;
        for(; i < len; i++) { // This runs fastest
            bid = data.battles[i].battle_id
            if (!(bid in battles)) {
                battles[bid] = true;
                $battles.append(battle_template(data.battles[i]));
            }
        }
    });

    socket.on('updatedBattle', function (data) {
        var $batCounts = $('.battle-' + data.battle_id + ' .count');
        $batCounts[0].innerText = data.left_count;
        $batCounts[1].innerText = data.right_count;
    });
})(jQuery)