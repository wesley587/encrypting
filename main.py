from cryptography.fernet import Fernet
import os
import argparse
import subprocess
from datetime import datetime
from json import dumps

arguments = argparse.ArgumentParser()
arguments.add_argument('-r --read -R - Read', action='store', dest='read', help='''
                       Read an encrypted message, you can pass the path to file or not, if not pass the path the script will read is data.txt file''',
                       const=True,
                       nargs='?',
                       default=False)
arguments.add_argument('-w --write -W --Write', dest='message', action='store', help='''
                       write a message encrypt''', required=False)
arguments.add_argument('-i --interactive', dest='interactive', default=False, const=True, nargs='?',
                       help='Interactie mode')
arguments.add_argument('-s --save', dest='save', default=False, help='Save the stdout in a file', const=True, nargs='?')
arguments.add_argument('-p --path', dest='path', help='Inform the path to save the file', action='store', default=False)
arguments.add_argument('-nk --numkeys', dest='numkeys', help='Show all keys on keys folder', const=True, nargs='?', default=False)
arguments.add_argument('-g --generatekey', dest='new_key', nargs='?', const=True, help='Generate new key value')
arguments.add_argument('-k --key', default='secret.key', dest='key', help='Ke that project will use..')
arguments.add_argument('-e --exist', default=False, dest='exist', help='Encrypt using a exist file', nargs='?', const=True)
arguments.add_argument('-f --folder', default=False, dest='folder', help='Used to emcrypt a folder')


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
            print('Inalid arguments')
            exit(0)
    
    def generate_folders(self):
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
        try:
            os.mkdir('cache')
        except:
            pass
    
    def generate_cache(self):
        data = dumps(self.control)
        with open(f'cache/{self.date}.json', 'w') as file:
            file.write(data)
        
    def generate_dict(self, parse):
        values_dict = dict()
        if parse.interactive:
            
            action = str(input('Action read or write? [w/r/n/g/e/f] ')).lower().strip()[0]
            self.exist = False
            self.folder = False
            if action == 'r':
                values_dict['action'] = 'read'
                self.write = False
                values_dict['path_to_read'] = str(input('Path: '))
                values_dict['save_output'] = True if str(input('Save the output? [y/n]')).lower().strip()[0] == 'y'  else False
                if values_dict['save_output']:
                    path = str(input('Path to save: [path/default]'))
                    if path.lower().strip() == 'default':    
                        values_dict['path_to_save'] = f'decrypt_folder/{self.date}.txt' 
                    else:
                        values_dict['path_to_save'] = path
            elif action == 'w': 
                values_dict['action'] = 'write'
                self.reading = False
                values_dict['content'] = str(input('Message: '))
                values_dict['save_output'] = True if str(input('save in a expecify path or not? [y/n]')).lower().strip()[0] == 'y'  else False
                if values_dict['save_output']:
                    values_dict['path_to_save'] = str(input('Path to save file, you can pass '))
                else:
                    values_dict['path_to_save'] = 'encrypt_folder/encrypt_data.txt'
            elif action == 'n':
                self.infokes()
                exit(0)
            elif action == 'g':
                self.generate_key()
                exit(0)
            elif action == 'e':
                values_dict['action'] = 'existing file'
                values_dict['path_to_read'] = values_dict['path_to_save'] = str(input('File path: '))
            elif action == 'f':
                values_dict['action'] = 'folder'
                self.exist = False
                values_dict['folder_path'] = str(input('folder path: '))
                action = str(input('Encripty ou decripty? [e/d] ')).lower().strip()[0]
                if action == 'd':
                    values_dict['folder_action'] = 'decrypt'
                    values_dict['save_output'] = True
                elif action == 'e':
                    values_dict['folder_action'] = 'encrypt'
                else:
                    print('error')
                    exit(0)
            else:
                print('Invalid action')
                exit(0)
            if values_dict['action'] == 'write' or values_dict['action'] == 'read' or values_dict['action'] == 'folder' or values_dict['action'] == 'existing file':
                keys = self.infokes(storage=True)
                key = str(input('Key num:'))
                values_dict['key'] = {'default': v for k, v in keys.items() if k == key}['default'] 
        else:            
            if parse.numkeys or parse.new_key:
                if parse.numkeys:
                    self.infokes()
                if parse.new_key:
                    self.generate_key()
                exit(0)
            elif parse.folder:
                values_dict['action'] = 'folder'
                if parse.folder.lower() == 'e' or parse.folder.lower() == 'encrypt':
                    values_dict['folder_action'] = 'encrypt' 
                elif parse.folder.lower() == 'd' or parse.folder.lower() == 'decrypt':
                    values_dict['folder_action'] = 'decrypt'
                    values_dict['save_output'] = True
                values_dict['folder_path'] = values_dict['path_to_read'] = parse.path
            elif parse.exist:
                values_dict['action'] = 'existing file'
                values_dict['path_to_read'] = values_dict['path_to_save'] = parse.path
            elif parse.message:
                values_dict['action'] = 'write'
                values_dict['content'] = parse.message
                values_dict['save_output'] = True if parse.save else False
                values_dict['path_to_save'] = parse.path if parse.path else 'encrypt_folder/encrypt_data.txt'        
            elif parse.read:
                values_dict['action'] = 'read'
                values_dict['path_to_read'] = 'default' if parse.read else parse.read

            if parse.save:
                values_dict['save_output'] = True
                if values_dict['path_to_read'] == 'encrypt_data.txt':
                    values_dict['path_to_save'] = 'decrypt_folder/decrypt_file.txt'
                else:
                    values_dict['path_to_save'] = parse.path
            elif not parse.save:
                values_dict['save_output'] = False
            if values_dict['action'] == 'write' or values_dict['action'] == 'read' or values_dict['action'] == 'folder' or values_dict['action'] == 'existing file':
                keys = self.infokes(show=False, storage=True)
                values_dict['key'] = {'default': v for k, v in keys.items() if k == parse.key}['default'] if parse.key != 'secret.key' else parse.key
                values_dict['path_to_read'] = parse.path if parse.path else 'encrypt_data.txt'
            
            
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
        with open(self.control['path_to_save'], 'wb') as file:
            encrypt_data = secret.encrypt(self.control['content'].encode())
            file.write(encrypt_data)
        with open(f'encrypt_folder/{self.date}' if not path else f'encrypt_folder/{path}/{self.date}', 'wb') as file:
            file.write(encrypt_data)

    
    def decrypt_msg(self, path=False):
        if self.control['path_to_read'] == 'default':
            file = 'encrypt_folder/encrypt_data.txt'
        else:
            file = self.control['path_to_read']
        with open(file, 'rb') as file:
            secret = self.reading_secret()
            decrypt_data = secret.decrypt(file.read())
        if self.control['save_output']:
            with open(self.control['path_to_save'], 'wb') as file:
                file.write(decrypt_data)
            with open(f'decrypt_folder/{self.date}' if not path else f'decrypt_folder/{path}/{self.date}', 'wb') as file:
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

    def encrypt_file(self, path=False):
        if self.control['path_to_read']:
            with open(self.control['path_to_read'], 'r') as file:
                self.control['content'] = file.read()
            self.encrypt_msg() if not path else self.encrypt_msg(path)
            
        else:
            print('Pass the -p parram to inform the path of file')
    
    def encrypt_folders(self):
        folder = self.control['folder_path'][self.control['folder_path'].rfind('/'):]
        for root, folders, files in os.walk(self.control['folder_path']):
            for file in files:
                self.control['path_to_read'] = self.control['path_to_save'] = f'{root}/{file}'
                if self.control['folder_action'] == 'encrypt':
                    try:
                        os.mkdir(f'encrypt_folder/{root[root.find(folder):]}')
                    except:
                        pass
                    self.date = datetime.now().strftime('%d-%m-%y %H:%M:%S:%f')
                    self.encrypt_file(path=root[root.find(folder):])
                elif self.control['folder_action'] == 'decrypt':
                    try:
                        os.mkdir(f'decrypt_folder/{root[root.find(folder):]}')
                    except:
                        pass
                    self.read = f'{root}/{file}'
                    self.decrypt_msg(path=root[root.find(folder):])
                
if __name__ == '__main__':
    start = crypt_and_decrypt()
    start.main()
