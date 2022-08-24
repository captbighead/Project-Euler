import io
import math

def printTitle(title):
    headerfooter = "-"*(len(title)+6)
    print(f'{headerfooter}\n-- {title} --\n{headerfooter}\n')

solutions = []
def solve(problem):
    if problem > len(solutions):
        raise IndexError
    printTitle(f"Problem {problem}")
    solutions[problem-1]()

def problem1():
    print("Find the sum of all natural numbers below 1000 that are multiples of"
         "3 or 5\n")
    sum = 0
    for i in range(1000):
        if not i % 3 or not i % 5:
            sum += i
    print(f"The answer is {sum}\n")
solutions.append(problem1)

def problem2():
    print("Find the sum of even-valued fibonacci numbers less than 4,000,000\n")
    sum = 0
    fibseq = [1,2]
    while True:
        newNum = fibseq[-1] + fibseq[-2]
        if newNum < 4000000:
            fibseq.append(newNum)
        else:
            break
    for n in fibseq:
        if n % 2:
            continue
        else:
            sum += n
    print(f"The answer is {sum}\n")
solutions.append(problem2)

def problem3():
    target = 600851475143
    stop = int(math.sqrt(target)) + 1   # Because math, answer is less than this
    print(f"What is the largest prime factor of the number {target}?\n")
    
    # Start off with a list of primes (2, 3 are excluded because they're checked
    # explicitly. 
    primes = [5, 7, 11, 13]
    def isPrime(n):
        # Some heuristics to eliminate non-primes 
        if not n % 2 or not n % 3:
            return False
        if not (n - 1) % 6 and not (n + 1) % 6:
            return False

        # Induction: 
        for p in primes:
            if p > math.sqrt(n):    # p > root(n) means n is prime (if allprimes
                break               # is correctly populated in order)
            if not n % p:
                return False
        
        # If we got here, we're prime
        primes.append(n)         # Remember for later n
        return True
    
    # With an isPrime function defined, we count up from the highest prime we've
    # hard-coded to the target's square root, checking each number for primeness
    lprime = primes[-1]              # Keeps largest prime's best option
    test = lprime                       # The number we're currently checking

    # 'stop' is the first whole number greater than the root of the target. 
    # The largest prime factor of the target is definitionally smaller than its
    # root. We'll count up the prime numbers until we'd go above stop; the last
    # one we found is the largest prime factor.  
    while test < stop:
        # 'test' is bigger than lprime, and we don't know if *it's* prime. 
        test += 2   # Skip all even numbers

        # 2 Important checks: Is 'test' prime, and does test divide the target.
        if isPrime(test) and not target % test:
            lprime = test

    # Whatever lprime is at this point in execution is the largest prime factor
    # of the target. 
    print(f"The largest prime factor of {target} is {lprime}\n")
solutions.append(problem3)

def problem4():
    print("Find the largest palindromic number made from two 3-digit numbers\n")

    # Naive: Go from largest possible product of 2 3-digit numbers, and check if
    # it's palindromic. Then if it is, check if it's the product of 2 3 digit
    # numbers. 

    answer = 0
    n = 999*999
    while n > 100*100:
        s = str(n)
        if s[0] == s[-1] and s[1] == s[-2] and (len(s) == 5 or s[2] == s[3]):
            # We *are* palindromic. 
            for i in range(100,1000):
                if not n % i:   # We *are* divisible by *one* three digit number
                    for j in range(100, 1000):
                        if i * j == n:
                            answer = n
                            break
                if answer:
                    break
        if answer:
            break
        n -= 1
    print(f"The answer is {answer}\n")
solutions.append(problem4)

def problem5():
    print("What is the smallest positive number evenly divisible by all of the "
          "numbers from 1 to 20?\n")

    factors = [2]
    for i in range(3,21):
        n = i
        # Every n needs to be composable by the factors within the factors list.
        composition = factors.copy()
        for c in composition:
            if not n % c:
                n = int(n/c)
        if n != 1:
            factors.append(n)

    equation = ""
    answer = 1
    for f in factors:
        answer *= f
        equation += f"{f}*"
    equation = equation[:-1]
           
    print(f"The answer is {answer} ({equation})\n")
solutions.append(problem5)

