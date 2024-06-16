// --- agama_functions for simple BIP39 examples
// 2024/06

async function sha256(message) {
    const msgBuffer = new TextEncoder().encode(message);
    const hashBuffer = await crypto.subtle.digest('SHA-256', msgBuffer);
    const hashArray = Array.from(new Uint8Array(hashBuffer));
    const hashHex = hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
    return hashHex;
}

// Funkce pro převod čísla na binární řetězec s pevnou délkou 11 číslic (length)
function toBinaryString(num, length) {
    return num.toString(2).padStart(length, '0');
}

// Function to convert a binary string to a number
function binaryToNum(bin) {
    return parseInt(bin, 2);
}

// Funkce pro převod čísla na "házení kostkami" na pevnou délku s posunem
function numToDice(num, length) {
    let base6 = num.toString(6).padStart(length, '0');
    let dice = "";
    for (let char of base6) {
        dice += (parseInt(char) + 1).toString();
    }
    return dice;
}

// Funkce pro provedení XOR operace mezi dvěma hexadecimálními řetězci
function xorHexStrings(hex1, hex2) {
    hex1 = hex1.padStart(32, '0');
    hex2 = hex2.padStart(32, '0');

    const bin1 = BigInt('0x' + hex1);
    const bin2 = BigInt('0x' + hex2);
    const xorResult = bin1 ^ bin2;
    return xorResult.toString(16).padStart(hex1.length, '0');
}


// Funkce pro zobrazení 128bit čísla jako matici 32x4 čtverečků
function displayHexAsGridHorizontal(hex) {
    const gridContainer = $('#gridContainer');
    gridContainer.empty(); // Vyprázdnění kontejneru

    if (hex.length !== 32) {
        gridContainer.text('Please enter a 32 Byte hex value.');
        return;
    }


    const grid = $('<div class="grid"></div>');
    
    for (let i = 0; i < hex.length; i++) {
        const value = parseInt(hex[i], 16);
        for (let bit = 3; bit >= 0; bit--) {
            const isBitSet = (value >> bit) & 1;
            const cell = $('<div class="cell"></div>');
            if (isBitSet) {
                cell.css('background-color', '#000');
            } else {
                cell.css('background-color', '#fa0');
            }
            grid.append(cell);
        }
    }
    
    gridContainer.append(grid);
}


// Funkce pro zobrazení 128bit čísla jako matici 32x8 čtverečků, Bytes horizontálně
function displayHexAsGrid(hex, containerId) {
    //const gridContainer = $('#gridContainer');
    const gridContainer = $(`#${containerId}`);
    gridContainer.empty(); // Vyprázdnění kontejneru

    hex = hex.padStart(32, '0');

    //if (hex.length !== 32) {
    //    gridContainer.text('Please enter a 32 Byte hex value.');
    //    return;
    //}

    const grid = $('<div class="grid"></div>');

    for (let i = 0; i < hex.length; i++) {
        const value = parseInt(hex[i], 16);
        const column = $('<div class="column"></div>');
        for (let bit = 3; bit >= 0; bit--) {
            const isBitSet = (value >> bit) & 1;
            const cell = $('<div class="cell"></div>');
            cell.css('background-color', isBitSet ? '#fa0' : '#000');
            column.append(cell);
        }
        grid.append(column);
    }

    gridContainer.append(grid);
}


// Define the BECH32 alphabet with uppercase characters
var ALPHABET = 'QPZRY9X8GF2TVDW0S3JN54KHCE6MUA7L';

// Function to convert a 5-bit binary number to its BECH32 equivalent
function binaryToBech32(bin) {
    if (bin.length !== 5) {
        return "Error: Input must be a 5-bit binary number.";
    }
    
    // Convert binary string to decimal
    var decimal = parseInt(bin, 2);
    
    // Get the corresponding character from the ALPHABET
    return ALPHABET[decimal];
}

// Function to convert a BECH32 character to a 5-bit binary number
function bech32ToBinary(char) {
    var index = ALPHABET.indexOf(char);
    if (index === -1) {
        return "Error: Character not in BECH32 alphabet.";
    }
    
    // Convert decimal to 5-bit binary string
    var binary = index.toString(2);
    
    // Pad with leading zeros to ensure it's 5 bits
    while (binary.length < 5) {
        binary = '0' + binary;
    }
    
    return binary;
}

// Function to convert a binary string to BECH32 string
function binaryStringToBech32String(binaryString) {
    // Pad the binary string with leading zeros to make its length a multiple of 5
    while (binaryString.length % 5 !== 0) {
        binaryString = '0' + binaryString;
    }

    var bech32String = '';
    for (var i = 0; i < binaryString.length; i += 5) {
        var chunk = binaryString.substr(i, 5);
        bech32String += binaryToBech32(chunk);
    }

    return bech32String;
}

// Function to convert a BECH32 string to binary string
function bech32StringToBinaryString(bech32String) {
    var binaryString = '';
    for (var i = 0; i < bech32String.length; i++) {
        var char = bech32String[i];
        binaryString += bech32ToBinary(char);
    }

    return binaryString;
}