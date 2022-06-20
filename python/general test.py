
###############################################################
# 1

# returns nth term of fibonacci sequence
# alternatively use nth term formula for O(1) complexity
def fibonacci(n): # O(n) time complexity
    if n == 1 or n==2:
        return 1
    elif n>2:
        a = 1
        b = 1
        for i in range(0,n-2):
            c = a + b
            a = b
            b = c
        return c
    else:
        return -1

#print(fibonacci(20)) # produces 6765 as expected


# returns sum of all terms even terms in fibonaci from 2 to n inclusive
# I believe the question wants every even number rather than every other term in the series.
# Note looking at the sequence, the numbers are even every 3 terms. This is due to the cyclic nature of odds & evens.
# i.e. odd + odd = even, odd + even = odd, even + odd = odd, odd + odd = even, ...
def sumFibEven(n):    
    total=0
    for even in range(3, n+1, 3):
        total += fibonacci(even)
    return(total)

#print(sumFibEven(12)) # returns 188 as expected


#################################################################################################
# 2 

# returns the intersection of two sorted arrays of integers
def intersect(arrayA, arrayB): # only for sorted arrays
    temp = []
    p=0
    for intB in arrayB: # compares every integer in arrayB to those in array A. Since the arrays are sorted, we can use 'p' to start the next loop from the current position in arrayA.
        for indexA in range(p,len(arrayA)):  
            if arrayA[indexA] == intB and (len(temp)==0 or intB != temp[-1]):
                temp.append(intB)
                p = indexA
                break # no point checking further since we ignore repeated integers
    return temp

#arrayA = [-1,2,3,3,4,7,12]
#arrayB = [-1,3,4,4,5,11,12]
#print(intersect(arrayA,arrayB)) # returns [-1,3,4,12] as expected


#################################################################################################
# 3

# returns boolean true if integer contains no odd digits else false
def checkNoOddDigits(integer): # converts integer to string to get each character and checks if they are odd/even
    string = str(integer)
    for char in string:
        if int(char) % 2 == 1:
            return False
    return True

#print(checkNoOddDigits(2846)) # returns True as expected

################################################################################################
# 4

# returns the sum of the digit X with XX, XXX and XXXX
def repeatedDigitSum(X):
    if X not in range(0,10):
        return -1
    else:
        total = 1234*X # i.e. 1234X = X + 11X + 111X + 1111X # i.e. 1111X = 1000X + 100X + 10X + X
        return total

#print(repeatedDigitSum(3)) # returns 3702 as expected
