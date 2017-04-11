#Cryptographic Musings

###To execute
For *AKS.cpp*:  
- `g++ AKS.cpp -lcln -o aks`
- `./aks.out`  
For *\*.py* files:  
- `python filename.py`  

###Notes
- **AKS.py**  
Implementation of the AKS primality testing algorithm in Python. This was pretty slow and hence a C++ implementation was also done. The link to the relevant paper <https://www.cse.iitk.ac.in/users/manindra/algebra/primality_v6.pdf>
- **AKS.cpp**  
Implementation of the AKS primality testing algorithm. It uses the `cln` library. Both the Python and the C++ implementations print out the polynomial from the loop.
- **BitCommit.py**  
This uses *Hash functions* to implement a commitment API (ensures *hiding* and *binding*). `commit(msg)` is a method which uses a hash function along with a length-k key and it outputs a result `com`. `verify(com, key, msg)` is a method which verifies the commited value. It achieves binding as follows. We hash the key and we hash the message. Then the hash of them both is concatenated and then hashed again which is the final commit *com*. If the key used is the same, then message cannot be changed, because if it is changed and we get the same output, it means the hash function is not collision free (as we get same output for two different inputs) - which is not true. It also reveals nothing as hashes are one-way. A helpful link <http://crypto.stackexchange.com/questions/6790/commitment-scheme-using-hash-functions>
- **BitCommitSigned.py**  
Extends `BitCommit.py` for cases where authentication of the commiter is required. The use-case scenario might be as follows: Suppose we have access to a committed value on a distributed server, we can verify the identity of the person who has commited the value using RSA based signatures (Sign and Hash protocols) Sign the commited value using the Private Key of the commiter and verify using his Public Key.
- **DHKeyExchange.py**  
Shows a step by step simulation of the *Diffie-Hellman Key Exchange*. Also shows how a *man in the middle attack* is possible.
- **DigiSignBdayAttack.py**  
Consider an organization with three roles: A, B and C. Whenever B has to issue some instruction to A, B has to take permission via C and only then will it be obeyed by A. This permission is issued with the help of a digital signature. A verifies the credibility of the message using C's public key (and digital signature), like any other digital signature scheme. The attack scenario is as follows. Consider a situation where B wants to issue any malicious instruction to A. Since a malicious message won't be signed by C, B has to find a clean message which generates the same signature (i.e. the same hash since if hash is the same, signature would be same) as that of the malicious message. Further, B will get the clean message signed by C with signature as σ and send (<malicious message>, σ) to A. So this program generates two messages `m1`, `m2` where m1 and m2 have the same hash value. One can be assumed to be a malicious message while the other is a clean message. Both should be valid English sentences and have different meanings for simulation purposes. This is a more constrainted version of the *Birthday attack*. Spaces, few commas, newlines and synonyms, etc when inserted into a message don't change its meaning. So this is used to generate new messages with the same hash. Different `length` parameters could be used in the definition of the hash function `hash_short`.
- **MsgHashGen.py**  
This is just a function which outputs the hash of two messages calculated from `DigiSignBdayAttack.py`.
- **MeetInTheMiddle.py**  
This solves the discrete log problem using meet in the middle attack. Let `g` be the generator of `Zp` and given a `h` in Zp such that `h = (g^x)mod(p)`, where `1 <= x <= 2^40`, find `x`. We write `x = i*(sqrt(p)) + j` where `i <= sqrt(p)` and `j <= sqrt(p)` where sqrt(p) is atmost `2^20`. The algorithm takes `O(sqrt(p))` space and `O(sqrt(p))` time. So we brute force over max(2^20) values instead of the original 2^40.
- **MillerRabin.py**  
This implements the Miller-Rabin primality testing algorithm. Also outputs the next nearest prime. For a *composite number*, it shows all the `strong liars` if it outputs `prime` and all the `strong witnesses` if it outputs `composite`.



