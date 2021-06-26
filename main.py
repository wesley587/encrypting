import os
import argparse
import subprocess
from datetime import datetime
from json import dumps
from platform import platform

first_execution = True
if first_execution:
    print('[*] Checking if cryptography module exists')
    validation = os.popen('pip3 show cryptography').read()
    if not validation:
        print(f'[info] Installing cryptography module')
        os.system('pip3 install cryptography')
        print(f'[info] Successful installing cryptography module')
    else:
        print(f'[info] Cryptography module already exists')

from cryptography.fernet import Fernet


arguments = argparse.ArgumentParser()
arguments.add_argument('-r --read -R - Read', action='store', dest='read', help='''
                       Read an encrypted file, it is possible to pass the path a file''', const=True, nargs='?', default=False)

arguments.add_argument('-w --write -W --Write', dest='message', action='store', help='Write a message encrypt, pass the content', required=False)

arguments.add_argument('-i --interactive', dest='interactive', default=False, const=True, nargs='?', help='Interactie mode')

arguments.add_argument('-s --save', dest='save', default=False, help='Save the stdout in a file', const=True, nargs='?')

arguments.add_argument('-p --path', dest='path', help='Inform the path to do something', const=True, nargs='?', default=False)

arguments.add_argument('-g --generatekey', dest='new_key', nargs='?', const=True, help='Generate new key value')

arguments.add_argument('-k --key', default='Default.key', dest='key', help='Key that will be used in the process')

arguments.add_argument('-n --numkeys', dest='numkeys', help='Show all keys on keys folder', const=True, nargs='?', default=False)

arguments.add_argument('-e --exist', default=False, dest='exist', help='Encrypt using a exist file', nargs='?', const=True)

arguments.add_argument('-f --folder', default=False, dest='folder', help='Used to encrypt or decrypt a folder use e(encrypt) d(decrypt)')

arguments.add_argument('-h --help', default='''                       ---- Arguments ----
        ================================================
                    -r --read -R - Read     Read an encrypted file, it is possible to pass the path a file
                    -w --write -W --Write   Write a message encrypt, pass the content
                    -i --interactive        Interactie mode
                    -s --save               Save the stdout in a file
                    -p --path               Inform the path to do something
                    -g --generatekey        Generate new key value
                    -k --key                Key that will be used in the process
                    -n --numkeys            Show all keys on keys folder
                    -e --exist              Encrypt using a exist file
                    -f --folder             Used to encrypt or decrypt a folder use e(encrypt) d(decrypt)
                    ''', dest='help', help='help mode')


