import os

def dfs(dir_name):
    result = []
    sub_list = os.listdir(dir_name)

    for sub in sub_list:
        if os.path.isdir(dir_name + '/' + sub):
            result += dfs(dir_name + '/' + sub)
        elif sub.endswith('.out'):
            result.append(dir_name + '/' + sub)

    return result

def search_by_keyword(targets):
    while len(targets) > 1:
        keyword = input(' >> ')
        tmp_result = []
        for target in targets:
            if keyword in target:
                tmp_result.append(target)
        targets = tmp_result
        print('{0:->120}'.format(' Result '))
        for target in targets:
            print(' > ' + target)
        print('{0:->120}'.format(''))
    if len(targets) == 0:
        return None
    return tmp_result[0]


def search_by_config(host_type, prefetcher, core_count, suite_fullname):
    output_file_path = './zsim_stats/' + host_type + '/' + prefetcher + '/' + core_count + '/' + suite_fullname
    if os.path.isfile(output_file_path):
        os.system('python2 ./scripts/get_stats_per_app.py ' + output_file_path + ' > tmp_search_result')
    elif os.path.isfile('tmp_search_result'):
        os.remove('tmp_search_result')

def read_result():
    result = { 'MPKI': 0.0, 'LFMR': 0.0 }
    try:
        with open('tmp_search_result', 'r') as f:
            tmp_search_result = f.readlines()
            for line in tmp_search_result:
                if 'Instruction' in line and int(line[line.find(':')+1:-1]) == 0:
                    result['MPKI'] = '-'
                    result['LFMR'] = '-'
                    break
                if 'MPKI' in line or 'LFMR' in line:
                    result[line[line.find(':')-4:line.find(':')]] = round(float(line[line.find(':')+2:-1]), 1)
    except:
        result['MPKI'] = '-'
        result['LFMR'] = '-'
        pass
    return result

def print_result(suite_fullname):
    host_config_list = ['host_ooo', 'host_inorder']
    prefetcher_config_list = ['no_prefetch', 'prefetch']
    core_config_list = [1, 4, 16, 64, 256]

    for host_config in host_config_list:
        print(host_config)
        print('{0:->120}'.format(''))
        for prefetcher_config in prefetcher_config_list:
            print('{0:<60}'.format(prefetcher_config), end='')
        print('{0:->120}'.format(''))
        for prefetcher_config in prefetcher_config_list:
            for core_config in core_config_list:
                print('{0:<12}'.format(core_config), end='')
        for prefetcher_config in prefetcher_config_list:
            for core_config in core_config_list:
                search_by_config(host_config, prefetcher_config, str(core_config), suite_fullname)
                tmp = read_result()
                print('{0:<12}'.format(str(tmp['MPKI']) + '/' + str(tmp['LFMR'])), end='')
        print('\n{0:->120}'.format(''))

def exit_EOF():
    print('EXIT')
    exit(0)

def main():
    zsim_stats_path = './zsim_stats'

    print('\n1. Search the Function')
    all_outputs = list(set([output.split('/')[-1] for output in dfs(zsim_stats_path)]))
    try:
        function = search_by_keyword(all_outputs)
    except EOFError:
        exit_EOF()

    if function is None:
        print('There is no result.')
        exit(0)

    print('\n2. Print Results')
    print('{0:->120}'.format(' ' + function.split('/')[-1] + ' '))
    print_result(function.split('/')[-1])

main()
