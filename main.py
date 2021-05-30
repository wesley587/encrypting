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
arguments.add_argument('-s --save', dest='save', default=False, help='Save the stdout in a file', const='', nargs='?')
arguments.add_argument('-p --path', dest='path', help='Inform the path to save the file')

try:
    os.mkdir('decrypt')
except:
    pass
try:
    os.mkdir('keys')
except:
    pass

class crypt_end_decrypt:
    def __init__(self):
        parse = arguments.parse_args()
        
        if parse.interactive or parse.interactive == '' or parse.interactive == ' ':
            action = str(input('Action read or write? [w/r] ')).lower().strip()
            if action == 'r' or action == 'read':
                self.write = False
                self.read = str(input('Path: '))
                self.save = True if str(input('Save the output? [y/n]')) == 'y' else False
                if self.save:
                    path = str(input('Path to save: [path/default]'))
                    if path.lower().strip() == 'default':    
                        self.path = 'decrypt/decrypt_file.txt' 
                    else:
                        self.path = path
            elif action == 'w' or action == 'write':
                self.reading = False
                self.write = str(input('Message: '))
                validation = str(input('save in a expecify path or not? [y/n]')).lower().strip()[0]
                if validation == 'y' or validation == 'n':
                    if validation == 'y':
                        self.path = str(input('Path to save file, you can pass '))
                    else:
                        self.path = 'encrypt_data.txt'
                else:
                    print('Invalid action')
                    exit(0)
            else:
                print('Invalid action')
                exit(0)
        else:
            self.path = parse.path if parse.path else 'encrypt_data.txt'
            self.write = parse.message if parse.message else False
            self.read = False if parse.read == '' else parse.read
            if parse.save == '' or parse.save:
                self.save = True
                if self.path == 'encrypt_data.txt':
                    self.path = 'decrypt/decrypt_file.txt'
                else:
                    self.path = parse.save
            else:
                self.save = False


    def generate_key(self):
        encrypt_key = Fernet.generate_key()            
        with open('keys/secret.key', 'wb') as file:
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
        with open('keys/secret.key', 'rb') as file:
            secret = Fernet(file.read())
        return secret

    def encrypt_msg(self):
        secret = self.reading_secret()
        print(self.path)
        with open(self.path, 'wb') as file:
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
        if self.save:
            with open(self.path, 'wb') as file:
                file.write(decrypt_data)
        else:
            print(decrypt_data.decode())
            
if __name__ == '__main__':
    start = crypt_end_decrypt()
    start.main()
