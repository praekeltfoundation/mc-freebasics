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

//jQuery UI sortable for the todo list
$(function () {

	"use strict";

/*	var list = document.getElementById("fb-blockcontainer");
	Sortable.create(list, {
		filter: '.locked-sect',
		handle: '.handle'
	});*/

	$("#fb-blockcontainer").sortable({
		items: "li.fb-block:not(.locked-sect)",
		placeholder: "sort-highlight",
		handle: ".handle",
		forcePlaceholderSize: true,
		axis: 'y',
		grid: [ 200, 1 ],
		scroll: true,
		scrollSensitivity: 100,
		//tolerance: "pointer",
		zIndex: 999999,
		change: function (event, ui) {
			$(event.target).trigger('changeOrder');
		}
	});

	/*

	 $("#fb-blockcontainer").gridster({
	 widget_margins: [10, 10],
	 widget_base_dimensions: [140, 140],
	 max_cols: 1
	 });

	 var gridster = $(".gridster ul").gridster().data('gridster');


	 */


});






// ColorPicker
$(function () {
	$("input.color-picker").each(function () {
		var $el = $(this);
		$el.ColorPickerSliders({
			size: 'sm',
			placement: 'bottom',
			swatches: false,
			sliders: false,
			hsvpanel: true,
			onchange: function () {
				$el.trigger('change');
			}
		});
	});
});

//Google font
WebFont.load({
   google: {
     families: ['Work Sans', 'Roboto', 'Bangers', 'Orbitron', 'Pacifico', 'Passion One', 'Yanone Kaffeesatz', 'Montserrat', 'Fjalla One', 'Oswald', 'Open Sans']
   }
 });
