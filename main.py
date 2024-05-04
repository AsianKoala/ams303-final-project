s = """
AWUOS EQSOR EYOZO AXECA XROAF ZURUI XSOLL AIXRU SYKYO FBJLK 
MSPXQ WSDCY KRYYQ RHCOI XFARL UMZLA RZLYU ZZSAQ LAJXW ZJKNK 
SOLVS ZLQSL ZJTWU OCEQG JTVZJ KNWYL CPJUU XRTGO SDYYM ZOFMR 
SSMZU OYTCX SPHJU VHQCQ OFUDC XSJTM PNAQM XTAXB NYAYL LLVAM 
AZBYX QWEOR GEYKN FOLHM SPUMA RQAXR TUJUU OMICI ZINLO RJRJN 
UAXRO ARDUU ALCYK QKMCR YJFKN IEROJ TTUEC XQAFJ NSWXS CRZUO 
MOAOY TUAXX TMFTG EYKNF OL
"""
s = s.replace(' ', '')
s = s.replace('\n', '')

alpha = [chr(ord('A') + x) for x in range(26)]
num = 4

def calc_hist():
    hist = [{} for _ in range(num)]
    for i, x in enumerate(s):
        hist[i % num][x] = hist[i % num].get(x, 0) + 1
    return hist

hist = calc_hist()

def run_ic_test():
    for h in hist:
        N = sum(h.values())
        lhs = 1.0 / (N * (N - 1))
        rhs = sum(h.get(chr(ord('A') + i), 0) * (h.get(chr(ord('A') + i), 0) - 1) for i in range(26))
        IC = lhs * rhs
        print(IC)

def print_freqs():
    for h in hist:
        for a in alpha:
            val = h.get(a, 0)
            print(f'{a}: {val}')
        print()

print_freqs()

def get_lists():
    res = []
    for h in hist:
        res.append([])
        for a in alpha:
            val = h.get(a, 0)
            res[-1].append(val)
        for a in alpha:
            val = h.get(a, 0)
            res[-1].append(val)
    return res

a = get_lists()

for x in a: print(x[:26])

def get_mse(shifts):
    mx = max(shifts)
    mse_sum = 0
    for sh in range(26):
        i = [mx - shifts[i] + sh for i in range(num)]
        sum = 0
        for j in range(num):
            sum += a[j][i[j]]
        mean = sum / num
        mse = 0
        for j in range(num):
            diff = a[j][i[j]] - mean
            mse += diff * diff
        mse_sum += mse
    return mse_sum / 26

def get_words(shifts):
    mx = max(shifts)
    words = []
    for sh in range(26):
        i = [mx - shifts[i] + sh for i in range(num)]
        word = ""
        for j in range(num):
            word += chr(ord('A') + (i[j] % 26))
        bad_list = "ZJXQKV"
        bad = False
        for w in word:
            if w in bad_list:
                bad = True
        if not bad:
            words.append(word)

    return words

def go():
    res = []
    for i in range(26):
        for j in range(26):
            for k in range(26):
                shift = [0, i, j, k]
                res.append((shift, get_mse(shift)))

    res.sort(key=lambda x: x[1])
    return res

best_shifts = go()[:10]
for shift in best_shifts:
    words = get_words(shift[0])
    print(f'shift: {shift[0]}, mse: {shift[1]}, words: {words}')


print()

KEYWORD = 'EDGE'
AO = ord('A')


def translate(encoded):
    translated = ""
    for i, c in enumerate(encoded):
        k = i % num
        translated += chr(AO + ((ord(c) - ord(KEYWORD[k]) + 26) % 26))
    return translated


s = translate(s)
print(s)
print()

def freqs():
    return {chr(AO + i):s.count(chr(AO + i)) for i in range(26)}

f = freqs()
print(f)
print()

voids = list(filter(lambda x: x[1] == 0, f.items()))
print('voids', voids)
print()


def get_trigraphs():
    res = {a: {} for a in alpha}
    for i, c in enumerate(s):
        l, r = '.', '.'
        if i > 0:
            l = s[i - 1]
        if i < len(s) - 1:
            r = s[i + 1]
        tri = l + r
        res[c][tri] = res[c].get(tri, 0) + 1
    return res

tri = get_trigraphs()
the = (0, 0, 0)
for k,v in tri.items():
    print(f'{k}: {v}')
    for tri, c in v.items():
        if c > the[2]:
            the = (k, tri, c)

print(f'most occ trigraph: {the}')
print()
print()

bef = 'bef'
aft = 'aft'
def get_digraphs():
    res = {a: {bef: {}, aft: {}} for a in alpha}
    for i, c in enumerate(s):
        if i > 0:
            res[c][bef][s[i - 1]] = res[c][bef].get(s[i - 1], 0) + 1
        if i < len(s) - 1:
            res[c][aft][s[i + 1]] = res[c][aft].get(s[i + 1], 0) + 1
    return res

di = get_digraphs()
for k,v in di.items():
    print(f'{k} bef: {v[bef]}')
    print(f'{k} aft: {v[aft]}')
        

english='DAKQYIBLSZRFMUEGNVCHOWTJPX'
mappings = {a:english[i] for i, a in enumerate(alpha)}

print()
for k, v in mappings.items():
    print(f'{k}: {v}')

print()
print('----------------')
print('FINAL MESSAGE:')
print('----------------')
print()

final_message = ''.join(list(map(lambda x: mappings[x], s)))
print(final_message)
