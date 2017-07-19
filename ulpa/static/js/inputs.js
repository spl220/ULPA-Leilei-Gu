
// Language Search

var $language = $('#id_language').selectize({
    delimiter: ',',
    persist: false,
    maxItems: null,
    value_field: 'language',
    sortField: 'text',
});

var allStudyRadios = document.getElementsByName('study_choice');
var allIntensityRadios = document.getElementsByName('intensity');

var booRadio;
var x = 0;
for(x = 0; x < allStudyRadios.length; x++){

        allStudyRadios[x].onclick = function(){

            if(booRadio == this){
                this.checked = false;
        booRadio = null;
            }else{
            booRadio = this;
        }
        };

}

for(x = 0; x < allIntensityRadios.length; x++){

        allIntensityRadios[x].onclick = function(){

            if(booRadio == this){
                this.checked = false;
        booRadio = null;
            }else{
            booRadio = this;
        }
        };

}