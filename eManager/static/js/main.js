function GetCookie(name) {
	var cookieValue = null;
	if (document.cookie && document.cookie !== '') {
		var cookies = document.cookie.split(';');
		for (var i = 0; i < cookies.length; i++) {
			var cookie = jQuery.trim(cookies[i]);
			if (cookie.substring(0, name.length + 1) === (name + '=')) {
				cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
				break;
			}
		}
	}
	return cookieValue;
}

function CSRFSafeMethod(method) {
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

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

function ToggleMenu() {
	$('.header .menu').toggleClass('menu_show');
}

var Comment = {
	focusin: function(element) {
		$(element).addClass('active');
	},

	focusout: function(element) {
		$(element).removeClass('active');
	},

	update: function(element) {
		var comment = $(element).parents('.comment'),
			form = comment.find('.comment-change')[0],
			text = $(form).find('.comment__text')[0].value,
			csrftoken = GetCookie('csrftoken');

		$.ajaxSetup({
		    beforeSend: function(xhr, settings) {
		        if (!CSRFSafeMethod(settings.type) && !this.crossDomain) {
		            xhr.setRequestHeader("X-CSRFToken", csrftoken);
		        }
		    }
		});

		$.ajax({
			url: form.getAttribute('action'),
			type: 'POST',
			data: 'new_text=' + text,
			success: function(data) {
				var container = comment.find('.comment-change__errors');

				if (data.errors) {
					container
						.text(data.errors.join(', '))
						.addClass('active');
				} else {
					container
						.text()
						.removeClass('active');
				}
			}
		});
	}
}

window.addEventListener('load', function() {
	var controller = $('.container').data('controller');

	if (controller) {
		window[controller].call();
	}
});