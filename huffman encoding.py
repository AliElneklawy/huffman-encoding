import heapq
import math

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

def total_gain(text, code_dict, char_freq):
    bef_comp = len(text) * 8
    after_comp = 0
    for symbol in code_dict.keys():
        cnt_char = char_freq[symbol]
        after_comp += cnt_char * len(code_dict[symbol])

    return (bef_comp, after_comp)


if __name__ == "__main__":
    text = "Hello, my name is Ali. I am 23 years old."
    char_freq = clc_freq(text) #frequency of each char
    probs = clc_probability(text) #probability of each char
    node = huffman_encoding(char_freq) 
    code_dict = clc_code(node[0])   #huffman code for each char
    entropy = clc_entropy(probs)    #entropy calculation
    efficiency = clc_efficiency(probs, code_dict, entropy) #efficiency calculation
    bef_comp, after_comp = total_gain(text, code_dict, char_freq)
    
    print(f"Huffman code: {code_dict}")
    print(f"Size before compression: {bef_comp} bits\nSize after compression: {after_comp} bits")
    print(f"Coding efficiency: {efficiency}")
