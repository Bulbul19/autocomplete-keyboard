alert("JS IS RUNNING");

const backendURL = "https://autocomplete-keyboard.onrender.com";
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
// ---------- AUTOMATED KEYBOARD GENERATOR ----------
function automateTyping(targetSentence) {
    console.log("Starting automation for:", targetSentence);
    
    // Reset the application state before starting
    currentText = "";
    updateUI({ updated_text: "", suggestions: [] });

    let index = 0;

    // Set an interval to run every 400 milliseconds (simulates a typing speed)
    const typingTimer = setInterval(() => {
        if (index < targetSentence.length) {
            let nextChar = targetSentence[index];

            // 1. Give visual feedback by lighting up the virtual key
            flashKeyUI(nextChar);

            // 2. Trigger your existing network event
            sendInput(nextChar);

            index++;
        } else {
            // Stop typing when we reach the end of the sentence
            clearInterval(typingTimer);
            console.log("Automation sequence complete.");
        }
    }, 400); 
}

// Helper to find the DOM element for the key and briefly highlight it
function flashKeyUI(char) {
    const allKeys = document.querySelectorAll(".key");
    allKeys.forEach(keyBtn => {
        const isSpace = (char === " " && keyBtn.innerText === "Space");
        const isNormalKey = (keyBtn.innerText === char);

        if (isNormalKey || isSpace) {
            keyBtn.classList.add("automated-active");
            // Remove the highlight effect after 200ms
            setTimeout(() => keyBtn.classList.remove("automated-active"), 200);
        }
    });
}
.key {
    transition: background-color 0.1s ease;
}

/* This class gets toggled by our JS animation function */
.key.automated-active {
    background-color: #4CAF50 !important; /* Vivid green highlight */
    color: white;
    transform: scale(0.95); /* Simulates a mechanical press down */
}
