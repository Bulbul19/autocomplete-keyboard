alert("JS IS RUNNING");

const backendURL = "http://127.0.0.1:8000";
let currentText = "";

// ---------- CREATE KEYBOARD ----------
const keyboard = document.getElementById("keyboard");

const layout = [
    "qwertyuiop",
    "asdfghjkl",
    "zxcvbnm"
];

layout.forEach(row => {
    let rowDiv = document.createElement("div");
    rowDiv.className = "keyboard-row";

    row.split("").forEach(k => {
        let btn = document.createElement("div");
        btn.className = "key";
        btn.innerText = k;
        btn.onclick = () => handleKey(k);

        rowDiv.appendChild(btn);
    });

    keyboard.appendChild(rowDiv);
});

// ---------- SPACE + BACKSPACE ----------
let specialRow = document.createElement("div");
specialRow.className = "keyboard-row";

// Space
let spaceBtn = document.createElement("div");
spaceBtn.className = "key space";
spaceBtn.innerText = "Space";
spaceBtn.onclick = () => handleKey(" ");
specialRow.appendChild(spaceBtn);

// Backspace
let backBtn = document.createElement("div");
backBtn.className = "key backspace";
backBtn.innerText = "⌫";
backBtn.onclick = () => handleKey("⌫");
specialRow.appendChild(backBtn);

// ✅ IMPORTANT (you missed this)
keyboard.appendChild(specialRow);

// ---------- HANDLE KEY ----------
function handleKey(key) {
    if (key === "⌫") {
        currentText = currentText.slice(0, -1);
        updateUI({ updated_text: currentText, suggestions: [] });
        return;
    }

    sendInput(key);
}

// ---------- SEND INPUT ----------
function sendInput(char) {
    fetch(`${backendURL}/input`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            text: currentText,
            char: char
        })
    })
    .then(res => res.json())
    .then(data => {
        console.log("Response:", data);
        currentText = data.updated_text;
        updateUI(data);
    })
    .catch(err => console.error("Error:", err));
}

// ---------- UPDATE UI ----------
function updateUI(data) {
    document.getElementById("textDisplay").value = data.updated_text;

    const suggestionsDiv = document.getElementById("suggestions");
    suggestionsDiv.innerHTML = "";

    data.suggestions.forEach(word => {
        let btn = document.createElement("div");
        btn.className = "suggestion";
        btn.innerText = word;

        btn.onclick = () => selectWord(word);

        suggestionsDiv.appendChild(btn);
    });
}

// ---------- SELECT WORD ----------
function selectWord(word) {
    console.log("Selected:", word);

    fetch(`${backendURL}/select`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            text: currentText,
            word: word
        })
    })
    .then(res => res.json())
    .then(data => {
        console.log("After select:", data);

        currentText = data.updated_text;
        updateUI(data);
    })
    .catch(err => console.error("Error:", err));
}
