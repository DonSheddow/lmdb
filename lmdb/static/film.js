'use strict';



window.onload = function() {


    videojs("video", {}, function() {
        var video = videojs('video');
        this.__duration = -1;
        this.duration = function() { return video.__duration; };

        this.currentTime = function(time) {
            if (time == undefined) {
                return video.start;
            }
            else {
                console.log(time);
                video.start = time;
                video.src("/media/test.ogv?start=" + time);
                video.play();
                console.log(this);
            }
        }

        video = this;
        var xhr = new XMLHttpRequest();
        xhr.onreadystatechange = function() {
            var response = JSON.parse(this.responseText);
            console.log(response.duration);
            video.__duration = response.duration;
        }
        xhr.open("GET", "/media/duration.js", true);
        xhr.send();
    });
}

