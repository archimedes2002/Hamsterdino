if (typeof PWJS == 'undefined') {
  window.PWJS = {};
}

PWJS['Shortcodes'] = {
  replaceForWidgets: function() {
    const widgets = document.body.textContent.match(/##PRODUCT-?WIDGETS-\d+##/gi) || [];
    for(widget of widgets) {
      const elements = Array.from(document.querySelectorAll('*'));
      let containingElements = elements.filter(element => {
        if (element.tagName == 'HTML' || element.tagName == 'HEAD' || element.tagName == 'BODY') {
          return false;
        }
        return element.textContent.includes(widget);
      });

      let container = containingElements.pop();
      if (container) {
        const id = widget.match(/\d+/);

        container.innerHTML = container.innerHTML.replace(widget, `<span id='pw${id}'></span>`);

        const script = document.createElement("script");
        script.setAttribute('src', `https://app.productwidgets.cz/e/${id}.js`);
        script.setAttribute('async', true);
        script.setAttribute('id', `pwjs${id}`);

        const span = container.querySelector(`span#pw${id}`)
        span.parentNode.replaceChild(script, span);
      }
    }
  },

  loadAfterDynamicPagination: function() {
    const scripts = document.querySelectorAll("script[id^='pwjs']");
    for(script of scripts) {
      const id = script.id.replace('pwjs', '');

      if (script.nextElementSibling && (script.nextElementSibling.id === `pwjsroot${id}`)) {
        // do nothing
      } else {
        const newScript = document.createElement("script");
        newScript.setAttribute('src', `https://app.productwidgets.cz/e/${id}.js`);
        newScript.setAttribute('async', true);
        newScript.setAttribute('id', `pwjs${id}`);

        script.parentNode.replaceChild(newScript, script);
      }
    }
  }
}

if (document.readyState != 'loading'){
  PWJS.Shortcodes.replaceForWidgets()
} else {
  document.addEventListener('DOMContentLoaded', PWJS.Shortcodes.replaceForWidgets);
  document.addEventListener('ShoptetDOMPageContentLoaded', PWJS.Shortcodes.replaceForWidgets);
  document.addEventListener('ShoptetDOMPageContentLoaded', PWJS.Shortcodes.loadAfterDynamicPagination);
}
