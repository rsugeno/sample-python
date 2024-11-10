#!/usr/bin/env python3

def retry(func):
    def _retry(*args, **kwargs):
        for count in range(1, 3):
            try:
                ret = func(*args, **kwargs)
                return ret
            except:
                print(f'Error occurred. Retry... ({count})')
        else:
            raise Exception('Retry limit exceeded')
                
    return _retry


def retry_with_param(retry_max, raise_exc=True):
    def decorate(func):
        def _retry(*args, **kwargs):
            for count in range(1, retry_max):
                try:
                    ret = func(*args, **kwargs)
                    return ret
                except:
                    print(f'Error occurred. Retry... ({count})')
            else:
                if raise_exc:
                    raise Exception('Retry limit exceeded')
                else:
                    print('Retry limit exceeded')

        return _retry
    return decorate

@retry
def print_string1(s):
    print(s)

    
@retry
def print_string2(s):
    _ = 1 / 0
    print(s)


@retry_with_param(5, False)
def print_string3(s):
    _ = 1 / 0
    print(s)


@retry_with_param(5)
def print_string4():
    _ = 1 / 0
    print('#### print_string4()')
    
def main():
    try:
        print('========= print_string1() ============')
        print_string1('aaa')
    except:
        print('catch Exception')

    try:
        print('========= print_string2() ============')
        print_string2('bbb')
    except:
        print('catch Exception')

    try:
        print('========= print_string3() ============')
        print_string3('ccc')
    except:
        print('catch Exception')
    
    try:
        print('========= print_string4() ============')
        print_string4('ddd')
    except:
        print('catch Exception')

    
if __name__ == '__main__':
    main()
