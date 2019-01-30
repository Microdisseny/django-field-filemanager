(function($){

  // From https://docs.djangoproject.com/en/2.1/ref/csrf/
  var getCookie = function(name) {
      var cookieValue = null;
      if (document.cookie && document.cookie !== '') {
          var cookies = document.cookie.split(';');
          for (var i = 0; i < cookies.length; i++) {
              var cookie = $.trim(cookies[i]);
              // Does this cookie string begin with the name we want?
              if (cookie.substring(0, name.length + 1) === (name + '=')) {
                  cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                  break;
              }
          }
      }
      return cookieValue;
  }

  var attach_filemanager = function(selector){
    $(selector + ' filemanager').attr(
      'v-bind:api-headers', "{'X-CSRFToken': '" + getCookie('csrftoken') + "'}")

    var FileManager = filemanager.default;
    Vue.component('filemanager', FileManager)
    new Vue({
        el: selector,
        components: {
          filemanager: FileManager
        }
    });
  }

  $(document).ready(function() {
    $('.filemanager_component').each(function(i, el){
      attach_filemanager('#' + django.jQuery(el).attr('id'));
    });
  });

}(django.jQuery || $));
