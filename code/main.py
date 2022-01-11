# Wenzel, Jennifer

from InquirerPy import prompt
from InquirerPy.validator import PathValidator
import ntpath
import os
import pandas as pd
from tabulate import tabulate

from ascii_art import intro
from functions import huber, denzin, form_factor

# TODO: clean up and check weather dsm_vol col exists before calculating form factor

# set style configuration
end_line = f'{"-"*60}\n'
prompt_style = {'questionmark': 'green bold', 'answer': 'green bold', 'input': 'green bold',  'pointer': 'green bold'}

os.system ("color") # uses ANSI escape sequence to style text in console
c = {
    "ENDC": "\033[0m",
    "Bold": "\u001b[1m",
}

# set default data directory
input_dir = '.\data\input\\'
output_dir = '.\data\output\\'

# show menu
def menu():
    options = [
        {
        'type': 'list',
        'message': 'Choose an option:',
        'choices': ['Show available methods and requirements', 'Calculate volumes', 'Exit\n']
        }
    ]

    result = prompt(options, prompt_style)
    # return option index
    return options[0]['choices'].index(result[0])

# available methods
methods = {
    'Huber': {'req': ['dbh', 'h'], 'method': huber},
    'Denzin': {'req': ['species', 'dbh', 'h'], 'method': denzin}
}

# print table of implemented methods and their required data columns
def show_methods():
   met_table = [[method, methods[method]['req']] for method in methods]
   print(tabulate(met_table, headers=['Name', 'Required columns']))

# select data source -> next step: upload file as df
def input():
    get_source = [
        {
            'type': 'filepath',
            'message': 'Enter data source to process:',
            'name': 'source',
            'default': input_dir,
            'validate': PathValidator(is_file=True, message='Input is not a file'),
            'only_files': True,
        }
    ]
    # return source path
    return prompt(get_source, style=prompt_style)['source']
    
# display menu: try all or select one method
def select_method():
    options = [
        {
            'type': 'list',
            'message': 'Select a method or choose all:',
            'choices': ['All', 'Huber', 'Denzin', 'Exit\n']
        },
        {'type': 'confirm', 'message': 'Confirm?'},
    ]

    result = prompt(options, prompt_style)
    confirmed = result[1]
    selection = result[0]

    return selection if confirmed else None

# checks whether the required data columns are available and calculates the volume with the selected method if successful
def calc_vol(selected_method, data):
    
    # check if all required columns for the selected method exist in the df
    if all(col in data.columns for col in methods[selected_method]['req']):
        # set name for new volume column
        vol_col = f'{selected_method.lower()}_vol'

        # get required columns from df
        params = [data[req] for req in methods[selected_method]['req']]

        # execute selected method and assign vol values to new column    
        data[vol_col] = methods[selected_method]['method'](params)
        return vol_col
    else:
        # return None, if the required columns don't exist
        return None

# saves data as df and tries to calculate selected method(s) -> if all is selected, all available methods are tried, otherwise just the specific method will be executed
def output(source_path, selected_method):

    # get csv file and save as dataframe
    df_trees = pd.read_csv(source_path)
    df_trees = df_trees.set_index('id')

    # set output path to default data dir and append 'vol' to existing file name
    output = f'{output_dir}{ntpath.basename(source_path).split(".")[0]}+vol.csv'
    success_title = '\033[1mSuccess \033[0m \n'
    error_title = '\033[1mError \033[0m \n'

    if selected_method == 'All':
        success = []
        error = []
        for method in methods:
            created = calc_vol(method, df_trees)

            if created is not None:
                success_met = f'{method}: Based on the input data, the stem volumes according to the {method} method were created.\n'
                success.append(method)
                if method == 'Huber' and 'dsm_vol' in df_trees:
                    df_trees['form_factor'] = form_factor(df_trees['dsm_vol'], df_trees['huber_vol'])

                # first one
                if len(success) == 1:
                    print(success_title)
                    print(success_met)
                    # write data to file already since it might be the only successful calculation
                    df_trees.to_csv(path_or_buf = output)
                # last one
                elif list(methods).index(method) == len(methods)-1:
                    print(success_met)
                    print(end_line)
                    df_trees.to_csv(path_or_buf = output)
                """ elif len(success) > 1 and len(list(methods)) > len(success):
                    print(f'{method}: Based on the input data, the stem volumes according to the {method} method were created.') """
            else:
                error_met = f'{method}: Requirements to use method not satisfied. The {method} method requires the columns {methods[method]["req"]}.\n'
                error.append(method)
                # none were created, not this time or before but more are coming
                if len(error) == 1 and (len(success)+len(error)) < len(methods):
                    print(error_title)
                    print(error_met)
                # none were created this time but there are still more to come and it's not the first one
                elif len(error) > 1 and (len(success)+len(error)) < len(methods):
                    print(error_met)
                # there have been errors before and this is the last one
                elif len(error) > 1 and methods.index(method) == len(methods)-1:
                    print(error_met)
                    print(end_line)
                # none were created this time but there may have been others created before, this is the last and only error
                else:
                    print(error_title)
                    print(error_met)
                    print(end_line)
    else:
        # will be executed if one specific method was chosen
        created = calc_vol(selected_method, df_trees)
        if created is not None:
            print(success_title)
            print(f'{selected_method}: Based on the input data, the stem volumes according to the {selected_method} method could be created.\n')
            print(end_line)
            if selected_method == 'Huber' and 'dsm_vol' in df_trees:
                df_trees['form_factor'] = form_factor(df_trees['dsm_vol'], df_trees['huber_vol'])
            df_trees.to_csv(path_or_buf = output)
        else:
            print(error_title)
            print(f'{selected_method}: Requirements to use method not satisfied. The {selected_method} method requires the columns {methods[selected_method]["req"]}.')
            print(f'\n{end_line}')

    # display final result if the calculations were successful, otherwise the input data table is shown 
    print('\033[1mData table \033[0m \n')
    print(f'{df_trees.head(10)}\n')

    # this will also be called, if a file with that name has been created previously
    if os.path.isfile(output):
        print(f'The target file was created at \033[1m{output}\033[0m.\n')

def main():
    # display intro headline
    intro()

    # show options menu
    option = menu()
    print(f'\n{end_line}')

    while option!= 2:
        if option == 0:
            show_methods()
            print(f'\n{end_line}')
            option = menu()
            print(end_line)

        elif option == 1:
            source_path = input()
            selected_method = select_method()
            print(f'\n{end_line}')

            while selected_method != 'Exit\n':
                output(source_path, selected_method)
                print(end_line)
                selected_method = select_method()
                print(f'\n{end_line}')

            option = menu()
            print(end_line)

    print('The end.\n')

if __name__ == '__main__':
    main()