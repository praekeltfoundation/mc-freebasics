//Progress bar
$('.next').click(function(){

  var nextId = $(this).parents('.tab-pane').next().attr("id");
  $('[href=#'+nextId+']').tab('show');
  return false;

})

$('.prev').click(function(){

  var prevId = $(this).parents('.tab-pane').prev().attr("id");
  $('[href=#'+prevId+']').tab('show');
  return false;

})

$('a[data-toggle="tab"]').on('shown.bs.tab', function (e) {

  var step = $(e.target).data('step');
  var percent = (parseInt(step) / 3) * 100;

  $('.progress-bar').css({width: percent + '%'});
  $('.progress-bar').text("Step " + step + " of 3");

})

$('.first').click(function(){

  $('#stepper a:first').tab('show')

})

//Google font
WebFont.load({
   google: {
     families: ['Work Sans', 'Roboto', 'Bangers', 'Orbitron', 'Pacifico', 'Passion One', 'Yanone Kaffeesatz', 'Montserrat', 'Fjalla One', 'Oswald', 'Open Sans']
   }
 });
