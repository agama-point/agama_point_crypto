// agama_function.js | 2015-24 | 
AF_VER = "0.7.21";


const charset64 = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_';
const charset58 = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'; // x: 0IOl
const charset32 = '2346789bdfghjmnpqrtBDFGHJLMNPQRT';
const charset16 = '0123456789abcdef';
const charset8 = '01234567';
const charset6 = '123456'; // dice
const charset4 = 'ATCG';
const charset2 = '01'; // bin / coin


function getSystemInfo() {
    // Detekce verze JavaScriptu
    const jsVersion = (() => {
        if (typeof BigInt === "function") return "ES11 (2019) +";
        if (typeof Symbol === "function") return "ES6 (2015)";
        if (typeof Map === "function") return "ES6 (2015)";
        if (typeof Set === "function") return "ES6 (2015)";
        if (typeof Promise === "function") return "ES6 (2015)";
        if (typeof Proxy === "function") return "ES6 (2015)";
        return "ES5 or lower";
    })();

    // Detekce verze prohlížeče
    const browserVersion = (() => {
        const userAgent = navigator.userAgent;
        let match = userAgent.match(/(firefox|msie|trident(?=\/))\/?\s*(\d+)/i) || [];
        if (/trident/i.test(match[1])) {
            const rv = /\brv[ :]+(\d+)/g.exec(userAgent) || [];
            return `IE ${rv[1] || ""}`;
        }
        if (match[1] === 'Chrome') {
            const tem = userAgent.match(/\b(OPR|Edge)\/(\d+)/);
            if (tem != null) return tem.slice(1).join(' ').replace('OPR', 'Opera');
        }
        match = match[2] ? [match[1], match[2]] : [navigator.appName, navigator.appVersion, '-?'];
        const tem = userAgent.match(/version\/(\d+)/i);
        if (tem != null) match.splice(1, 1, tem[1]);
        return match.join(' ');
    })();

    // Detekce verze OS
    const osVersion = (() => {
        const userAgent = navigator.userAgent;
        let os = "Unknown OS";
        if (userAgent.indexOf("Win") != -1) os = "Windows";
        if (userAgent.indexOf("Mac") != -1) os = "MacOS";
        if (userAgent.indexOf("X11") != -1) os = "UNIX";
        if (userAgent.indexOf("Linux") != -1) os = "Linux";

        let version = "Unknown Version";
        if (/Windows NT 10.0/.test(userAgent)) version = "10";
        if (/Windows NT 6.2/.test(userAgent)) version = "8";
        if (/Windows NT 6.1/.test(userAgent)) version = "7";
        if (/Windows NT 6.0/.test(userAgent)) version = "Vista";
        if (/Windows NT 5.1/.test(userAgent)) version = "XP";
        if (/Windows NT 5.0/.test(userAgent)) version = "2000";
        if (/Mac OS X 10_[0-9]+_[0-9]+/.test(userAgent)) version = userAgent.match(/Mac OS X 10_[0-9]+_[0-9]+/)[0].replace(/_/g, '.');
        if (/Linux/.test(userAgent)) version = "Various Versions";

        return `${os} ${version}`;
    })();

    return {
        jsVersion: jsVersion,
        browserVersion: browserVersion,
        osVersion: osVersion
    };
}
//console.log(getSystemInfo());


// --- agama_functions for simple BIP39 examples 2024/05-08

// Function to convert binary string to hexadecimal string
function longBinToHex(bin) {
   let hex = '';
   for (let i = 0; i < bin.length; i += 4) {
      let binSegment = bin.substr(i, 4);
      let hexSegment = parseInt(binSegment, 2).toString(16);
      hex += hexSegment;
              }
   return hex;
}


function longHexToBin(hex) {
   let bin = '';
   for (let i = 0; i < hex.length; i++) {
      let hexSegment = hex[i];
      let binSegment = parseInt(hexSegment, 16).toString(2);
      bin += binSegment.padStart(4, '0');
   }
   return bin;
}


function hexToString(hex) {
    let str = '';
    for (let i = 0; i < hex.length; i += 2) {
        str += String.fromCharCode(parseInt(hex.substr(i, 2), 16));
    }
    return str;
}


function hexToBase64(hexString) {
    // hex 2 byte array
    let bytes = [];
    for (let i = 0; i < hexString.length; i += 2) {
        bytes.push(parseInt(hexString.substr(i, 2), 16));
    }
    let binaryString = String.fromCharCode.apply(null, bytes); // B arr 2 bin
    let base64String = btoa(binaryString); // bin 2 base64
    return base64String;
}


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


