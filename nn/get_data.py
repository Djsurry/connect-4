import requests, pickle, json, random, time
from bs4 import BeautifulSoup
from selenium import webdriver

url = "https://azfour.com/?model1=000050&model2=000050&skill1=7&skill2=7&autoplay1=false&autoplay2=false&discs={}"

def ternery(n):
    try:
        n = int(n)
    except TypeError:
        print(n)
        raise(TypeError)
    if n == 0:
        return '0'
    nums = []
    while n:
        n, r = divmod(n, 3)
        nums.append(str(r))
    return ''.join(reversed(nums))

def state_to_pos(state):
    s = [ternery(n) for n in state.split()]
    pos = []
    to_find = '1'
    empty = 0
    while empty < 2:
        found = False
        for j, col in enumerate(s):
            for i, cell in enumerate(col):
                if cell == to_find:
                    found = True
                    pos.append((5-i, j))
                    break
            if found:
                
                break
        if found:
            c = list(s[pos[-1][1]])
            c[5-pos[-1][0]] = 'X'
            s[pos[-1][1]] = ''.join(c)
            to_find = '2' if to_find == '1' else '1'
        else:
            empty += 1
    string = ''
    for p in pos:
        string += f'{p[0]},{p[1]};'
    print(string[:-1])
    return string[:-1]

def webscrape(url):
    driver.get(url)
    time.sleep(0.5)
    soup = BeautifulSoup(driver.page_source, 'lxml')
    scores = []
    try:
        for i in ['s' + str(n) for n in range(7)]:
            print(i)
            scores.append(soup.find('div', {'id': i}).contents[0].strip().replace('%', ''))
    except IndexError:
        return None

    return scores.index(max(scores))

def gen(s=0):
    print('Loading states')
    data = read_chunk(s=s)
    states = json.loads(data).keys()
    print('States loaded')
    solutions = {}
    for i, state in enumerate(states):
        s = state_to_pos(state)
       
        best = webscrape(url.format(s))
        if best == None:
            continue
        solutions[state] = best
        print(f'finished {i+1}/{len(states)}')
    with open('data/raw-data.json') as f:
        data = json.load(f)

        data.update(solutions)


    with open('data/raw-data.json', 'w+') as f:
        json.dump(data, f)

def read_chunk(s=0, b=10000):
    with open('../qTable.json') as f:
        f.seek(s)
        data = f.read(b)
    print(f'data {data}')
    if data[0] != '{':
        i = 0
        for j in data:
            if j == '"' and data[i+1] != ':':
                break
            i += 1
        data = '{' + data[i:]

    s = list(reversed(data))

    to_remove = 0
    j = 0
    for i in s:
        if j % 2 != 0:
            if s[j] == ']' and s[j-1] == ',':
                to_remove += 1
                break
            else:
                to_remove += 2
        j+= 1
    
    return data[:-to_remove] + '}'



if __name__ == '__main__':
    driver = webdriver.Chrome()

    for i in [10000*n for n in range(500, 10000)]:
        try:
            gen(i)
        except:
            continue
    driver.close()
    
   

def iterate(n):
    pos = [0,0]
    for i in range(n):
        d = random.choice(['u','d','r','l'])
        if d == 'u':
            pos[1] += 1
        elif d == 'd':
            pos[1] -= 1
        elif d == 'r':
            pos[0] += 1
        elif d == 'l':
            pos[0] -= 1
    return (pos[0]*pos[0] + pos[1]*pos[1])*0.5












