from crypto_agama.agama_transform_tools import decimal_to_base, base_to_decimal

desitky = [0,1,5,6,9,10,255,512,999,1024,1295,2048]

for decimal_number in desitky:
    cislo_petkova = decimal_to_base(decimal_number,5)
    cislo_sestkova = decimal_to_base(decimal_number,6)
    print(f"{str(decimal_number).zfill(4)} (10) = {cislo_petkova} (5) = {cislo_sestkova} (6)")

print("="*30)

numbers = ['001',"5",'006','10','010','055','333','5555','13231','13252']
base = 4
for number in numbers: 
    decimal_number = base_to_decimal(number, base)
    print(f"{number.zfill(5)} ({base}) = {str(decimal_number).zfill(4)} (10)")

print("-"*30)

base = 5
for number in numbers: 
    decimal_number = base_to_decimal(number, base)
    print(f"{number.zfill(5)} ({base}) = {str(decimal_number).zfill(4)} (10)")

print("-"*30)

base = 6
for number in numbers: 
    decimal_number = base_to_decimal(number, base)
    print(f"{number.zfill(5)} ({base}) = {str(decimal_number).zfill(4)} (10)")

print("-"*30)

base = 7
for number in numbers: 
    decimal_number = base_to_decimal(number, base)
    print(f"{number.zfill(5)} ({base}) = {str(decimal_number).zfill(4)} (10)")
