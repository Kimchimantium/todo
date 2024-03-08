//make index.html table collapse button 'caret-up, caret-down'
document.addEventListener("DOMContentLoaded", function() {
    var collapseElement = document.getElementById('collapseTable');
    var toggleIcon = document.getElementById('toggleIcon');

    // Listen for when the collapse element is shown
    collapseElement.addEventListener('show.bs.collapse', function () {
        toggleIcon.classList.remove('fa-rotate-180');
    });

    // Listen for when the collapse element is hidden
    collapseElement.addEventListener('hide.bs.collapse', function () {
        toggleIcon.classList.add('fa-rotate-180');
    });
});

document.addEventListener('DOMContentLoaded', function() {
    var countDownDate = new Date("{{ todo.date }}T{{ todo.time }}").getTime();

    var x = setInterval(function() {
        var now = new Date().getTime();
        var distance = countDownDate - now;

        if (distance < 0) {
            clearInterval(x);
            document.getElementById("timer{{ todo.id }}").innerHTML = "EXPIRED";
        } else {
            var days = Math.floor(distance / (1000 * 60 * 60 * 24));
            var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
            var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
            var seconds = Math.floor((distance % (1000 * 60)) / 1000);

            document.getElementById("timer{{ todo.id }}").innerHTML = days + "d " + hours + "h "
            + minutes + "m " + seconds + "s ";
        }
    }, 1000);
});
document.addEventListener('DOMContentLoaded', function() {
    var timers = document.querySelectorAll('.timer');

    timers.forEach(function(timer) {
        var countDownDate = new Date(timer.getAttribute('data-time')).getTime();
        var x = setInterval(function() {
            var now = new Date().getTime();
            var distance = countDownDate - now;

            if (distance < 0) {
                clearInterval(x);
                timer.innerHTML = "OUTDATED";
                timer.style.color = "grey"; // Set to grey if the event is outdated
            } else {
                var days = Math.floor(distance / (1000 * 60 * 60 * 24));
                var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
                var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
                var seconds = Math.floor((distance % (1000 * 60)) / 1000);

                timer.innerHTML = days + "d " + hours + "h " + minutes + "m " + seconds + "s ";

                // Remove any previously set color if more than one day is left
                if (days > 0) {
                    timer.style.color = ""; // Don't apply any color if more than a day is left
                } else if (hours < 1) {
                    timer.style.color = "red"; // Less than 1 hour
                } else if (hours < 3) {
                    timer.style.color = "orange"; // Less than 3 hours
                } else if (24 > hours <= 3) {
                    timer.style.color = "green"; // Less than 3 hours
                } else {
                    timer.style.color = "grey"; // Apply grey for 3 hours or more but less than a day
                }
            }
        }, 1000);
    });
});

//index.html fa-plus anime when collapsed expanded
$(document).ready(function() {
    // Listen for when the collapse element begins to be shown
    $('#collapseExample').on('show.bs.collapse', function () {
        anime({
            targets: 'a[href="#collapseExample"] .fa-plus', // Target the icon within the anchor
            rotate: 45, // Rotate to 45 degrees
            duration: 300, // Duration of the animation
            easing: 'easeInOutSine' // Easing function for a smooth effect
        });
    });

    // Listen for when the collapse element begins to be hidden
    $('#collapseExample').on('hide.bs.collapse', function () {
        anime({
            targets: 'a[href="#collapseExample"] .fa-plus', // Target the icon within the anchor
            rotate: 0, // Rotate back to 0 degrees
            duration: 300, // Duration of the animation
            easing: 'easeInOutSine' // Easing function for a smooth effect
        });
    });
});

//index.html fa-caret anime when collapsed expanded
//index.html fa-plus anime when collapsed expanded
$(document).ready(function() {
    // Listen for when the collapse element begins to be shown
    $('#collapseTable').on('show.bs.collapse', function () {
        anime({
            targets: 'a[href="#collapseTable"] .fa-caret-up', // Target the icon within the anchor
            rotate: 0, // Rotate to 180 degrees
            duration: 300, // Duration of the animation
            easing: 'easeInOutSine' // Easing function for a smooth effect
        });
    });

    // Listen for when the collapse element begins to be hidden
    $('#collapseTable').on('hide.bs.collapse', function () {
        anime({
            targets: 'a[href="#collapseTable"] .fa-caret-up', // Target the icon within the anchor
            rotate: 180, // Rotate back to 0 degrees
            duration: 300, // Duration of the animation
            easing: 'easeInOutSine' // Easing function for a smooth effect
        });
    });
});
