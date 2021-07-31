import bls from 'bls-wasm';

await bls.init(bls.BN254)

function hexStringToByte(str) {
    if (!str) {
        return new Uint8Array();
    }
    var a = [];
    for (var i = 0, len = str.length; i < len; i += 2) {
        a.push(parseInt(str.substr(i, 2), 16));
    }
    return new Uint8Array(a);
}

const sign = (secretKey, hashPayload) => {

    const byteHash = hexStringToByte(hashPayload)
    const sec = new bls.SecretKey()
    sec.deserializeHexStr(secretKey)
    const sig = sec.sign(byteHash)

    process.stdout.write(sig.serializeToHexStr())
}

const args = process.argv.slice(2)
const secretKey = args[0]
const hashPayload = args[1]

sign(secretKey, hashPayload)