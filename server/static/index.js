window.setInterval(pollPi, 2000);
window.setInterval(pollLight, 2000);
window.setInterval(pollDoor, 2000);
window.setInterval(pollMotion, 2000);
window.setInterval(clearMotion, 5000);
window.setInterval(pollWater, 2000);
window.setInterval(pollSound, 2000);
window.setInterval(pollFlame, 2000);

var statusp = document.getElementById("pinstatus");
var humid = document.getElementById("humidity");
var light = document.getElementById("light");
var door = document.getElementById("door");
var motion = document.getElementById("motion");
var water = document.getElementById("water");
var flame = document.getElementById("flame");
var mode = document.getElementById("mode");

getMode();

const checkbox = document.getElementById('modecheck')

checkbox.addEventListener('change', async (event) => {
  if (event.currentTarget.checked) {
  mode.innerHTML = "Mode: armed";
    let response = fetch('/setmode', {
  method: 'POST', // or 'PUT'
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({mode: "Mode: armed"}),
});
  } else {
  mode.innerHTML = "Mode: disarmed";
    let response = fetch('/setmode', {
  method: 'POST', // or 'PUT'
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({mode: "Mode: disarmed"}),
});
  }
})

async function getMode() {
    let response = await fetch('/mode');
    if (response.ok) { // if HTTP-status is 200-299
        let resp = await response.text();
        mode.innerHTML = resp;
        if (resp === "Mode: armed") {
            checkbox.checked = true;
           }
    } else {
        console.log("HTTP-Error: " + response.status);
     }
}

async function pollPi() {
    let response = await fetch('/status');
    if (response.ok) { // if HTTP-status is 200-299
        let resp = await response.text();
        let humidity = resp.split("$")[1].trim();
        resp = resp.split("$")[0].trim();
        if (resp !== "none") {
            statusp.innerHTML = resp;
        }
        if (humidity !== "none") {
            humid.innerHTML = humidity;
        }
    } else {
        console.log("HTTP-Error: " + response.status);
     }
}

async function pollLight() {
    let response = await fetch('/light');
    if (response.ok) { // if HTTP-status is 200-299
        let resp = await response.text();
	light.innerHTML = resp;
    } else {
        console.log("HTTP-Error: " + response.status);
     }
}

async function pollDoor() {
    let response = await fetch('/door');
    if (response.ok) { // if HTTP-status is 200-299
        let resp = await response.text();
        door.innerHTML = resp;
    } else {
        console.log("HTTP-Error: " + response.status);
     }
}

async function pollMotion() {
    let response = await fetch('/motion');
    if (response.ok) { // if HTTP-status is 200-299
        let resp = await response.text();
        if (resp == "1") {
            motion.innerHTML = "YES";
        }
        else {
            motion.innerHTML = "NO";
        }
    } else {
        console.log("HTTP-Error: " + response.status);
     }
}

async function pollWater() {
    let response = await fetch('/water');
    if (response.ok) { // if HTTP-status is 200-299
        let resp = await response.text();
        water.innerHTML = resp;
    } else {
        console.log("HTTP-Error: " + response.status);
     }
}

async function pollSound() {
    let response = await fetch('/sound');
    if (response.ok) { // if HTTP-status is 200-299
        let resp = await response.text();
        if (resp === "1")
            sound.innerHTML = "YES";
        else 
            sound.innerHTML = "NO";
    } else {
        console.log("HTTP-Error: " + response.status);
     }
}

async function pollFlame() {
    let response = await fetch('/flame');
    if (response.ok) { // if HTTP-status is 200-299
        let resp = await response.text();
        flame.innerHTML = resp;
    } else {
        console.log("HTTP-Error: " + response.status);
     }
}

async function clearMotion() {
    let response = await fetch('/clear');
}