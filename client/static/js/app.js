URL = window.URL || window.webkitURL;

var gumStream;
var rec;
var input;
var AudioContext = window.AudioContext || window.webkitAudioContext;
var audioContext;
var recordButton = document.getElementById("recordButton");
var stopButton = document.getElementById("stopButton");

recordButton.addEventListener("click", startRecording);
stopButton.addEventListener("click", stopRecording);

function startRecording() {
  var constraints = { audio: true, video: false };
  recordButton.disabled = true;
  stopButton.disabled = false;
  navigator.mediaDevices
    .getUserMedia(constraints)
    .then(function (stream) {
      audioContext = new AudioContext();
      document.getElementById("formats").innerHTML =
        "Format: 1 channel pcm @ " + audioContext.sampleRate / 1000 + "kHz";
      gumStream = stream;
      input = audioContext.createMediaStreamSource(stream);
      rec = new Recorder(input, { numChannels: 1 });
      rec.record();
    })
    .catch(function (err) {
      recordButton.disabled = false;
      stopButton.disabled = true;
    });
}

function stopRecording() {
  stopButton.disabled = true;
  recordButton.disabled = false;
  rec.stop();
  gumStream.getAudioTracks()[0].stop();
  rec.exportWAV(createDownloadLink);
}

function createDownloadLink(blob) {
  var url = URL.createObjectURL(blob);
  var au = document.createElement("audio");
  var li = document.createElement("li");
  var filename = new Date().toISOString();
  au.controls = true;
  au.src = url;
  li.appendChild(au);

  var upload = document.createElement("a");
  upload.href = "#";
  upload.innerHTML = "<button>Submit</button>";
  upload.addEventListener("click", function (event) {
    var xhr = new XMLHttpRequest();
    var fd = new FormData();
    fd.append("audio_data", blob, filename);
    xhr.open("POST", "/api/v1/process-audio", true);
    xhr.send(fd);
    recordingsList.innerHTML = "";
  });
  li.appendChild(upload);
  recordingsList.innerHTML = "";
  recordingsList.appendChild(li);
}
