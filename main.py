import tkinter as tk
import csv

valid_alphabet = ['a', 'ą', 'b', 'c', 'ć', 'd', 'e', 'ę', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'ł',
'm', 'n', 'ń', 'o', 'ó', 'p', 'q', 'r', 's', 'ś', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'ź', 'ż']

def load_key(file_name):
    with open(file_name, newline='', encoding='utf-8') as key_file:
        key = csv.reader(key_file)
        key = [row for row in key]
        key_reshaped = [item for row in key for item in row]

        if sorted(key_reshaped) != sorted(valid_alphabet):
            raise ValueError("The key matrix is incorrect.")

        return key

def find_letter_index(letter):
    for row_idx, row in enumerate(key):
        if letter in row:
            return row_idx, row.index(letter)
    return None

def encrypt():
    input_text = encrypt_entry1.get().lower()

    input_text = ''.join([char for char in input_text if char in valid_alphabet])

    if len(input_text) == 0:
        encrypt_response.config(text="Wprowadzony tekst jest niepoprawny!")
        return

    valid_text = ''

    for i, letter in enumerate(input_text):
        if i != 0 and input_text[i - 1] == input_text[i]:
            if letter == 'x':
                valid_text += 'yx'
            else:
                valid_text += ('x' + letter)
        else:
            valid_text += letter

    if len(valid_text) % 2 != 0:
        if valid_text[-1] == 'x':
            valid_text = valid_text + 'y'
        else:
            valid_text = valid_text + 'x'

    list_to_encrypt = [valid_text[i:i+2] for i in range(0, len(valid_text), 2)]

    encrypted_list = []

    for pair in list_to_encrypt:
        first_letter_idx = find_letter_index(pair[0])
        second_letter_idx = find_letter_index(pair[1])

        new_pair = ''

        if first_letter_idx[0] == second_letter_idx[0]:
            if first_letter_idx[1] + 1 == len(key[0]):
                new_pair += key[first_letter_idx[0]][0]
                new_pair += key[second_letter_idx[0]][second_letter_idx[1] + 1]
            elif second_letter_idx[1] + 1 == len(key[0]):
                new_pair += key[first_letter_idx[0]][first_letter_idx[1] + 1]
                new_pair += key[second_letter_idx[0]][0]
            else:
                new_pair += key[first_letter_idx[0]][first_letter_idx[1] + 1]
                new_pair += key[second_letter_idx[0]][second_letter_idx[1] + 1]
        elif first_letter_idx[1] == second_letter_idx[1]:
            if first_letter_idx[0] + 1 == len(key):
                new_pair += key[0][first_letter_idx[1]]
                new_pair += key[second_letter_idx[0] + 1][second_letter_idx[1]]
            elif second_letter_idx[0] + 1 == len(key):
                new_pair += key[first_letter_idx[0] + 1][first_letter_idx[1]]
                new_pair += key[0][second_letter_idx[1]]
            else:
                new_pair += key[first_letter_idx[0] + 1][first_letter_idx[1]]
                new_pair += key[second_letter_idx[0] + 1][second_letter_idx[1]]
        else:
            new_pair += key[first_letter_idx[0]][second_letter_idx[1]]
            new_pair += key[second_letter_idx[0]][first_letter_idx[1]]

        encrypted_list.append(new_pair)

    encrypt_response.config(text=''.join(encrypted_list))



