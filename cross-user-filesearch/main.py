import os

def find_psd_files(format):
    for root, dirs, files in os.walk('/Users/'):
        for file in files:
            if file.endswith(format):
                yield os.path.join(root, file)

def main():
    psd_files = list(find_psd_files())
    if not psd_files:
        print('No files found')
        return

    print('Found the following files:')
    for i, file in enumerate(psd_files):
        print(f'{i+1}: {file}')

    while True:
        selection = input('Enter the numbers of the files to copy, separated by commas: ')
        selected_files = []
        for index in selection.split(','):
            index = index.strip()
            if index.isdigit() and int(index) <= len(psd_files):
                selected_files.append(psd_files[int(index)-1])
        if selected_files:
            break
        else:
            print('Invalid selection, please try again')

    for file in selected_files:
        os.system(f'sudo cp "{file}" /path/to/destination')

if __name__ == '__main__':
    main()