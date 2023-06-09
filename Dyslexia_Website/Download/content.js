console.log("LEXILEARN extension started !!");

let session = {
    'DyslexicFont': {
        'status': false,
        'family': "opendyslexic-regular",
        'size': 14
    },
    'Spacing': {
        'status': false,
        'letter': 0.1,
        'word': 0.5
    },
    'Ruler': {
        'status': false,
        'height': 24
    },
    'LineHeight': {
        'status': false,
        'factor': 1.5
    }
};

chrome.runtime.onMessage.addListener(
    function(request, sender, sendResponse) {
        if (request.begin) {
            sendResponse({ session: session });
        } else {
            console.log(request.session);
            var req = request.session;

            session['DyslexicFont'] = req.DyslexicFont;
            session['Spacing'] = req.Spacing;
            session['Ruler'] = req.Ruler;
            session['LineHeight'] = req.LineHeight;

            console.log(session);
            // Font
            if (session['DyslexicFont']['status']) {
                applyFont("font-family", session['DyslexicFont']['family']);
                applyFont("font-size", session['DyslexicFont']['size']);
            } else {
                revertFont("font-family");
                revertFont("font-size");
            }

            // Spacing
            if (session['Spacing']['status']) {
                applySpacing("word-spacing", session['Spacing']['word']);
                applySpacing("letter-spacing", session['Spacing']['letter']);
            } else {
                revertSpacing("word-spacing");
                revertSpacing("letter-spacing");
            }

            // Ruler
            createRuler(session['Ruler']['status'], session['Ruler']['height']);

            // Line Height
            if (session['LineHeight']['status']) {
                let tags = ["p", "ul", "ol"];
                applyLineHeight(tags, session['LineHeight']['factor']);
            } else {
                revertLineHeight(["p", "ul", "ol"]);
            }
        }
    }
);


/* Font */
function applyFont(attr, input) {
    if (attr == "font-size") {
        input = `${input}pt`;
    }
    document.querySelector('body').style[attr] = input;
};

function revertFont(attr) {
    document.querySelector('body').style.removeProperty(attr);
}

/* Spacing */
function applySpacing(attr, input) {
    input = `${input}em`;
    document.querySelector('body').style[attr] = input;
};

function revertSpacing(attr) {
    document.querySelector('body').style.removeProperty(attr);
}

/* Ruler */
function createRuler(active, height) {
    var ruler = document.querySelector("#readingRuler");

    // If ruler doesn't exist:
    if (!ruler) {
        // Make ruler:
        ruler = document.createElement("div");
        ruler.id = "readingRuler";
        let body = document.querySelector("body")
        body.appendChild(ruler);
    }

    if (active) {
        // Active/Inactive:
        if (parseInt(active) === 0) {
            ruler.classList.add("inactive");
        } else {
            ruler.classList.remove("inactive");
        }

        ruler.style.setProperty('--height', `${height}px`);
        document.addEventListener('mousemove', e => {
            ruler.style.setProperty('--mouse-y', `${e.clientY-(height*0.66)}px`);
        });
        ruler.style.setProperty('--hue', 'hsl(54, 97%, 49%)');
        ruler.style.setProperty('--opacity', 0.2);
    } else {
        ruler.style.setProperty('--opacity', 0);
    }
}

/* Line Height */
function getTagList(tag) {
    let body = document.querySelector('body');
    return body.querySelectorAll(tag);
}

function applyLineHeight(tags, input) {
    let factor = parseFloat(input);
    tags.forEach(function(tag) {
        let els = getTagList(tag);
        for (let i = 0; i < els.length; i++) {
            let el = els[i];
            el.style.removeProperty('line-height');
            let original = getComputedStyle(el).lineHeight;
            let originalVal = parseFloat(original.slice(0, original.length - 2));
            let adjusted = originalVal * factor;
            let adjustedStr = `${adjusted}px`;
            el.style.lineHeight = adjustedStr;
        }
    });
};

function revertLineHeight(tags) {
    tags.forEach(function(tag) {
        let els = getTagList(tag);
        for (let i = 0; i < els.length; i++) {
            els[i].style.removeProperty('line-height');
        }
    });
}

