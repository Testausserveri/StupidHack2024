const promptsu = document.getElementById('promptsu');
const API_BASE = '';

let correctionRunning = false;

async function correct() {
    /*
    Takes the content of input #promptsu and sends it to the server
    Replaces the content of #promptsu with the response
     */

    // Prevent multiple requests
    if (correctionRunning) {
        return;
    }
    correctionRunning = true;

    // Send the request
    try {
        const data = new FormData();
        data.append('input', promptsu.value);
        promptsu.value = await fetch(`${API_BASE}/correct`, {
            method: 'POST',
            body: data
        }).then(d => d.text());
    } catch (e) {
        console.error(e);
    }

    correctionRunning = false;
}

function isQuestionReady() {
    /*
    Returns true if the user has entered a question
     */
    return  ['.', '?', '!'].includes(promptsu.value.slice(-1));
}

// Attach to events
promptsu.addEventListener('input', async (ev) => {
    // Check for space key
    if (ev.data && ev.data.slice(-1) === ' ') {
        await correct();

        if (!['.', '?', '!'].includes(promptsu.value.slice(-1))) {
            promptsu.value += ' ';
        }
    }
});

promptsu.addEventListener('change', correct);

// Initial value
promptsu.value = '';

document.getElementById('user-input').addEventListener('submit', async (ev) => {
    ev.preventDefault();
    await correct();
    const body = new FormData();
    body.append('input', promptsu.value);
    const resp = await fetch('/submit', {
        method: 'POST',
        body: body
    }).then(d => d.json());

    console.log(resp)
    document.querySelector('.right-bubble').innerText = resp[0];
    document.querySelector('.left-bubble').innerText = resp[1];

});