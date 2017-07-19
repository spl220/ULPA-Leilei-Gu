//On load setup

$(document).ready(function() {
    $("#step1").show().delay(10);
});

// Next step transitions

$('#step1-next').click(function(event) {
    event.preventDefault();
    if ($('#step1 .selectize-input .item').length == 0) {
        $('#no-language-error').removeClass('hide');
    } else {
        selected_languages = {}
        languages = $('#step1 .selectize-input .item');
        $.each(languages, function(index, val) {
            selected_languages[index] = $(this).text();
        });
        populate_universities(selected_languages);
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
    $.each($('label[id$="-university"].chosen'), function(index, val) {
        $('select#id_university').append('<option value="'+$(this).text()+'" selected="selected">'+$(this).text()+'</option')
    });
});

$('.panel-heading').on('click', function () {
    $($(this).data('target')).collapse('toggle');
});

// Accordion and University selection functionality
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

function populate_universities(selected_languages) {
    $.ajax({
        url: '/languages/list_universities',
        type: 'GET',
        dataType: 'json',
        data: selected_languages,
    })
    .done(function(data) {
        states = [];
        $.each(data, function(index, val) {
            $('#' + index.toLowerCase() + '-collapse .panel-body').empty();
            state = index.toLowerCase();
            states.push(state);

            $.each(val, function(index, val) {
                $('#' + state + '-collapse .panel-body').prepend('<div class="btn-group" data-toggle="buttons"><label id="'+state+'-university" class="'+state+'-university btn btn-default btn-university"><input type="checkbox" class="btn btn-default">'+val+'</input></label></div>');
            });
        });
        $.each(states, function(index, val) {
            if ($('#' + val + '-collapse .panel-body label[id$="-university"]')) {
                $('#' + val + '-collapse .panel-body').append('<div class="btn-group" data-toggle="buttons"><label id="'+val+'-select-all" class="btn btn-default"><input type="checkbox" class="btn btn-default">Select All</input></label></div>');
            } else {
                $('#' + val + '-collapse .panel-body').append('<p>No Universities Available.</p>');
            }
        });
        $.each($('.panel-body:not(:has(.btn-group))'), function(index, val) {
            $(this).append('<p>No Universities Available.</p>');
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