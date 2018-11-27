const dialog = $( "#login-dialog" ).dialog({
   autoOpen: false,
   modal: true,
   width: 500,
});

dialog.find( "form" ).on( "submit", function( event ) {
   debugger;
   event.preventDefault();
   $.ajax({
         type: 'POST',
         url: 'http://127.0.0.1:5000/login',
         data: $(this).serialize(),
         success: get_question
      });
   dialog.dialog( "close" );
});



const check_login = () => {
   if(!document.cookie.includes('session=')) {
      $( "#login-dialog" ).dialog( "open" );
      return false;
   }
   return true;
}
