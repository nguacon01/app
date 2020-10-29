$(document).ready(function(){
    $('img').each(function(){
        var src = ($(this).attr('alt'));
        $(this).attr('src', src);
    });
    // var $this_img = $(".fig-cms-media-image img");
    // console.log($this_img.attr("data-src"));
});