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

  var upload = document.createElement("button");
  upload.innerHTML = "Submit";
  li.appendChild(upload);
  var predict = document.createElement("button");
  predict.innerHTML = "Predict";
  li.appendChild(predict);
  recordingsList.innerHTML = "";
  recordingsList.appendChild(li);

  upload.addEventListener("click", function (event) {
    var xhr = new XMLHttpRequest();
    var fd = new FormData();
    fd.append("audio_data", blob, filename);
    xhr.open("POST", "/api/v1/process-audio", false);
    xhr.send(fd);
    xhr.open("GET", "/", false);
    xhr.send(null);
    recordingsList.innerHTML = "";
  });

  predict.addEventListener("click", function (event) {
    predict.disabled = true;
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function () {
      if (xhr.readyState == XMLHttpRequest.DONE) {
        alert("The model thought this sentence showed " + xhr.responseText + ".");
      }
    };
    var fd = new FormData();
    fd.append("audio_data", blob, filename);
    xhr.open("POST", "/api/v1/predict", false);
    resp = xhr.send(fd);
  });
}