def problem6():
    print("Find the difference between the sum of the squares of the first one "
          "hundred natural numbers and the square of the sum.\n")

    smsq = 0
    sqsm = 0
    for i in range(1,101):
        smsq += i * i
        sqsm += i
    sqsm = sqsm * sqsm

    answer = sqsm - smsq

    print(f"The answer is {answer}\n")
solutions.append(problem6)

def problem7():
    print("What is the 10,001st prime number?\n")

    primes = [2,3]
    primeCandidates = []
    for i in range(1,20001):
        primeCandidates.append(i*6-1)
        primeCandidates.append(i*6+1)

    def isPrime(n):
        # Some heuristics to eliminate non-primes 
        if not n % 2 or not n % 3:
            return False
        # Unnecessary check; all values are guaranteed to be here
        #if not (n - 1) % 6 and not (n + 1) % 6:
        #    return False

        # Induction: 
        for p in primes:
            if p > math.sqrt(n):    # p > root(n) means n is prime (if allprimes
                break               # is correctly populated in order)
            if not n % p:
                return False
        
        # If we got here, we're prime
        primes.append(n)         # Remember for later n
        return True

    answer = 0
    for pc in primeCandidates:
        isPrime(pc)
        if len(primes) == 10001:
            answer = primes[10000]
            break

    print(f"The answer is {answer}\n")
solutions.append(problem7)

def problem8():
    num = (
    "73167176531330624919225119674426574742355349194934"
    "96983520312774506326239578318016984801869478851843"
    "85861560789112949495459501737958331952853208805511"
    "12540698747158523863050715693290963295227443043557"
    "66896648950445244523161731856403098711121722383113"
    "62229893423380308135336276614282806444486645238749"
    "30358907296290491560440772390713810515859307960866"
    "70172427121883998797908792274921901699720888093776"
    "65727333001053367881220235421809751254540594752243"
    "52584907711670556013604839586446706324415722155397"
    "53697817977846174064955149290862569321978468622482"
    "83972241375657056057490261407972968652414535100474"
    "82166370484403199890008895243450658541227588666881"
    "16427171479924442928230863465674813919123162824586"
    "17866458359124566529476545682848912883142607690042"
    "24219022671055626321111109370544217506941658960408"
    "07198403850962455444362981230987879927244284909188"
    "84580156166097919133875499200524063689912560717606"
    "05886116467109405077541002256983155200055935729725"
    "71636269561882670428252483600823257530420752963450")
    
    print("In the given thousand-digit number, what is the product of the 13 ad"
          "jacent digits that give the greatest product?\n")

    lProd = 0
    try:
        for i in range(len(num)):
            lProd = max(lProd, int(num[i+0]) * int(num[i+1]) * int(num[i+2]) * 
                        int(num[i+3]) * int(num[i+4]) * int(num[i+5]) * 
                        int(num[i+6]) * int(num[i+7]) * int(num[i+8]) * 
                        int(num[i+9]) * int(num[i+10]) * int(num[i+11]) * 
                        int(num[i+12]))
    except IndexError:
        # In other words: I can't be arsed to put the right end to the range. 
        # It's probably len(num) - 13, but I've been burned by off-by-one errors
        # before. But I do know that if the indexing breaks, we know we've 
        # checked all possible sets of 13 adjacent digits, and we have lProd. 
        lProd = lProd
    
    print(f"The answer is {lProd}\n")
solutions.append(problem8)

def problem9():
    print("Find the Pythagorean triplet that sums to 1000\n")
    answer = 0

    for i in range(1,999):
        for j in range(i, 1000-i):
            if i + j > 999:
                break
            for k in range(j,1001-i-j):
                if i + j + k == 1000:
                    if i * i + j * j == k * k:
                        answer = [(i,j,k),i*j*k]
                elif i + j + k > 1000:
                    break

    a = answer[0][0]
    b = answer[0][1]
    c = answer[0][2]
    answer = answer[1]
    print(f"The answer is {answer} ({a}*{b}*{c})\n")
solutions.append(problem9)

