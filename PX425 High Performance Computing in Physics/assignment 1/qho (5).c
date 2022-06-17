/******************************************************************************

                            Online C Compiler.
                Code, Compile, Run and Debug C program online.
Write your code in this editor and press "Run" button to compile and execute it.

*******************************************************************************/

#include <stdio.h>
#include <stdlib.h>
#include <math.h>

double f(double x) // integrand, i.e. H3(x)^2 * exp(-x^2)
{
    return (8.0d*x*x*x - 12.0d*x)*(8.0d*x*x*x - 12.0d*x) * exp(-x*x);   
}

double x(int i, double a) // ith grid point (non-uniform)
{
    return a*i*i;
}

double h(int i, double a) // grid spacing
{
    return a*(2*i+1);
}
int main() // for some reason echo wasnt working properly. Entering the two inputs manually does work
{
    int imax = 0;
    double a = 0;
    scanf("%lf", &a);
    scanf("%d", &imax); // note, truncates to integer
    
    // input validation
    if (imax <= 0)
    {
        printf("invalid imax entered, escaping early");
        return -1;

    }
    else if (a <= 0.0d)
    {
        printf("invalid a entered, escaping early");
        return -1;
    }
    double sum = 0;
    int i=0;
    // approximates integral using composite Simpson's rule
    for(i=0;i<imax;i++) // note, the loop runs from i=0 to i=imax not imax/2-1. Conflicting definition of imax or N
    {
        double h2i = h(2*i, a); // h_(2i)
        double h2i1 = h(2*i+1, a); // h_(2i+1)
        // sum term
        sum += (h2i+h2i1)/6.0d * (  (2.0d-h2i1/h2i)*f(x(2*i,a))  +  (h2i+h2i1)*(h2i+h2i1)/(h2i*h2i1)*f(x(2*i+1,a))  +  (2.0d-h2i/h2i1)*f(x(2*i+2,a))  );
    }
    double pi = 3.14159265358979323846;
    double pi4 = pow(pi, -0.25);
    double A3 = pi4/sqrt(48.0d);
    
    double expected = 1.0d/(A3*A3); // 1/|An|^2
    double diff = expected - 2.0d*sum; // result is twice the integral approximated
    printf("Numerical integral:  %.17g\n",2.0d*sum);
    printf("Analytic integral:   %.17g\n",expected);
    printf("Difference (error):  %.17lf\n",diff); 
    return 0;
}
