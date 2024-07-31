import re

# Reducing to the bare minimal removes the need for a dotenv dependency
def get_env_variables_from_file(filename):
    '''Reads variable values in an environment file'''
    dict = {}
    with open(filename) as f:
        for line in f:
            res = re.search(r'^(\w+)=(.+)$',line.strip())
            if line.strip().startswith('#') or line.strip() == '':
                continue
            if not res:
                print("PBM can't parse that line in the environment variable file:",line)
                sys.exit(-3)
            dict[res.group(1)] = res.group(2)
    return dict

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print('\n\tUsage: '+sys.argv[0]+' [path_to_file/]<file_containing_variables>\n')
    else:
        vars = get_env_variables_from_file(sys.argv[1])
        for var,val in vars.items():
            print(var,"=",val)