def problem10():
    print("Find the sum of all prime numbers below two million\n")
    answer = 0

    print("Generating Candidates")
    primes = [2,3]
    primeCandidates = []
    i = 1
    while 6 * i + 1 < 2000001:
        primeCandidates.append(i*6-1)
        primeCandidates.append(i*6+1)
        i += 1

    print("Definining Primacy Check")
    def isPrime(n):
        # Some heuristics to eliminate non-primes 
        if not n % 2 or not n % 3:
            return False
        # Unnecessary check; all values are guaranteed to be here
        #if not (n - 1) % 6 and not (n + 1) % 6:
        #    return False

        # Induction: 
        for p in primes:
            if p > math.sqrt(n):    # p > root(n) means n is prime (if allprimes
                break               # is correctly populated in order)
            if not n % p:
                return False
        
        # If we got here, we're prime
        primes.append(n)         # Remember for later n
        return True

    print("Pruning sieve")
    for pc in primeCandidates:
        isPrime(pc)

    print("Summing Primes")
    for p in primes:
        answer += p if p < 2000000 else 0

    print(f"The answer is {answer}\n")
solutions.append(problem10)

def problem11():
    grid = [[ 8, 2,22,97,38,15, 0,40, 0,75, 4, 5, 7,78,52,12,50,77,91, 8],
            [49,49,99,40,17,81,18,57,60,87,17,40,98,43,69,48, 4,56,62, 0],
            [81,49,31,73,55,79,14,29,93,71,40,67,53,88,30, 3,49,13,36,65],
            [52,70,95,23, 4,60,11,42,69,24,68,56, 1,32,56,71,37, 2,36,91],
            [22,31,16,71,51,67,63,89,41,92,36,54,22,40,40,28,66,33,13,80],
            [24,47,32,60,99, 3,45, 2,44,75,33,53,78,36,84,20,35,17,12,50],
            [32,98,81,28,64,23,67,10,26,38,40,67,59,54,70,66,18,38,64,70],
            [67,26,20,68, 2,62,12,20,95,63,94,39,63, 8,40,91,66,49,94,21],
            [24,55,58, 5,66,73,99,26,97,17,78,78,96,83,14,88,34,89,63,72],
            [21,36,23, 9,75, 0,76,44,20,45,35,14, 0,61,33,97,34,31,33,95],
            [78,17,53,28,22,75,31,67,15,94, 3,80, 4,62,16,14, 9,53,56,92],
            [16,39, 5,42,96,35,31,47,55,58,88,24, 0,17,54,24,36,29,85,57],
            [86,56, 0,48,35,71,89, 7, 5,44,44,37,44,60,21,58,51,54,17,58],
            [19,80,81,68, 5,94,47,69,28,73,92,13,86,52,17,77, 4,89,55,40],
            [ 4,52, 8,83,97,35,99,16, 7,97,57,32,16,26,26,79,33,27,98,66],
            [88,36,68,87,57,62,20,72, 3,46,33,67,46,55,12,32,63,93,53,69],
            [ 4,42,16,73,38,25,39,11,24,94,72,18, 8,46,29,32,40,62,76,36],
            [20,69,36,41,72,30,23,88,34,62,99,69,82,67,59,85,74, 4,36,16],
            [20,73,35,29,78,31,90, 1,74,31,49,71,48,86,81,16,23,57, 5,54],
            [ 1,70,54,71,83,51,54,69,16,92,33,48,61,43,52, 1,89,19,67,48]]

    print("What is the greatest product of 4 adjacent numbers in the given grid"
          "? (Adjacency includes diagonals)\n")

    answer = 0
    coords = []
    for x in range(len(grid)):
        for y in range(len(grid)):
            # Only one check needed per axis; a sweep of right-facing products
            # checks all left-facing products in reverse.
            
            
            # Right/Left
            try:
                p = grid[x+0][y+0]*grid[x+1][y+0]*grid[x+2][y+0]*grid[x+3][y+0]
                answer = max(answer, p)
                if answer == p:
                    coords = [x,y,x+3,y]
            except IndexError:
                # Instead of futzing with iterating only over legal indices, 
                # we'll just ignore the exception if we screw up and move on. 
                pass

            # Up/Down
            try:
                p = grid[x+0][y+0]*grid[x+0][y+1]*grid[x+0][y+2]*grid[x+0][y+3]
                answer = max(answer, p)
                if answer == p:
                    coords = [x,y,x,y+3]
            except IndexError:
                pass
            
            # Diagonal Left
            try:
                p = grid[x+0][y+0]*grid[x+1][y+1]*grid[x+2][y+2]*grid[x+3][y+3]
                answer = max(answer, p)
                if answer == p:
                    coords = [x,y,x+3,y+3]
            except IndexError:
                pass

            # Diagonal Right
            try:
                p = grid[x+0][y+0]*grid[x-1][y+1]*grid[x-2][y+2]*grid[x-3][y+3]
                answer = max(answer, p)
                if answer == p:
                    coords = [x,y,x-3,y+3]
            except IndexError:
                pass

    origin = (coords[0],coords[1])
    terminus = (coords[2],coords[3])
    print(f"The answer is {answer}; From {origin} to {terminus}\n")
