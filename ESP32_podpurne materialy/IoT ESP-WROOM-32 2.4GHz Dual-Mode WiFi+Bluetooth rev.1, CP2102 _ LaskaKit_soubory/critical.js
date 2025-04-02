function shoptetRun($) {
	$('.in-index .benefitBanner').addClass('container').insertAfter($('#content-wrapper'))
	$('.body-banners > div').removeClass('col-sm-4').removeClass('col-sm-8')
	// KATEGORIE
	$('.category-perex').insertAfter('.category-title')
	let drobky = $('.breadcrumbs')
	drobky.prependTo('#content')
	document.addEventListener('ShoptetDOMPageContentLoaded', function () {
		$('.category-perex').insertAfter('.category-title')
		drobky.prependTo('#content')
	})

	$('.breadcrumbs').addClass('wrap-this')
	$('.category-title').addClass('wrap-this')
	$('.category-perex').addClass('wrap-this')
	$('.wrap-this').wrapAll('<div class="category-heading-wrapper"></div>')
	$('.category-perex .category-blog').appendTo('.category-heading-wrapper')
	document.addEventListener('ShoptetDOMPageContentLoaded', function () {
		if (!$('.category-heading-wrapper').length) {
			$('.breadcrumbs').addClass('wrap-this')
			$('.category-title').addClass('wrap-this')
			$('.category-perex').addClass('wrap-this')
			$('.wrap-this').wrapAll('<div class="category-heading-wrapper"></div>')
			$('.category-perex .category-blog').appendTo('.category-heading-wrapper')
			$('.wrap-this').wrapAll('<div class="category-heading-main"></div>')
		}
	})

	$('.wrap-this').wrapAll('<div class="category-heading-main"></div>')

	$('.site-msg.information').insertBefore($('.overall-wrapper'))
	$('#formSearchForm button').text('')
	$('#formSearchForm input').attr('placeholder', 'Zadejte hledaný výraz')
	$('.navigation-buttons a[data-target="cart"] .sr-only').text('Košík')
	$('.top-navigation-contacts > strong').text('Máte dotaz?')

	if (window.innerWidth > 767) {
		$('.top-navigation-tools a[data-target="login"].top-nav-button').prependTo('.navigation-buttons').text('Přihlásit')
		$('.top-navigation-tools .top-nav-button-account').prependTo('.navigation-buttons')
	} else {
		$('.header-top #oblibeneBtn').prependTo('.responsive-tools')
		document.addEventListener('dkLabFavouriteProductsLoaded', () => {
			$('.header-top #oblibeneBtn').prependTo('.responsive-tools')
		})
	}

	let cartPrice = $('.navigation-buttons a[data-target="cart"] .cart-price')
	if ($.trim(cartPrice.text()) === 'Prázdný košík') {
		cartPrice.text('0 Kč')
	}

	let openingHoursParent = $('.custom-footer .opening-hours').parent().parent().parent().parent()
	$('.custom-footer .opening-hours').insertAfter($('.top-navigation-contacts .project-phone'))
	openingHoursParent.remove()

	let categoryButton = $(document.createElement('a'))
	categoryButton.text('Kategorie').addClass('btn btn-conversion category-toggler')
	categoryButton.click(function () {
		$('.sidebar').toggle()
		$('body').toggleClass('sidebar-hidden')
	})
	categoryButton.prependTo($('#navigation .navigation-in'))

	if (window.innerWidth < 768) {
		$('.top-navigation-bar').insertAfter('#header')
		$('.header-top .navigation-buttons').appendTo('.top-navigation-bar .responsive-tools')
		$('#navigation .navigation-close').appendTo('.top-navigation-bar .responsive-tools')
		$('.navigation-close').on('touchstart', function (e) {
			e.preventDefault()
		})
		let sideControlers = $(document.createElement('div'))
		sideControlers.addClass('side-controlers')
		sideControlers.prependTo('.navigation-in')
		$(document).ready(function () {
			$('.top-navigation-tools .dropdown').prependTo(sideControlers)
			$('.top-navigation-tools .switcher').prependTo(sideControlers)
		})
		$('.p-detail-inner-header').insertBefore('.p-image-wrapper')
		$('.product-top .stars-wrapper').insertBefore('.p-image-wrapper')
		// DETAIL SLIDER
		let urlArray = Array()
		urlArray.push($('.p-main-image > img').attr('src'))
		$('.p-thumbnails-inner .p-thumbnail')
			.not(':first-child')
			.each(function () {
				urlArray.push($(this).attr('href'))
			})
		let sliderWrapper = $(document.createElement('div'))
		sliderWrapper.addClass('slick-slider-wrapper')
		$.each(urlArray, function () {
			let imgEl = $(document.createElement('img'))
			imgEl.attr('src', this)
			imgEl.appendTo(sliderWrapper)
		})
		$('.p-main-image').replaceWith(sliderWrapper)
		$(document).ready(function () {
			sliderWrapper.slick({
				autoplay: true,
				arrows: true,
				prevArrow: '<button class="slick-prev" type="button"><img src="/user/documents/assets/img/icon/slider-arrow.svg"></button>',
				nextArrow: '<button class="slick-next" type="button"><img src="/user/documents/assets/img/icon/slider-arrow.svg"></button>',
			})
		})
	}

	if ($('.type-detail').length) {
		$('.p-detail-inner-header').prependTo('.p-info-wrapper')
		$('.p-detail-info .stars-wrapper').insertAfter('.p-detail-inner-header')
		$('.p-detail-inner-header .p-code').insertAfter('.stars-wrapper')
		$('.p-detail-info > div').insertAfter('.p-code')

		let pocetSkladem = $('.p-info-wrapper .availability-amount')
		pocetSkladem.each(function () {
			$(this).text($(this).text().replace('(', ''))
			$(this).text($(this).text().replace(')', ''))
			$(this).css('color', document.querySelector('.p-info-wrapper .availability-label').style.color)
		})

		let deliveryWrapper = $(document.createElement('div')),
			sideInfoWrapper = $(document.createElement('div')),
			addToCartWrapper = $(document.createElement('div'))
		deliveryWrapper.addClass('delivery-wrapper')
		sideInfoWrapper.addClass('side-info-wrapper')
		addToCartWrapper.addClass('add-to-cart-wrapper')
		addToCartWrapper.insertBefore('.social-buttons-wrapper')
		$('.p-info-wrapper .detail-parameters .delivery-time-label').appendTo(deliveryWrapper)
		$('.p-info-wrapper .detail-parameters .delivery-time').appendTo(deliveryWrapper)

		deliveryWrapper.prependTo(sideInfoWrapper)
		$('.p-info-wrapper .availability-value').prependTo(sideInfoWrapper)
		sideInfoWrapper.prependTo(addToCartWrapper)
		$('.p-info-wrapper .p-final-price-wrapper').prependTo(addToCartWrapper)
		let shortDesc = $('.p-short-description'),
			moreInfo = shortDesc.next()
		shortDesc.insertBefore(addToCartWrapper)
		moreInfo.insertBefore(addToCartWrapper)
		$('.add-to-cart').appendTo(addToCartWrapper)
		moreInfo.find('a').text('Celý popis')
		$('.type-detail .p-info-wrapper .flags-default').appendTo('.p-image')
		setTimeout(function () {
			$('.p-info-wrapper .dkLabFavDiv').prependTo('.social-buttons-wrapper .link-icons')
		}, 100)
	}

	$('.cart-empty .cart-heading').text('V košíku nemáš žádné zboží')
	$('.cart-empty .empty-cart-boxes h3').text('Můžeš vyzkoušet naše vyhledávání')
	$('.cart-empty .empty-cart-boxes .search input').attr('placeholder', 'Co hledáš? Např. vývojová deska Arduino')
	$('.cart-empty .empty-cart-boxes').append('<a href="/" title="Zpět do obchodu" class="back-to-shop">Nebo to zkus znovu v obchodě</a>')
	document.addEventListener('ShoptetCartDeleteCartItem', function () {
		document.addEventListener('ShoptetDOMCartContentLoaded', function () {
			if (!$('.empty-cart-boxes .back-to-shop').length) {
				$('.cart-empty .empty-cart-boxes').append(
					'<a href="/" title="Zpět do obchodu" class="back-to-shop">Nebo to zkus znovu v obchodě</a>'
				)
			}
		})
	})
	$('.cart-header').prependTo('.cart-row')

	$('#highlited-categories .topic a').each(function () {
		let highlightedCat = $(this).attr('href')
		$('#categories .topic a[href="' + highlightedCat + '"]')
			.parent()
			.parent()
			.hide()
	})

	if ($('.type-category').length) {
		handleFilters()
		document.addEventListener('ShoptetDOMPageContentLoaded', handleFilters)
		document.addEventListener('ShoptetPageFilterValueChange', function () {
			let classVisible = $('.category-filter-headings .active').attr('class').split(/\s+/)[0]
			// console.log($('.category-filter-headings .active').attr('class'));
			window.sessionStorage.setItem('visible', classVisible)
		})
		document.addEventListener('ShoptetPageFiltersCleared', function () {
			window.sessionStorage.clear()
		})

		function handleFilters() {
			if (window.innerWidth >= 768) {
				$('#filters').addClass('visible filters').insertBefore('#category-header')
				$('.box-filters .filters-unveil-button-wrapper').remove()

				let categoryFilterHeadings = $(document.createElement('div'))
				categoryFilterHeadings.addClass('category-filter-headings')

				$('#manufacturer-filter h4').clone().addClass('filter-section-manufacturer').appendTo(categoryFilterHeadings)

				$('.filter-section-parametric h4').each(function () {
					$(this).parent().hide()
					let classList = $(this).parent().attr('class').split(/\s+/),
						identifier
					$.each(classList, function (index, item) {
						if (item.includes('filter-section-parametric-id')) {
							identifier = item
						}
					})
					$(this).clone().addClass(identifier).appendTo(categoryFilterHeadings)
				})
				$('#manufacturer-filter').hide()

				$('#clear-filters').appendTo(categoryFilterHeadings)

				$('.filter-section-count').insertAfter('#category-filter-hover')
				categoryFilterHeadings.prependTo('#category-filter-hover')
				$('.slider-wrapper').addClass('price-slider filter-section').prependTo('#filters .filter-section-boolean')

				let cacheVisible = window.sessionStorage.getItem('visible')
				if (cacheVisible) {
					$('.' + cacheVisible).addClass('active')
					$('#category-filter-hover .' + cacheVisible)
						.addClass('active')
						.show()
				}
				categoryFilterHeadings.find('h4').on('click', function () {
					let classList = $(this).attr('class').split(/\s+/),
						classToShow
					$.each(classList, function (index, item) {
						if (
							item.includes('filter-section-parametric-id') ||
							item.includes('filter-section-manufacturer') ||
							item.includes('price-slider')
						) {
							classToShow = item
						}
					})
					categoryFilterHeadings.find('h4').removeClass('active')
					$(this).addClass('active')
					$('#category-filter-hover .filter-section').hide().removeClass('active')
					$('#category-filter-hover')
						.children('.' + classToShow)
						.show()
						.addClass('active')
				})
			}
			if ($('.desktop').length) {
				$('<div class="filters-info"></div>').insertBefore('#filters')
			} else {
				$('<div class="filters-info"></div>').prependTo('.filters-wrapper')
				$('#category-filter-hover h4').each(function () {
					$(this).next('form').hide()
					$(this).click(function () {
						$(this).next('form').toggle()
					})
				})
			}
			$('#category-header>div').appendTo('.filters-info')
			$('.filter-total-count').appendTo('.filters-info')
			$('#category-header').appendTo('.filters-info')
			$('<span class="order-title"></span>').text($('#category-header input:checked + label').text()).prependTo('#category-header')

			$('#category-header .order-title').click(function () {
				$(this).next('form').toggleClass('visible')
			})
		}
	}

	// DPH SWITCHER
	if ($('.top-navigation-tools').length) {
		$(
			'<label class="switcher"><input type="checkbox" id="dph-switcher"><span class="switcher-slider switcher-round"></span> bez DPH</label>'
		).prependTo('.top-navigation-tools')

		handleDphSwitcher()

		if (
			localStorage.getItem('dph-switcher') !== null &&
			localStorage.getItem('dph-switcher') !== undefined &&
			localStorage.getItem('dph-switcher') === 'true'
		) {
			$('#dph-switcher').attr('checked', 'true')
			$('#productsTop .price-final, #products .price-final, #products-1 .price-final, #products-5 .price-final').css(
				'display',
				'none'
			)
			$(
				'#productsTop .price-additional, #products .price-additional, #products-1 .price-additional, #products-5 .price-additional'
			).css('display', 'flex !important')
			$('.products-top .product').each(function (idx) {
				const $priceAdditional = $(this).find('.price-additional')
				$priceAdditional[0].style.setProperty('display', 'block', 'important')
				$priceAdditional[0].style.setProperty('color', '#000')
				$priceAdditional[0].style.setProperty('font-size', '17px')
				$priceAdditional[0].style.setProperty('font-weight', '700')
			})
		} else {
			$('#dph-switcher').removeAttr('checked')
			$('#productsTop .price-final, #products .price-final, #products-1 .price-final, #products-5 .price-final').css(
				'display',
				'block'
			)
			$(
				'#productsTop .price-additional, #products .price-additional, #products-1 .price-additional, #products-5 .price-additional'
			).css('display', 'none')
		}

		$('#dph-switcher').change(function () {
			const isDphChecked = this.checked

			if (isDphChecked) {
				$('.products-top .price-final, #products .price-final, #products-1 .price-final, #products-5 .price-final').css(
					'display',
					'none'
				)
				$(
					'.products-top .price-additional, #products .price-additional, #products-1 .price-additional, #products-5 .price-additional'
				).css('display', 'flex')

				$('.products-top .product').each(function (idx) {
					const $priceAdditional = $(this).find('.price-additional')
					$priceAdditional[0].style.setProperty('display', 'block', 'important')
					$priceAdditional[0].style.setProperty('color', '#000')
					$priceAdditional[0].style.setProperty('font-size', '17px')
					$priceAdditional[0].style.setProperty('font-weight', '700')
				})
			} else {
				$('.products-top .price-final, #products .price-final, #products-1 .price-final, #products-5 .price-final').css(
					'display',
					'block'
				)
				$(
					'.products-top .price-additional, #products .price-additional, #products-1 .price-additional, #products-5 .price-additional'
				).css('display', 'none')
			}

			if (isDphChecked) {
				$('#dph-switcher').attr('checked', 'true')
				localStorage.setItem('dph-switcher', true)
			} else {
				$('#dph-switcher').removeAttr('checked')
				localStorage.setItem('dph-switcher', false)
			}
		})
	}

	document.addEventListener('ShoptetDOMContentLoaded', handleDphSwitcher)
	document.addEventListener('ShoptetPageFilterValueChange', handleDphSwitcher)
	document.addEventListener('ShoptetPagePaginationUsed', handleDphSwitcher)
	document.addEventListener('ShoptetPageSortingChanged', handleDphSwitcher)
	document.addEventListener('ShoptetPageSortingChanged', handleDphSwitcher)
	document.addEventListener('ShoptetPageFiltersRecalledFromHistory', handleDphSwitcher)
	document.addEventListener('ShoptetPagePriceFilterChange', handleDphSwitcher)
	document.addEventListener('ShoptetPageFilterValueChange', handleDphSwitcher)
	document.addEventListener('ShoptetPageFiltersCleared', handleDphSwitcher)
	document.addEventListener('ShoptetDOMPageMoreProductsLoaded', handleDphSwitcher)
	document.addEventListener('ShoptetDOMPageContentLoaded', handleDphSwitcher)
	document.addEventListener('resizeEnd', handleDphSwitcher)
	if ($('.in-oblibene')) {
		setTimeout(handleDphSwitcher, 1000)
	}

	function handleDphSwitcher() {
		$('.products .product').each(function () {
			if (!$(this).find('.price-additional strong').length) {
				$(this)
					.find('.price-additional')
					.wrapInner('<strong>' + /* $(this).find('.price-additional').text() + */ +'</strong>')
			}

			const strIndex = $(this).find('.price-additional strong').text().indexOf('bez DPH')
			if (strIndex > 0) {
				$(this).find('.price-additional strong').text($(this).find('.price-additional strong').text().slice(0, strIndex))
			}

			$(this).find('.price-additional').text($(this).find('.price-additional').text().split('(')[1])

			$(this).find('.price-additional').appendTo($(this).find('.product-bottom-prices'))
		})

		if (
			localStorage.getItem('dph-switcher') !== null &&
			localStorage.getItem('dph-switcher') !== undefined &&
			localStorage.getItem('dph-switcher') === 'true'
		) {
			$('#dph-switcher').attr('checked', 'true')
			$('#productsTop .price-final, #products .price-final, #products-1 .price-final, #products-5 .price-final').css(
				'display',
				'none'
			)
			$(
				'#productsTop .price-additional, #products .price-additional, #products-1 .price-additional, #products-5 .price-additional'
			).css('display', 'flex !important')
			$('.products-top .product').each(function (idx) {
				const $priceAdditional = $(this).find('.price-additional')
				$priceAdditional[0].style.setProperty('display', 'block', 'important')
				$priceAdditional[0].style.setProperty('color', '#000')
				$priceAdditional[0].style.setProperty('font-size', '17px')
				$priceAdditional[0].style.setProperty('font-weight', '700')
			})
		} else {
			$('#dph-switcher').removeAttr('checked')
			$('#productsTop .price-final, #products .price-final, #products-1 .price-final, #products-5 .price-final').css(
				'display',
				'block'
			)
			$(
				'#productsTop .price-additional, #products .price-additional, #products-1 .price-additional, #products-5 .price-additional'
			).css('display', 'none')
		}
		$('.products .product').each(function () {
			if (!($(this).find('.price-additional>span').text() == 'bez DPH')) {
				$(this).find('.price-additional').append('<span>bez DPH</span>')
			}
		})
	}

	if ($('.type-detail').length) {
		const withoutDph = $('.p-final-price-wrapper .price-additional')
		const withDph = $('.p-final-price-wrapper .price-final')

		if (
			localStorage.getItem('dph-switcher') !== null &&
			localStorage.getItem('dph-switcher') !== undefined &&
			localStorage.getItem('dph-switcher') === 'true'
		) {
			withoutDph[0].style.setProperty('font-size', '17px')
			withoutDph[0].style.setProperty('font-weight', '700')
			withDph[0].style.setProperty('font-size', '12px')
			withDph[0].style.setProperty('font-weight', '400')
		} else {
			withoutDph[0].style.setProperty('font-size', '12px')
			withoutDph[0].style.setProperty('font-weight', '400')
			withDph[0].style.setProperty('font-size', '24px')
			withDph[0].style.setProperty('font-weight', '700')
		}
	}

	document.documentElement.style.opacity = 1
}
const jQueryInterval = setInterval(function () {
	if (typeof jQuery != 'undefined') {
		shoptetRun(jQuery)
		clearInterval(jQueryInterval)
	}
}, 10)
