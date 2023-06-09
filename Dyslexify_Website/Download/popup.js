const toggles = document.querySelectorAll(".section-toggle");

toggles.forEach((toggle) => {
  toggle.addEventListener("change", () => {
  	if(toggle.checked) {
    	toggle.parentNode.parentNode.parentNode.classList.add("active");
    }
    else{
    	toggle.parentNode.parentNode.parentNode.classList.remove("active");
    }
  });
});

var session = {
	'DyslexicFont': {
	    'status': false,
	    'family': 'opendyslexic-regular',
	    'size': 14
	},
	'Spacing': {
	    'status': false,
	    'letter': 0.1,
	    'word': 0.5
	},
	'Ruler': {
	    'status': false,
	    'height' : 24
	},
	'LineHeight': {
	    'status': false,
	    'factor': 1.5
	}
};

var font_toggle = document.getElementById('FontToggle');
var ruler_toggle = document.getElementById('RulerToggle');
var spacing_toggle = document.getElementById('SpacingToggle');
var lineht_toggle = document.getElementById('LineHtToggle');

window.onload = function() {
	chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
		chrome.tabs.sendMessage(tabs[0].id, {begin: "Send Session"}, function(response) {
			session = response.session;
			console.log("updated");
			console.log(session);

			// Font
			document.querySelector(`option[value="${session['DyslexicFont']['family']}"]`).selected = true;
			document.querySelector('#fontsize-num').value = session['DyslexicFont']['size'];
			document.querySelector('#fontsize-slider').value = session['DyslexicFont']['size'];
			if (session['DyslexicFont']['status']) {
		        font_toggle.checked = true;
		        font_toggle.parentNode.parentNode.parentNode.classList.add("active");
		    }

		    // Spacing
			document.querySelector('#wordsp-num').value = session['Spacing']['word'];
			document.querySelector('#lettersp-num').value = session['Spacing']['letter'];
			document.querySelector('#wordsp-slider').value = session['Spacing']['word'];
			document.querySelector('#lettersp-slider').value = session['Spacing']['letter'];
			if (session['Spacing']['status']) {
		        spacing_toggle.checked = true;
		        spacing_toggle.parentNode.parentNode.parentNode.classList.add("active");
		    }

		    // Ruler
			document.querySelector('#ruler-height-num').value = session['Ruler']['height'];
			document.querySelector('#ruler-height-slider').value = session['Ruler']['height'];
			if (session['Ruler']['status']) {
		        ruler_toggle.checked = true;
		        ruler_toggle.parentNode.parentNode.parentNode.classList.add("active");
		    }

		    // Line Height
			document.querySelector('#lha-num').value = session['LineHeight']['factor'];
			document.querySelector('#lha-slider').value = session['LineHeight']['factor'];
			if (session['LineHeight']['status']) {
		        lineht_toggle.checked = true;
		        lineht_toggle.parentNode.parentNode.parentNode.classList.add("active");
		    }

		});
	});
}

// toggle events
font_toggle.addEventListener('change', function(event) {
  chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
    session['DyslexicFont']['status'] = font_toggle.checked;
    chrome.tabs.sendMessage(tabs[0].id, {session: session});
  });
});

ruler_toggle.addEventListener('change', function(event) {
  chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
    session['Ruler']['status'] = ruler_toggle.checked;
    chrome.tabs.sendMessage(tabs[0].id, {session: session});
  });
});

spacing_toggle.addEventListener('change', function(event) {
  chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
    session['Spacing']['status'] = spacing_toggle.checked;
    chrome.tabs.sendMessage(tabs[0].id, {session: session});
  });
});

lineht_toggle.addEventListener('change', function(event) {
  chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
    session['LineHeight']['status'] = lineht_toggle.checked;
    chrome.tabs.sendMessage(tabs[0].id, {session: session});
  });
});


// update events
document.querySelector('select[name=fonttype]').addEventListener('change', event => {
	chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
	    session['DyslexicFont']['family'] = event.target.value;
	    chrome.tabs.sendMessage(tabs[0].id, {session: session});
	});
})

document.querySelector('#fontsize-num').addEventListener('input', function(event) {
	document.querySelector('#fontsize-slider').value = event.target.value;
	chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
	    session['DyslexicFont']['size'] = event.target.value;
	    chrome.tabs.sendMessage(tabs[0].id, {session: session});
	});
});

document.querySelector('#fontsize-slider').addEventListener('input', function(event) {
	document.querySelector('#fontsize-num').value = event.target.value;
	chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
	    session['DyslexicFont']['size'] = event.target.value;
	    chrome.tabs.sendMessage(tabs[0].id, {session: session});
	});
});

document.querySelector('#lha-num').addEventListener('input', function(event) {
	document.querySelector('#lha-slider').value = event.target.value;
	chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
	    session['LineHeight']['factor'] = event.target.value;
	    chrome.tabs.sendMessage(tabs[0].id, {session: session});
	});
});

document.querySelector('#lha-slider').addEventListener('input', function(event) {
	document.querySelector('#lha-num').value = event.target.value;
	chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
	    session['LineHeight']['factor'] = event.target.value;
	    chrome.tabs.sendMessage(tabs[0].id, {session: session});
	});
});

document.querySelector('#ruler-height-num').addEventListener('input', function(event) {
	document.querySelector('#ruler-height-slider').value = event.target.value; 
	chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
    	session['Ruler']['height'] = event.target.value;
   		chrome.tabs.sendMessage(tabs[0].id, {session: session});
   	});
});

document.querySelector('#ruler-height-slider').addEventListener('input', function(event) {
	document.querySelector('#ruler-height-num').value = event.target.value; 
	chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
    	session['Ruler']['height'] = event.target.value;
   		chrome.tabs.sendMessage(tabs[0].id, {session: session});
   	});
});

document.querySelector('#wordsp-num').addEventListener('input', function(event) {
	document.querySelector('#wordsp-slider').value = event.target.value;
	chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
	    session['Spacing']['word'] = event.target.value;
	    chrome.tabs.sendMessage(tabs[0].id, {session: session});
	});
});

document.querySelector('#wordsp-slider').addEventListener('input', function(event) {
	document.querySelector('#wordsp-num').value = event.target.value;
	chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
	    session['Spacing']['word'] = event.target.value;
	    chrome.tabs.sendMessage(tabs[0].id, {session: session});
	});
});

document.querySelector('#lettersp-num').addEventListener('input', function(event) {
	document.querySelector('#lettersp-slider').value = event.target.value;
	chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
    	session['Spacing']['letter'] = event.target.value;
    	chrome.tabs.sendMessage(tabs[0].id, {session: session});
    });
});

document.querySelector('#lettersp-slider').addEventListener('input', function(event) {
	document.querySelector('#lettersp-num').value = event.target.value;
	chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
    	session['Spacing']['letter'] = event.target.value;
    	chrome.tabs.sendMessage(tabs[0].id, {session: session});
    });
});