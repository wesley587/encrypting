def __init__(self):
    self.dict = self.generate_dict()
    
    
def generate_dict():
    values_dict = dict()
    values_dict['date'] = datetime.now().strftime('%d-%m-%y %H:%M:%S.key')
    parse = arguments.parse_args()
    keys = self.infokes(storage=True)
    key = str(input('Key num:'))
    values_dict['key'] = {'default': v for k, v in keys.items() if k == key}['default'] 
    if parse.interactive():
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
                    values_dict['path_to_save'] = f'decrypt_folder/{values_dict["date"]}.txt' 
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
                values_dict['path_to_save'] = 'encrypt_data.txt'
        elif action == 'nk' or action == 'numkeys':
            self.infokes()
            exit(0)
        elif action == 'g':
            self.generate_key()
            exit(0)
        elif action == 'e':
            values_dict['action'] = 'existing file'
            values_dict['path_to_read'] = str(input('File path: '))
        elif action == 'f' or action == 'folder':
            values_dict['action'] = 'folder'
            self.exist = False
            values_dict['path_folder'] = str(input('folder path: '))
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
    else:
        keys = self.infokes(show=False, storage=True)
        values_dict['key'] = {'default': v for k, v in keys.items() if k == parse.key}['default'] if parse.key != 'secret.key' else parse.key
        values_dict['path_to_read'] = parse.path if parse.path else 'encrypt_data.txt'
        
        if parse.numkeys or parse.new_key:
            if parse.numkeys:
                self.infokes()
            if parse.new_key:
                self.generate_key()
            exit(0)
        elif parse.folder:
            values_dict['action'] = 'folder'
        elif parse.exist:
            values_dict['action'] = 'existing file'
        elif parse.message:
           values_dict['action'] = 'write'
           values_dict['content'] = parse.message
        elif parse.read:
            values_dict['action'] = 'read'
            values_dict['path_to_read'] = 'default' if parse.read else parse.read

        if parse.save:
            values_dict['save_output'] = True
            if values_dict['path_to_read'] == 'encrypt_data.txt':
                values_dict['path_to_save'] = 'decrypt_folder/decrypt_file.txt'
            else:
                values_dict['path_to_save'] = parse.save
        else:
            values_dict['save_output'] = False
    return values_dict