/* Google Custom Image Search API */
document.body.innerHTML += "<div data-ml-modal id='speakModal'><a href='' class='modal-overlay'></a><div class='modal-dialog'><div class='modal-content text-center'><p  id='speakText'></p><div id='imgdiv' style='margin-bottom: 20px; display: none'><img id='textImg' src='' width='50%'></div><button id='text-to-speech-btn' type='button' class='modal-button'><span>SPEAK</span></button></div></div></div>";

function loadImageClient() {
    gapi.client.setApiKey("GOOGLE_API_KEY");
    return gapi.client.load("https://content.googleapis.com/discovery/v1/apis/customsearch/v1/rest")
        .then(function() { console.log("GAPI client loaded for API"); },
            function(err) { console.error("Error loading GAPI client for API", err); });
}

function executeImageSearch(text) {
    return gapi.client.search.cse.list({
            "cx": "1d1e43e846323a46a",
            "exactTerms": text,
            "filter": "1",
            "num": 1,
            "searchType": "image",
            "start": 1
        })
        .then(function(response) {
                //console.log("Response", response.result);
                return response.result.queries.items[0].image.thumbnailLink;
            },
            function(err) { console.error("Execute error", err); });
}

gapi.load("client");

window.addEventListener("mouseup", function(e) {
    e.preventDefault();
    var selectedText = getSelectedText();

    if (selectedText != "") {
        console.log(selectedText);

        var modal = document.getElementById("speakText");
        modal.innerHTML = selectedText;

        var imgdiv = document.getElementById("imgdiv");
        var img = document.getElementById("textImg");
        var text = selectedText;

        loadImageClient();
        var imgurl = executeImageSearch(text);

        img.src = imgurl;
        imgdiv.style.display = 'block';

        var str = window.location.href;
        var url = str.substring(0, str.indexOf('#'));
        console.log(url);
        window.location.href = url + "#speakModal";
    } else {
        console.log("Nothing!");
    }
});

function getSelectedText() {
    var selectedText = '';

    // window.getSelection 
    if (window.getSelection) {
        selectedText = window.getSelection().toString();
    }
    // document.getSelection 
    else if (document.getSelection) {
        selectedText = document.getSelection().toString();
    }
    // document.selection 
    else if (document.selection) {
        selectedText =
            document.selection.createRange().text;
    }
    return selectedText;
}

/* Google Text-To-Speech API */
function authenticate() {
    return gapi.auth2.getAuthInstance()
        .signIn({ scope: "https://www.googleapis.com/auth/cloud-platform" })
        .then(function() { console.log("Sign-in successful"); },
            function(err) { console.error("Error signing in", err); });
}

function loadTTSClient() {
    gapi.client.setApiKey("GOOGLE_TEXT_TO_SPEECH_API_KEY");
    return gapi.client.load("https://texttospeech.googleapis.com/$discovery/rest?version=v1beta1")
        .then(function() { console.log("GAPI client loaded for API"); },
            function(err) { console.error("Error loading GAPI client for API", err); });
}

function executeTTS() {
    return gapi.client.texttospeech.text.synthesize({
            "resource": {
                "input": {
                    "text": "Good Morning"
                },
                "audioConfig": {
                    "audioEncoding": "OGG_OPUS"
                },
                "voice": {
                    "languageCode": "en-US",
                    "ssmlGender": "MALE"
                }
            }
        })
        .then(function(response) {
                console.log("Response", response.result.audioContent);
                return response.result.audioContent;
            },
            function(err) {
                console.error("Execute error", err);
            });
}

gapi.load("client:auth2", function() {
    gapi.auth2.init({ client_id: "GOOGLE_CLIENT_ID" });
});

document.getElementById("text-to-speech-btn").addEventListener("click", function(e) {
    e.preventDefault();

    var txt = document.getElementById('speakText').innerHTML;
    console.log(txt);

    // Loading and authenticating the client
    authenticate();
    loadTTSClient();

    executeTTS();
})