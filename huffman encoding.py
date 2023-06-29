import heapq
import math
import json
import os


class Node:
    def __init__(self, symbol, freq, left=None, right=None) -> None:

        self.symbol = symbol
        self.freq = freq
        self.left = left
        self.right = right
        self.code = ""

    def __lt__(self, next):
        return self.freq < next.freq


def huffman_encoding(char_freq: dict):
    nodes = []
    for symb, freq in char_freq.items():
        heapq.heappush(nodes, Node(symb, freq))

    while len(nodes) > 1:
        left = heapq.heappop(nodes)
        right = heapq.heappop(nodes)

        left.code = '0'
        right.code = '1'

        new_node = Node(left.symbol + right.symbol, left.freq + right.freq, left, right)
        heapq.heappush(nodes, new_node)

    return nodes


def clc_freq(text):
    freq_dict = {}
    for char in text:
        if char not in freq_dict:
            freq_dict[char] = 1
        else:
            freq_dict[char] += 1

    return freq_dict


def clc_code(node: Node, val="", code_dict: dict={}):
    new_val = val + node.code

    if node.left:
        clc_code(node.left, new_val)
    if node.right:
        clc_code(node.right, new_val)
    if not node.left and not node.right:
        code_dict[node.symbol] = new_val

    return code_dict    


def clc_efficiency(alpha_probs, code_dict, entropy):
    L_bar = 0
    for alpha in alpha_probs:
        L_bar += alpha[1] * len(code_dict[alpha[0]])
    efficiency = (entropy / L_bar) * 100

    return efficiency


def clc_probability(text):
    text_len = len(text)
    alpha_probs = set()  

    #probability calculation
    for char in text:
        alpha_probs.add((char, text.count(char)/text_len))

    return alpha_probs

def clc_entropy(probs):
    entropy = 0
    probs = dict(probs)
    for prob in probs.values():
       entropy += prob * math.log2(prob)
    entropy = -entropy
    return entropy

def total_gain(text, code_dict):
    bef_comp = len(text) * 8
    after_comp = 0
    for symbol in code_dict.keys():
        cnt_char = text.count(symbol)
        after_comp += cnt_char * len(code_dict[symbol])

    return (bef_comp, after_comp)


def write_compressed_data(text, code_dict, output_file):
    with open(output_file, 'wb') as file:
        tree_info = get_tree_info(code_dict)
        file.write(tree_info.encode('utf-8'))
        file.write(b'\n')

        encoded_data = encode_text(text, code_dict)
        file.write(encoded_data)


def get_tree_info(code_dict):
    tree_info = json.dumps(code_dict)

    return tree_info


def encode_text(text, code_dict):
    encoded_data = ''.join(code_dict[char] for char in text)
    padding = 8 - len(encoded_data) % 8
    encoded_data += '0' * padding

    encoded_bytes = bytes(int(encoded_data[i:i+8], 2) for i in range(0, len(encoded_data), 8))

    return encoded_bytes


def huffman_decoding(input_file):
    with open(input_file, 'rb') as file:
        dict_line = file.readline().decode().rstrip()
        code_dict = json.loads(dict_line)
        encoded_data = file.read()

    encoded_bits = ''.join(format(byte, '08b') for byte in encoded_data)
    encoded_bits = encoded_bits[:-8]
    dict_end_marker = encoded_bits.find('\n')
    encoded_data = encoded_bits[dict_end_marker + 1:]
    reverse_code_dict = {v: k for k, v in code_dict.items()}

    decoded_text = ""
    current_code = ""
    for bit in encoded_data:
        current_code += bit
        if current_code in reverse_code_dict:
            decoded_text += reverse_code_dict[current_code]
            current_code = ""

    return decoded_text


if __name__ == "__main__":
    choice = int(input("Enter 1 to decode or 0 to encode: "))
    if choice == 0:
        input_file = input("Enter the path to the target file: ")
        with open(input_file, 'r') as file:
            text = file.read()

        char_freq = clc_freq(text)  # frequency of each char
        print("Calculating the frequency of each character.....")
        probs = clc_probability(text)  # probability of each char
        print("Calculating the probability of each character.....")
        node = huffman_encoding(char_freq)
        print("Encodeing....")
        code_dict = clc_code(node[0])  # huffman code for each char
        entropy = clc_entropy(probs)  # entropy calculation
        efficiency = clc_efficiency(probs, code_dict, entropy)  # efficiency calculation
        print("Calculating efficiency....")
        bef_comp, after_comp = total_gain(text, code_dict)
        write_compressed_data(text, code_dict, input_file)
        print("Writing the encoded data....")

        print(f"Huffman code: {code_dict}")
        print(f"Size before compression: {bef_comp} bits\nSize after compression: {after_comp} bits")
        print(f"Coding efficiency: {efficiency}")

    else:
        input_file = input("Enter the path to the encoded file: ")
        output_file = os.path.join(os.path.dirname(input_file), "output.txt")

        with open(output_file, 'w') as file:
            decoded_text = huffman_decoding(input_file)
            file.write(decoded_text)
