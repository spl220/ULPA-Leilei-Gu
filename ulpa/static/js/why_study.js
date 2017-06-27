$(function() {
    jQuery.each( $('.why-study h2'), function( i, val ) {
        str = val.innerHTML.replace(/\s+/g, '-').toLowerCase();
        $(this).attr('id', str);
        $('#nav').append('<li class=""><a href="#'+ str +'">' + val.innerHTML + '</a></li>');
    })
});

$(function() {
    jQuery.each( $('.why-study h2'), function( i, val ) {
        str = val.innerHTML.replace(/\s+/g, '-').toLowerCase();
        $(this).attr('id', str);
        $('#contents').append('<li class=""><a href="#'+ str +'">' + val.innerHTML + '</a></li>');
    })
});

$('#nav').affix({
    offset: {
        top: 300,
    }
});