solutions.append(problem11)

def problem12():
    print("Find the first triangular number that has over five hundred divisors"
          ".\n")

    answer = 0
    record = 0
    last = 0
    n = 1
    while True:
        # The nth Triangular number is equal to n + the (n-1)th Triangular
        t = n + last
        last = t
        n += 1

        def generateDivisors(k):
            divisors = []
            symmetryPoint = int(math.sqrt(k))
            for i in range(1,int(symmetryPoint+1)):
                if not k % i:
                    divisors.append(i)
            for d in divisors.copy():
                # There's always an exception to the rule. 
                if d * d == k:
                    continue
                divisors.append(int(k/d))
            return divisors

        divisors = generateDivisors(t)
        record = max(record, len(divisors))

        if record > 500:
            print("We found the answer")
            break

    answer = last
    print(f"If we found the answer, it is {answer}. If we didn't, we found a nu"
          f"mber with {record} divisors. \n")
solutions.append(problem12)

def problem13():
    nums = [
        37107287533902102798797998220837590246510135740250,
        46376937677490009712648124896970078050417018260538,
        74324986199524741059474233309513058123726617309629,
        91942213363574161572522430563301811072406154908250,
        23067588207539346171171980310421047513778063246676,
        89261670696623633820136378418383684178734361726757,
        28112879812849979408065481931592621691275889832738,
        44274228917432520321923589422876796487670272189318,
        47451445736001306439091167216856844588711603153276,
        70386486105843025439939619828917593665686757934951,
        62176457141856560629502157223196586755079324193331,
        64906352462741904929101432445813822663347944758178,
        92575867718337217661963751590579239728245598838407,
        58203565325359399008402633568948830189458628227828,
        80181199384826282014278194139940567587151170094390,
        35398664372827112653829987240784473053190104293586,
        86515506006295864861532075273371959191420517255829,
        71693888707715466499115593487603532921714970056938,
        54370070576826684624621495650076471787294438377604,
        53282654108756828443191190634694037855217779295145,
        36123272525000296071075082563815656710885258350721,
        45876576172410976447339110607218265236877223636045,
        17423706905851860660448207621209813287860733969412,
        81142660418086830619328460811191061556940512689692,
        51934325451728388641918047049293215058642563049483,
        62467221648435076201727918039944693004732956340691,
        15732444386908125794514089057706229429197107928209,
        55037687525678773091862540744969844508330393682126,
        18336384825330154686196124348767681297534375946515,
        80386287592878490201521685554828717201219257766954,
        78182833757993103614740356856449095527097864797581,
        16726320100436897842553539920931837441497806860984,
        48403098129077791799088218795327364475675590848030,
        87086987551392711854517078544161852424320693150332,
        59959406895756536782107074926966537676326235447210,
        69793950679652694742597709739166693763042633987085,
        41052684708299085211399427365734116182760315001271,
        65378607361501080857009149939512557028198746004375,
        35829035317434717326932123578154982629742552737307,
        94953759765105305946966067683156574377167401875275,
        88902802571733229619176668713819931811048770190271,
        25267680276078003013678680992525463401061632866526,
        36270218540497705585629946580636237993140746255962,
        24074486908231174977792365466257246923322810917141,
        91430288197103288597806669760892938638285025333403,
        34413065578016127815921815005561868836468420090470,
        23053081172816430487623791969842487255036638784583,
        11487696932154902810424020138335124462181441773470,
        63783299490636259666498587618221225225512486764533,
        67720186971698544312419572409913959008952310058822,
        95548255300263520781532296796249481641953868218774,
        76085327132285723110424803456124867697064507995236,
        37774242535411291684276865538926205024910326572967,
        23701913275725675285653248258265463092207058596522,
        29798860272258331913126375147341994889534765745501,
        18495701454879288984856827726077713721403798879715,
        38298203783031473527721580348144513491373226651381,
        34829543829199918180278916522431027392251122869539,
        40957953066405232632538044100059654939159879593635,
        29746152185502371307642255121183693803580388584903,
        41698116222072977186158236678424689157993532961922,
        62467957194401269043877107275048102390895523597457,
        23189706772547915061505504953922979530901129967519,
        86188088225875314529584099251203829009407770775672,
        11306739708304724483816533873502340845647058077308,
        82959174767140363198008187129011875491310547126581,
        97623331044818386269515456334926366572897563400500,
        42846280183517070527831839425882145521227251250327,
        55121603546981200581762165212827652751691296897789,
        32238195734329339946437501907836945765883352399886,
        75506164965184775180738168837861091527357929701337,
        62177842752192623401942399639168044983993173312731,
        32924185707147349566916674687634660915035914677504,
        99518671430235219628894890102423325116913619626622,
        73267460800591547471830798392868535206946944540724,
        76841822524674417161514036427982273348055556214818,
        97142617910342598647204516893989422179826088076852,
        87783646182799346313767754307809363333018982642090,
        10848802521674670883215120185883543223812876952786,
        71329612474782464538636993009049310363619763878039,
        62184073572399794223406235393808339651327408011116,
        66627891981488087797941876876144230030984490851411,
        60661826293682836764744779239180335110989069790714,
        85786944089552990653640447425576083659976645795096,
        66024396409905389607120198219976047599490197230297,
        64913982680032973156037120041377903785566085089252,
        16730939319872750275468906903707539413042652315011,
        94809377245048795150954100921645863754710598436791,
        78639167021187492431995700641917969777599028300699,
        15368713711936614952811305876380278410754449733078,
        40789923115535562561142322423255033685442488917353,
        44889911501440648020369068063960672322193204149535,
        41503128880339536053299340368006977710650566631954,
        81234880673210146739058568557934581403627822703280,
        82616570773948327592232845941706525094512325230608,
        22918802058777319719839450180888072429661980811197,
        77158542502016545090413245809786882778948721859617,
        72107838435069186155435662884062257473692284509516,
        20849603980134001723930671666823555245252804609722,
        53503534226472524250874054075591789781264330331690
        ]
    print("What are the first ten digits of the sum of the given 50-digit numbe"
          "rs?\n")

    answer = 0
    for n in nums:
        answer += n

    answer = str(answer)
    answer = answer[0:10]
    print(f"The answer is {answer}\n")