def decrypt():
    input_text = decrypt_entry1.get()

    if not all(x in valid_alphabet for x in input_text) or len(input_text) % 2 != 0:
        decrypt_response.config(text='Wprowadzony szyfr jest niepoprawny!')

    decrypted_list = []

    for pair in [input_text[i:i+2] for i in range(0, len(input_text), 2)]:
        first_letter_idx = find_letter_index(pair[0])
        second_letter_idx = find_letter_index(pair[1])

        decrypted_pair = ''

        if first_letter_idx[0] == second_letter_idx[0]:
            row = first_letter_idx[0]
            first_new_index = (first_letter_idx[1] - 1) % len(key[row])
            second_new_index = (second_letter_idx[1] - 1) % len(key[row])
            decrypted_pair += key[row][first_new_index]
            decrypted_pair += key[row][second_new_index]
        elif first_letter_idx[1] == second_letter_idx[1]:
            col = first_letter_idx[1]
            first_new_index = (first_letter_idx[0] - 1) % len(key)
            second_new_index = (second_letter_idx[0] - 1) % len(key)
            decrypted_pair += key[first_new_index][col]
            decrypted_pair += key[second_new_index][col]
        else:
            decrypted_pair += key[first_letter_idx[0]][second_letter_idx[1]]
            decrypted_pair += key[second_letter_idx[0]][first_letter_idx[1]]

        decrypted_list.append(decrypted_pair)

    decrypt_response.config(text=''.join(decrypted_list))

key = load_key('key.csv')

#GŁÓWNE OKNO
root = tk.Tk()
root.title("Szyfr Polibiusza")
root.geometry("800x400")
root.configure(bg="#1A1A1A")

#SZYFROWANIE
encrypt_box = tk.Frame(root, padx=15, pady=15, bg="#1A1A1A", relief="ridge", bd=2)
encrypt_box.pack(pady=20)

encrypt_label0 = tk.Label(encrypt_box, text="SZYFROWANIE", bg="#1A1A1A", fg="#FF8C42", font=("Arial", 18, "bold"))
encrypt_label0.grid(row=0, column=0, columnspan=2, pady=10)

encrypt_label1 = tk.Label(encrypt_box, text="Tekst do zaszyfrowania:", bg="#1A1A1A", fg="#CCCCCC", font=("Arial", 12))
encrypt_label1.grid(row=1, column=0, pady=10, sticky="w")

encrypt_entry1 = tk.Entry(encrypt_box, width=40, bg="#333333", fg="#FFFFFF", insertbackground="#FF8C42", font=("Arial", 12))
encrypt_entry1.grid(row=1, column=1, pady=10)

encrypt_btn = tk.Button(encrypt_box, text="Szyfruj", command=encrypt, bg="#FF8C42", fg="#1A1A1A", font=("Arial", 12, "bold"), relief="flat", padx=10)
encrypt_btn.grid(row=2, column=0, columnspan=2, pady=10)

encrypt_response = tk.Label(encrypt_box, text="", bg="#1A1A1A", fg="#80FF80", font=("Arial", 12))
encrypt_response.grid(row=3, column=0, columnspan=2)

#DESZYFROWANIE
decrypt_box = tk.Frame(root, padx=15, pady=15, bg="#1A1A1A", relief="ridge", bd=2)
decrypt_box.pack(pady=20)

decrypt_label0 = tk.Label(decrypt_box, text="DESZYFROWANIE", bg="#1A1A1A", fg="#FF8C42", font=("Arial", 18, "bold"))
decrypt_label0.grid(row=0, column=0, columnspan=2, pady=10)

decrypt_label1 = tk.Label(decrypt_box, text="Tekst do odszyfrowania:", bg="#1A1A1A", fg="#CCCCCC", font=("Arial", 12))
decrypt_label1.grid(row=1, column=0, pady=10, sticky="w")

decrypt_entry1 = tk.Entry(decrypt_box, width=40, bg="#333333", fg="#FFFFFF", insertbackground="#FF8C42", font=("Arial", 12))
decrypt_entry1.grid(row=1, column=1, pady=10)

decrypt_btn = tk.Button(decrypt_box, text="Odszyfruj", command=decrypt, bg="#FF8C42", fg="#1A1A1A", font=("Arial", 12, "bold"), relief="flat", padx=10)
decrypt_btn.grid(row=2, column=0, columnspan=2, pady=10)

decrypt_response = tk.Label(decrypt_box, text="", bg="#1A1A1A", fg="#80FF80", font=("Arial", 12))
decrypt_response.grid(row=3, column=0, columnspan=2)

#ODPALA APLIKACJE
root.mainloop()
