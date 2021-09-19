function include(file) {
    const script = document.createElement('script');
    script.src = file;
    script.type = 'text/javascript';
    script.defer = true;

    document.getElementsByTagName('head').item(0).appendChild(script);
}

/* include all the components js file */

include('http://localhost:5000/files/static/js/components/chat.js');
include('http://localhost:5000/files/static/js/constants.js');
include('http://localhost:5000/files/static/js/components/cardsCarousel.js');
include('http://localhost:5000/files/static/js/components/botTyping.js');
include('http://localhost:5000/files/static/js/components/charts.js');
include('http://localhost:5000/files/static/js/components/collapsible.js');
include('http://localhost:5000/files/static/js/components/dropDown.js');
include('http://localhost:5000/files/static/js/components/location.js');
include('http://localhost:5000/files/static/js/components/pdfAttachment.js');
include('http://localhost:5000/files/static/js/components/quickReplies.js');
include('http://localhost:5000/files/static/js/components/suggestionButtons.js');
