from cryptography.fernet import Fernet
import os
import argparse
import subprocess
from datetime import datetime

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
arguments.add_argument('-nk --numkeys', dest='numkeys', help='Show all keys on keys folder', const='', nargs='?', default=False)
arguments.add_argument('-g --generatekey', dest='new_key', nargs='?', const='', help='Generate new key value')
arguments.add_argument('-k --key', default='secret.key', dest='key', help='Ke that project will use..')
arguments.add_argument('-e --exist', default=False, dest='exist', help='Encrypt using a exist file', nargs='?', const=True)
class crypt_end_decrypt:
    def __init__(self):
        parse = arguments.parse_args()
        self.date = datetime.now().strftime('%d-%m-%y %H:%M:%S.key')

        if parse.interactive or parse.interactive == '' or parse.interactive == ' ':
            self.exist = False
            action = str(input('Action read or write? [w/r/nk/g/e] ')).lower().strip()
            if action == 'r' or action == 'read':
                keys = self.infokes(storage=True)
                key = str(input('Key num:'))
                self.num_key = {'default': v for k, v in keys.items() if k == key}['default'] 
                self.write = False
                self.read = str(input('Path: '))
                self.save = True if str(input('Save the output? [y/n]')) == 'y'  else False
                if self.save:
                    path = str(input('Path to save: [path/default]'))
                    if path.lower().strip() == 'default':    
                        self.path = 'decrypt_folder/decrypt_file.txt' 
                    else:
                        self.path = path
            elif action == 'w' or action == 'write':
                keys = self.infokes(storage=True)
                key = str(input('Key num:'))
                self.num_key = {'default': v for k, v in keys.items() if k == key}['default'] 
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
            elif action == 'nk' or action == 'numkeys':
                self.infokes()
                exit(0)
            elif action == 'g' or action == 'generatekey':
                self.generate_key()
                exit(0)
            else:
                print('Invalid action')
                exit(0)
        else:
            if parse.numkeys == '' or parse.numkeys or parse.new_key == '' or parse.new_key:
                if parse.numkeys == '' or parse.numkeys:
                    self.infokes()
                elif parse.new_key == '' or parse.new_key:
                    self.generate_key()
                exit(0)
            self.exist = True if parse.exist == '' or parse.exist else False
            keys = self.infokes(show=False, storage=True)
            self.num_key = {'default': v for k, v in keys.items() if k == parse.key}['default'] if parse.key != 'secret.key' else parse.key
            print(self.num_key)
            self.path = parse.path if parse.path else 'encrypt_data.txt'
            self.write = parse.message if parse.message else False
            self.read = 'default' if parse.read == '' else parse.read
            if parse.save == '' or parse.save:
                self.save = True
                if self.path == 'encrypt_data.txt':
                    self.path = 'decrypt_folder/decrypt_file.txt'
                else:
                    self.path = parse.save
            else:
                self.save = False


    def generate_key(self):
        encrypt_key = Fernet.generate_key()            
        with open('keys/secret.key', 'wb') as file:
            file.write(encrypt_key)
        with open(f'keys/{self.date}', 'wb') as file:
            file.write(encrypt_key)
        

    def main(self):
        first_execution = True
        if first_execution:
            try:
                os.mkdir('decrypt_folder')
            except:
                pass
            try:
                os.mkdir('keys')
            except:
                pass
            try:
                os.mkdir('encrypt_folder')
            except:
                pass
            with open(os.path.basename(__file__), 'r') as file:
                content = file.read()
                
            with open(os.path.basename(__file__), 'w') as file:
                file.write(content.replace('first_execution = True', 'first_execution = False'))

            self.generate_key()
        if self.exist:
            self.encrypt_file()
        elif self.write:
            self.encrypt_msg()    
        elif self.read:
            self.decrypt_msg()
         
    def reading_secret(self):
        with open(f'keys/{self.num_key}', 'rb') as file:
            secret = Fernet(file.read())
        return secret

    def encrypt_msg(self, path=False):
        secret = self.reading_secret()
        print(self.path)
        with open(f'encrypt_folder/{self.path}' if not path else self.path, 'wb') as file:
            encrypt_data = secret.encrypt(self.write.encode())
            file.write(encrypt_data)
        with open(f'encrypt_folder/{self.date}', 'wb') as file:
            file.write(encrypt_data)

    
    def decrypt_msg(self):
        if self.read == 'default':
            path = 'encrypt_folder/encrypt_data.txt'
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
    
    def infokes(self, show=True, storage=False):
        key_info = dict()
        stdout = subprocess.check_output(['ls', 'keys']).decode().replace('\n', ', ').split(', ')
        for x in range(0, len(stdout)):
            if stdout[x]:
                if show:
                    print(f'[{x}] {stdout[x]}')
                if storage:
                    key_info[str(x)] = stdout[x]
        return key_info

    def encrypt_file(self):
        if self.path:
            with open(self.path, 'r') as file:
                self.write = file.read()
            self.encrypt_msg(path=True)
        else:
            print('Pass the -p parram to inform the path of file')

if __name__ == '__main__':
    start = crypt_end_decrypt()
    start.main()
