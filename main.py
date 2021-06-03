from cryptography.fernet import Fernet
import os
import argparse
import subprocess
from datetime import datetime
from json import dumps
from colorama import Back, Fore, Style


arguments = argparse.ArgumentParser()
arguments.add_argument('-r --read -R - Read', action='store', dest='read', help='''
                       Read an encrypted file, it is possible to pass the path a file''', const=True, nargs='?', default=False)

arguments.add_argument('-w --write -W --Write', dest='message', action='store', help='Write a message encrypt, pass the content', required=False)

arguments.add_argument('-i --interactive', dest='interactive', default=False, const=True, nargs='?', help='Interactie mode')

arguments.add_argument('-s --save', dest='save', default=False, help='Save the stdout in a file', const=True, nargs='?')

arguments.add_argument('-p --path', dest='path', help='Inform the path to do something', const=True, nargs='?', default=False)

arguments.add_argument('-g --generatekey', dest='new_key', nargs='?', const=True, help='Generate new key value')

arguments.add_argument('-k --key', default='secret.key', dest='key', help='Key that will be used in the process')

arguments.add_argument('-n --numkeys', dest='numkeys', help='Show all keys on keys folder', const=True, nargs='?', default=False)

arguments.add_argument('-e --exist', default=False, dest='exist', help='Encrypt using a exist file', nargs='?', const=True)

arguments.add_argument('-f --folder', default=False, dest='folder', help='Used to encrypt or decrypt a folder')


