// --- agama_functions for simple BIP39 examples
// 2024/06

// Funkce pro převod čísla na binární řetězec s pevnou délkou 11 číslic (length)
function toBinaryString(num, length) {
    return num.toString(2).padStart(length, '0');
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
