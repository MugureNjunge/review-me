// $(document).ready(function () {

//   // hover over landing page
//   $('.landing').hover(function () {
//       // over
//       $('.landing-abs-fade').addClass('dark-fade');
//       $('.landing-abs-fade').removeClass('light-fade');
//   }, function () {
//       // out
//       $('.landing-abs-fade').addClass('light-fade');
//       $('.landing-abs-fade').removeClass('dark-fade');
//   });

//   // hover over individual website box
// });

// function getid(fadeId) {
//   // over
//   let fade = '#fade' + fadeId
//   $(fade).addClass('site-fade-in');
//   $(fade).removeClass('site-fade-out');
// }

// function outmouse(fadeId) {
//   // out
//   let fade = '#fade' + fadeId
//   $(fade).removeClass('site-fade-in');
//   $(fade).addClass('site-fade-out');
// };





$(document).ready(function() {
  $('form').submit(function(event) {
          event.preventDefault()
          form = $("form")

          $.ajax({
                  'url': '/ajax/register/',
                  'type': 'POST',
                  'data': form.serialize(),
                  'dataType': 'json',
                  'success': function(data) {
                      alert(data['success'])
                  },
              }) // END of Ajax method
          $('#id_username').val('')
          $("#id_email").val('')
          $("#id_password1").val('')
          $("#id_password2").val('')
      })

    })   