"""
Stronk module
"""

import secrets as random
import os


key = ''
letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
symbols = '!@#$%+=?&*()'


def generate_random_keys(number_of_keys=1, key_length=16):
    """ Returns the generated keys """
    number_of_keys_iterator = 0
    keys = []
    error_message = ''
    if number_of_keys > 100:
        error_message += "ERROR: Number of keys must be <= 100\n"
    if number_of_keys <= 0:
        error_message += "ERROR: Number of keys must be non-zero and non-negative\n"
    if key_length > 256:
        error_message += "ERROR: Key length must be <= 256\n"
    if key_length < 16:
        error_message += "ERROR: Key length must be non-zero and non-negative\n"
    if not error_message:
        while number_of_keys_iterator < number_of_keys:
            key_length_iterator = 0
            key = ''
            while key_length_iterator < key_length:
                key += str(_generate_random_char())
                key_length_iterator += 1
            keys.append(_shuffle_key(key))
            number_of_keys_iterator += 1
        return keys
    return error_message


def generate_sha5_hash():
    """ Generate sha5 hash """
    return 0


def _shuffle_key(key):
    """ Returns the shuffled key """
    random.SystemRandom().shuffle(list(key))
    return ''.join(key)


def _generate_random_char():
    """ Generate a random integer, letter, or symbol """
    character_type = random.randbelow(11)
    if character_type == (0 or 1):
        return random.randbelow(10)
    if character_type != (0 or 1 or 2):
        return random.choice(letters)
    if character_type == 2:
        return random.choice(symbols)


def _prettify_output(output):
    if isinstance(output, list):
        for out in output:
            print(out)
    else:
        print(output)


def _print_to_txt_file(keys):
    current_working_directory = os.getcwd()
    output_file = open(current_working_directory + "/stronk.txt", "w")
    for key in keys:
        output_file.write(key + "\n")
    output_file.close()
