import json

def main():
    while True:
        token = input("Please input your bot token here: ")

        if token != '':
            break
        else: print('\nPlease enter your bot token!')

    while True:
        dump_channel = input("Please input the channel id here: ")

        if dump_channel != '':
            break
        else: print('\nPlease enter your bot token!')

    while True:
        command_prefix = input("Please input the command prefix you would like here: ")

        if command_prefix != '':
            break
        else: print('\nPlease enter your bot token!')

    while True:
        about_me = input("Please input the about me you would like here: ")

        if about_me != '':
            break
        else: print('\nPlease enter your bot token!')

    data = {
        'token': token,
        'dump_channel': dump_channel,
        'command_prefix': command_prefix,
        'about_me': about_me
    }

    with open('./src/data.json', 'w') as f:
        f.write(json.dumps(data, indent=4))
        
    print('''\nYour data is saved in ./src/data.json and can be edited if any of the previously input information is incorrect or needs to be updated!''')    

if __name__ == '__main__':
    main()
else:
    print("Please run this as the main file!")