function plot_7segment_hex(box, hex, style="char-box") {
   var hexElement = $(box);
   hexElement.empty(); // Vyprázdní obsah prvku
   var charMap = {'A':'k','B':'l','C':'m','D':'n','E':'o','F':'p'};
   hex = hex.toUpperCase();

   for(var i = 0; i < hex.length; i++) {
      var char = hex[i];
      if(charMap[char]) { char = charMap[char]; }
      var charBox = $('<div></div>').addClass(style).text(char);
      hexElement.append(charBox);
   }
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
    while (binaryString.length % 5 !== 0) {  binaryString = '0' + binaryString;  }

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
 'A':'faf','B':'fd7','C':'f99','D':'f96','E':'fd9',
 'F':'fa8','G':'f9b','H':'f2f','I':'f',  'J':'1f',
 'K':'f2d','L':'f11','M':'f8f','N':'f4f','O':'f9f',
 'P':'fae','R':'fad','S':'dda','T':'8f8','U':'f1f',
 'V':'e1e','X':'d2d','Y':'c3c','Z':'b9d',
 '1':'4f', '2':'9b5','3':'bf6','4':'e27','5':'dbb',
 '6':'f53','7':'88f','8':'fbf','9':'dbf','0':'f9f',
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


//simple first n primes
function calculatePrimes(n) {
   const primes = [];
   let num = 2; // 
   while (primes.length < n) {
      if (isPrime(num)) { primes.push(num); }
        num++;
   }
   return primes;
}


function isPrime(num) {
   if (num <= 1) return false;
   if (num <= 3) return true;
   if (num % 2 === 0 || num % 3 === 0) return false;

   for (let i = 5; i * i <= num; i += 6) {
      if (num % i === 0 || num % (i + 2) === 0) return false;
    }
    return true;
}


function getBitcoinPrice() {
  return fetch('https://api.coinpaprika.com/v1/tickers/btc-bitcoin')
    .then(response => {
       if (!response.ok) {
          throw new Error('Network response was not ok');
       }
       return response.json();
    })
    .then(data => {
       // Získání ceny bitcoinu a převod na celé číslo
       const btcusd = Math.round(data.quotes.USD.price);
       return btcusd;  // Vrátí cenu jako celé číslo
     })
    .catch(error => {
       console.error('Error fetching Bitcoin price:', error);
       return 'E';  // Vrátí "E" v případě chyby
    });
}


//------- deterministic or discredited entropy --------------
class dde32 {

   static A = "0c1e24e5917779d297e14d45f14e1a1a";
   static F = "ffffffffffffffffffffffffffffffff";
   static F2 = "6a09e667bb67ae853c6ef372a54ff53a";
   static F3 = "428a2f9871374491b5c0fbcfe9b5dba5";
   static K = "6B6F62796C61206D61206D616C792062";
   static T = "752f85035563adff915ac0c3ae1252ed";
   static Z = "00000000000000000000000000000000";

   // Metoda xor pro dva parametry
   static xor(A, B) {
      let result = "";
      for (let i = 0; i < A.length && i < B.length; i++) {
          // Převod každého znaku na jeho ASCII hodnotu a provedení XOR operace
          result += String.fromCharCode(A.charCodeAt(i) ^ B.charCodeAt(i));
      }
      return result;
    }

    //static pad032(A) { return = A.padStart(32, '0'); }
}


function asciiStrToHex(str) {
    let hex = '';
    for (let i = 0; i < str.length; i++) {
        let char = str.charCodeAt(i).toString(16);
        hex += (char.length === 1 ? '0' : '') + char;
    }
    return hex;
}


function hexToASCII(shex) {
    // Remove any spaces from the input hex string
    shex = shex.replace(/\s+/g, '');

    // If the length of the hex string is odd, pad with an additional zero
    if (shex.length % 2 !== 0) {
        shex += '0';
    }

    let ascii = '';

    // Loop through each pair of characters in the hex string
    for (let i = 0; i < shex.length; i += 2) {
        // Convert the pair of hex characters to an integer
        let hexPair = shex.substring(i, i + 2);
        let charCode = parseInt(hexPair, 16);

        // If the character code is printable, add the corresponding character to the ASCII string
        // Otherwise, add a dot (.)
        if (charCode >= 32 && charCode <= 126) {
            ascii += String.fromCharCode(charCode);
        } else {
            ascii += '.';
        }
    }
    return ascii;
}


// Function to remove diacritics
function removeDiacritics(str) {
     return str.normalize('NFD').replace(/[\u0300-\u036f]/g, '');
}


// hexdump - output "="
function asciiToHexDump(str) {
   let hex = '';
   let longHex ="";
   let ascii = '';
   let offset = 0;
   const width = 16; // 16 bytes per line

   str = removeDiacritics(str); // Remove diacritics from input string

   for (let i = 0; i < str.length; i++) {
       let char = str.charCodeAt(i).toString(16).toUpperCase();
       if (char.length === 1) char = '0' + char; // ensure two digits
       hex += char + ' ';
       longHex += char;
       ascii += (str[i].charCodeAt(0) >= 32 && str[i].charCodeAt(0) <= 126) ? str[i] : '.';

       if ((i + 1) % width === 0 || i === str.length - 1) {
           // Print offset
           let offsetStr = offset.toString(16).toUpperCase();
           while (offsetStr.length < 8) { offsetStr = '0' + offsetStr; }

           if ((i + 1) % width !== 0) {
               // Pad with "00 " and "."
               const remaining = width - (i % width) - 1;
               for (let j = 0; j < remaining; j++) {
                   hex += '00 ';
                   ascii += '.';
               }
           }

           hex = hex.trim();
           $('#hexdump').append(`${offsetStr}  ${hex}  |${ascii}|\n`);
           hex = '';
           ascii = '';
           offset += width;
       }
    }
    const base64str = hexToBase64(longHex);
    $('#hexdump').append(`\n\n\nHEX: ${splitLongString(longHex)}\nBASE64: ${base64str}\n`);
}