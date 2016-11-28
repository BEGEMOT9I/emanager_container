function ActivateField(element) {
	$(element)
		.css({ display: 'none' })
		.prev()
		.removeAttr('disabled')
		.focus();
}

function DeactivateField(element) {
	$(element)
		.attr('disabled', '')
		.next()
		.css({ display: 'block' });
}

function FindEvents(element) {
	var value = element.value.replace(' ', '');
	$('.event').each(function() {
		var eventName = $(this).find('.event__name').text().replace(' ', ''),
			eventLocation = $(this).find('.address__name').text().replace(' ', ''),
			eventDate = $(this).find('.time__name').text().replace(' ', '');

		if (eventName.indexOf(value) != -1 || eventLocation.indexOf(value) != -1 || eventDate.indexOf(value) != -1 || !value) {
			$(this).show();
		} else {
			$(this).hide();
		}
	});
}