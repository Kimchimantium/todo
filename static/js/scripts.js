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

$(document).ready(function() {
    $('form').submit(function(e) {
        var formData = $(this).serialize(); // Serialize form data

        $.ajax({
            type: "POST",
            url: $(this).attr('action'), // or directly to your route, e.g., '/your-route'
            data: formData,
            success: function(response) {
                // Reset the form here
                $('form')[0].reset();
            }
        });
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

            // Calculate time left
            var days = Math.floor(distance / (1000 * 60 * 60 * 24));
            var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
            var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));

            // Change timer color based on time left
            if (distance < 0) {
                clearInterval(x);
                timer.innerHTML = "OUTDATED";
                timer.style.color = "grey"; // Choose a color for outdated timers
            } else {
                timer.innerHTML = days + "d " + hours + "h " + minutes + "m ";

                // Applying color based on the remaining time
                if (days > 0) {
                    timer.style.color = "green"; // If it's more than a day left
                } else if (hours < 1) {
                    timer.style.color = "red"; // Less than 1 hour
                } else if (hours < 3) {
                    timer.style.color = "orange"; // Less than 3 hours
                } else {
                    timer.style.color = "green"; // 3 hours or more but less than a day
                }
            }
        }, 1000);
    });
});