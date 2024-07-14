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


// Získání frakční části čísla
function fractionalx(num, B) {    
    let fractionalPart = num - Math.floor(num);
    // Přeměna frakční části na celé číslo pro práci s bity
    let fractionalInt = Math.floor(fractionalPart * Math.pow(2, B));
    // Omezení výsledku na "B" počet bajtů
    let mask = (1 << (8 * B)) - 1;
    
    return fractionalInt & mask;
}


function fractional(num, B) {
     const fractionalPart = num - Math.floor(num);
     const result = Math.floor(fractionalPart * (2 ** (8 * B)));
     return {
     decimal: result,
         //hex: result.toString(16).padStart(8, '0')
         hex: result.toString(16).padStart(2 * B, '0')
         };
     }


function splitLongString(longStr, chunkSize = 32, separator = '<br>') {
    // Rozdělí řetězec na části o délce chunkSize
    const chunks = [];
    for (let i = 0; i < longStr.length; i += chunkSize) {
        chunks.push(longStr.substring(i, i + chunkSize));
    }

    // Spojí části s použitím separatoru a vrátí výsledek
    return chunks.join(separator);
}


function getHexHistx(longHexString) {
    // Převést hexadecimální řetězec na pole znaků
    const chars = longHexString.split('');
    const histagram = {};

    // Projít všechny znaky a počítat četnosti
    chars.forEach(char => {
        if (/[0-9A-Fa-f]/.test(char)) {
            const normalizedChar = char.toUpperCase(); // Normalizovat na velká písmena
            histagram[normalizedChar] = (histagram[normalizedChar] || 0) + 1;
        }
    });
    return histagram;
}


function getHexHist(longHexString) {
    const histagram = {};

    // Projít všechny znaky hexadecimálního řetězce a počítat četnosti
    for (let i = 0; i < longHexString.length; i++) {
        const char = longHexString[i];
        if (/[0-9A-Fa-f]/.test(char)) {
            const normalizedChar = char.toUpperCase(); // Normalizovat na velká písmena
            histagram[normalizedChar] = (histagram[normalizedChar] || 0) + 1;
        }
    }

    // Vytvořit pole seřazeného histagramu
    const sortedHistogram = {};
    '0123456789ABCDEF'.split('').forEach(char => {
        if (histagram[char]) {
            sortedHistogram[char] = histagram[char];
        }
    });

    return sortedHistogram;
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


function diceToNum(dice) {
    let base6 = "";
    for (let char of dice) {
        base6 += (parseInt(char) - 1).toString();
    }
    return parseInt(base6, 6);
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


// entropy
function calculateEntropyFromHex(hexString) {
    // Převést hexadecimální řetězec na pole desetinných čísel
    const arr = hexString.split('').map(char => parseInt(char, 16));

    // Výpočet entropie pomocí stávající funkce
    return calculateEntropy(arr);
}


function calculateEntropy(arr) {
   const frequency = {};
   arr.forEach(num => {
      frequency[num] = (frequency[num] || 0) + 1;
      });

     let entropy = 0;
     const len = arr.length;

     for (let num in frequency) {
        const p_x = frequency[num] / len;
        entropy -= p_x * Math.log2(p_x);
     }
     entropy = Math.round(entropy * 1000) / 1000; // 3 des.místa
     return entropy;
}


function convertToHex(arr) {
      let numberString = arr.join('');
      const hexValue = BigInt(numberString).toString(16).toUpperCase(); // Převod na hex a velká písmena (A-F)
      return {
         hexString: hexValue,
         hexLength: hexValue.length //numberString.length
         };
}

//---2024/07
const substitutionTable21 = {
  'A': 'faf','B': 'fd7','C': 'f99','D': 'f96','E': 'fd9',
  'F': 'fa8','G': 'f9b','H': 'f2f','I': 'f','J': '1f',
  'K': 'f2d','L': 'f11','M': 'f8f','N': 'f4f','O': 'f9f',
  'P': 'fae','R': 'fad','S': 'dda','T': '8f8','U': 'f1f',
  'V': 'e1e','X': 'd2d','Y': 'c3c','Z': 'b9d'
   };


// --- histagram ---
function drawHistagram(histagram, containerId) {
    const container = document.getElementById(containerId);
    if (!container) return; // Pokud kontejner neexistuje, vrátit

      container.innerHTML = ''; // Vyčistit kontejner

       // Vytvořit 16 obdélníků podle histagramu
       '0123456789ABCDEF'.split('').forEach(char => {
           const barHeight = histagram[char] ? histagram[char] * 3 : 0; // Výška obdélníku
           const bar = document.createElement('div');
           bar.classList.add('hbar');
           bar.style.height = `${barHeight}px`;

           const label = document.createElement('div');
           label.classList.add('label');
           label.textContent = char;
           bar.appendChild(label);

           const value = document.createElement('div');
           value.classList.add('value');
           value.textContent = histagram[char] || 0;
           bar.appendChild(value);

           container.appendChild(bar);
       });
}