class crypt_and_decrypt:
    def __init__(self):
        self.date = datetime.now().strftime('%d-%m-%y %H-%M-%S')
        first_execution = True
        if first_execution:
            self.generate_folders()
            
            with open(os.path.basename(__file__), 'r') as file:
                content = file.read()
                
            with open(os.path.basename(__file__), 'w') as file:
                file.write(content.replace('first_execution = True', 'first_execution = False'))
                
            self.generate_key()
            
        parse = arguments.parse_args()
        self.parse_args(parse)
        self.control = self.generate_dict(parse) 
        self.generate_cache() 
    
    def parse_args(self, parse):
        if parse.message and parse.read or parse.interactive and parse.message or parse.interactive and parse.read or parse.numkeys and parse.message or parse.numkeys and parse.interactive:
            print('[Error] Error, invalid arguments')
            exit(0)
        if not parse.message and not parse.read and not parse.interactive  and not parse.numkeys and not parse.exist and not parse.new_key:
            print('[Error] Error, invalid arguments')
            print(parse.help)
            exit(0)

    
    def generate_folders(self):
        try:
            os.mkdir('decrypt_folder')
            print('[*] Created folder: decrypt_folder')
        except:
            pass
        
        try:
            os.mkdir('keys')
            print('[*] Created folder: keys')
        except:
            pass
        
        try:
            os.mkdir('encrypt_folder')
            print('[*] Created folder: keys')
        except:
            pass
        
        try:
            os.mkdir('cache')
            print('[*] Created folder: cache')
        except:
            pass
    
    def generate_cache(self):
        data = dumps(self.control)
        with open(f'cache/{self.date}.json', 'w') as file:
            file.write(data)
        print(f'[*] Salving cache...')
        
    def generate_dict(self, parse):
        values_dict = dict()
        
        if parse.interactive:
            print('   ----- Actions -----')
            print(f'[w] = write \n[r] = read \n[n] = view the keys \n[g] = generate a new key \n[e] = encrypt an existing file \n[f] = folder')
            
            action = str(input('What do you want to do? ')).lower().strip()[0]
            if action == 'r':
                print('   ---- Reading mode ----')
                values_dict['action'] = 'read'
                print(f'[default] = encrypt_folder/encrypt_data.txt')
                values_dict['path_to_read'] = str(input('Path to read the file: '))
                values_dict['save_output'] = True if str(input('Save the output? [y/n] ')).lower().strip()[0] == 'y'  else False
                
                if values_dict['save_output']:
                    path = str(input('Path to save: [path/default]'))
                    
                    if path.lower().strip() == 'default':    
                        values_dict['path_to_save'] = f'decrypt_folder/{self.date}.txt' 
                    else:
                        values_dict['path_to_save'] = path
                        
            elif action == 'w': 
                print('   ---- Write mode ----')
                values_dict['action'] = 'write'
                self.reading = False
                values_dict['content'] = str(input('message you want to encrypt: '))
                values_dict['save_output'] = True if str(input('save in a expecify path? [y/n]')).lower().strip()[0] == 'y'  else False
                
                if values_dict['save_output']:
                    values_dict['path_to_save'] = str(input('Path to save file, you can pass '))
                else:
                    values_dict['path_to_save'] = 'encrypt_folder/encrypt_data.txt'
                    
            elif action == 'n':
                self.infokeys()
                exit(0)
            elif action == 'g':
                values_dict['action'] = 'Generate key'
                print('Generating new Key')
                self.generate_key()
                print('Success in key creation')
            elif action == 'e':
                print('  ----- Existe file mode -----')
                values_dict['action'] = 'existing file'
                values_dict['path_to_read'] = values_dict['path_to_save'] = str(input('File path: '))
            elif action == 'f':
                print('  ----- Folder mode -----')
                values_dict['action'] = 'folder'
                self.exist = False
                values_dict['folder_path'] = str(input('folder path: '))
                print(f'[e] = Encrypt \n[d] = Decrypt')
                action = str(input('Encripty ou decripty? [e/d] ')).lower().strip()[0]
                if action == 'd':
                    values_dict['folder_action'] = 'decrypt'
                    values_dict['save_output'] = True
                elif action == 'e':
                    values_dict['folder_action'] = 'encrypt'
                else:
                    print('[Error] ERROR, INVALID ACTION...')
                    exit(0)
            else:
                print('[Error] ERROR, INVALID ACTION...')
                exit(0)
            if values_dict['action'] == 'write' or values_dict['action'] == 'read' or values_dict['action'] == 'folder' or values_dict['action'] == 'existing file':
                keys = self.infokeys(storage=True)
                key = str(input('Key that will be used in the action: '))
                values_dict['key'] = {'default': v for k, v in keys.items() if k == key}['default'] 
        else:            
            if parse.numkeys or parse.new_key:
                if parse.numkeys:
                    values_dict['action'] = 'View keys'
                    self.infokeys()
        
                if parse.new_key:
                    values_dict['action'] = 'Generate key'
                    print(f'[*] Generating new Key')
                    self.generate_key()
                    print('[Info] Success in creationg key')
        
            elif parse.folder:
                values_dict['action'] = 'folder'
                if parse.folder.lower() == 'e' or parse.folder.lower() == 'encrypt':
                    values_dict['folder_action'] = 'encrypt' 
                    print(f'[*] Encrypting folder')
                elif parse.folder.lower() == 'd' or parse.folder.lower() == 'decrypt':
                    values_dict['folder_action'] = 'decrypt'
                    values_dict['save_output'] = True            
                    print(f'[*] Decrypting folder')

                values_dict['folder_path'] = values_dict['path_to_read'] = parse.path
                
        
            elif parse.exist:
                values_dict['action'] = 'existing file'
                values_dict['path_to_read'] = values_dict['path_to_save'] = parse.path
                print(f'[*] Encrypting file')

                
            elif parse.message:
                print(f'[*] Encrypting message')
                values_dict['action'] = 'write'
                values_dict['content'] = parse.message
                values_dict['save_output'] = True if parse.save else False
                values_dict['path_to_save'] = parse.path if parse.path else 'encrypt_folder/encrypt_data.txt'


            elif parse.read:
                values_dict['action'] = 'read'
                values_dict['path_to_read'] = 'default' if parse.read else parse.read
                print(f'[*] Reading encrypting message')


            if parse.save:
                values_dict['save_output'] = True
                if values_dict['path_to_read'] == 'encrypt_data.txt':
                    values_dict['path_to_save'] = 'decrypt_folder/decrypt_file.txt'

                else:
                    values_dict['path_to_save'] = parse.path
                print(f'[Info] Save the file on : {values_dict["path_to_save"]}')

                    
            elif not parse.save:
                values_dict['save_output'] = False
            if values_dict['action'] == 'write' or values_dict['action'] == 'read' or values_dict['action'] == 'folder' or values_dict['action'] == 'existing file':
                keys = self.infokeys(show=False, storage=True)
                values_dict['key'] = {'default': v for k, v in keys.items() if k == parse.key}['default'] if parse.key != 'Default.key' else parse.key
                print(f'[Info] Using key: {values_dict["key"]}')
            
            
            
        return values_dict

    def generate_key(self):
        encrypt_key = Fernet.generate_key()            
        with open('keys/Default.key', 'wb') as file:
            file.write(encrypt_key)
        with open(f'keys/{self.date}.key', 'wb') as file:
            file.write(encrypt_key)
        

    def main(self):
        if self.control['action']:
            if self.control['action'] == 'existing file':
                self.encrypt_file(path=False)
            if self.control['action'] == 'folder':
                self.encrypt_folders()
            if self.control['action'] == 'write':
                self.encrypt_msg()    
            elif self.control['action'] == 'read':
                self.decrypt_msg()
        else:
            print('[Error] error...')
         
    def reading_secret(self):
        with open(f'keys/{self.control["key"]}', 'rb') as file:
            secret = Fernet(file.read())
        return secret

    def encrypt_msg(self, path=False):      
        secret = self.reading_secret()
        if not path:
            print(f'[Info] Salving file on: {self.control["path_to_save"]} ')
        else:
            print(f'[Info] Salving file on: encrypt_folder/{path}')
        with open(self.control['path_to_save'], 'wb') as file:
            encrypt_data = secret.encrypt(self.control['content'].encode())
            file.write(encrypt_data)
        with open(f'encrypt_folder/{self.date}' if not path else f'encrypt_folder/{path}/{self.date}', 'wb') as file:
            file.write(encrypt_data)
       

    
    def decrypt_msg(self, path=False):
        if self.control['path_to_read'] == 'default':
            file_to_read = 'encrypt_folder/encrypt_data.txt'
        else:
            file_to_read = self.control['path_to_read']
        print(f'[Info] Reading the file on : {file_to_read}')
        try:
            with open(file_to_read, 'rb') as file:
                secret = self.reading_secret()
                decrypt_data = secret.decrypt(file.read())
            if self.control['save_output']:
                print(f'[Info] Salving file: {self.control["path_to_save"]} ')

                with open(self.control['path_to_save'], 'wb') as file:
                    file.write(decrypt_data)
                with open(f'decrypt_folder/{self.date}' if not path else f'decrypt_folder/{path}/{self.date}', 'wb') as file:
                    file.write(decrypt_data)
        except:
            print(f'[Error] ERROR, Impossible encrypt the file: {self.control["path_to_save"]}')

                
        else:
            print(f'[Content] content: {decrypt_data.decode()}\n')
    
    def infokeys(self, show=True, storage=False):
        key_info = dict()
        stdout = os.listdir('keys')
        if show:
            print('     ----- Keys -----')
            print('='*30)
        for x in range(0, len(stdout)):
            if stdout[x]:
                if show:
                    print(f'[{x}] {stdout[x]}')
                if storage:
                    key_info[str(x)] = stdout[x]
        if show:
            print('='*30)
        return key_info

    def encrypt_file(self, path=False):
        print(f'Reading the file on : {self.control["path_to_read"]}')
        if self.control['path_to_read']:
            try:
                with open(self.control['path_to_read'], 'r') as file:
                    self.control['content'] = file.read()
                    self.encrypt_msg() if not path else self.encrypt_msg(path)
            except:
                print(f'[Error] ERROR, Impossible encrypt the file: {self.control["path_to_save"]}')

            
            
        else:
            print('Pass the -p parram to inform the path of file')
    
    def encrypt_folders(self):
        print(f'     ---- Folder actions ----')
        print('='*35)
        folder = self.control['folder_path'][self.control['folder_path'].rfind('/'):]
        for root, folders, files in os.walk(self.control['folder_path']):
            for file in files:
                self.control['path_to_read'] = self.control['path_to_save'] = f'{root}/{file}'
                if self.control['folder_action'] == 'encrypt':
                    try:
                        os.mkdir(f'encrypt_folder/{root[root.find(folder):]}')
                        print(f'[info] Created folder: encrypt_folder/{root[root.find(folder):]}')
                    except:
                        pass
                    self.date = datetime.now().strftime('%d-%m-%y %H-%M-%S-%f')
                    self.encrypt_file(path=root[root.find(folder):])
                elif self.control['folder_action'] == 'decrypt':
                    try:
                        os.mkdir(f'decrypt_folder/{root[root.find(folder):]}')
                        print(f'[Info] Created folder: encrypt_folder/{root[root.find(folder):]}')
                    except:
                        pass
                    self.date = datetime.now().strftime('%d-%m-%y %H-%M-%S-%f')
                    self.read = f'{root}/{file}'
                    self.decrypt_msg(path=root[root.find(folder):])
                
if __name__ == '__main__':
    start = crypt_and_decrypt()
    start.main()