solutions.append(problem13)

def problem14():
    print("Find the positive integer less than 1,000,000 that yields the longes"
          "t chain of Collatz Conjecture numbers.\n")
    collatzIndex = {}
    collatzIndex[1] = 1
    record = 1
    answer = 0

    def collatz(n):
        # If we've already generated the sequence for this number, we're done. 
        if collatzIndex.get(n,-1) == -1 and n % 2:
            collatzIndex[n] = 1 + collatz(3*n+1)
        elif collatzIndex.get(n,-1) == -1:
            collatzIndex[n] = 1 + collatz(int(n/2))
        return collatzIndex[n]
    
    for i in range(1,1000001):
        r = collatz(i)
        record = max(record, r)
        if r == record:
            answer = i

    print(f"The answer is {answer}\n")

def problem14Alt():
    print("Find the positive integer less than 1,000,000 that yields the longes"
          "t chain of Collatz Conjecture numbers.\n")
    
    # Non-recursive, memory-light (I hope) approach:
    # Start with 1. The list of numbers that produces 1 is [1] 
    # Create a list to store the numbers that have a collatz length of 2
    # For each number in that list of 1, add the numbers that lead to it to the
    # list of numbers that have a length of 2. If the new list has more than one
    # number less than 1 million, iterate over the list of length 2 to produce
    # the list of length 3; etc... 
    length = 1
    lengthProducers = [1]
    finished = False
    answer = 0
    while not finished:
        newLength = length + 1
        newLengthProducers = []

        for lp in lengthProducers:
            if lp <= 0:
                continue
            newLengthProducers.append(2 * lp)
            newLengthProducers.append(int((lp - 1)/3))

        length = newLength
        lengthProducers = newLengthProducers

        contenders = 0
        for lp in lengthProducers:
            if lp < 1000000:
                contenders += 1
                answer = lp
        if contenders == 1:
            break
        elif contenders == 0:
            print("Some assumptions were made. Poorly. The next print is a lie")
            break

    print(f"The answer is {answer}\n")
solutions.append(problem14)

