""" Euler

This script is a simple interface to run the solutions I've written for each
project Euler problem. It runs an infinite loop on the console, taking commands
in the form of the integer ID of a Project Euler problem, and runs the
solution I wrote for that problem. The program is terminated with an input of 0.

I imagine that in the future I'll need a wider respository for all the problems,
but for now (21 solutions written as of this writing) it's not unmanageable to 
store them all in a single script. 

Since Project Euler problems are solved by submitting single numeric values, the
solutions below aren't made very generically. I've taken some care to make them
a little more robust than a brute-force solution to a single problem, but I 
haven't come across a need to code the problems for generic input... yet :) 

More documentation effort is made for problems that actually gave me trouble, or
ones where the solution was less straight-forward. If there's less comments on a
solution, it was a pretty easy/straight-forward one. 
"""

import io
import math

class EulerUtils:
    """ A repository for functions that keep coming up. 
    """

    def __init__(self):
        # Initialize our listing of all of our known prime numbers. 
        self.primes = {}
        self.primesFile = open("Primes.txt", "r+")
        self.greatestPrime = 2
        for line in self.primesFile:
            self.primes[int(line)] = True
            self.greatestPrime = max(self.greatestPrime, int(line))
        self.primesList = list(self.primes.keys())
        self.primesList.sort()

    def divides(self, x, y):
        """Checks if a number x divides a second number, y. 

            Just a utility. "not y % x" is less imminently readable than 
            "divides(x, y)"
        """
        return x == y or not y % x

    def isPrime(self, n):
        """Checks if a number is prime using heuristics and dynamic programming

            The basic methodology to identify primes is to check if it takes the
            form of a prime number, allowing us to exclude all n that don't, and
            then for the n that do, we test it by iterating over the list of all
            prime numbers below it(s square root) to see if any of them divide 
            it. 

            To that end, I've been storing the list of numbers we've determined
            are prime and for each new problem, I've iterated up through all the
            numbers less than n. Since that's how we've been doing it from 
            scratch in each problem, it's time to start storing them for use in
            future problems (in a text file). 

            Args:
                n: The number to determine the primacy of. 
        """

        if n == 0 or n == 1:
            return False

        if self.primes.get(n, False):
            return self.primes[n]

        for p in self.primesList:
            if p > int(math.sqrt(n)+1):
                break
            if self.divides(p, n):
                return False
        return True
       

    def properDivisors(self, n):
        """ Returns a list of the proper divisors of n.

            A 'Proper Divisor' of n is any divisor of n that is less than itself

            Args:
                n: The number to find the proper divisors for. 
        """
        
        pd = [] # The list we're going to return.

        # Edge cases: 1 is the only natural number that has no proper divisors, 
        # because although every number has 1 as a divisor, 1 is the only one 
        # where 1 is not less than it. 4 can't search from 2 to its root 
        # (excluded) because 2 is it's root. 2 and 3 are fine, but if I'm hard-
        # coding 1 and 4, why not do 2 and 3? 
        if n == 1: 
            return pd
        elif n == 2 or n == 3: 
            return [1]
        elif n == 4: 
            return [1,2]

        # Grab the root; any divisor greater than the root is the quotient of n
        # and an earlier divisor already found
        root = int(math.sqrt(n))
        isSquare = root == math.sqrt(n)


        # Iterate from 2 to the root, finding all divisors up to that point.
        # We want to check up to the last whole number before the root. In cases
        # where the root is not a whole number, the integer casting of that root
        # is the last number we want to check, so we need to add 1 to it. But
        # when the integer casting is the same as the root (IE: if n is a 
        # perfect square), we can use it as the bound in the range function.
        for d in range(2,root + (1 if not isSquare else 0)):
            if self.divides(d, n):
                pd.append(d)

        # Find the complements of the divisors we found through iteration:
        for d in pd.copy():
            pd.append(n // d)

        # Now add 1 (we hadn't until this point because 1's complement is n, 
        # which is not a proper divisor) and the root (we also omitted this 
        # because it's its own complement, and we only want to include it once)
        pd.append(1)
        if isSquare: 
            pd.append(root)

        return pd

    def permutations(self, original):
        """ Generates all permutations of a string

            If in some kind of ordering, the final list of returned permutations
            will be in that same ordering as well. (IE: If you give it a word in
            alphabetical order, the resultant list of permutations will be 
            sorted in that same order as a consequence of the generation algo.

            Args:
                original: The string to create permutations for. 
        """

        def secretRecursion(orig, used, final):
            """ The actual method. It was dumb to elevate the used/final fields
                needed for the recursion/referencing, since in all cases the 
                base call is supposed to set those as empty lists. 
            """
            if len(used) == len(orig):
                final.append("".join(used))
                return
            
            select = orig.copy()
            for val in used:
                select.remove(val)

            for val in select:
                newUsed = used.copy()
                newUsed.append(val)
                secretRecursion(orig, newUsed, final)

        stringAsList = []
        for c in original:
            stringAsList.append(c)

        permsList = []
        secretRecursion(stringAsList, [], permsList)
        return permsList





eu = EulerUtils()         

def printTitle(title):
    """ Generic method for formatting and printing a header that looks nice in a 
        console. 

        The header is a series of '-' characters above, below, and to either
        side of the message being displayed. 

        Args: 
            title: The text to surround with dash ('-') characters.
    """

    headerfooter = "-"*(len(title)+6)
    print(f'{headerfooter}\n-- {title} --\n{headerfooter}\n')

solutions = []  # Stores the solution for each problem as a function to be 
                # called from the solve() function

def solve(problem):
    """ Takes a Euler Project problem number and executes the solution. 

    The solution to each problem is coded as a function with the name 'problemN'
    where N is the problem ID from the Project Euler website's archive. If a 
    problem hasn't been solved yet, this function will raise an IndexError. 
    """
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
    """ To get the smallest number divisible by all numbers n in a set, you 
        compile all prime factors of the numbers in the set, without including
        common factors amongst those numbers. 

        IE: Let's say you've added found factors up to 3: [2, 3]. You're going 
        to add the factors of 4 next. The factors between [2, 3] and [2, 2] have
        a 2 in common, so we don't add it, and instead get [2, 3, 2]. (Each 
        occurence counts as a distinct number). Simillarly, when you get to 6, 
        the sets are [2, 3, 2, 5] and [2, 3]. Since all factors of 6 are already
        included, you don't add anything here; the number 2*3*2*5 is already
        divisible by 6. 
    """
    print("What is the smallest positive number evenly divisible by all of the "
          "numbers from 1 to 20?\n")

    factors = [2]
    for i in range(3,21):
        n = i
        # Eliminate common factors by dividing n by every factor that divides it
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
    """ The 'trick' here is that in many (most) languages, ints are bound to a 
        few bytes. But Python is basically magic, and it takes a hell of a lot 
        to get it to overflow. This, and many problems to follow, are trivial in
        python, without any extra consideration. 
    """
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
            # definitionally finds all left-facing products (in reverse order)
            
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
        answer += n     # What overflow? Python is maaaaaaagic!

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
    """ We can just pretend this doesn't exist... I wanted to make it better,
        but I decidedly didn't. 
    """
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
    num = int(num)          # Maaaaaaaagic!
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
    # I entered the triangle upside-down here, because that's how I intended to
    # traverse it :) 
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

    # I spend way more time formatting the printing of a calendar to console 
    # than solving the problem. 
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
        n *= i              # MAGIC!!!
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

def problem22():
    print("What is the sum of all name scores (position in list * sum of each l"
          "etter's position in the alphabet) for the names in the given list?\n"
          )
    answer = 0
    
    # Input in the form of a file: 
    names = []
    with open("p022_names.txt") as f:
        for line in f:
            names = line.replace("\"","").split(",")
    names.sort()

    # Create Translation for letters to their score (1-indexed position in the 
    # english alphabet)
    lScoreOffset = 1 - ord("A")
    def letterScore(letter):
        return ord(letter) + lScoreOffset
    def wordScore(index, word):
        s = 0
        for l in word:
            s += letterScore(l)
        return s * index

    for i in range(len(names)):
        answer += wordScore(i+1, names[i])

    print(f"The answer is {answer}\n")
solutions.append(problem22)

def problem23():
    print("Find the sum of all the positive integers which cannot be written as"
          " the sum of two abundant numbers.\n")
    # An abundant number n is one in which the sum of its proper divisors is 
    # greater than n. All numbers greater than 28123 can be written as the sum 
    # of two abundant numbers. The greatest number than cannot be expressed as 
    # the sum of two abundant numbers is less than that; but not provided, and 
    # it weirdly can't be proven that the numbers between it and 28123 are all
    # able to be expressed as the sum of two abundant numbers. 

    # Find out if each number up to 28123 is abundant.
    abundants = {}
    for i in range(1, 28124):
        s = sum(eu.properDivisors(i))
        if s > i:
            abundants[i] = True

    answer = 0

    # Try each n, and for all abundant number a < n, see if (n-a) is abundant
    for n in range(1, 28124):
        foundA = False
        for a in abundants.keys():
            if a >= n:
                continue
            if abundants.get(n-a, False):
                foundA = True
                break
        answer += n if not foundA else 0

    print(f"The answer is {answer}\n")
solutions.append(problem23)

def problem24():
    print("What is the 1,000,000th lexicographic permutation of [0-9]?\n")

    def permutations(original):
        """ Generates all permutations of a string

            If in some kind of ordering, the final list of returned permutations
            will be in that same ordering as well. (IE: If you give it a word in
            alphabetical order, the resultant list of permutations will be 
            sorted in that same order as a consequence of the generation algo.

            Args:
                original: The string to create permutations for. 
        """

        def secretRecursion(orig, used, final):
            """ The actual method. It was dumb to elevate the used/final fields
                needed for the recursion/referencing, since in all cases the 
                base call is supposed to set those as empty lists. 
            """
            if len(used) == len(orig):
                final.append("".join(used))
                return
            
            select = orig.copy()
            for val in used:
                select.remove(val)

            for val in select:
                newUsed = used.copy()
                newUsed.append(val)
                secretRecursion(orig, newUsed, final)

        stringAsList = []
        for c in original:
            stringAsList.append(c)

        permsList = []
        secretRecursion(stringAsList, [], permsList)
        return permsList

    answer = permutations("0123456789")[999999]
    print(f"The answer is {answer}\n")
solutions.append(problem24)

def problem25():
    print("At which index is the first Fibonacci number to contain 1000 digits?"
          "\n")

    # I mean, we can just do the naive approach, because python is magic, right?
    
    # Time travel notes: I called this the 'naive' approach, because I 
    # remembered there being a trick to problems like this. But then I solved it
    # with dynamic programming, which I've been doing over and over, and which 
    # *was* the trick. 

    # Technically still magic, because 1000 digit ints are insane, actually. But
    # still. 
    fibonacciNumbers = {1:1, 2:1}
    def fibonacci(index):
        if fibonacciNumbers.get(index-1, -1) == -1:
            fibonacciNumbers[index-1] = fibonacci(index-1)
        return fibonacciNumbers[index - 1] + fibonacciNumbers[index - 2]

    answer = 3
    while len(str(fibonacci(answer))) < 1000:
        print(str(fibonacci(answer)))
        answer += 1

    print(f"The answer is {answer}\n")
solutions.append(problem25)

def problem26():
    print("What is the value of d < 1000 for which 1/d contains the longest rec"
          "urring cycle in its decimal fraction part?\n")
    # Quick refresher for my own edification: "Rational numbers" are the ones 
    # that eventually repeat. One of the definitions of rational numbers is that
    # they can be written as the quotient of two integers, so definitionally, 
    # this problem *isn't* trying to account for infinitely non-repeating 
    # numbers. 

    # Okay. Let's do this like I did it in elementary school!
    answer = 0
    maxPeriod = 0
    for d in range(1,1000):
        # Find a big enough number that you *can* divide into at least once.
        numerator = 10
        while d >= numerator:
            numerator *= 10

        # Remember every numerator you use, starting with this first one you 
        # just made. 
        numHistory = [numerator]
        unsure = True   # We're "unsure" if this is a cycle or not. 
        while unsure:
            # Get the result an remainder. 
            remainder = numerator % d
            
            # If there is no remainder, there's no cycle. We're just done. 
            if not d:
                sure = True
            else:
                numerator = remainder * numHistory[0]
                
                # This is how we know if we're in a cycle. If we are, we check
                # if it's a longer-period cycle than any we've found already and
                # maintain the record of the longest. 
                if numerator in numHistory:
                    unsure = False
                    period = len(numHistory) - numHistory.index(numerator)
                    maxPeriod = max(maxPeriod, period)    
                    answer = d if maxPeriod == period else answer
                else:
                    numHistory.append(numerator)

    floatAnswer = 1/answer
    print(f"The answer is {answer}, which caused a cycle of length {maxPeriod}."
          f" Check it out!\n1/{answer} = {floatAnswer}\n")
solutions.append(problem26)

def problem27():
    print("Find the product of the coefficients a and b such that n^2 + an + b "
          "(where |a| < 1000, and |b| <= 1000) that produces the maximum number"
          "of primes for consecutive values of n, starting with n = 0. \n")
    
    checked = {}
    answer = 0
    answerPrimes = 0
    for a in range(1000):
        for b in range(a, 1001):    # We've checked all numbers lower already
            
            n0 = 0
            while eu.isPrime(n0 * n0 + a * n0 + b):
                n0 += 1
            n1 = 0
            while eu.isPrime(n1 * n1 + a * n1 - b):
                n1 += 1
            n2 = 0
            while eu.isPrime(n2 * n2 - a * n2 + b):
                n2 += 1
            n3 = 0
            while eu.isPrime(n3 * n3 - a * n3 - b):
                n3 += 1

            if n0 > answerPrimes:
                answerPrimes = n0
                answer = a * b
                print(f"{answer}: {a} and {b} produced {answerPrimes} primes.")
            elif n1 > answerPrimes:
                answerPrimes = n1
                answer = a * (-b)
                print(f"{answer}: {a} and -{b} produced {answerPrimes} primes.")
            elif n2 > answerPrimes:
                answerPrimes = n2
                answer = (-a) * b
                print(f"{answer}: -{a} and {b} produced {answerPrimes} primes.")
            elif n3 > answerPrimes:
                answerPrimes = n3
                answer = (-a) * (-b)
                print(f"{answer}: -{a} and -{b} produced {answerPrimes} primes.")
    
    print(f"The answer is {answer}\n")
solutions.append(problem27)


def problem28():
    print("What is the sum of the numbers on the diagonals in a 1001x1001 spira"
          "l, starting from 1 and moving right in a clockwise fashion?\n")
    
    # Looks like the pattern is: Start from 1. Then add the first even number 
    # (2) 4 times, taking each number and adding it to the sum. Then add the 
    # second even number (4) 4 times and adding it to the sum. And so on, until 
    # the square is finished. 

    sides = 1001
    diagonals = [1]
    n = 2
    while(diagonals[-1] != sides * sides):
        for i in range(4):
            diagonals.append(diagonals[-1] + n)
        n += 2
    answer = sum(diagonals)
    print(f"The answer is {answer}\n")
solutions.append(problem28)


def problem29():
    print("How many distinct terms exist in a sequence generated from all integ"
          "er combinations a^b for 2 <=  a, b <= 100?\n")
    
    answer = 0
    terms = {}                  # Hashing means we won't get dupes. Do it naive
    for a in range(2, 101):
        for b in range(2, 101):
            terms[a ** b] = 1
            terms[b ** a] = 1
    answer = len(terms.keys())

    print(f"The answer is {answer}\n")
solutions.append(problem29)


def problem30():
    print("Find the sum of all the numbers that can be written as the sum of th"
          "e fifth powers of their digits.\n")

    # Okay. So. There are only 3 numbers that can be written as the sum of 
    # fourth powers of their digits: 1634, 8208, 9474. 
    # 
    # Why is that the case? Are the other combinations of the fourth powers of 
    # digits too big? 
    # 
    # for i in range(10):
    #     p = i ** 4
    #     print(f"{i}^4 = {p}")
    # 
    # The digits raised to 4th powers are: 
    # 
    # 0 - 0
    # 1 - 1
    # 2 - 16
    # 3 - 81
    # 4 - 256
    # 5 - 625
    # 6 - 1296
    # 7 - 2401
    # 8 - 4096
    # 9 - 6561
    #
    # In order for a number with a 9 in it to be considered, it must be larger
    # than 6461.
    # 
    # The numbers have to be larger than single digit numbers.  

    # Doing the same for fifth powers: 
    # 
    # 0^5 = 0
    # 1^5 = 1
    # 2^5 = 32
    # 3^5 = 243
    # 4^5 = 1024
    # 5^5 = 3125
    # 6^5 = 7776
    # 7^5 = 16807
    # 8^5 = 32768
    # 9^5 = 59049
    # 
    # If we had a number 999,999 the sum would be 354,294, so we'd have 
    # overshot. So there's a soft limit... 
    
    # Give us a lookup by digit:
    lookup = {}
    for i in range(10):
        lookup[i] = i ** 5
        
    # Brute Force it:
    answer = 0
    for n in range(2,354295):
        sn = str(n)          
        sum = 0
        for digit in sn:
            i = int(digit)
            sum += lookup[i]
        if sum == n:
            answer += sum
    
    print(f"The answer is {answer}\n")
    #... I'm not proud of this one. 
solutions.append(problem30)


def problem31():
    print("How many ways can you make 2 dollars with any number of the followin"
          "g coins: $2, $1, $0.5, $0.2, $0.1, $0.05, $0.02, $0.01\n")
    
    knowns = {}
    dontchecks = {}

    def setValue(set):
        return set[0] + set[1] * 2 + set[2] * 5 + set[3] * 10 + set[4] * 20 + \
            set[5] * 50 + set[6] * 100 + set[7] * 200

    def findSets(s):
        # Base cases: we've been here before, or it is 200. 
        if dontchecks.get(s, False):
            return
        elif setValue(s) == 200:
            knowns[s] = True
            dontchecks[s] = True
            return
        elif setValue(s) > 200: # Technically, we "don't need to check" this one
            return              # again either, but it's also just a stop point. 

        # If we get here, we haven't been here before, and it's not 200. Don't 
        # come back:
        dontchecks[s] = True

        # If we get here, we are less than 200. Let's search every version of 
        # ourself with one more of each coin, and then we're done. 
        findSets((s[0]+1, s[1], s[2], s[3], s[4], s[5], s[6], s[7]))
        findSets((s[0], s[1]+1, s[2], s[3], s[4], s[5], s[6], s[7]))
        findSets((s[0], s[1], s[2]+1, s[3], s[4], s[5], s[6], s[7]))
        findSets((s[0], s[1], s[2], s[3]+1, s[4], s[5], s[6], s[7]))
        findSets((s[0], s[1], s[2], s[3], s[4]+1, s[5], s[6], s[7]))
        findSets((s[0], s[1], s[2], s[3], s[4], s[5]+1, s[6], s[7]))
        findSets((s[0], s[1], s[2], s[3], s[4], s[5], s[6]+1, s[7]))
        findSets((s[0], s[1], s[2], s[3], s[4], s[5], s[6], s[7]+1))
        return

    nocoinset = (0, 0,  0,  0,  0, 0, 0, 0)
    findSets(nocoinset)
    answer = len(knowns.keys())
    print(f"The answer is {answer}\n")
solutions.append(problem31)


def problem32():
    print("Find the sum of all products whose multiplicand/multiplier/product i"
          "dentity can be written as 1 through 9 pandigital.\n")

    # Some reasoning: 
    # 
    # No multiplicand can be 1, as the multiplier would be equal to the product,
    # resulting in double use of the numbers. 
    # 
    # No zeroes appear in any of the problem statement; I'm confidently assuming
    # they won't be incorporated in any of the results. 
    # 
    # The largest pandigital 1 through 9 number is 987654321
    #
    # We have 8 spaces that partition a set of 9 numbers such that you have 
    # at least one digit on either side of the partition:
    # 
    # 9_8_7_6_5_4_3_2_1
    # 
    # We want to choose 2 non-adjacent partitions.
    partitions = []
    for i in range(8):
        for j in range(i+2, 8):
            partitions.append((i,j))
            p = len(partitions)

    # Next we want to apply those partitions to each permutation of 987654321. 
    # We'll revisit the function we made in problem 24. I've copied it into 
    # EulerUils:
    permutations = eu.permutations("987654321")

    # After we have all permutations of 987654321, and all of the indices we 
    # need to partition them into sets of three numbers each with at least one 
    # digit, we can validate those that are actual multiplicand/multiplier/
    # product identities. If we store them in a dictionary where the key is the
    # product, then we won't get those duplicate pairings we were warned about
    # in the question description; we'll overwrite them instead. Since we just
    # want to sum the products, this is fine. 
    #
    # Side note, this is probably one of the more inefficient ways of doing this
    # given that there turns out to be 7 identities and we are searching 21 * 
    # ~380,000 permutations. But (if you're not debugging,) it's quick enough.
    pandigitalIdentities = {}
    for perm in permutations:
        for part in partitions:

            # messy substring carving, but essentailly the positons in the 
            # partitions are one less than their index within the string. 
            multiplicand = int(perm[0:part[0]+1])
            multiplier = int(perm[part[0]+1:part[1]+1])
            product = int(perm[part[1]+1:])
            
            if multiplicand * multiplier == product:
                pandigitalIdentities[product] = (multiplicand, multiplier)

    answer = sum(pandigitalIdentities.keys())
    print(f"The answer is {answer}\n")
solutions.append(problem32)


def problem33():
    print("Find the value of the denominator of the product of the four 'curiou"
          "s fractions' given in its lowest common terms\nThe four curious frac"
          "tions are those that are less than 1 in value, consisting of two-dig"
          "it numbers in the numerator and denominator, that can be accurately "
          "reduced by incorrectly cancelling out a digit that appears in both. "
          "49/98, for instance, reduces to 4/8, but not because you can cancel "
          "out the nines. To get the answer, find the other 3. \n")

    digits = [1,2,3,4,5,6,7,8,9]    # 0 cases are trivial
    for i in range(10,100):
        for j in range(i+1,100):
            for d in digits:
                sd = str(d)
                si = str(i)
                sj = str(j)
                if si.find(sd) != -1 and sj.find(sd) != -1:
                    si = si.replace(sd, "", 1)
                    sj = sj.replace(sd, "", 1)

                    ii = int(si)
                    ij = int(sj)
                    if ij == 0:
                        continue

                    x = max(ii/ij, i/j)
                    n = min(ii/ij, i/j)
                    if x - n < 0.00000001 and x < 1:
                        print(f"{i}/{j} = {si}/{sj}")
            
            
    # Since it's 4 items, and I don't want to find a generic solution for 
    # simplifying fractions:
    print("\nThe product is 8/800, or 1/100.\n\nErgo, the answer is 100.")
solutions.append(problem33)


def problem34():
    print("Find the sum of all numbers which are equal to the sum of the factor"
          "ial of their digits.\n")

    # I hate these. 
    # 
    # So we'll start by figuring out the terms we'll be summing.
    factorialLookup = {0:1}
    for i in range(1,10):
        f = 1
        for n in range(i, 1, -1):
            f *= n
        factorialLookup[i] = f
        print(f"{i}! = {f}")

    # So any number that qualifies that has a 9 within it has to be larger than
    # 362880. A six-digit number consisting only of 9s would have a sum higher 
    # than 2 million, so it's safe to say that all of the numbers that have this
    # property have 6 or fewer digits at most... right? 
    answer = 0
    for i in range(3, 999999):  # skip 2, 1.
        si = str(i)
        f = 0
        for d in si:
            f += factorialLookup[int(d)]
        if f == i:
            answer += i

    print(f"The answer is {answer}\n")
solutions.append(problem34)

def problem35():
    print("How many circular primes are there below one million?\n")

    print(eu.isPrime(1000000))

    print(eu.isPrime(5))
    print(eu.isPrime(7))

    answer = 0
    for p in eu.primes.keys():
        if p >= 100:
            continue

        sp = str(p)
        iupg = True
        for i in range(len(sp)):
            spv = sp[i:] + sp[0:i]
            if not eu.isPrime(int(spv)):
                iupg = False
        if iupg:
            print(f"{sp} is a circular prime.")
            answer += 1



    print(f"The answer is {answer}\n")
solutions.append(problem35)

def problem36():
    print("Find the sum of all numbers less than one million which are palindro"
          "mic in both base 10 and base 2.\n")

    # The stipulation that in either base, the number may not include leading 
    # zeroes means that it cannot be divisible by 10 or by 2. So we can narrow
    # our search off of that. 

    def binary(n):

        if not n: return "0"

        wipn = n
        bstr = ""
        for exp in range(19,-1,-1): # All nums less than 1m are less than 2^20
            if wipn >= 2 ** exp:    # If n >= 2^exp, then it includes that digit
                bstr += "1"
                wipn -= 2 ** exp
            elif wipn == n:         # If it isn't bigger, AND we haven't done 
                bstr += ""          # anything to it yet, then this is leading 0
            else:
                bstr += "0"
        return bstr

    def pallindromic(s):
        halfLen = len(s) // 2
        for i in range(halfLen):
            complement = (-1 * i) - 1
            if s[i] != s[complement]:
                return False
        return True

    answer = 0
    for i in range(1, 1000000, 2):  # No even number is pallindromic in binary. 
        if pallindromic(str(i)) and pallindromic(binary(i)):
            print(f"{i} and {binary(i)} are both pallindromic.")
            answer += i

    print(f"The answer is {answer}\n")
solutions.append(problem36)

def problem37():
    print("Find the sum of the 11 primes that are truncatable from left to righ"
          "t and vice versa. \n")
    
    def check(p, dir):

        if p <= 7: return False

        sp = str(p)
        start = 1 if not dir else -1
        end = len(sp) if not dir else -1 * len(sp)
        step = 1 if not dir else -1
        for i in range(start, end, step):
            spt = sp[i:] if not dir else sp[:i]
            if not eu.isPrime(int(spt)):
                return False
        return True

    answer = 0
    counter = 0
    for p in eu.primes.keys():
        answer += p if check(p, 0) and check(p,1) else 0
        if check(p, 0) and check(p,1):
            counter += 1
            print(f"{counter}:\t{p} is one of the primes.")
                
    print(f"The answer is {answer}\n")
solutions.append(problem37)

def problem38():
    print("What is the largest pandigital 9-digit number that can be formed as "
          "the concatenated product of an integer with (1, 2, ..., n) where n >"
          " 1?\n")

    def isPandigital(n):
        sn = str(n)
        digits = [1,2,3,4,5,6,7,8,9]

        if len(sn) != len(digits):
            return False

        for d in digits:
            sd = sn.replace(str(d), "")
            if len(sd) != len(sn) - 1:
                return False
        return True

    # Since the number is 9 digits long, and the multiplication will give us n
    # terms of at least 1 digit, our largest theoretical tuple is where n = 9. 
    # That one can only be multiplied by 1 to get us the pandigital 123456789, 
    # and we know that the example case is larger than that. So n is at most 8
    # (put it's probably lower). 
    #
    # We also know that the smallest tuple is (1, 2) (or maybe (1, 2, 3)?). 
    # 
    # Because the first number is always 1, we know that the first l digits will
    # consist of the digits of the integer (whose length is l). We also know 
    # that none of the digits in the tuple is greater than 9, meaning that we 
    # can't produce a product with any one multiplication larger than a number 
    # with length l + 1. 
    #
    # So I think that means that the largest the integer can be is 4 digits. 
    # The smallest tuple we can multiply by consists of 2 numbers, and one of 
    # the products will always produce a l digit number. Since the final product
    # will have 9 digits, and it has to be the concatenation of two numbers, it
    # will have to be produced by a 4 digit integer i where 2i is a 5 digit 
    # number.
    #
    # We could theoretically reign in this scope a bit more by carrying on that
    # train of thought (IE: in order for n to be 8, then the integer would have 
    # to be such that only multiplying it by 8 would get you a two digit number,
    # which is probably impossible, and probably excludes that case), ~10,000 *
    # the 7 possible tuples  is easily searched in brute force. 
    tuples = [(1, 2), (1, 2, 3), (1, 2, 3, 4), (1, 2, 3, 4, 5), 
              (1, 2, 3, 4, 5, 6), (1, 2, 3, 4, 5, 6, 7), 
              (1, 2, 3, 4, 5, 6, 7, 8)
              ]

    answer = 0
    generator = []
    for t in tuples:
        for i in range(10000):
            result = ""
            for n in t:
                result += str(n*i)
            if isPandigital(int(result)):
                answer = max(answer, int(result))
                if answer == int(result):
                    generator = [i, t]

    print(f"The answer is {answer}\nIt was generated by: {generator[0]} - "
          f"{generator[1]}")
solutions.append(problem38)

def problem39():
    print("For which permieter value p <= 1000 are there the most possible righ"
          "t angle triangles with integral side lengths [a, b, c] such that a +"
          " b + c = p?\n")

    def generateTriplets(p):
        triplets = {}
        for i in range(1, p-1):
            for j in range(1, ((p-i)//2+1)):
                triplet = [i, j, p-i-j]
                triplet.sort()
                triplets[triplet[0],triplet[1],triplet[2]] = True
        retList = []
        for t in triplets:
            retList.append(t)
        return retList
     
    maxTriplets = 0
    answer = 0
    for i in range(3,1001):
        triplets = generateTriplets(i)
        for t in triplets.copy():
            if t[0] ** 2 + t[1] ** 2 != t[2] ** 2:
                triplets.remove(t)
        if len(triplets) > maxTriplets:
            maxTriplets = len(triplets)
            answer = i

    print(f"The answer is {answer}, with {maxTriplets} solutions.\n")
solutions.append(problem39)

def problem40():
    print("The irrational decimal fraction IDF is created by concatenating the "
          "positive integers from 1 to infinity. If dn is the nth digit of IDF,"
          "what is the value of the product d1 * d10 * d100 * d1000 * d10000 * "
          "d100000 * d1000000?\n")
    answer = 0

    # So the first nine digits d1 through d9 are equal to n. 
    #
    # Then the next 20 digits alternate between 1, and the next digit. The 20 
    # after that alternate between 2, and the next digit. And so on until the 
    # 9 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 1 = 191st digit. 

    # ... sanity check: Python is magic right? 
    string = "1"
    i = 2
    while(len(string) < 1000000):
        string += str(i)
        i += 1
    answer = int(string[0]) * int(string[9]) * int(string[99]) * \
        int(string[999]) * int(string[9999]) * int(string[99999]) * \
        int(string[999999])
    print(f"The answer is {answer}\n")
    # Yup. Python is magic. 
solutions.append(problem40)

def problem41():
    print("What is the largest n-digit pandigital prime?\n")

    # For posterity, I've preserved my brute force solution in these comments.
    # But in looking up what was wrong with my solution (see "NOTE FROM THE
    # FUTURE" below), I learned that a very valuable heuristic I learned in 
    # grade school actually prunes the scope really well. All numbers divisible
    # by 3 are such that their digits equal a multiple of three. All pandigital 
    # numbers with n-digits have the same sum of digits. Therefore:
    # 
    # 9+8+7+6+5+4+3+2+1 = 45    -> So none of them are prime
    # 8+7+6+5+4+3+2+1 = 36      -> So none of them are prime
    # 7+6+5+4+3+2+1 = 28        -> So one *could* be prime; so start with n=7.

    # So in the worst case scenario, none of the 9-digit pandigital numbers are
    # prime. In which case we'll need to check the 8-digit ones, and if none of
    # those are prime, we'll need to check the 7 digit ones, etc...
    n = 7
    answer = 0
    while n > 1: 
        pandigitalSeed = ""
        for i in range(n, 0, -1):
            pandigitalSeed += str(i)
        nDigitPandigitals = eu.permutations(pandigitalSeed)

        # Now we want to search all of them to see which one is the largest 
        # prime. I believe they're in reverse order, so lets iterate backwards:
        #
        # NOTE FROM THE FUTURE: 
        # I'm a dumbass. They *are* in reverse order... so we need to iterate 
        # forwards. 
        for i in range(len(nDigitPandigitals)):
            if eu.isPrime(int(nDigitPandigitals[i])):
                answer = nDigitPandigitals[i]
                break

        if answer == 0:
            n -= 1
        else:
           n = 0

    print(f"The answer is {answer}\n")
solutions.append(problem41)

def problem42():
    print("How many words in the provided list are 'triangle-words'?\n")
    answer = 0

    # The triangle numbers are 1/2*n*(n+1). 
    # The highest possible score a word will get is (max number of letters) * 
    # 26. 
    # So once we've read the word list, we can track it's max length, and then
    # use that to cap our triangle numbers. 

    # Input in the form of a file: 
    words = []
    with open("p042_words.txt") as f:
        for line in f:
            words = line.replace("\"","").split(",")
    words.sort()

    # Create Translation for letters to their score (1-indexed position in the 
    # english alphabet) (Copied from problem 22. If we have to do it again, it's
    # going into EulerUtils. 
    lScoreOffset = 1 - ord("A")
    def letterScore(letter):
        return ord(letter) + lScoreOffset
    def wordScore(word):
        s = 0
        for l in word:
            s += letterScore(l)
        return s
    def triangleNum(n):
        return n*(n+1) // 2

    # Now we can process the words. 
    maxLen = 0
    scores = {}
    for word in words:
        # Track the biggest word
        if len(word) > maxLen:
            maxLen = len(word)
        scores[word] = wordScore(word)

    triangleNums = []
    maxTriangleNum = maxLen * 26
    n = 1
    while triangleNum(n) < maxTriangleNum:
        triangleNums.append(triangleNum(n))
        n += 1

    for word in words:
        if scores[word] in triangleNums:
            answer += 1
    
    print(f"The answer is {answer}\n")
solutions.append(problem42)

def problem43():
    print("Find the sum of all 0 to 9 pandigital numbers with the property laid"
          " out in the problem statement.\n")

    # The rule: d2d3d4 is divisible by 2, d3d4d5 is divisible by 3, d4d5d6 is 
    # divisible by 5, and then the subsequent dn+1,dn+2,dn+3 are divisible by
    # 7, 11, 13, 17

    answer = 0
    divisibility = [2,3,5,7,11,13,17]
    pandigitals = eu.permutations("9876543210")
    #pandigitals = ["1406357289"]    # Test Case
    for p in pandigitals:
        i = 1
        provenTrue = True
        for d in divisibility:
            num = int(p[i:i+3])
            i += 1
            if not eu.divides(d, num):
                provenTrue = False
                break
        if provenTrue:
            answer += int(p)


    print(f"The answer is {answer}\n")
solutions.append(problem43)

def problem44():
    print("Find the pair of pentagonal numbers Pj and Pk, for which their sum a"
          "nd difference are pentagonal and D = |Pk-Pj| is minimised, and provi"
          "de the value of D.\n")
    answer = 0

    # Pentagonal numbers are generated by: Pn = n(3n-1)/2.
    pentagonals = {}
    for n in range(1,10000):
        pentagonals[(3*n*n-n)//2] = True

    print()
    pentagonalsList = list(pentagonals.keys())
    for i in range(len(pentagonals.keys())):
        for j in range(i+1, len(pentagonals.keys())):
            s = pentagonalsList[i] + pentagonalsList[j]
            d = pentagonalsList[j] - pentagonalsList[i]
            if pentagonals.get(s, False) and pentagonals.get(d, False):
                answer = d
                print(f"The answer is {answer}\n")
                return
solutions.append(problem44)

def problem45():
    print("Find the next number after 407555 that is a triangle, pentagonal and"
          " a hexagonal number.\n")

    pents = {}
    hexes = {}
    for n in range(1,100000):       # These bounds are guesses
        pents[(n*3*n-n)//2] = True
        hexes[(n*2*n-n)] = True

    for n in range(286, 1000286):   # These bounds are guesses
        t = (n*n+n)//2
        if pents.get(t,False) and hexes.get(t,False):
            print(f"The answer is {t}\n")
            return
solutions.append(problem45)

def problem46():
    print("What is the smallest odd composite that cannot be written as the sum"
          "of a prime and twice a square?\n")

    # Starting to notice a pattern in these problems lately. We're going to go
    # with arbitrary bounds to get our squares list. The first 10000 squares 
    # should give us room to find the number :) 
    squares = []
    for i in range(10000):
        squares.append(i*i)

    primseLookup = eu.primes
    primesList = eu.primesList

    oddComp = 33    # The last one given in the example
    while True:
        oddComp += 2
        proven = True
        if not primseLookup.get(oddComp, False):
            # It *is* an odd composite. 
            for p in primesList:
                if p > oddComp:
                    break
                for s in squares:
                    if 2 * s + p > oddComp:
                        break
                    if p + 2*s == oddComp:
                        proven = False
                        break
                
            if proven:
                print(f"The answer is {oddComp}")
                return
solutions.append(problem46)

def problem47():
    print("What is the first of the first four consecutive numbers to have four"
          " distinct prime factors?\n")

    n = 4
    consec = 0
    primes = eu.primesList
    while True:

        if n == 644:
            print("Holup")


        alterable_n = n
        primeFactors = []
        for p in primes:
            if p > alterable_n:
                break
            while eu.divides(p, alterable_n):
                if p not in primeFactors:
                    primeFactors.append(p)
                alterable_n //= p

        if len(primeFactors) == 4:
            consec += 1
        else:
            consec = 0
        if consec == 4:
            print(f"The answer is {n-3}\n")
            return
        n += 1
solutions.append(problem47)

def problem48():
    print("Find the last ten digits of the series 1^1+2^2...1000^1000\n")
    s = 0
    for i in range(1,1001):
        s += i ** i
    answer = str(s)[-10:]
    print(f"The answer is {answer}\n")
solutions.append(problem48)

def problem49():
    print("What 12-digit number is formed by concatenating the three terms in t"
          "he sequence specified in the problem statement?\n")
    answer = 0

    def id(p):
        r = [p[0], p[1], p[2], p[3]]
        r.sort()
        return int(r[0]) * 1000 + int(r[1]) * 100 + int(r[2]) * 10 + int(r[3])

    # 4-digit primes, permutations of each other, in increasing order

    fourdigitprimes = []
    for p in eu.primesList:
        if p < 1000:
            continue
        elif p > 9999:
            break
        fourdigitprimes.append(p)

    for i in range(len(fourdigitprimes)):
        pStarter = fourdigitprimes[i]
        buddies = []
        for j in range(i+1, len(fourdigitprimes)):
            if id(str(pStarter)) == id(str(fourdigitprimes[j])):
                buddies.append(fourdigitprimes[j])
        if len(buddies) == 2:
            if buddies[1] - buddies[0] == buddies[0] - pStarter:
                print(f"The answer is {pStarter}{buddies[0]}{buddies[1]}")
                return
solutions.append(problem49)


def problem50():
    print("Which prime, below one-million, can be written as the sum of the mos"
          "t consecutive primes? \n")
    
    bound = 1000000
    answer = (0,0)
    primes = eu.primes
    primesList = eu.primesList
    i = 0
    for i in range(len(primesList)):
        if primesList[i] > bound:
            break
        first = primesList[i]
        runningSum = primesList[i]
        for j in range(i+1, len(primesList)):
            runningSum += primesList[j]
            if runningSum > bound:
                break
            if eu.isPrime(runningSum) and j-i+1 > answer[1]:
                answer = (runningSum, j-i+1)
                print(f"Current Contender: {answer[0]} from {first} through the"
                      f" next {answer[1]} primes.")

    print(f"The answer is {answer}\n")
solutions.append(problem50)


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
