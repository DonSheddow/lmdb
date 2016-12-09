'use strict';

window.onload = function() {
    var player = videojs("video", {aspectRatio: "16:9", preload: "none"}, function() {
        var player = this;
        player.__duration = -1;
        player.duration = function() { return player.__duration; };

        player.oldCurrentTime = player.currentTime;
        player.currentTime = function(time) {
            if (time == undefined) {
                return player.oldCurrentTime() + player.start;
            }
            else {
                player.start = time;
                player.oldCurrentTime(0);
                player.src("/media/test.mp4?start=" + time);
                player.play();
                return this;
            }
        }

        var xhr = new XMLHttpRequest();
        xhr.onreadystatechange = function() {
            var response = JSON.parse(this.responseText);
            console.log(response.duration);
            player.__duration = response.duration;
        }
        xhr.open("GET", "/media/duration.js", true);
        xhr.send();
    });

    var play_button = document.getElementById("play-button");
    var video_hider = document.getElementById("video-hider");
    var video_container = document.getElementById("video-container");
    play_button.onclick = function() {
        video_hider.classList.remove("hidden");
        video_container.classList.add("show");
        play_button.classList.toggle("rotate");

        player.play();
        // Call currentTime() to get duration to display and seek bar to move
        player.currentTime(0);

        var hidden = false;
        play_button.onclick = function() {
            video_hider.classList.toggle("hidden");
            play_button.classList.toggle("rotate");

            if (!hidden){
                player.pause();
            }
            hidden = !hidden;
        }

/*        video_container.addEventListener("animationend", function() {

        });*/
    }
}

