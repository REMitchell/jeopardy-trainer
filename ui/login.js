const dialog = $( "#login-dialog" ).dialog({
   autoOpen: false,
   modal: true,
   width: 500,
});

dialog.find( "form" ).on( "submit", function( event ) {
   event.preventDefault();
   $.ajax({
         type: 'POST',
         url: 'login',
         data: $(this).serialize(),
         success: () => get_question('similar')
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