class crypt_and_decrypt:
    def __init__(self):
        self.date = datetime.now().strftime('%d-%m-%y %H:%M:%S')
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
            print(Fore.RED + 'Error, invalid arguments' + Style.RESET_ALL)
            exit(0)
    
    def generate_folders(self):
        msg = Fore.GREEN + '[*]' + Style.RESET_ALL
        
        try:
            os.mkdir('decrypt_folder')
            print(msg, 'Created folder: decrypt_folder')
        except:
            pass
        
        try:
            os.mkdir('keys')
            print(msg, 'Created folder: keys')
        except:
            pass
        
        try:
            os.mkdir('encrypt_folder')
            print(msg, 'Created folder: keys')
        except:
            pass
        
        try:
            os.mkdir('cache')
            print(msg, 'Created folder: cache')
        except:
            pass
    
    def generate_cache(self):
        data = dumps(self.control)
        with open(f'cache/{self.date}.json', 'w') as file:
            file.write(data)
        print(f'[{Fore.GREEN + "*" + Style.RESET_ALL}] Salving cache...')
        
    def generate_dict(self, parse):
        values_dict = dict()
        
        if parse.interactive:
            print('   ----- Actions -----')
            print(f'[{Fore.LIGHTGREEN_EX + "w" + Style.RESET_ALL}] = write \n[{Fore.LIGHTGREEN_EX + "r" + Style.RESET_ALL}] = read \n[{Fore.LIGHTGREEN_EX + "n" + Style.RESET_ALL}] = view the keys \n[{Fore.LIGHTGREEN_EX + "g" + Style.RESET_ALL}] = generate a new key \n[{Fore.LIGHTGREEN_EX + "e" + Style.RESET_ALL}] = encrypt an existing file \n[{Fore.LIGHTGREEN_EX + "f" + Style.RESET_ALL}] = folder')
            
            action = str(input('What do you want to do? ')).lower().strip()[0]
            if action == 'r':
                print('   ---- Reading mode ----')
                values_dict['action'] = 'read'
                print(f'[{Fore.LIGHTGREEN_EX + "default" + Style.RESET_ALL}] = encrypt_folder/encrypt_data.txt')
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
                self.infokes()
                exit(0)
            elif action == 'g':
                values_dict['action'] = 'Generate key'
                print(Fore.GREEN + 'Generating new Key')
                self.generate_key()
                print('Success in creationg key' + Style.RESET_ALL)
            elif action == 'e':
                print('  ----- Existe file mode -----')
                values_dict['action'] = 'existing file'
                values_dict['path_to_read'] = values_dict['path_to_save'] = str(input('File path: '))
            elif action == 'f':
                print('  ----- Folder mode -----')
                values_dict['action'] = 'folder'
                self.exist = False
                values_dict['folder_path'] = str(input('folder path: '))
                print(f'[{Fore.LIGHTGREEN_EX + "e" + Style.RESET_ALL}] = Encrypt \n[{Fore.LIGHTGREEN_EX + "d" + Style.RESET_ALL}] = Decrypt')
                action = str(input('Encripty ou decripty? [e/d] ')).lower().strip()[0]
                if action == 'd':
                    values_dict['folder_action'] = 'decrypt'
                    values_dict['save_output'] = True
                elif action == 'e':
                    values_dict['folder_action'] = 'encrypt'
                else:
                    print(Fore.RED + 'ERROR, INVALID ACTION...' + Style.RESET_ALL)
                    exit(0)
            else:
                print(Fore.RED + 'ERROR, INVALID ACTION...' + Style.RESET_ALL)
                exit(0)
            if values_dict['action'] == 'write' or values_dict['action'] == 'read' or values_dict['action'] == 'folder' or values_dict['action'] == 'existing file':
                keys = self.infokes(storage=True)
                key = str(input('Key that will be used in the action: '))
                values_dict['key'] = {'default': v for k, v in keys.items() if k == key}['default'] 
        else:            
            if parse.numkeys or parse.new_key:
                if parse.numkeys:
                    values_dict['action'] = 'View keys'
                    self.infokes()
        
                if parse.new_key:
                    values_dict['action'] = 'Generate key'
                    print(f'[{Fore.GREEN + "*" + Style.RESET_ALL}] Generating new Key')
                    self.generate_key()
                    print('Success in creationg key')
        
            elif parse.folder:
                values_dict['action'] = 'folder'
                if parse.folder.lower() == 'e' or parse.folder.lower() == 'encrypt':
                    values_dict['folder_action'] = 'encrypt' 
                    print(f'[{Fore.GREEN + "*" + Style.RESET_ALL}] Encrypting folder')
                elif parse.folder.lower() == 'd' or parse.folder.lower() == 'decrypt':
                    values_dict['folder_action'] = 'decrypt'
                    values_dict['save_output'] = True            
                    print(f'[{Fore.GREEN + "*" + Style.RESET_ALL}] Decrypting folder')

                values_dict['folder_path'] = values_dict['path_to_read'] = parse.path
                
        
            elif parse.exist:
                values_dict['action'] = 'existing file'
                values_dict['path_to_read'] = values_dict['path_to_save'] = parse.path
                print(f'[{Fore.GREEN + "*" + Style.RESET_ALL}] Encrypting file')

                
            elif parse.message:
                print(f'[{Fore.GREEN + "*" + Style.RESET_ALL}] Encrypting message')
                values_dict['action'] = 'write'
                values_dict['content'] = parse.message
                values_dict['save_output'] = True if parse.save else False
                values_dict['path_to_save'] = parse.path if parse.path else 'encrypt_folder/encrypt_data.txt'


            elif parse.read:
                values_dict['action'] = 'read'
                values_dict['path_to_read'] = 'default' if parse.read else parse.read
                print(f'[{Fore.GREEN + "*" + Style.RESET_ALL}] Reading encrypting message')


            if parse.save:
                values_dict['save_output'] = True
                if values_dict['path_to_read'] == 'encrypt_data.txt':
                    values_dict['path_to_save'] = 'decrypt_folder/decrypt_file.txt'

                else:
                    values_dict['path_to_save'] = parse.path
                print(f'Save the file on : {Fore.LIGHTCYAN_EX + values_dict["path_to_save"] + Style.RESET_ALL}')

                    
            elif not parse.save:
                values_dict['save_output'] = False
            if values_dict['action'] == 'write' or values_dict['action'] == 'read' or values_dict['action'] == 'folder' or values_dict['action'] == 'existing file':
                keys = self.infokes(show=False, storage=True)
                values_dict['key'] = {'default': v for k, v in keys.items() if k == parse.key}['default'] if parse.key != 'secret.key' else parse.key
                print(f'Using key: {Fore.LIGHTGREEN_EX +  values_dict["key"] + Style.RESET_ALL}')
            
            
            
        return values_dict

    def generate_key(self):
        encrypt_key = Fernet.generate_key()            
        with open('keys/secret.key', 'wb') as file:
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
            print('error...')
         
    def reading_secret(self):
        with open(f'keys/{self.control["key"]}', 'rb') as file:
            secret = Fernet(file.read())
        return secret

    def encrypt_msg(self, path=False):      
        secret = self.reading_secret()
        if not path:
            print(f'Salving file on: {Fore.GREEN + self.control["path_to_save"] + Style.RESET_ALL} ')
        else:
            print(f'Salving file on: {Fore.GREEN + f"encrypt_folder/{path}" + Style.RESET_ALL} ')
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
        print(f'Reading the file on : {Fore.LIGHTCYAN_EX + file_to_read + Style.RESET_ALL}')

        with open(file_to_read, 'rb') as file:
            secret = self.reading_secret()
            decrypt_data = secret.decrypt(file.read())
        if self.control['save_output']:
            print(f'Salving file: {Fore.GREEN + self.control["path_to_save"] + Style.RESET_ALL} ')

            with open(self.control['path_to_save'], 'wb') as file:
                file.write(decrypt_data)
            with open(f'decrypt_folder/{self.date}' if not path else f'decrypt_folder/{path}/{self.date}', 'wb') as file:
                file.write(decrypt_data)            
                
        else:
            print(f'content: {Fore.RED + decrypt_data.decode() + Style.RESET_ALL}')
    
    def infokes(self, show=True, storage=False):
        key_info = dict()
        stdout = subprocess.check_output(['ls', 'keys']).decode().replace('\n', ', ').split(', ')
        if show:
            print(Fore.RED + '     ----- Keys -----' + Style.RESET_ALL)
            print('='*30)
        for x in range(0, len(stdout)):
            if stdout[x]:
                if show:
                    print(f'[{Fore.RED +  str(x) + Style.RESET_ALL}] {stdout[x]}')
                if storage:
                    key_info[str(x)] = stdout[x]
        if show:
            print('='*30)
        return key_info

    def encrypt_file(self, path=False):
        print(f'Reading the file on : {Fore.LIGHTCYAN_EX + self.control["path_to_read"] + Style.RESET_ALL}')
        if self.control['path_to_read']:
            try:
                with open(self.control['path_to_read'], 'r') as file:
                    self.control['content'] = file.read()
            except:
                print(f'{Fore.RED + "ERROR, Impossible encrypt the file: " + Style.RESET_ALL + self.control["path_to_save"]}')

            self.encrypt_msg() if not path else self.encrypt_msg(path)
            
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
                        print(f'Created folder: {Fore.RED}encrypt_folder/{root[root.find(folder):]}{Style.RESET_ALL}')
                    except:
                        pass
                    self.date = datetime.now().strftime('%d-%m-%y %H:%M:%S:%f')
                    self.encrypt_file(path=root[root.find(folder):])
                elif self.control['folder_action'] == 'decrypt':
                    try:
                        os.mkdir(f'decrypt_folder/{root[root.find(folder):]}')
                        print(f'Created folder: {Fore.RED}encrypt_folder/{root[root.find(folder):]}{Style.RESET_ALL}')
                    except:
                        pass
                    self.date = datetime.now().strftime('%d-%m-%y %H:%M:%S:%f')
                    self.read = f'{root}/{file}'
                    self.decrypt_msg(path=root[root.find(folder):])
                
if __name__ == '__main__':
    start = crypt_and_decrypt()
    start.main()
