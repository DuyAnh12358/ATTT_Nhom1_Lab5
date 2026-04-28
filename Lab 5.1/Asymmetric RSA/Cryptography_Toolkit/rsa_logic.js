
function generateKeys() {
    const pki = forge.pki;
    alert("Đang tạo khóa, vui lòng đợi vài giây...");
    
    const keys = pki.rsa.generateKeyPair(2048);
    
    const publicKeyPem = pki.publicKeyToPem(keys.publicKey);
    const privateKeyPem = pki.privateKeyToPem(keys.privateKey);

    document.getElementById('publicKeyDisplay').value = publicKeyPem;
    document.getElementById('privateKeyDisplay').value = privateKeyPem;
    
    document.getElementById('publicKeyInput').value = publicKeyPem;
    document.getElementById('privateKeyInput').value = privateKeyPem;
}


function encryptData() {
    try {
        const plaintext = document.getElementById('plainTextInput').value;
        const publicKeyPem = document.getElementById('publicKeyInput').value;

        if (!plaintext || !publicKeyPem) {
            alert("Vui lòng nhập đầy đủ Plaintext và Public Key!");
            return;
        }

        const publicKey = forge.pki.publicKeyFromPem(publicKeyPem);
        const encrypted = publicKey.encrypt(plaintext, 'RSAES-PKCS1-V1_5');
        
        const base64Cipher = forge.util.encode64(encrypted);
        document.getElementById('cipherTextResult').value = base64Cipher;
        
        
        document.getElementById('cipherTextInput').value = base64Cipher;
    } catch (err) {
        alert("Lỗi mã hóa: Có thể do Public Key sai định dạng!");
    }
}


function decryptData() {
    try {
        const ciphertextBase64 = document.getElementById('cipherTextInput').value;
        const privateKeyPem = document.getElementById('privateKeyInput').value;

        if (!ciphertextBase64 || !privateKeyPem) {
            alert("Vui lòng nhập đầy đủ Ciphertext và Private Key!");
            return;
        }

        const privateKey = forge.pki.privateKeyFromPem(privateKeyPem);
        const encryptedBytes = forge.util.decode64(ciphertextBase64);
        const decrypted = privateKey.decrypt(encryptedBytes, 'RSAES-PKCS1-V1_5');
        
        document.getElementById('plainTextResult').value = decrypted;
    } catch (err) {
        alert("Lỗi giải mã: Vui lòng kiểm tra lại Ciphertext hoặc Private Key!");
    }
} 

function copyToClipboard(id) {
    const text = document.getElementById(id).value;
    if (!text) {
        alert("Không có nội dung để copy!");
        return;
    }
    navigator.clipboard.writeText(text);
    alert("Đã copy vào bộ nhớ tạm!");
}

function tryAgain() {
    if (confirm("sure?")) {
        location.reload(); 
    }
}