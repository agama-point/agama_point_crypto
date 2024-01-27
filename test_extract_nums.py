from crypto_agama.agama_transform_tools import extract_numbers, split_numbers

# Example usage
input_string = "14abc1592653589793238462643383279502884197169399375xyz10"
result = extract_numbers(input_string)

if len(result) > 0:
    numbers_list = split_numbers(result)
    print(numbers_list)