 function getCommentList() {
    $.ajax({
        url: "/get_list_json",
        dataType : "json",
        success: updateCommentList
    });

}

function updateCommentList(comments) {
    // Removes the old to-do list items
    $("li").remove();
    $("ol img").remove();


    // Adds each new todo-list item to the list
    $(comments).each(function() {
        $("#commentslist" + this.fields.comment_post).append(
        	'<li>' + "<img src= \" picture/"+ this.fields.comment_user+ "\" alt= \"Wrong\" width=\"50px\" height=\"50px\">"+
                    sanitize(this.fields.comment_content) +
                    '<span class="details">' +
                    "(id=" + this.pk + ", comment time:" + this.fields.comment_time + ", userid:" + this.fields.comment_user + ")" +
                    // "<img src= '{%url 'picture' id= " this.fields.comment_user+ " %}' alt= 'Wrong' height="50" width="50">" +
                    "</span></li>"
                    // + '<img src=' + '{% url "picture" id= ' + this.fields.comment_user + '%}  alt= "Wrong" height="50" width="50'>"
                     // "<img src= \" picture/"+ this.fields.comment_user+ "\" alt= \"Wrong\" width=\"50px\" height=\"50px\">"
        );
    });
}

function addComment(id) {
    var commentTextElement = $("#comment" + id);
    var commentTextValue   = commentTextElement.val();


    // Clear input box and old error message (if any)
    commentTextElement.val('');
    displayError('');

    $.ajax({
        url: "add_comment",
        type: "POST",
        data: "comment="+commentTextValue+"&csrfmiddlewaretoken="+getCSRFToken()+"&postid=" + id,
        dataType : "json",
        success: function(response) {
            if (Array.isArray(response)) {
                updateCommentList(response);
            } else {
                displayError(response.error);
            }
        }
    });
}

function sanitize(s) {
    // Be sure to replace ampersand first
    return s.replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;');
}

function getCSRFToken() {
    var cookies = document.cookie.split(";");
    for (var i = 0; i < cookies.length; i++) {
        if (cookies[i].startsWith("csrftoken=")) {
            return cookies[i].substring("csrftoken=".length, cookies[i].length);
        }
    }
    return "unknown";
}


function displayError(message) {
    $("#error").html(message);
}

$( "#commentslist" ).on( "click", "li", function( event ) {
    event.preventDefault();
    console.log( $( this ).text() );
});

window.onload = getCommentList;

// causes list to be re-fetched every 5 seconds
window.setInterval(getCommentList, 5000);
