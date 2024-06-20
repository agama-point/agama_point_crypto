// AgamaPoint iTing 2016-2023

const iChingHexagrams = [
    { index: 1, ch: "Čchien", cz: "Tvoření", en: "The Creative", binary: "111111" },
    { index: 2, ch: "Kchun", cz: "Přijetí", en: "The Receptive", binary: "000000" },
    { index: 3, ch: "Čun", cz: "Rození", en: "Difficulty at the Beginning", binary: "010001" },
    { index: 4, ch: "Meng", cz: "Zrání", en: "Youthful Folly", binary: "100010" },
    { index: 5, ch: "Sü", cz: "Očekávání", en: "Waiting", binary: "010111" },
    { index: 6, ch: "Sung", cz: "Svár", en: "Conflict", binary: "111010" },
    { index: 7, ch: "Š'", cz: "Vojsko", en: "The Army", binary: "000010" },
    { index: 8, ch: "Pi", cz: "Spojení", en: "Holding Together", binary: "010000" },
    { index: 9, ch: "Siao-čchu", cz: "Podrobení malého", en: "The Taming Power of the Small", binary: "110111" },
    { index: 10, ch: "Lü", cz: "Vykročení", en: "Treading", binary: "111011" },
    { index: 11, ch: "Tchaj", cz: "Prosperita", en: "Peace", binary: "000111" },
    { index: 12, ch: "Pchi", cz: "Úpadek", en: "Standstill", binary: "111000" },
    { index: 13, ch: "Tchung-žen", cz: "Lidské společenství", en: "Fellowship with Men", binary: "111101" },
    { index: 14, ch: "Ta-jou", cz: "Veliké držení", en: "Possession in Great Measure", binary: "101111" },
    { index: 15, ch: "Ťien", cz: "Skromnost", en: "Modesty", binary: "000100" },
    { index: 16, ch: "Jü", cz: "Nadšení", en: "Enthusiasm", binary: "001000" },
    { index: 17, ch: "Suej", cz: "Následování", en: "Following", binary: "011001" },
    { index: 18, ch: "Ku", cz: "Zkaženost", en: "Work on the Decayed", binary: "100110" },
    { index: 19, ch: "Lin", cz: "Sblížení", en: "Approach", binary: "000011" },
    { index: 20, ch: "Kuan", cz: "Pozorování", en: "Contemplation", binary: "110000" },
    { index: 21, ch: "Š'-chuo", cz: "Skousnutí", en: "Biting Through", binary: "101001" },
    { index: 22, ch: "Pi", cz: "Půvab", en: "Grace", binary: "100101" },
    { index: 23, ch: "Po", cz: "Odpadání", en: "Splitting Apart", binary: "100000" },
    { index: 24, ch: "Fu", cz: "Návraty", en: "Return", binary: "000001" },
    { index: 25, ch: "Wu-wang", cz: "Nevinnost", en: "Innocence", binary: "111001" },
    { index: 26, ch: "Ta-čchu", cz: "Podrobení velkého", en: "The Taming Power of the Great", binary: "100111" },
    { index: 27, ch: "I", cz: "Čelisti", en: "The Corners of the Mouth", binary: "100001" },
    { index: 28, ch: "Ta-kuo", cz: "Převaha velkého", en: "Preponderance of the Great", binary: "011110" },
    { index: 29, ch: "Kchan", cz: "Propadání", en: "The Abysmal", binary: "010010" },
    { index: 30, ch: "Li", cz: "Záření", en: "The Clinging", binary: "101101" },
    { index: 31, ch: "Sien", cz: "Přitažlivost", en: "Influence", binary: "011100" },
    { index: 32, ch: "Cheng", cz: "Trvání", en: "Duration", binary: "001110" },
    { index: 33, ch: "Tun", cz: "Ústup", en: "Retreat", binary: "111100" },
    { index: 34, ch: "Ta-čuang", cz: "Síla velkého", en: "The Power of the Great", binary: "001111" },
    { index: 35, ch: "Ťin", cz: "Pokrok", en: "Progress", binary: "101000" },
    { index: 36, ch: "Ming-i", cz: "Soumrak", en: "Darkening of the Light", binary: "000101" },
    { index: 37, ch: "Ťia-žen", cz: "Rodina", en: "The Family", binary: "110101" },
    { index: 38, ch: "Kchuej", cz: "Vzdálení", en: "Opposition", binary: "101011" },
    { index: 39, ch: "Ťien", cz: "Překážka", en: "Obstruction", binary: "010100" },
    { index: 40, ch: "Ťie", cz: "Uvolnění", en: "Deliverance", binary: "001010" },
    { index: 41, ch: "Sun", cz: "Ubývání", en: "Decrease", binary: "100011" },
    { index: 42, ch: "I", cz: "Přidání", en: "Increase", binary: "110001" },
    { index: 43, ch: "Kuej", cz: "Rozhodnost", en: "Breakthrough", binary: "011111" },
    { index: 44, ch: "Kou", cz: "Spojení", en: "Coming to Meet", binary: "111110" },
    { index: 45, ch: "Cuej", cz: "Shromáždění", en: "Gathering Together", binary: "011000" },
    { index: 46, ch: "Šeng", cz: "Stoupání", en: "Pushing Upward", binary: "000110" },
    { index: 47, ch: "Kchun", cz: "Tíseň", en: "Oppression", binary: "011010" },
    { index: 48, ch: "Ťing", cz: "Studna", en: "The Well", binary: "010110" },
    { index: 49, ch: "Ke", cz: "Převrat", en: "Revolution", binary: "011101" },
    { index: 50, ch: "Ting", cz: "Kotel", en: "The Cauldron", binary: "101110" },
    { index: 51, ch: "Čen", cz: "Bouře", en: "The Arousing", binary: "001001" },
    { index: 52, ch: "Ken", cz: "Stání", en: "Keeping Still", binary: "100100" },
    { index: 53, ch: "Ťien", cz: "Plynutí", en: "Development", binary: "110100" },
    { index: 54, ch: "Kuej-mej", cz: "Provdání", en: "The Marrying Maiden", binary: "001011" },
    { index: 55, ch: "Feng", cz: "Hojnost", en: "Abundance", binary: "001101" },
    { index: 56, ch: "Lü", cz: "Putování", en: "The Wanderer", binary: "101100" },
    { index: 57, ch: "Sun", cz: "Pronikání", en: "The Gentle", binary: "110110" },
    { index: 58, ch: "Tuej", cz: "Radost", en: "The Joyous", binary: "011011" },
    { index: 59, ch: "Chuan", cz: "Odloučení", en: "Dispersion", binary: "110010" },
    { index: 60, ch: "Ťie", cz: "Omezení", en: "Limitation", binary: "010011" },
    { index: 61, ch: "Čung-fou", cz: "Vnitřní opravdovost", en: "Inner Truth", binary: "110011" },
    { index: 62, ch: "Siao-kuo", cz: "Převaha malého", en: "Preponderance of the Small", binary: "001100" },
    { index: 63, ch: "Čchi-ťi", cz: "Ukončení", en: "After Completion", binary: "010101" },
    { index: 64, ch: "Wej-ťi", cz: "Nedokončení", en: "Before Completion", binary: "101010" }
];


    
    /*
    // Funkce pro převod binárního čísla na číslo a názvy
    function convertBinaryToIChing(bin) {
        //const binaries = [bin1, bin2, bin3];
        //const results = binaries.map(bin => {
        const decimal = parseInt(bin, 2);
        if (decimal >= 0 && decimal < hexagrams.length) {
        return {
        binary: bin,
        decimal: decimal + 1, // Hexagramy jsou číslovány od 1 do 64
        englishName: hexagrams[decimal].en,
        czechName: hexagrams[decimal].cz
        };
    } else {
    return {
    binary: bin,
    decimal: decimal,
    englishName: "out of range",
    czechName: "mimo rozsah"
    };
    }
}
    */

function numToIChing(num) {
    //const binaries = [bin1, bin2, bin3];
    //const results = binaries.map(bin => {
    const index = parseInt(num); // parseInt(bin, 2);   
    return {
    i: index,
    bin: iChingHexagrams[index].binary,
    ch: iChingHexagrams[index].ch,
    cz: iChingHexagrams[index].cz,
    en: iChingHexagrams[index].en
    //decimal: decimal + 1, // Hexagramy jsou číslovány od 1 do 64
    //englishName: hexagrams[decimal].en,
    //czechName: hexagrams[decimal].cz
    };
}  