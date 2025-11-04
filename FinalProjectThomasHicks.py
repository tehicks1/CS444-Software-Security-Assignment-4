


# count alphanumeric characters and punctuation in user text
# zyLab Function 1
def get_num_of_non_WS_characters(usr_str):
    count = 0
    for i in usr_str:
        if not i.isspace():
            count += 1
    return count

# count number of words in user text
# zyLab Function 2
def get_num_of_words(usr_str):
    count = 0
    for i in range(1, len(usr_str)):
        if (usr_str[i].isspace()) and (not usr_str[i-1].isspace()):
            count += 1

    if not usr_str[len(usr_str)-1].isspace():
        count += 1
    return count

# converts to sentence case throughout and counts capitalization changes
# zyLab Function 3
def fix_capitalization(usr_str):
    last_char = ' '
    string_edit = ''
    count = 0
    if usr_str[0].islower():
        string_edit = string_edit + usr_str[0].upper()
        count += 1
    else:
        string_edit = string_edit + usr_str[0]

    for i in range(1, len(usr_str)):
        if (last_char == '.' or last_char == '!' or last_char == '?') and usr_str[i].islower():
            string_edit = string_edit + usr_str[i].upper()
            count += 1
        else:
            string_edit = string_edit + usr_str[i]
        if not usr_str[i].isspace():
            last_char = usr_str[i]

    return string_edit, count

# replaces ! and ; throughout and counts changes
# zyLab Function 4
def replace_punctuation(usr_str, **kwargs):
    string_edit = ''
    for i in usr_str:
        if i == '!':
            string_edit = string_edit + '.'
            kwargs['exclamation_count'] += 1

        elif i ==';':
            string_edit = string_edit + ','
            kwargs['semicolon_count'] += 1

        else:
         string_edit = string_edit + i

    print('Punctuation replaced')
    print(f"exclamation_count: {kwargs['exclamation_count']}")
    print(f"semicolon_count: {kwargs['semicolon_count']}")

    return string_edit

# replaces double space bars with single space bars
# zyLab Function 5
def shorten_space(usr_str):
    string_edit = ''
    for i in range(1, len(usr_str)):
        if not (usr_str[i].isspace() and usr_str[i-1].isspace()):
            string_edit = string_edit + usr_str[i-1]
        if i == (len(usr_str) - 1):
            string_edit = string_edit + usr_str[i]

    return string_edit

# replaces every E in the string with 3
def replace_E(usr_str):
    string_edit = ''
    num_changes = 0
    for i in range(len(usr_str)):
        if (usr_str[i] == 'E'):
            string_edit += '3'
            num_changes += 1
        else:
            string_edit += usr_str[i]
            
    return string_edit, num_changes
    
# reverses the string it is fed
def reverse_str(usr_str):
    string_edit = ''
    for i in range(len(usr_str)):
        string_edit += usr_str[(len(usr_str) - 1) - i]
        
    return string_edit

#replaces every s and every S with $
def replace_Ss(usr_str):
    string_edit = ''
    num_changes = 0
    for i in range(len(usr_str)):
        if (usr_str[i] == 's'):
            string_edit += '$'
            num_changes += 1
        elif (usr_str[i] == 'S'):
            string_edit += '$'
            num_changes += 1
        else:
            string_edit += usr_str[i]
            
    return string_edit, num_changes


# displays the menu of options
# ..............add your 3 additional functions to this menu.............
def print_menu():
    print('MENU')
    print('c - Number of non-whitespace characters')
    print('w - Number of words')
    print('f - Fix capitalization')
    print('r - Replace punctuation')
    print('s - Shorten spaces')
    print('1 - Convert E to 3')
    print('2 - Print input in reverse')
    print('3 - Convert s and S to $')
    print('q - Quit\n')

# selections sequence to call each menu option
# ..............add elif options for each of your three functions.............
def execute_menu(option, usr_str):
    if option == 'c':
        print(f'Number of non-whitespace characters: {get_num_of_non_WS_characters(usr_str)}\n')

    elif option == 'w':
        print(f'Number of words: {get_num_of_words(usr_str)}\n')

    elif option == 'f':
        new_str, capital_count = fix_capitalization(usr_str)
        print(f'Number of letters capitalized: {capital_count}')
        print(f'Edited text: {new_str}\n')

    elif option == 'r':
        new_str = replace_punctuation(usr_str, exclamation_count = 0, semicolon_count = 0)
        print(f'Edited text: {new_str}\n')

    elif option == 's':
        new_str = shorten_space(usr_str)
        print(f'Edited text: {new_str}\n')
        
    elif option == '1':
        new_str, letters_changed = replace_E(usr_str)
        print(f"Number of E's changed: {letters_changed}")
        print(f'Edited text: {new_str}\n')
        
    elif option == '2':
        new_str = reverse_str(usr_str)
        print(f'Reversed text: {new_str}\n')
    
    elif option == '3':
        new_str, letters_changed = replace_Ss(usr_str)
        print(f"Number of S's and s's changed: {letters_changed}")
        print(f'Edited text: {new_str}\n')

    
#......................................................................
#start of executable code

if __name__ == '__main__':
    menu_choice = ' '
    user_string = input('Enter a sample text:\n')
    print(f'\nYou entered: { user_string }')
    print()

    print_menu()
    
    while menu_choice != 'q':
        menu_choice = input('Choose an option:\n')
        if menu_choice in ['c', 'w', 'f', 'r', 's', '1', '2', '3']:  #.............<< add your three function triggers here……….....
            execute_menu(menu_choice, user_string)
            print_menu()

# in Final Project Part B, you are to add three (3) additional functions
# your 3 functions should be unique to you and creative to adjust the input passage
# use of API/Library functions is appropriate
# consider string functions we discussed in class during lecture 11, slide 38
# see also: https://www.analyticsvidhya.com/blog/2021/07/10-useful-python-string-functions-every-data-scientist-should-know-about/ 

