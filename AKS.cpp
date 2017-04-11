#include <iostream>
#include <vector>
#include <cln/integer.h>
#include <cln/real.h>
#include <cln/real_io.h>
#include <cln/integer_io.h>
#include <cln/io.h>
#include <cln/input.h>

using namespace std;
using namespace cln;

typedef vector<cl_I> Polynomial;

cl_I order(cl_I r, cl_I n){
	cl_I order = 3;
	while(true){
		if(mod(expt_pos(n, order), r) == 1)
			return order;
		order += 1;
	}
}

cl_I totient(cl_I n){
	cl_I totient;
	for(cl_I i = 1; i < n + 1; i += 1){
		if(gcd(n, i) == 1)
			totient += 1;
	}
	return totient;
}

Polynomial poly_mult_with_mod(Polynomial a, Polynomial b, cl_I r, cl_I n){
	Polynomial product(cl_I_to_ulong(r));
	for(unsigned long long i = 0; i < a.size(); i += 1)
		for(unsigned long long j = 0; j < b.size(); j += 1)
			product[(i + j) % cl_I_to_ulong(r)] = mod(product[(i + j) % cl_I_to_ulong(r)] + (a[i] * b[j]), n);
	return product;
}

Polynomial poly_mod_exp(cl_I a, cl_I r, cl_I n){
	Polynomial xplusa(cl_I_to_ulong(r)), modexp(cl_I_to_ulong(r));
	xplusa[0] = a;
	xplusa[1] = 1;
	modexp[0] = 1;
	unsigned long long power = cl_I_to_ulong(n);
	while(power > 0){
		if(power & 1){
			modexp = poly_mult_with_mod(modexp, xplusa, r, n);
		}
		xplusa = poly_mult_with_mod(xplusa, xplusa, r, n);
		power /= 2;
	}
	return modexp;
}

int main(){
	cl_I n, sqrtn;
	cout<<"Enter an integer > 1 "<<endl;
	cin>>n;
	isqrt(n, &sqrtn);
	// step 1 - checking n == a**b
	for(cl_I a = 2; a < sqrtn + 1; a += 1){
		cl_I num = a;
		for(cl_I b = 2; b < n; b += 1){
			num = num*a;
			if(num == n){
				cout<<"Composite\n";
				return 0;
			}
			else if(num > n)
				break;
		}
	}

	// step 2 - finding smallest r
	cl_R logn = log(n, 2);
	cl_R logsquaredn = (logn)*(logn);
	cl_I r = 3;
	while(true){
		if(gcd(n, r) == 1 && order(r, n) >= logsquaredn)
			break;
		r += 1;
	}

	// step 3 check if 1 < (a, n) < n
	for(cl_I a = 2; a < r + 1; a += 1){
		if(1 < gcd(a, n) && gcd(a, n) < n){
			cout<<"Composite\n";
			return 0;
		}
	}

	// step 4 if n <= r, output prime
	if(n <= r){
		cout<<"Prime\n";
		return 0;
	}

	// step 5 loop iterations to check compositeness
	cl_I termcondtn = floor1(sqrt(totient(r)) * logn);
	for(cl_I a = 1; a <= termcondtn; a += 1){
		cout<<"a: "<<a<<endl;
		Polynomial xplusapown(cl_I_to_ulong(r)), xnplusa(cl_I_to_ulong(r));
		xplusapown = poly_mod_exp(a, r, n);
		xnplusa[cl_I_to_ulong(mod(n, r))] = mod(xnplusa[cl_I_to_ulong(mod(n, r))] + 1, n);
		xnplusa[0] += mod(xnplusa[0] + a, n);

		for(unsigned long i = 0; i < cl_I_to_ulong(r); i++){
			if(i < r-1 && xplusapown[i] != 0)
				cout<<xplusapown[i]<<"x^"<<i<<" ";
			else if(xplusapown[i] != 0)
				cout<<xplusapown[i]<<"x^"<<i;
		}
		cout<<endl;

		for(unsigned long i = 0; i < cl_I_to_ulong(r); i++){
			if(xplusapown[i] != xnplusa[i]){
				cout<<"Composite\n";
				return 0;
			}
		}
	}

	// step 6 output prime
	cout<<"Prime\n";
	return 0;
}