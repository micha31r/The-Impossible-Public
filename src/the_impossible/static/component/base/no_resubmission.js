// Js to prevent form resubmission
// https://www.webtrickshome.com/faq/how-to-stop-form-resubmission-on-page-refresh
if ( window.history.replaceState ) window.history.replaceState( null, null, window.location.href );