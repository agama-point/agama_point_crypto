# agama_point_crypto

a set of libraries and basic examples for privacy, based on cryptography, simple ciphers and proper access to your data 

---

## install

```
git clone https://github.com/agama-point/agama_point_crypto.git
cd agama_point_crypto
python3 -m venv venv  
source venv/bin/activate
pip install -r requirements.txt
touch .env
```


---

Building digital security and privacy is a complex task that requires a combination of technical, legal and organisational measures. Here are some key areas on which digital security and privacy can be built:


Strong encryption: the use of strong and reliable encryption is an essential element to protect data from unauthorised access. It is important to use reliable encryption algorithms and ensure proper implementation and key management.


Managing access rights: Managing access rights and permissions is important to ensure that only authorized individuals have access to sensitive information. This includes the use of strong passwords, two-factor authentication, and proper permission settings at the user, network, and system levels.


Software and hardware security solutions: Using updated and reliable antivirus software, firewalls and other security tools is important to detect and protect against malware, hacker attacks and other threats.


Employee education: educating employees on proper cybersecurity practices is key. Employees should be made aware of the risks associated with phishing, social engineering and other attack techniques. They should be able to identify potentially dangerous situations and know how to respond to them.


Regular data backup and recovery: regular data backup is important to minimise data loss in the event of an attack or technical failure. It is also important to perform data recovery tests to ensure that backups are functional and available when needed.


Compliance with data privacy regulations: compliance with data privacy regulations and laws is essential to protect privacy. This includes, for example, compliance with the GDPR in the European Union or other relevant laws in various countries.


Security auditing and monitoring: Regular security auditing and monitoring of systems and networks is essential to detect potential vulnerabilities and unusual activity. Monitoring should be carried out in real time and include security incident detection and response systems (IDS/IPS).


It is important to recognize that digital security and privacy is an ongoing process that requires constant updating, education, and response to new threats and challenges in cyberspace.

---
```python
from crypto_agama.agama_cipher import caesar_encrypt

s = 13
text = "agama" # so better just no spaces without diacritics and numbers
print("Cipher: " + caesar_encrypt(text,s))
print("Test decrypt: " + caesar_encrypt("NTNZN",s))

#--------------------------------------------------------------------------------
# NTNZN
# AGAMA
```

```python
from crypto_agama.agama_seed_tools import seed_words, mnemonic_info

words_andreas = "army van defense carry jealous true garbage claim echo media make crunch"
mnemonic_info(words_andreas)

#--------------------------------------------------------------------------------
# [mnemonic_info]
# army van def... make crunch ( 12 )
# 96 1929 459 279 956 1866 764 333 559 1107 1076 423 
# validate:  (True, True)
```

```python
from crypto_agama.agama_trezor import get_default_client, t_connect,t_connect_first

client = t_connect_first() 
# client = get_default_client()  
"""
------------------------------------------------------------
- connecting to Trezor (get_default_client)
============================================================
device basic info:
============================================================
- client  <trezorlib.client.TrezorClient object at 0x7f0...>
---  label      T202011
---  device_id  B3D...9A7
---  fw_version 2 4 2
------------------------------------------------------------
"""
```

---

Links:

https://github.com/primal100/pybitcointools

https://github.com/octopusengine/CryptFile

https://github.com/octopusengine/krtek

https://github.com/octopusengine/virtualcoin

https://github.com/octopusengine/nodata.store
