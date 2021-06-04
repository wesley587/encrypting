# Encrypting

![pgp-encryption-hero](https://user-images.githubusercontent.com/72465364/120722465-263bca80-c4a6-11eb-9b42-3be790f8b388.png)
![shild](https://img.shields.io/badge/python-3.8.5-orange)
![shild](https://img.shields.io/badge/cryptography-2.8-orange)
![shild](https://img.shields.io/badge/pip-20.0.2-orange)

## What is Encrypting

Encrypt project is 100% written in python language.
It's used to encrypt and decrypt files and folders.

## Usage

### How to install

To start the use of this project clone the [repos](https://github.com/wesley587/encrypting) or copy the [main.py](https://github.com/wesley587/encrypting/blob/main/main.py) and install the [requirements.txt](https://github.com/wesley587/encrypting/blob/main/requirements.txt) in your environment

#### Cloning the repos

```bash
git clone https://github.com/wesley587/encrypting.git
```
#### instaling the requirements.txt
```bash
pip3 install -r requirements.txt 
```
[main.py](https://github.com/wesley587/encrypting/blob/main/main.py) can create  the folders and  download the cryptography module

### Commands table



| command | details | how to use |
| - | - | - |
| w | Used to write a encrypt file | -w content [-p path to save] [-k for use a specify key] |
| r | Used to read a encrypt file | -r path [-s to save the output] [-k for use a specify key] |
| e | Used to encrypt a existing file | -e -p path_to_file |
| f | Folder active actions only allows for a foler use with -p | -f [e/d] -p [-s save the output] |
| i | Active the interactive mode | -i |
| p | Used to specify the path | -p |
| s | Used to save the output | -s |
| n | Used to see the Keys | -n |

### Examples

Some examples using this project:

#### Using the interactive mode

```bash
python3 main.py -i
```

#### Writing an encrypting file

```bash
python3 main.py -w 'Write an encrypt message'
```

#### Reading an encrypting file

```bash
python3 main.py -r [path or default] -s
```

#### Seeing the keys

```bash
python3 main.py -n
```

#### Encrypting a folder

```bash
python main.py -f e -p path_to_folder 
```

#### Decrypting a folder

```bash
python3 main.py -f d -p path_to_folder -s
```

#### Generate a new key

```bash
python3 min.py -g
```

#### Encrypting a folder with a specific key

```bash
python main.py -f e -p path_to_folder  -k 10
```

#### Decrypting a folder with a specific key

```bash
python3 main.py -f d -p path_to_folder -s -k 3
```

## How to Contribute

1. Clone repo and create a new branch
2. Make changes and test
3. Submit Pull Request with a description of changes
