// https://medium.com/@haxzie/dark-and-light-theme-switcher-using-css-variables-and-pure-javascript-zocada-dd0059d72fa2

// function to set a given theme/color-scheme
function set_theme(theme_name) {
    localStorage.setItem('theme', theme_name);
    document.documentElement.className = theme_name;
}

// function to toggle between light and dark theme
function toggle_theme() {
   if (localStorage.getItem('theme') === 'theme-dark'){
       set_theme('theme-light');
   } else {
       set_theme('theme-dark');
   }
}

// Immediately invoked function to set the theme on initial load
function init_theme() {
    try {
        if (localStorage.getItem('theme') === 'theme-dark') {
            set_theme('theme-dark');
            $(".color-theme-toggle input").prop("checked", true);
        } else {
            set_theme('theme-light');
            $(".color-theme-toggle input").prop("checked", false);
        }
    } catch (error) {}
}

// Run this as soon as possible to set the color theme for loading screen
init_theme();

auto_run.queue( 
    function() {
        // Initiate theme again to set the toggle button state based on the current theme
        init_theme();

        // Change color theme on click and still show the menu
        $(".color-theme-toggle input").click(toggle_theme);
        // https://stackoverflow.com/questions/25089297/avoid-dropdown-menu-close-on-click-inside
        $('.dropdown-menu').on('click', function(event) {
            // The event won't be propagated up to the document NODE and 
            // therefore delegated events won't be fired
            event.stopPropagation();
        });
    }
);

