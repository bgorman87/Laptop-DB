
function voted(vote_type, up_item_id, down_item_id){ 
    var up_element = document.getElementById(up_item_id);
    var down_element = document.getElementById(down_item_id);
    if(vote_type == "upvote"){
        up_element.classList.add("upvoted");
        down_element.classList.remove("downvoted");
    } else if(vote_type == "downvote"){
        down_element.classList.add("downvoted");
        up_element.classList.remove("upvoted");
    } else if(vote_type == "removed"){
        up_element.classList.remove("upvoted");
        down_element.classList.remove("downvoted");
    }
}


$(".part-upvote-click").on('click', function(){
    var partid = $(this).data("answer");
    $.ajax({
        url: "/part-upvote/",
        type: "POST",
        data: {
            partid: partid,
            csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val()
        },
        datatype: "json",
        success: function(res){
            console.log(res);
            if(res.bool){
                var newscore = res.score
                console.log(newscore);
                $(".part-score-count-"+partid).text(newscore);
                voted(res.vote_type, "part-upvote-"+partid, "part-downvote-"+partid);
            }
        }
    });
});

$(".part-downvote-click").on('click', function(){
    var partid = $(this).data("answer");
    $.ajax({
        url: "/part-downvote/",
        type: "POST",
        data: {
            partid: partid,
            csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val()
        },
        datatype: "json",
        success: function(res){
            console.log(res);
            if(res.bool){
                var newscore = res.score
                console.log(newscore);
                $(".part-score-count-"+partid).text(newscore);
                voted(res.vote_type, "part-upvote-"+partid, "part-downvote-"+partid);
            }
        }
    });
});

$(".laptop-upvote-click").on('click', function(){
    var laptopid = $(this).data("answer");
    $.ajax({
        url: "/laptop-upvote/",
        type: "POST",
        data: {
            laptopid: laptopid,
            csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val()
        },
        datatype: "json",
        success: function(res){
            console.log(res);
            if(res.bool){
                var newscore = res.score
                console.log(newscore);
                $(".laptop-score-count-"+laptopid).text(newscore);
                voted(res.vote_type, "laptop-upvote-"+laptopid, "laptop-downvote-"+laptopid);
            }
        }
    });
});

$(".laptop-downvote-click").on('click', function(){
    var laptopid = $(this).data("answer");
    $.ajax({
        url: "/laptop-downvote/",
        type: "POST",
        data: {
            laptopid: laptopid,
            csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val()
        },
        datatype: "json",
        success: function(res){
            console.log(res);
            if(res.bool){
                var newscore = res.score
                console.log(newscore);
                $(".laptop-score-count-"+laptopid).text(newscore);
                voted(res.vote_type, "laptop-upvote-"+laptopid, "laptop-downvote-"+laptopid);
            }
        }
    });
});

