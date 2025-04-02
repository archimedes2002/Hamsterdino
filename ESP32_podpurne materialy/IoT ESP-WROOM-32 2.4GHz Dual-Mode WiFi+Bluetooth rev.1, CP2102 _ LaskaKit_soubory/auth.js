$(function () {
	// Registration page
	if ($('.in-registrace').length) {
		$('.in-registrace h1').text('Registrace nového uživatele')
		$('.in-registrace .register-soc').appendTo('.in-registrace #register-form .col-md-8')
		$('.in-registrace .register-soc h4').text('nebo')

		$('.in-registrace h4').each(function () {
			const h4 = $(this)
			if (h4.text() === 'Osobní údaje') {
				h4.text('Přihlašovací údaje (povinné)')
			}
		})

		$('.in-registrace .submit-wrapper').appendTo('.in-registrace #register-form .col-md-8 .co-box .box')

		$('.in-registrace .consents').each(function (idx, _) {
			if (idx === 0) {
				$(this).parent().remove()
				$(this).appendTo('.in-registrace #register-form .col-md-8 .co-box .box')
			}
		})

		$('.in-registrace #sendNewsletter').parent().parent().parent().appendTo('.in-registrace #register-form .col-md-8 .co-box .box')

		$(`<div class="auth-info">
      <div class="auth-info-title">Proč se registrovat?</div>
      <div class="auth-info-items">
        <p>
          <span><img src="/user/documents/assets/img/icon/done.svg" alt="done icon" /></span>
          <span>Nemusíš znovu vyplňovat adresy</span>
        </p>
        <p>
          <span><img src="/user/documents/assets/img/icon/done.svg" alt="done icon" /></span>
          <span>Získáš věrnostní slevy</span>
        </p>
        <p>
          <span><img src="/user/documents/assets/img/icon/done.svg" alt="done icon" /></span>
          <span>Můžeš sledovat objednávky</span>
        </p>
        <p>
          <span><img src="/user/documents/assets/img/icon/done.svg" alt="done icon" /></span>
          <span>30 dní na vrácení zboží</span>
        </p>
      </div>
    </div>`).appendTo('.in-registrace #register-form .col-md-4')
	}
	if ($('.in-registration').length) {
		$('.in-registration h1').text('New user registration')
		$('.in-registration .register-soc').appendTo('.in-registration #register-form .col-md-8')
		$('.in-registration .register-soc h4').text('or')

		$('.in-registration h4').each(function () {
			const h4 = $(this)
			if (h4.text() === 'Personal data') {
				h4.text('Login data (required)')
			}
		})

		$('.in-registration .submit-wrapper').appendTo('.in-registration #register-form .col-md-8 .co-box .box')

		$('.in-registration .consents').each(function (idx, _) {
			if (idx === 0) {
				$(this).parent().remove()
				$(this).appendTo('.in-registration #register-form .col-md-8 .co-box .box')
			}
		})

		$('.in-registration #sendNewsletter').parent().parent().parent().appendTo('.in-registration #register-form .col-md-8 .co-box .box')

		$(`<div class="auth-info">
      <div class="auth-info-title">Why to register?</div>
      <div class="auth-info-items">
        <p>
          <span><img src="/user/documents/assets/img/icon/done.svg" alt="done icon" /></span>
          <span>You don't have to fill in the addresses again</span>
        </p>
        <p>
          <span><img src="/user/documents/assets/img/icon/done.svg" alt="done icon" /></span>
          <span>You get loyalty discounts</span>
        </p>
        <p>
          <span><img src="/user/documents/assets/img/icon/done.svg" alt="done icon" /></span>
          <span>You can track orders</span>
        </p>
        <p>
          <span><img src="/user/documents/assets/img/icon/done.svg" alt="done icon" /></span>
          <span>30 days to return the goods</span>
        </p>
      </div>
    </div>`).appendTo('.in-registration #register-form .col-md-4')
	}

	// Forgot password page
	if ($('.in-zapomenute-heslo').length) {
		$('#formForgottenPassword h2').text('Zapomenuté heslo')

		$(`<div class="auth-password-info">
      <div class="auth-password-title">Jak to funguje?</div>
      <div class="auth-password-items">
      
        <div class="auth-password-item">
          <span class="auth-password-number">1.</span>
          <span class="auth-password-text">Zadej svůj e-mail, který jsi uvedl při registraci a klikni na Obnovit heslo.</span>
        </div>
        
        <div class="auth-password-item">
          <span class="auth-password-number">2.</span>
          <span class="auth-password-text">Zkontroluj svůj e-mail. Zaslali jsme ti návod, jak si nastavit nové heslo.</span>
        </div>
        
        <div class="auth-password-item">
          <span class="auth-password-number">3.</span>
          <span class="auth-password-text">Uloži si nové heslo do seznamu hesel v prohlížeči, aby jsi ho znovu nezapomněl :)</span>
        </div>

      </div>
    </div>
    `).appendTo('#formForgottenPassword')
	}

	if ($('.in-forgotten-password').length) {
		$('#formForgottenPassword h2').text('Forgotten password')

		$(`<div class="auth-password-info">
      <div class="auth-password-title">How does it work?</div>
      <div class="auth-password-items">
      
        <div class="auth-password-item">
          <span class="auth-password-number">1.</span>
          <span class="auth-password-text">Enter the email you provided when you registered and click on Reset Password.</span>
        </div>
        
        <div class="auth-password-item">
          <span class="auth-password-number">2.</span>
          <span class="auth-password-text">Check your email. We've sent you instructions on how to set a new password.</span>
        </div>
        
        <div class="auth-password-item">
          <span class="auth-password-number">3.</span>
          <span class="auth-password-text">Save your new password in your browser's password list so you don't forget it again :)</span>
        </div>

      </div>
    </div>
    `).appendTo('#formForgottenPassword')
	}
})