def problem15():
    print("How many legal routes exist through a 20x20 grid?\n")

    origin = (0,0)
    coordsSolved = {origin:1}
    def routesTo(coord):
        # You can't get to a place that doesn't exist
        if coord is None:
            return 0
        # If we haven't solved it before, we'll have to figure it out. 
        elif coordsSolved.get(coord,-1) == -1:
            coordUp = (coord[0],coord[1]-1) if coord[1] > 0 else None
            coordLt = (coord[0]-1,coord[1]) if coord[0] > 0 else None
            coordsSolved[coord] = routesTo(coordUp) + routesTo(coordLt)
        # Whether we solved it in this call or a previous one, it's stored here:
        return coordsSolved[coord]

    for i in range(20):
        r = routesTo((i,i))
        print(f"There are {r} ways to get to ({i},{i})")
    
    answer = routesTo((20,20))
    print(f"The answer is {answer}\n")
solutions.append(problem15)

def problem16():
    print("What is the sum of the digits of 2 raised to the 1000th power?\n")

    answer = 0
    num = math.pow(2,1000)
    num = int(num)
    for d in str(num):
        answer += int(d)
    print(f"The answer is {answer}\n")
solutions.append(problem16)

def problem17():
    print("How many letters are used to spell all the numbers in [1,1000]?")
    print("Note that spaces and hyphens are not counted, and there is an 'and' "
          "included after the hundreds place.\n")
    answer = 0

    first20 = ["zero","one","two","three","four","five","six","seven","eight",
               "nine","ten","eleven","twelve","thirteen","fourteen","fifteen",
               "sixteen","seventeen","eighteen","nineteen", "twenty"]
    tens = ["twenty","thirty","forty","fifty","sixty","seventy","eighty",
            "ninety"]

    def spell(n):
        if n == 0:                  # Don't *actually* spell 0; it's just there
            return ""               # for indexing.
        elif n == 1000:             # highest possible number, follows none of 
            return "onethousand"    # established rules
        elif n <= 20:
            return first20[n]
        elif n < 100:
            t = (n // 10) - 2
            o = n % 10
            return tens[t] + spell(o)
        else:
            h = n // 100
            to = n % 100
            return spell(h)+"hundred" + ("and" if to > 0 else "") + spell(to)

    for i in range(1,1001):
        s = spell(i)
        l = len(s)
        answer += l
        print(f"The number {i} is spelled '{s}' ({l} letters)")

    print(f"The answer is {answer}\n")
solutions.append(problem17)

def problem18():
    triangle = [
        [ 4, 62, 98, 27, 23,  9, 70, 98, 73, 93, 38, 53, 60,  4, 23],
        [63, 66,  4, 68, 89, 53, 67, 30, 73, 16, 69, 87, 40, 31],
        [91, 71, 52, 38, 17, 14, 91, 43, 58, 50, 27, 29, 48],
        [70, 11, 33, 28, 77, 73, 17, 78, 39, 68, 17, 57],
        [53, 71, 44, 65, 25, 43, 91, 52, 97, 51, 14],
        [41, 48, 72, 33, 47, 32, 37, 16, 94, 29],
        [41, 41, 26, 56, 83, 40, 80, 70, 33],
        [99, 65,  4, 28,  6, 16, 70, 92],
        [88,  2, 77, 73,  7, 63, 67],
        [19,  1, 23, 75,  3, 34],
        [20,  4, 82, 47, 65],
        [18, 35, 87, 10],
        [17, 47, 82],
        [95, 64],
        [75]
        ]

    for l in range(len(triangle)-1):   # l is for layer
        replacement = []
        for i in range(len(triangle[l])-1):
            # Find the maximal option that each node from the next layer could
            # pick. 
            replacement.append(max(triangle[l][i],triangle[l][i+1]))
        
        # 'replacement' is now equal to the next layer's length, and each 
        # element is the best element the next layer could have picked. So, if
        # we add each element from replacement to the next layer, that layer 
        # will have its value + the maximal value of all of the paths it could
        # have taken. 
        for i in range(len(replacement)):
            triangle[l+1][i] += replacement[i]
    
    print("What is the sum of the maximal path through the given triangle?\n")
    answer = triangle[-1][0]
    print(f"The answer is {answer}\n")
solutions.append(problem18)

def problem19():
    print("How many sundays fell on the first of the month during the 20th cent"
          "ury?\n")
    answer = 0
    # Maaaan. Eff time. 

    year = 1900
    month = 0
    day = 1
    dow = 1
                #   0  1  2  3  4  5  6  7  8  9  10 11           
                #   J  F  M  A  M  J  J  A  S  O  N  D
    monthlengths = [31,28,31,30,31,30,31,31,30,31,30,31]
    monthNames = ["  JANUARY",
                  "  FEBRUARY",
                  "  MARCH",
                  "  APRIL",
                  "  MAY",
                  "  JUNE",
                  "  JULY",
                  "  AUGUST",
                  "  SEPTEMBER",
                  "  OCTOBER",
                  "  NOVEMBER",
                  "  DECEMBER"]
    daysOfWeek = ["SUN","MON","TUE","WED","THU","FRI","SAT"]
    spaces = {"SUN":0, "MON":3, "TUE":6, "WED":9, "THU":12, "FRI":15, "SAT":18}

    cal = []
    while year <= 2000:
        cal.append((year,month,day,daysOfWeek[dow]))

        # Figure out the next day
        dow += 1 if dow != 6 else -6
        day = (day + 1) if day < monthlengths[month] else 1
        # Rolling over the month/year:
        if day == 1:
            month += 1 if month < 11 else -11
            if month == 0:
                year += 1
                if not year % 4 and (year % 100 or not year % 400):
                    monthlengths[1] = 29
                else:
                    monthlengths[1] = 28

    lastDay = (1899, 11, 31, "SUN")
    for d in cal:

        if d[0] != lastDay[0]:
            newyear = d[0]
            print(f"\n\n--------\n- {newyear} -\n--------\n")
        if d[1] != lastDay[1]:
            newmonth = d[1]
            print("\n\n" + monthNames[d[1]])
            print(" "*spaces[d[3]], end="")

        strNum = (" " if d[2] < 10 else "") + str(d[2])
        print(strNum, end=("\n" if d[3] == "SAT" else " "))


        answer += 1 if d[0] != 1900 and d[2] == 1 and d[3] == "SUN" else 0
        lastDay = d

    print(f"The answer is {answer}\n")
solutions.append(problem19)

def problem20():
    print("What is the sum of the digits of 100!?\n")
    answer = 0
    n = 1
    for i in range(1,101):
        n *= i
    n = str(n)
    for d in n:
        answer += int(d)
    print(f"The answer is {answer}\n")
solutions.append(problem20)

def problem21():
    print("What is the sum of all amicable numbers less than 10000?\n")
    answer = 0

    dLookup = {1:0} # 1 Has no proper divisors; it's the only natural number 
                    # with a single divisor, and that divisor is equal to itself
    def d(n):
        # Do it once
        if dLookup.get(n, -1) != -1:
            return dLookup[n]
        
        # All 'proper divisors' of n (IE: all divisors that are not n)
        pd = [] 
        
        # Find non-trivial divisors less than root(n). Don't include root(n) or
        # 1, because they would make the next step double count the root and 
        # include n itself, respectively.
        for i in range(2, int(math.sqrt(n))):
            if not n % i:
                pd.append(i)
        
        # For each non-trivial divisor, find its match:
        for d in pd.copy():
            pd.append(n//d)

        # *Now* we add 1 (and root(n) if it's a perfect square)
        pd.append(1)
        if int(math.sqrt(n)) == math.sqrt(n):
            pd.append(int(math.sqrt(n)))

        dLookup[n] = sum(pd)
        return dLookup[n]

    amicables = []
    # Initialize an index of numbers that we've determined to be amicable.
    for a in range(2, 10001):
        b = d(a)
        if d(b) == a and a not in amicables and a != b: 
            answer += a + b
            amicables.append(a)
            amicables.append(b)

    print(f"The answer is {answer}\n")
solutions.append(problem21)

#def problemX():
#    print("Problem Statement Goes Here\n")
#    answer = 0
#    print(f"The answer is {answer}\n")
#solutions.append(problemX)

# 'MAIN': Pick a Euler problem to see the solution. 
while True:
    try:
        cursor = int(input("Choose a problem to solve (0 to quit): "))
        if cursor:
            solve(cursor)
        else:
            print("\nGoodbye!\n")
            exit(0)
    except (ValueError, IndexError) as err:
        print(err)
        print("Invalid option\n")
        continue
