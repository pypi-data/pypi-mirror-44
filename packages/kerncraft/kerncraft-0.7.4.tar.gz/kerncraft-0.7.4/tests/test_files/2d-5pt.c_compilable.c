#include "kerncraft.h"
#include <stdlib.h>

void dummy(void *);
extern int var_false;
int main(int argc, char **argv)
{
  const int N = atoi(argv[2]);
  const int M = atoi(argv[3]);
  double *a = aligned_malloc((sizeof(double)) * (M * N), 32);
  double *b = aligned_malloc((sizeof(double)) * (M * N), 32);
  double s = 0.49795506534730005;
  for (int j = 1; j < (M - 1); ++j)
    for (int i = 1; i < (N - 1); ++i)
  {
    b[i + (j * N)] = 0.4150803324887108;
    a[(i - 1) + (j * N)] = 0.4150803324887108;
    a[(i + 1) + (j * N)] = 0.4150803324887108;
    a[i + ((j - 1) * N)] = 0.4150803324887108;
    a[i + ((j + 1) * N)] = 0.4150803324887108;
  }


  if (var_false)
  {
    dummy(a);
    dummy(b);
    dummy(&s);
  }

  for (int j = 1; j < (M - 1); ++j)
    for (int i = 1; i < (N - 1); ++i)
    b[i + (j * N)] = (((a[(i - 1) + (j * N)] + a[(i + 1) + (j * N)]) + a[i + ((j - 1) * N)]) + a[i + ((j + 1) * N)]) * s;


  if (var_false)
  {
    dummy(a);
    dummy(b);
    dummy(&s);
  }

}

