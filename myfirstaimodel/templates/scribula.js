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