// Panel Background
$('.panel').on('show.bs.collapse', function () {
     $(this).addClass('active');
});

$('.panel').on('hide.bs.collapse', function () {
     $(this).removeClass('active');
});

$(function() {
    jQuery.each( $('.faq h4'), function( i, val ) {
        str = val.innerHTML.replace(/\s+/g, '-').toLowerCase();
        $(this).attr('id', str);
        $('#nav').append('<li class=""><a href="#'+ str +'">' + val.innerHTML + '</a></li>');
    })
});

$(function() {
    jQuery.each( $('.faq h4'), function( i, val ) {
        str = val.innerHTML.replace(/\s+/g, '-').toLowerCase();
        $(this).attr('id', str);
        $('#contents').append('<li class=""><a href="#'+ str +'">' + val.innerHTML + '</a></li>');
    })
});

$('#nav').affix({
    offset: {
        top: $('#nav').offset().top,
        bottom: $('footer').outerHeight(true) + 40
    }
});
