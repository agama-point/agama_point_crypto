from crypto_agama.agama_umbrel import Mempool

DEBUG = True

m = Mempool()
m.set_url_base("local")
print("start", m.url_base)

file_name = "data_input/block_0-1000.txt"


with open(file_name, "r") as f:
    lines = f.readlines()
    
for i, line in enumerate(lines):
    if i == 0:
        continue
    values = line.strip().split(";")
    block = values[0]
    m.get_block_info(block, True, False)

"""
--------------------------------------------------
class Mempool init
--------------------------------------------------
set_url_base --- > http://192.168.0.220:3006/api/
start http://192.168.0.220:3006/api/

[get_block_info]

==================================================
get_block: 170
- url http://192.168.0.220:3006/api/block-height/170
===== json_data {'id': '00000000d1145790a8694403d4063f323d499e655c83426834d4ce2f8dd4a2ee', 'timestamp': 1231731025, 'height': 170, 'version': 1, 'bits': 486604799, 'nonce': 1889418792, 'difficulty': 1, 'merkle_root': '7dac2c5666815c17a3b36427de37bb9d2e2c5ccec3f8633eb91a4205cb4c10ff', 'tx_count': 2, 'size': 490, 'weight': 1960, 'previousblockhash': '000000002a22cfee1f2c846adbd12b3e183d4f97683f85dad08a79780a84bd55', 'extras': {'coinbaseRaw': '04ffff001d0102', 'medianFee': 0, 'feeRange': [0, 0, 0, 0, 0, 0, 0], 'reward': 5000000000, 'totalFees': 0, 'avgFee': 0, 'avgFeeRate': 0, 'pool': {'id': 137, 'name': 'Unknown', 'slug': 'unknown'}}}
- id 00000000d1145790a8694403d4063f323d499e655c83426834d4ce2f8dd4a2ee
[170] 00000000d1145790a8694403d4063f323d499e655c83426834d4ce2f8dd4a2ee 2009-01-12 04:30:25
transactions ["b1fea52486ce0c62bb442b530a3f0132b826c74e473d1f2c220bfa78111c5082","f4184fc596403b9d638783cf57adfe4c75c605f6356fbc91338530e9831e9e16"]
len 2

[get_block_info]

==================================================
get_block: 181
- url http://192.168.0.220:3006/api/block-height/181
===== json_data {'id': '00000000dc55860c8a29c58d45209318fa9e9dc2c1833a7226d86bc465afc6e5', 'timestamp': 1231740133, 'height': 181, 'version': 1, 'bits': 486604799, 'nonce': 792669465, 'difficulty': 1, 'merkle_root': 'ed92b1db0b3e998c0a4351ee3f825fd5ac6571ce50c050b4b45df015092a6c36', 'tx_count': 2, 'size': 490, 'weight': 1960, 'previousblockhash': '00000000b5ef0ea215becad97402ce59d1416fe554261405cda943afd2a8c8f2', 'extras': {'coinbaseRaw': '04ffff001d0128', 'medianFee': 0, 'feeRange': [0, 0, 0, 0, 0, 0, 0], 'reward': 5000000000, 'totalFees': 0, 'avgFee': 0, 'avgFeeRate': 0, 'pool': {'id': 137, 'name': 'Unknown', 'slug': 'unknown'}}}
- id 00000000dc55860c8a29c58d45209318fa9e9dc2c1833a7226d86bc465afc6e5
[181] 00000000dc55860c8a29c58d45209318fa9e9dc2c1833a7226d86bc465afc6e5 2009-01-12 07:02:13
transactions ["8347cee4a1cb5ad1bb0d92e86e6612dbf6cfc7649c9964f210d4069b426e720a","a16f3ce4dd5deb92d98ef5cf8afeaf0775ebca408f708b2146c4fb42b41e14be"]
len 2

[get_block_info]

==================================================
get_block: 182
- url http://192.168.0.220:3006/api/block-height/182
===== json_data {'id': '0000000054487811fc4ff7a95be738aa5ad9320c394c482b27c0da28b227ad5d', 'timestamp': 1231740736, 'height': 182, 'version': 1, 'bits': 486604799, 'nonce': 2662131500, 'difficulty': 1, 'merkle_root': '2f0f017f1991a1393798ff851bfc02ce7ba3f5e066815ed3104afb4bd3a0c230', 'tx_count': 2, 'size': 490, 'weight': 1960, 'previousblockhash': '00000000dc55860c8a29c58d45209318fa9e9dc2c1833a7226d86bc465afc6e5', 'extras': {'coinbaseRaw': '04ffff001d0129', 'medianFee': 0, 'feeRange': [0, 0, 0, 0, 0, 0, 0], 'reward': 5000000000, 'totalFees': 0, 'avgFee': 0, 'avgFeeRate': 0, 'pool': {'id': 137, 'name': 'Unknown', 'slug': 'unknown'}}}
- id 0000000054487811fc4ff7a95be738aa5ad9320c394c482b27c0da28b227ad5d
[182] 0000000054487811fc4ff7a95be738aa5ad9320c394c482b27c0da28b227ad5d 2009-01-12 07:12:16
transactions ["09e5c4a5a089928bbe368cd0f2b09abafb3ebf328cd0d262d06ec35bdda1077f","591e91f809d716912ca1d4a9295e70c3e78bab077683f79350f101da64588073"]
len 2

[get_block_info]

==================================================
get_block: 183
- url http://192.168.0.220:3006/api/block-height/183
===== json_data {'id': '00000000f46e513f038baf6f2d9a95b2a28d8a6c985bcf24b9e07f0f63a29888', 'timestamp': 1231742062, 'height': 183, 'version': 1, 'bits': 486604799, 'nonce': 3235118355, 'difficulty': 1, 'merkle_root': 'df25983b51d84d40b4efcb5556cdd6d524ac2d21bca49037494e413ae0712529', 'tx_count': 2, 'size': 491, 'weight': 1964, 'previousblockhash': '0000000054487811fc4ff7a95be738aa5ad9320c394c482b27c0da28b227ad5d', 'extras': {'coinbaseRaw': '04ffff001d012a', 'medianFee': 0, 'feeRange': [0, 0, 0, 0, 0, 0, 0], 'reward': 5000000000, 'totalFees': 0, 'avgFee': 0, 'avgFeeRate': 0, 'pool': {'id': 137, 'name': 'Unknown', 'slug': 'unknown'}}}
- id 00000000f46e513f038baf6f2d9a95b2a28d8a6c985bcf24b9e07f0f63a29888
[183] 00000000f46e513f038baf6f2d9a95b2a28d8a6c985bcf24b9e07f0f63a29888 2009-01-12 07:34:22
transactions ["b2e561eb278f5aba7a2c78d46422f496f4998003635cc65807e230407190a355","12b5633bad1f9c167d523ad1aa1947b2732a865bf5414eab2f9e5ae5d5c191ba"]
len 2

[get_block_info]

==================================================
get_block: 187
- url http://192.168.0.220:3006/api/block-height/187
===== json_data {'id': '00000000b2cde2159116889837ecf300bd77d229d49b138c55366b54626e495d', 'timestamp': 1231744600, 'height': 187, 'version': 1, 'bits': 486604799, 'nonce': 853721115, 'difficulty': 1, 'merkle_root': '52478db532c594119845eb8260d640d78798e4b7fcb77fed4e2bad4c3ecbaf1c', 'tx_count': 2, 'size': 414, 'weight': 1656, 'previousblockhash': '000000008b3ff2aaf3427f2a624cb9978e687d9fbba5000dc2f52bb4cc82d4be', 'extras': {'coinbaseRaw': '04ffff001d011a', 'medianFee': 0, 'feeRange': [0, 0, 0, 0, 0, 0, 0], 'reward': 5000000000, 'totalFees': 0, 'avgFee': 0, 'avgFeeRate': 0, 'pool': {'id': 137, 'name': 'Unknown', 'slug': 'unknown'}}}
- id 00000000b2cde2159116889837ecf300bd77d229d49b138c55366b54626e495d
[187] 00000000b2cde2159116889837ecf300bd77d229d49b138c55366b54626e495d 2009-01-12 08:16:40
transactions ["70587f1780ccd2ebbace28a7b33d83d19f4362f10ff7a4ad88f8c413883f94b7","4385fcf8b14497d0659adccfe06ae7e38e0b5dc95ff8a13d7c62035994a0cd79"]
len 2

[get_block_info]

==================================================
get_block: 221
- url http://192.168.0.220:3006/api/block-height/221
===== json_data {'id': '0000000066356691a4353dd8bdc2c60da20d68ad34fff93d8839a133b2a6d42a', 'timestamp': 1231770060, 'height': 221, 'version': 1, 'bits': 486604799, 'nonce': 1772122369, 'difficulty': 1, 'merkle_root': '67f445c708d28c16aeb6eaa81d7ccff29a0c39ff48c6d6298c9ff1e0b6899f07', 'tx_count': 2, 'size': 417, 'weight': 1668, 'previousblockhash': '00000000b66ac539d2cdfebdd4720cb08603b48edec56cc07273c40b082b1d58', 'extras': {'coinbaseRaw': '04ffff001d029e00', 'medianFee': 0, 'feeRange': [0, 0, 0, 0, 0, 0, 0], 'reward': 5000000000, 'totalFees': 0, 'avgFee': 0, 'avgFeeRate': 0, 'pool': {'id': 137, 'name': 'Unknown', 'slug': 'unknown'}}}
- id 0000000066356691a4353dd8bdc2c60da20d68ad34fff93d8839a133b2a6d42a
[221] 0000000066356691a4353dd8bdc2c60da20d68ad34fff93d8839a133b2a6d42a 2009-01-12 15:21:00
transactions ["264e7238ddc574d5d6ded85d77bfcb69d99a0de17dfcdef0b7e97d430c4f202d","298ca2045d174f8a158961806ffc4ef96fad02d71a6b84d9fa0491813a776160"]
len 2

[get_block_info]

...

==================================================
get_block: 546
- url http://192.168.0.220:3006/api/block-height/546
===== json_data {'id': '000000005a4ded781e667e06ceefafb71410b511fe0d5adc3e5a27ecbec34ae6', 'timestamp': 1231999700, 'height': 546, 'version': 1, 'bits': 486604799, 'nonce': 1101328384, 'difficulty': 1, 'merkle_root': 'e10a7f8442ea6cc6803a2b83713765c0b1199924110205f601f90fef125e7dfe', 'tx_count': 4, 'size': 1385, 'weight': 5540, 'previousblockhash': '00000000689051c09ff2cd091cc4c22c10b965eb8db3ad5f032621cc36626175', 'extras': {'coinbaseRaw': '04ffff001d029105', 'medianFee': 0, 'feeRange': [0, 0, 0, 0, 0, 0, 0], 'reward': 5000000000, 'totalFees': 0, 'avgFee': 0, 'avgFeeRate': 0, 'pool': {'id': 137, 'name': 'Unknown', 'slug': 'unknown'}}}
- id 000000005a4ded781e667e06ceefafb71410b511fe0d5adc3e5a27ecbec34ae6
[546] 000000005a4ded781e667e06ceefafb71410b511fe0d5adc3e5a27ecbec34ae6 2009-01-15 07:08:20
transactions ["e980fe9f792d014e73b95203dc1335c5f9ce19ac537a419e6df5b47aecb93b70","28204cad1d7fc1d199e8ef4fa22f182de6258a3eaafe1bbe56ebdcacd3069a5f","6b0f8a73a56c04b519f1883e8aafda643ba61a30bd1439969df21bea5f4e27e2","3c1d7e82342158e4109df2e0b6348b6e84e403d8b4046d7007663ace63cddb23"]
len 4

[get_block_info]

==================================================
get_block: 586
- url http://192.168.0.220:3006/api/block-height/586
===== json_data {'id': '000000000d0d23516c5efd3af4eb951603bb30b2c93884b522a318b30e918ee7', 'timestamp': 1232029520, 'height': 586, 'version': 1, 'bits': 486604799, 'nonce': 932288301, 'difficulty': 1, 'merkle_root': '197b3d968ce463aa5da7d8eeba8af35eba80ded4e4fe6808e6cc0dd1c069594d', 'tx_count': 3, 'size': 1071, 'weight': 4284, 'previousblockhash': '0000000046ff6c4f9a7224aa331c407c7e37f49434571307d6fca58695bcba38', 'extras': {'coinbaseRaw': '04ffff001d025d06', 'medianFee': 0, 'feeRange': [0, 0, 0, 0, 0, 0, 0], 'reward': 5000000000, 'totalFees': 0, 'avgFee': 0, 'avgFeeRate': 0, 'pool': {'id': 137, 'name': 'Unknown', 'slug': 'unknown'}}}
- id 000000000d0d23516c5efd3af4eb951603bb30b2c93884b522a318b30e918ee7
[586] 000000000d0d23516c5efd3af4eb951603bb30b2c93884b522a318b30e918ee7 2009-01-15 15:25:20
transactions ["d45724bacd1480b0c94d363ebf59f844fb54e60cdfda0cd38ef67154e9d0bc43","4d6edbeb62735d45ff1565385a8b0045f066055c9425e21540ea7a8060f08bf2","6bf363548b08aa8761e278be802a2d84b8e40daefe8150f9af7dd7b65a0de49f"]
len 3

[get_block_info]

==================================================
get_block: 593
- url http://192.168.0.220:3006/api/block-height/593
===== json_data {'id': '000000001d6a5eaa63b653d569e87179366ffee019ea4108f766e79578b5ebb2', 'timestamp': 1232034716, 'height': 593, 'version': 1, 'bits': 486604799, 'nonce': 2441341989, 'difficulty': 1, 'merkle_root': '952ddfa93b195f31a0c1a1114bf8e6d66ee861ae7f0e93e0593ba68fb6c10359', 'tx_count': 2, 'size': 492, 'weight': 1968, 'previousblockhash': '000000007ba4ed8233fba72ad14360d0aa1bd8ef5675c2d06659dfabd5862084', 'extras': {'coinbaseRaw': '04ffff001d028c06', 'medianFee': 0, 'feeRange': [0, 0, 0, 0, 0, 0, 0], 'reward': 5000000000, 'totalFees': 0, 'avgFee': 0, 'avgFeeRate': 0, 'pool': {'id': 137, 'name': 'Unknown', 'slug': 'unknown'}}}
- id 000000001d6a5eaa63b653d569e87179366ffee019ea4108f766e79578b5ebb2
[593] 000000001d6a5eaa63b653d569e87179366ffee019ea4108f766e79578b5ebb2 2009-01-15 16:51:56
transactions ["8b3e3337952cbd2dac159723c972954efb02c05b9c583a081a1e11ed8e861ae4","e36f06a8dfe44c3d64be2d3fe56c77f91f6a39da4a5ffc086ecb5db9664e8583"]
len 2

[get_block_info]

==================================================
get_block: 707
- url http://192.168.0.220:3006/api/block-height/707
===== json_data {'id': '00000000bf9c7f7b8b72d82164a9328e331581e68885d1f5003da874f23fa474', 'timestamp': 1232113906, 'height': 707, 'version': 1, 'bits': 486604799, 'nonce': 7512790, 'difficulty': 1, 'merkle_root': '56ef0aca70b659257a4bd9f74b01c5c370645a6370e06a36e831a498142fb1d9', 'tx_count': 2, 'size': 529, 'weight': 2116, 'previousblockhash': '000000006f6709b76bed31001b32309167757007aa4fb899f8168c8e9c084b1a', 'extras': {'coinbaseRaw': '04ffff001d014e', 'medianFee': 0, 'feeRange': [0, 0, 0, 0, 0, 0, 0], 'reward': 5000000000, 'totalFees': 0, 'avgFee': 0, 'avgFeeRate': 0, 'pool': {'id': 137, 'name': 'Unknown', 'slug': 'unknown'}}}
- id 00000000bf9c7f7b8b72d82164a9328e331581e68885d1f5003da874f23fa474
[707] 00000000bf9c7f7b8b72d82164a9328e331581e68885d1f5003da874f23fa474 2009-01-16 14:51:46
transactions ["eee136c1ba8f9b76f31b8d049d6e373a331f20f0b00c02395ace5156b2ccaa20","5439c37c4c6dad4ad93b1d5598d57f1aace9d0f68b892236da903b3f136451a1"]
len 2

[get_block_info]

==================================================
get_block: 728
- url http://192.168.0.220:3006/api/block-height/728
===== json_data {'id': '00000000d14f2e97678951ad004d6699babd27e07ca722c46b30dc24c67eed7a', 'timestamp': 1232133515, 'height': 728, 'version': 1, 'bits': 486604799, 'nonce': 95106676, 'difficulty': 1, 'merkle_root': '1f7fd770697c167ca75e3d742f3b1b81244165e0fee87310cd20b15f6975b961', 'tx_count': 2, 'size': 489, 'weight': 1956, 'previousblockhash': '000000001c7eb6ab129cf14659aea1f77f6e116ea8da2193182b08eae6ecf5f7', 'extras': {'coinbaseRaw': '04ffff001d0164', 'medianFee': 0, 'feeRange': [0, 0, 0, 0, 0, 0, 0], 'reward': 5000000000, 'totalFees': 0, 'avgFee': 0, 'avgFeeRate': 0, 'pool': {'id': 137, 'name': 'Unknown', 'slug': 'unknown'}}}
- id 00000000d14f2e97678951ad004d6699babd27e07ca722c46b30dc24c67eed7a
[728] 00000000d14f2e97678951ad004d6699babd27e07ca722c46b30dc24c67eed7a 2009-01-16 20:18:35
transactions ["5fe6030e8a649b3b3fb257303e89a06d6556226e24118b494f9ccbba06e96254","6f7cf9580f1c2dfb3c4d5d043cdbb128c640e3f20161245aa7372e9666168516"]
len 2

[get_block_info]

==================================================
get_block: 943
- url http://192.168.0.220:3006/api/block-height/943
===== json_data {'id': '00000000e9a0e6f8f08cc1ac6198e3ea633bce375316c3d593a6654ec7e08b2d', 'timestamp': 1232308979, 'height': 943, 'version': 1, 'bits': 486604799, 'nonce': 3294000686, 'difficulty': 1, 'merkle_root': 'a660e96c749aca24d055bf0754931b0aa036bf9a799836df1e08c0c57e7cc7df', 'tx_count': 2, 'size': 642, 'weight': 2568, 'previousblockhash': '0000000002edf896a1d087514c37b37680e1e9d93058bd6fab49711169a2a79b', 'extras': {'coinbaseRaw': '04ffff001d024104', 'medianFee': 0, 'feeRange': [0, 0, 0, 0, 0, 0, 0], 'reward': 5000000000, 'totalFees': 0, 'avgFee': 0, 'avgFeeRate': 0, 'pool': {'id': 137, 'name': 'Unknown', 'slug': 'unknown'}}}
- id 00000000e9a0e6f8f08cc1ac6198e3ea633bce375316c3d593a6654ec7e08b2d
[943] 00000000e9a0e6f8f08cc1ac6198e3ea633bce375316c3d593a6654ec7e08b2d 2009-01-18 21:02:59
transactions ["7fad6c73cf98d9d5d158a918504ec2ab72131bea0dc8b9c5b6ca397b7673bf5e","3e4cc1f71c998d080528ae305dffcc01419851e0d7b5191edfada9528625bff6"]
len 2
"""
