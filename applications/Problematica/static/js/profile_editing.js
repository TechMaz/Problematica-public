$("document").ready(function() {

    //Add CSS to forms
    $("#profile_bio_edit_bio").addClass('profile_edit_form');
    $("#profile_fields_edit_acadfields").addClass('profile_edit_form');

    //Make Edit buttons show on hover
    $('.profile-section').hover(function() {$(this).find('.profile-edit').show()},
      function() {$(this).find('.profile-edit').hide()});

    $(".profile-edit").click(function() {
      var editable;
      var textbox;
      var textboxLen;

      /* Hide all other text boxes*/
      $(".content").show();
      $(".editable-content").hide();
      /* Hide this content*/
      $(this).parent().hide();
      /* Show this ediable content*/
      editable = $(this).parent().siblings(".editable-content");
      editable.show();

      /* put cursor in textbox */
      textbox = editable.find(".form-control")[0];
      textboxLen = textbox.value.length;
      textbox.selectionStart = textboxLen;
      textbox.selectionEnd = textboxLen;
      textbox.focus();

    });

    //Make image show upload option on hover
    $('.profile-photo-container').hover(function() {$(".profile-photo").addClass('profile-photo-hovered');$("#upload-image").show()},
      function() {$(".profile-photo").removeClass('profile-photo-hovered');$("#upload-image").hide()});
    //Make image link to upload image page

})
