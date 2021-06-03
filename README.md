# Encrypting

![pgp-encryption-hero](https://user-images.githubusercontent.com/72465364/120722465-263bca80-c4a6-11eb-9b42-3be790f8b388.png)

# What is Encrypting project

Encrypt project is 100% writen in python language.

It's used for encrypt and decrypt files and folders.

# usage

To start the use this project clone the [repos](ttps://github.com/wesley587/encrypting) or copy the [main.py](ttps://github.com/wesley587/encrypting/blob/main/main.py)

# Commands

| command | detaills | how to use |
| - | - | - |
| w | Used to write a encrypt file | -w content [-p path to save] |
| r | Used to read a encrypt file | -r path [-s to save the output] [-k for use a specify key] |
| e | Used to encrypt a existing file | -e -p |
| f | Active actions only allows for a foler use with -p | -f [e/d] -p [-s save the output] |
| p | Used to specify the path | -p |
| s | Used to save the output | -s |
| n | Used to see the Keys | -n |

# Examples

Some examples using this project

## Writing an encrypting file

```shell
python3 main.py -w 'Write an encrypt message'
```

## Reading an encrypting file

```shell
python3 main.py -r [path or default] -s
```

## Seeing the keys

```shell
python3 main.py -n
```

## Encrypting an folder

```shell
python main.py -f e -p path_to_folder 
```

## Desenrypting an folder

```shell
python3 main.py -f d -p path_to_folder -s
```

## Generte a new key

```shell
python3 min.py -g
```
