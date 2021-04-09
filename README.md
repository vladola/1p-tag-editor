# 1p-tag-editor
Allows to batch edit 1password tags which is currently not possible via the GUI

## How to login to your 1password via CLI

`op signin <sign_in_address> <email_address> <secret_key> [--raw]`

After the first sign-in:

`eval $(op <shorthand>)`

## How to run the script

After installing the dependencies (see pip-file), first you need to sign-in (execute the commands above) in the same terminal from which you're going to run the script, otherwise the environment will be different and it would look like you're not signed-in.

Here's the help from the script:

```
usage: tagger.py [-h] -o OLD_TAG -n NEW_TAG (--override | --sub | --append)

Update tags in 1Password

optional arguments:
  -h, --help            show this help message and exit
  -o OLD_TAG, --old-tag OLD_TAG
                        The old tag
  -n NEW_TAG, --new-tag NEW_TAG
                        The new tag to use
  --override            Replace the old tag with the new one. If there's other tags on the item, all will be removed
  --sub                 Substitute old tag with new. All other tags are preserved
  --append              Simply append the new tag and keep the old
  ```