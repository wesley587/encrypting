from cryptography.fernet import Fernet
import os
import argparse

arguments = argparse.ArgumentParser()
arguments.add_argument('-r --read -R - Read', action='store', dest='read', help='''
                       Read an encrypted message, you can pass the path to file or not, if not pass the path the script will read is data.txt file''',
                       const='',
                       nargs='?',
                       default=False)
arguments.add_argument('-w --write -W --Write', dest='message', action='store', help='''
                       write a message encrypt''', required=False)
arguments.add_argument('-i --interactive', dest='interactive', default=False, const='', nargs='?',
                       help='Interactie mode')

class crypt_end_decrypt:
    def __init__(self):
        parse = arguments.parse_args()
        
        if parse.interactive or parse.interactive == '' or parse.interactive == ' ':
            action = str(input('Action read or write? [w/r] ')).lower().strip()
            if action == 'r' or action == 'read':
                self.write = False
                self.read = str(input('Path: '))
            elif action == 'w' or action == 'write':
                self.reading = False
                self.write = str(input('Message: '))
            else:
                print('Invalid action')
                exit(0)
        else:
            self.write = parse.message if parse.message else False
            self.read = False if parse.read == '' else parse.read

    def generate_key(self):
        encrypt_key = Fernet.generate_key()            
        with open('secret.key', 'wb') as file:
            file.write(encrypt_key)
        

    def main(self):
        first_execution = True
        if first_execution:
            with open(os.path.basename(__file__), 'r') as file:
                content = file.read()
                
            with open(os.path.basename(__file__), 'w') as file:
                file.write(content.replace('first_execution = True', 'first_execution = False'))

            self.generate_key()
        self.encrypt_msg() if self.write else self.decrypt_msg()
         
    def reading_secret(self):
        with open('secret.key', 'rb') as file:
            secret = Fernet(file.read())
        return secret

    def encrypt_msg(self):
        secret = self.reading_secret()
        with open('encrypt_data.txt', 'wb') as file:
            encrypt_data = secret.encrypt(self.write.encode())
            file.write(encrypt_data)
    
    def decrypt_msg(self):
        if not self.read:
            path = 'encrypt_data.txt'
        else:
            path = self.read
        with open(path, 'rb') as file:
            secret = self.reading_secret()
            decrypt_data = secret.decrypt(file.read())
            print(decrypt_data.decode())
            
if __name__ == "__main__":
    start = crypt_end_decrypt()
    start.main()
