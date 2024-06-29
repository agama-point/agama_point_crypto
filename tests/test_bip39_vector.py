import requests, json 
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from crypto_agama.agama_seed_tools import BIP39Functions, create_root_key
from crypto_agama.trezor_mnemonic import Mnemonic


bip39f = BIP39Functions()

# url = "https://github.com/trezor/python-mnemonic/blob/master/vectors.json"
url = "https://raw.githubusercontent.com/trezor/python-mnemonic/master/vectors.json"

response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    
    for item in data['english']:
        mnemo = Mnemonic("english")
        hex_value = item[0]
        mnemonic = item[1]
        seed = item[2]
        xprv = item[3]
        
        print(f"Hex: {hex_value}")
        print(f"Mnemonic: {mnemonic}")
        phrase = bip39f.entropy_to_phrase(hex_value)
        print(f"Mnemonic? {phrase}")

        print(f"Seed: {seed}")
        bip39f.create_binary_seed()
        print(f"Seed? {bip39f.binary_seed}") # x ???

        seed_bytes = mnemo.to_seed(mnemonic, "")
    
        #print("seed_bytes",seed_bytes)
        print("--- BIP39 seed:")
        print(seed_bytes.hex()) # hexadecimal_string = some_bytes.hex()
        print("--- BIP32 root key:")
        root_key = create_root_key(seed_bytes)
        print(root_key)

        print(f"xPrv: {xprv}")
        print("---------")
else:
    print(f"Chyba při načítání souboru: {response.status_code}")

"""
...
---------
Hex: 7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f
Mnemonic: legal winner thank year wave sausage worth useful legal winner thank year wave sausage worth useful legal will
Mnemonic? legal winner thank year wave sausage worth useful legal winner thank year wave sausage worth useful legal will
Seed: f2b94508732bcbacbcc020faefecfc89feafa6649a5491b8c952cede496c214a0c7b3c392d168748f2d4a612bada0753b52a1c7ac53c1e93abd5c6320b9e95dd
Seed? 76fa4cc1759a7c2240e4899e0579803dbd0b47b546338dcc57e9c8aad246f529bc718bb4085b6973ab8fc246694b8f43a5d14da82ed3ef67e48591abace286c8
--- BIP39 seed:
b059400ce0f55498a5527667e77048bb482ff6daa16c37b4b9e8af70c85b3f4df588004f19812a1a027c9a51e5e94259a560268e91cd10e206451a129826e740
--- BIP32 root key:
version_BYTES:  mainnet_private
xprv9s21ZrQH143K4Vgw4mbHCunAxHVRuR1irqSiqXVGpSuca7rczLU2w6hiPkA1HW7GEUZTNtsFJrwggFJZNGRhmRP1e6y8BYH98xMnYDavzB4
xPrv: xprv9s21ZrQH143K3Lv9MZLj16np5GzLe7tDKQfVusBni7toqJGcnKRtHSxUwbKUyUWiwpK55g1DUSsw76TF1T93VT4gz4wt5RM23pkaQLnvBh7
---------
Hex: 808080808080808080808080808080808080808080808080
Mnemonic: letter advice cage absurd amount doctor acoustic avoid letter advice cage absurd amount doctor acoustic avoid letter always
Mnemonic? letter advice cage absurd amount doctor acoustic avoid letter advice cage absurd amount doctor acoustic avoid letter always
Seed: 107d7c02a5aa6f38c58083ff74f04c607c2d2c0ecc55501dadd72d025b751bc27fe913ffb796f841c49b1d33b610cf0e91d3aa239027f5e99fe4ce9e5088cd65
Seed? cbbf67d534fe6b54229b5cdaf8f76d165086b1910986d420762b1a736f6cabac5fb3894b0fe42b86baca2a752ed50cc1d0db4cf2d71ab8fd02071144d0f9888d
--- BIP39 seed:
04d5f77103510c41d610f7f5fb3f0badc77c377090815cee808ea5d2f264fdfabf7c7ded4be6d4c6d7cdb021ba4c777b0b7e57ca8aa6de15aeb9905dba674d66
--- BIP32 root key:
version_BYTES:  mainnet_private
xprv9s21ZrQH143K2Z2MAexszKEd4vm8bHh9vdxreb2KFq2deUv57Xd8winRtRaRFAvbixr43BhviFF9mSQ2TyGHuwKKRAmeVc17wxFKEbrvKh2
xPrv: xprv9s21ZrQH143K3VPCbxbUtpkh9pRG371UCLDz3BjceqP1jz7XZsQ5EnNkYAEkfeZp62cDNj13ZTEVG1TEro9sZ9grfRmcYWLBhCocViKEJae
---------
...
"""


