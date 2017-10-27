document.addEventListener('DOMContentLoaded', function(){
 
   var study_choices = document.getElementById('study_choices');
   var study_choices_disable = document.getElementById('study_choices_disable');
   var radios_study_choice = document.getElementsByName('study-choice-radio');
    for(var i=0,length= radios_study_choice.length;i< length;i++){
        if(study_choices != null && radios_study_choice[i].value == study_choices.innerHTML){
              radios_study_choice[i].checked =true;
        }
        if(study_choices_disable != null && radios_study_choice[i].value == study_choices_disable.innerHTML){
              radios_study_choice[i].disabled =true;
        }
    }

   var intensities = document.getElementById('intensities');;
   var intensities_disable = document.getElementById('intensities_disable');
   var radios_intensities = document.getElementsByName('intensities-radio');
    for(var i=0,length= radios_intensities.length;i< length;i++){
        if(intensities != null && radios_intensities[i].value == intensities.innerHTML){
              radios_intensities[i].checked =true;
        }
        
        if(intensities_disable != null && radios_intensities[i].value == intensities_disable.innerHTML){
             console.log("intensity disable not empty"); 
             radios_intensities[i].disabled =true;
        }
    }
}, false);
    
function myFilterFunction() {
        var studyChoice;
        var intensity;
        var studyChoice_disable;
        var intensity_disable;
        var radios = document.getElementsByName('study-choice-radio');
        for(var i=0,length= radios.length;i< length;i++){
            if(radios[i].checked){
               studyChoice = radios[i].value;
               console.log("get study choice checked: "+ radios[i].value)
               continue;
           }
           if(radios[i].disabled){
               studyChoice_disable = radios[i].value;
               console.log("get study-choice disabled: "+ radios[i].value)
               continue;
           }
        }
        var intensity_radios = document.getElementsByName('intensities-radio');
        for(var i=0,length = intensity_radios.length;i<length;i++){
           if(intensity_radios[i].checked){
               intensity = intensity_radios[i].value;
           }
           if(intensity_radios[i].disabled){
               intensity_disable = intensity_radios[i].value;
               console.log("get intensity disabled choice: "+ radios[i].value)
               continue;
           }
        }
       var currentURL = window.location.href;
       var pathArray = currentURL.split( '&' );
       var newPathname = "";
       for (i = 0; i < pathArray.length; i++) {
           if(pathArray[i].includes('study_choices')||pathArray[i].includes('intensities')||pathArray[i].includes('intensities_disable')||pathArray[i].includes('study_choices_disable')){
              continue;
          }else{
              console.log(pathArray[i]);
              newPathname += (pathArray[i]+'&')
          }
       }
       if(studyChoice){
          newPathname += "study_choices="+ studyChoice+'&';
       }
       if(intensity){
          newPathname += "intensities="+ intensity+"&";
       }
       if(studyChoice_disable){
          newPathname += "study_choices_disable="+ studyChoice_disable+'&';
       }
       if(intensity_disable){
          newPathname += "intensities_disable="+ intensity_disable+'&';
       }
       pathName = newPathname.substring(0,newPathname.length-1);
       console.log(pathName);
       location.replace(pathName);
    }

function online_disabled() {
        // check whether there are online-regular subjects  
        document.getElementById('intensity-regular').removeAttribute("disabled");
        var online_regular_subjects = document.getElementById('online_regular_subjects');
        if(online_regular_subjects == null){
           document.getElementById('intensity-regular').removeAttribute("checked");            
           document.getElementById('intensity-regular').setAttribute("disabled","disabled");
        }

        // check whether there are online-intensive subjects. if not disable "intensive" option
        document.getElementById('intensity-intensive').removeAttribute("disabled");
        var online_intensive_subjects = document.getElementById('online_intensive_subjects');
       
        if(online_intensive_subjects == null){
            document.getElementById('intensity-intensive').removeAttribute("checked");
            document.getElementById('intensity-intensive').setAttribute("disabled","disabled");
        }

        // hide information about 'oncampus'
        var oncampusInfo = document.getElementsByName('oncampusInfo');
        for(var i=0,length= oncampusInfo.length;i< length;i++){
           oncampusInfo[i].setAttribute("hidden","hidden"); 
        }
        // show information about 'online'
        document.getElementById('online_subjects').removeAttribute("hidden");
        
        // intensive is also chosen,
        if(document.getElementById('intensity-regular').checked){
          document.getElementById('online_regular_subjects').removeAttribute("hidden");
        }
        // regular is also chosen
        if(document.getElementById('intensity-intensive').checked){
          document.getElementById('online_intensive_subjects').removeAttribute("hidden");
        }
    }

