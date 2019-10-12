import json, pickle

def ternery(n):
    try:
        n = int(n)
    except TypeError:
        print(n)
        raise(TypeError)
    if n == 0:
        return ''
    nums = []
    while n:
        n, r = divmod(n, 3)
        nums.append(str(r))
    return ''.join(reversed(nums))

def handle_state(state):
	inputs = []
	for col in state.split():
		tern = ternery(col) if col != ' ' else ''
		a = [int(n) for n in list(tern)]
		for n, i in enumerate(a):
			if i == 2:
				a[n] = -1
		
		while len(a) != 6:
			a.append(0)
		inputs += a
	
	return inputs

def handle_output(d):
	for key in d.keys():
		out = d[key]
		a = [0,0,0,0,0,0,0]
		a[out] = 1
		d[key] = a
	return d


if __name__ == '__main__':
	with open('data/raw-data.json') as f:
		d = json.load(f)
	d = handle_output(d)
	cutoff = int(len(d)/4)
	data = []
	train = list(d.keys())[:cutoff]
	test = list(d.keys())[cutoff:]
	
	data.append([handle_state(n) for n in train])
	print(data[0][0])
	data.append([d[n] for n in train])
	data.append([handle_state(n) for n in test])
	data.append([d[n] for n in test])
	with open('data/data.pckl', 'wb') as f: 
		pickle.dump(data, f)


