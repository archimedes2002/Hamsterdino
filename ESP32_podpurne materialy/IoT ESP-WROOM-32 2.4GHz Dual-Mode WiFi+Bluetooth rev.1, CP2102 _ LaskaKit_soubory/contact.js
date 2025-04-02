$(function () {
	$('.in-kontakty p').each(function () {
		if ($(this).text() === 'Máte nějaké otázky? Zodpovíme je. Prosíme o pečlivé vyplnění kontaktních údajů.') {
			$(this).remove()
		}
	})
	$('.in-contacts p').each(function () {
		if ($(this).text() === 'Do you have any questions? We will answer them. Please fill in the contact details carefully.') {
			$(this).remove()
		}
	})

	$('.in-shanim-produkt p').each(function () {
		if ($(this).text() === 'Máte nějaké otázky? Zodpovíme je. Prosíme o pečlivé vyplnění kontaktních údajů.') {
			$(this).remove()
		}
	})
	$('.in-find-product p').each(function () {
		if ($(this).text() === 'Do you have any questions? We will answer them. Please fill in the contact details carefully.') {
			$(this).remove()
		}
	})
	if ($('.in-kontakty').length) {
		$('<div class="contact-form-title">Chcete se na něco zeptat?</div>').prependTo('#formContact')
	}
	if ($('.in-contacts').length) {
		$('<div class="contact-form-title">Do you have any questions?</div>').prependTo('#formContact')
	}
})
