// Cipher utility functions
function encrypt(plaintext, key1, key2) {
    const step1 = columnarTransposition(plaintext, key1);
    const step2 = columnarTransposition(step1, key2);
    return step2;
}

function decrypt(ciphertext, key1, key2) {
    const step1 = inverseColumnarTransposition(ciphertext, key2);
    const step2 = inverseColumnarTransposition(step1, key1);
    return step2;
}

function columnarTransposition(text, key) {
    const numCols = key.length;
    const paddedText = text.replace(/ /g, '_');
    const numRows = Math.ceil(paddedText.length / numCols);
    const grid = Array(numRows).fill(null).map(() => Array(numCols).fill('_'));

    // Fill the grid
    let index = 0;
    for (let i = 0; i < numRows; i++) {
        for (let j = 0; j < numCols; j++) {
            if (index < paddedText.length) {
                grid[i][j] = paddedText[index++];
            }
        }
    }

    // Sort columns based on key
    const sortedColumns = key.split('').map((char, index) => ({ char, index }))
        .sort((a, b) => a.char.localeCompare(b.char))
        .map(item => item.index);

    // Read off the columns
    let result = '';
    for (const col of sortedColumns) {
        for (let row = 0; row < numRows; row++) {
            result += grid[row][col];
        }
    }

    return result;
}

function inverseColumnarTransposition(text, key) {
    const numCols = key.length;
    const numRows = Math.ceil(text.length / numCols);
    const grid = Array(numRows).fill(null).map(() => Array(numCols).fill(''));

    // Sort columns based on key
    const sortedColumns = key.split('').map((char, index) => ({ char, index }))
        .sort((a, b) => a.char.localeCompare(b.char))
        .map(item => item.index);

    // Fill the grid
    let index = 0;
    for (const col of sortedColumns) {
        for (let row = 0; row < numRows && index < text.length; row++) {
            grid[row][col] = text[index++];
        }
    }

    // Read off the rows
    let result = '';
    for (const row of grid) {
        result += row.join('');
    }

    return result.replace(/_+$/, '').replace(/_/g, ' '); // Remove trailing underscores and replace remaining with spaces
}

function getEncryptionSteps(plaintext, key1, key2) {
    const step1Grid = createGrid(plaintext, key1);
    const step1Result = columnarTransposition(plaintext, key1);
    const step2Grid = createGrid(step1Result, key2);
    const step2Result = columnarTransposition(step1Result, key2);

    return { step1Grid, step1Result, step2Grid, step2Result };
}

function getDecryptionSteps(ciphertext, key1, key2) {
    const step1Grid = createInverseGrid(ciphertext, key2);
    const step1Result = inverseColumnarTransposition(ciphertext, key2);
    const step2Grid = createInverseGrid(step1Result, key1);
    const step2Result = inverseColumnarTransposition(step1Result, key1);

    return { step1Grid, step1Result, step2Grid, step2Result };
}

function createGrid(text, key) {
    const numCols = key.length;
    const paddedText = text.replace(/ /g, '_');
    const numRows = Math.ceil(paddedText.length / numCols);
    const grid = Array(numRows).fill(null).map(() => Array(numCols).fill('_'));

    let index = 0;
    for (let i = 0; i < numRows; i++) {
        for (let j = 0; j < numCols; j++) {
            if (index < paddedText.length) {
                grid[i][j] = paddedText[index++];
            }
        }
    }

    return grid;
}

function createInverseGrid(text, key) {
    const numCols = key.length;
    const numRows = Math.ceil(text.length / numCols);
    const grid = Array(numRows).fill(null).map(() => Array(numCols).fill(''));

    const sortedColumns = key.split('').map((char, index) => ({ char, index }))
        .sort((a, b) => a.char.localeCompare(b.char))
        .map(item => item.index);

    let index = 0;
    for (const col of sortedColumns) {
        for (let row = 0; row < numRows && index < text.length; row++) {
            grid[row][col] = text[index++];
        }
    }

    return grid;
}

// DOM manipulation
document.addEventListener('DOMContentLoaded', () => {
    const encryptBtn = document.getElementById('encryptBtn');
    const decryptBtn = document.getElementById('decryptBtn');

    encryptBtn.addEventListener('click', handleEncrypt);
    decryptBtn.addEventListener('click', handleDecrypt);
});

function handleEncrypt() {
    const plaintext = document.getElementById('plaintext').value;
    const key1 = document.getElementById('encryptKey1').value;
    const key2 = document.getElementById('encryptKey2').value;

    const encrypted = encrypt(plaintext, key1, key2);
    document.getElementById('ciphertext').value = encrypted;
    document.getElementById('decryptCiphertext').value = encrypted;
    document.getElementById('decryptKey1').value = key1;
    document.getElementById('decryptKey2').value = key2;

    const steps = getEncryptionSteps(plaintext, key1, key2);
    displayEncryptionSteps(steps, key1, key2);
}

function handleDecrypt() {
    const ciphertext = document.getElementById('decryptCiphertext').value;
    const key1 = document.getElementById('decryptKey1').value;
    const key2 = document.getElementById('decryptKey2').value;

    const decrypted = decrypt(ciphertext, key1, key2);
    document.getElementById('decryptedText').value = decrypted;
    document.getElementById('plaintext').value = decrypted;
    document.getElementById('encryptKey1').value = key1;
    document.getElementById('encryptKey2').value = key2;

    const steps = getDecryptionSteps(ciphertext, key1, key2);
    displayDecryptionSteps(steps, key1, key2);
}

function displayEncryptionSteps(steps, key1, key2) {
    const encryptionSteps = document.getElementById('encryptionSteps');
    encryptionSteps.style.display = 'block';

    document.getElementById('step1Grid').innerHTML = renderGrid(steps.step1Grid, key1);
    document.getElementById('step1Result').textContent = `Result: ${steps.step1Result}`;
    document.getElementById('step2Grid').innerHTML = renderGrid(steps.step2Grid, key2);
    document.getElementById('step2Result').textContent = `Final Ciphertext: ${steps.step2Result}`;
}

function displayDecryptionSteps(steps, key1, key2) {
    const decryptionSteps = document.getElementById('decryptionSteps');
    decryptionSteps.style.display = 'block';

    document.getElementById('decryptStep1Grid').innerHTML = renderGrid(steps.step1Grid, key2);
    document.getElementById('decryptStep1Result').textContent = `Result: ${steps.step1Result}`;
    document.getElementById('decryptStep2Grid').innerHTML = renderGrid(steps.step2Grid, key1);
    document.getElementById('decryptStep2Result').textContent = `Final Plaintext: ${steps.step2Result}`;
}

function renderGrid(grid, key) {
    let html = '<table><thead><tr>';
    for (const char of key) {
        html += `<th>${char}</th>`;
    }
    html += '</tr></thead><tbody>';

    for (const row of grid) {
        html += '<tr>';
        for (const cell of row) {
            html += `<td>${cell === '_' ? '<span style="color: #ccc;">_</span>' : cell}</td>`;
        }
        html += '</tr>';
    }

    html += '</tbody></table>';
    return html;
}

