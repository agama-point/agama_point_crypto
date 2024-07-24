// Agama Point - CBC  | cipher block chaining simple example | ver. 0.2

class CBC_XOR {
    constructor(key, iv, block_size = 16) {
        this.key = key;
        this.iv = iv;
        this.block_size = block_size;

        if (this.key.length !== this.block_size || this.iv.length !== this.block_size) {
            throw new Error("Key and IV must be of the size block_size");
        }
    }

    // XORs two byte arrays of the same length
    xor_bytes(a, b) {
        const length = Math.min(a.length, b.length);
        const result = [];
        for (let i = 0; i < length; i++) {
            result.push(a.charCodeAt(i) ^ b.charCodeAt(i));
        }
        return String.fromCharCode(...result);
    }

    // Pads plaintext to the block size using PKCS7 padding
    pad(plaintext) {
        const padding_len = this.block_size - (plaintext.length % this.block_size);
        const padding = String.fromCharCode(padding_len).repeat(padding_len);
        return plaintext + padding;
    }

    // Removes PKCS7 padding from plaintext
    unpad(padded_plaintext) {
        const padding_len = padded_plaintext.charCodeAt(padded_plaintext.length - 1);
        return padded_plaintext.slice(0, -padding_len);
    }

    // Encrypts plaintext using CBC mode and XOR operation
    encrypt(plaintext) {
        plaintext = this.pad(plaintext);
        let ciphertext = '';
        let previous_block = this.iv;

        for (let i = 0; i < plaintext.length; i += this.block_size) {
            const block = plaintext.slice(i, i + this.block_size);
            const xored_with_key = this.xor_bytes(block, this.key);
            const encrypted_block = this.xor_bytes(xored_with_key, previous_block);
            ciphertext += encrypted_block;
            previous_block = encrypted_block;
        }

        return ciphertext;
    }

    // Decrypts ciphertext using CBC mode and XOR operation
    decrypt(ciphertext) {
        let decrypted = '';
        let previous_block = this.iv;

        for (let i = 0; i < ciphertext.length; i += this.block_size) {
            const block = ciphertext.slice(i, i + this.block_size);
            const xored_with_prev = this.xor_bytes(block, previous_block);
            const decrypted_block = this.xor_bytes(xored_with_prev, this.key);
            decrypted += decrypted_block;
            previous_block = block;
        }

        return this.unpad(decrypted);
    }

    // Helper function to get the n-th block of the plaintext in hex format
    iblock(plaintext, n) {
        const start = n * this.block_size;
        let block = plaintext.slice(start, start + this.block_size);

        // Pad the block with zeros if it's not long enough
        while (block.length < this.block_size) {
            block += '\x00';
        }

        return this.bytesToHex(block);
    }

    // Converts a byte array to a hex string
    bytesToHex(bytes) {
        const hex = [];
        for (let i = 0; i < bytes.length; i++) {
            const byte = bytes.charCodeAt(i);
            hex.push((byte >> 4).toString(16));
            hex.push((byte & 0xF).toString(16));
        }
        return hex.join('');
    }
}
