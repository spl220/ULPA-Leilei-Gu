//On load setup

$(document).ready(function() {
    $("#step1").show().delay(10);
});

// Next step transitions

$('#step1-next').click(function(event) {
    event.preventDefault();
    $.each($('label[id$="-university"].chosen'), function(index, val) {
        $('select#id_university').append('<option value="'+$(this).text()+'" selected="selected">'+$(this).text()+'</option')
    });
    if ($('select#id_university option').length == 0) {
        $('#no-university-error').removeClass('hide');
    } else {
        selected_universities = {}
        universities = $('select#id_university option');
        $.each(universities, function(index, val) {
            selected_universities[index] = $(this).val();
        });
        populate_languages(selected_universities);
        $('#step1').addClass('hide');
        $('#step2').removeClass('hide');
    }
    $('html, body').animate({ scrollTop: 0 }, 'fast');
});

$('#step2-back').click(function(event) {
    event.preventDefault();
    $('#step2').addClass('hide');
    $('#step1').removeClass('hide');
    $('html, body').animate({ scrollTop: 0 }, 'fast');
});

$('#step2-next').click(function(event) {
    event.preventDefault();
    $('#step2').addClass('hide');
    $('#step3').removeClass('hide');
    $('html, body').animate({ scrollTop: 0 }, 'fast');
});

$('#step3-back').click(function(event) {
    event.preventDefault();
    $('#step3').addClass('hide');
    $('#step2').removeClass('hide');
    $('html, body').animate({ scrollTop: 0 }, 'fast');
});

$('#step3-next').click(function(event) {
    event.preventDefault();
    $('#step3').addClass('hide');
    $('#step4').removeClass('hide');
    $('html, body').animate({ scrollTop: 0 }, 'fast');
});

$('#step4-back').click(function(event) {
    event.preventDefault();
    $('#step4').addClass('hide');
    $('#step3').removeClass('hide');
    $('html, body').animate({ scrollTop: 0 }, 'fast');
});

$('#step4-next').click(function(event) {
});

// Accordion and University selection functionality
$('.panel-heading').on('click', function () {
    $($(this).data('target')).collapse('toggle');
});

$(document).on('click', 'label[id$="-select-all"]', function(event) {

    id = $(this).attr('id');
    split_id = id.split('-');
    state = split_id[0];

    universities = state + "-university";
    
    if ($(this).hasClass("active")) {
        $('#' + state).removeClass('active');
        $('#' + state + ' .custom-checkbox-selected').addClass('hide');
        $('label[id$="' + universities + '"]').removeClass("chosen");
        $('label[id$="' + universities + '"]').removeClass("active");
    } else {
        $('#' + state).addClass('active');
        $('#' + state + ' .custom-checkbox-selected').removeClass('hide');
        $('label[id$="' + universities + '"]').addClass("chosen");
        $('label[id$="' + universities + '"]').addClass("active");
    }
});

$(document).on('click', 'label[id$="-university"]', function(event) {
    id = $(this).attr('id');
    split_id = id.split('-');
    state = split_id[0];

    universities_select_all = state + "-select-all";
    
    $('#' + state).addClass('active');
    $('#' + state + ' .custom-checkbox-selected').removeClass('hide');
    $(this).toggleClass('chosen');

    if ($(this).hasClass("chosen")) {
        $('label[id$="' + universities_select_all + '"]').removeClass("active");
    } 

    if ($('.' + id).length == $('.' + id + '.chosen').length) {
        $('label[id$="' + universities_select_all + '"]').addClass("active");
    } else {
        $('label[id$="' + universities_select_all + '"]').removeClass("active");
    };

    if ($('.' + id + '.chosen').length == 0) {
        $('#' + state).removeClass('active');
        $('#' + state + ' .custom-checkbox-selected').addClass('hide');
    }
});
// Ajax calls

function populate_languages(selected_universities) {
    $.ajax({
        url: '/universities/list_languages',
        type: 'GET',
        dataType: 'json',
        data: selected_universities,
    })
    .done(function(data) {
        languages = [];
        var selectize = $("#id_language")[0].selectize;
        $.each(data, function(index, val) {
            if (index == 0) {
                selectize.clear();
                selectize.clearOptions();
            };
            selectize.addOption({
                value: val,
                text: val
            });
            selectize.refreshOptions(false);
        });
    })
    .fail(function() {
        console.log("error");
    })
    .always(function() {
        console.log("complete");
    });
    return;
}