function oncampus_disabled() {
        // check whether there are oncampus-regular subjects
        document.getElementById('intensity-regular').removeAttribute("disabled");
        var oncampus_regular_subjects = document.getElementById('oncampus_regular_subjects');
        if(oncampus_regular_subjects == null){
            document.getElementById('intensity-regular').checked = false;  
            document.getElementById('intensity-regular').setAttribute("disabled","disabled");
        }
        // check whethe there are oncampus-intensive subjects
        document.getElementById('intensity-intensive').removeAttribute("disabled");
        var oncampus_intensive_subjects = document.getElementById('oncampus_intensive_subjects');
        if(oncampus_intensive_subjects == null){
            document.getElementById('intensity-intensive').checked = false;
            document.getElementById('intensity-intensive').setAttribute("disabled","disabled");
        }
        // hide information about 'online'
        var onlineInfo = document.getElementsByName('onlineInfo');
        for(var i=0,length= onlineInfo.length;i< length;i++){
           onlineInfo[i].setAttribute("hidden","hidden"); 
        }
        // show information about 'oncampus'
        document.getElementById('oncampus_subjects').removeAttribute("hidden");
        // intensive is also chosen,
        if(document.getElementById('intensity-regular').checked){
          document.getElementById('oncampus_regular_subjects').removeAttribute("hidden");
        }
        // regular is also chosen
        if(document.getElementById('intensity-intensive').checked){
          document.getElementById('oncampus_intensive_subjects').removeAttribute("hidden");
        }
    }

function showRegularSubjects(){
        // hide all information 
        var onlineInfo = document.getElementsByName('onlineInfo');
        for(var i=0,length= onlineInfo.length;i< length;i++){
           onlineInfo[i].setAttribute("hidden","hidden"); 
        }

        // hide all information 
        var oncampusInfo = document.getElementsByName('oncampusInfo');
        for(var i=0,length= oncampusInfo.length;i< length;i++){
           oncampusInfo[i].setAttribute("hidden","hidden"); 
        }
        // 'online-regular'is chosen
        if(document.getElementById('study-choice-online').checked){
          document.getElementById('online_subjects').removeAttribute("hidden");
          document.getElementById('online_regular_subjects').removeAttribute("hidden");
        }
        // 'oncampus-regular'is chosen
        if(document.getElementById('study-choice-oncampus').checked){
          document.getElementById('oncampus_subjects').removeAttribute("hidden");
          document.getElementById('oncampus_regular_subjects').removeAttribute("hidden");
        }
     }
function showIntensiveSubjects(){
        // hide all information 
        var onlineInfo = document.getElementsByName('onlineInfo');
        //console.log(onlineInfo.length);
        for(var i=0,length= onlineInfo.length;i< length;i++){
           onlineInfo[i].setAttribute("hidden","hidden"); 
        }
        
        // hide all information 
        var oncampusInfo = document.getElementsByName('oncampusInfo');
        for(var i=0,length= oncampusInfo.length;i< length;i++){
           oncampusInfo[i].setAttribute("hidden","hidden"); 
        }
        // 'online-regular'is chosen
        if(document.getElementById('study-choice-online').checked){
          document.getElementById('online_subjects').removeAttribute("hidden");
          document.getElementById('online_intensive_subjects').removeAttribute("hidden");
        }
        // 'oncampus-regular'is chosen
        if(document.getElementById('study-choice-oncampus').checked){
          document.getElementById('oncampus_subjects').removeAttribute("hidden");
          document.getElementById('oncampus_intensive_subjects').removeAttribute("hidden");
        }
     }

