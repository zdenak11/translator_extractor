# No more maintanence
This project started as a test, when I tried to learn python and was discontinued. If anyone wants to continue on this project, please contact me.

# Translator extractor
Utility for extracting translations in Nette projects with Kdyby/Translator

## Requirements

- Python v2.7
- PyYaml
 
## Using

add to beginnig of your .php and .latte files comment with settings:
  - extractor_setting         % first line, start finding keys
  - beginning                 % string before every key
  - ending                    % string after every key
  - namespace                 % where the keys should be inserted
  - translator_format_start   % string that should be inserted in code before key
  - translator_format_end     % string that should be inserted in code after key

open konsole (cmd in windows)

go to your_project_directory/app

call: python location_of_extractor/translator_extractor.py

extracted keys will be in your_project_directory/app/lang/*.neon % * means 'front' and modules names

it also add new keys in existing dictionaries

for each file is also generated backup (original_file.bak)

## Example

Example you can find in example.php
