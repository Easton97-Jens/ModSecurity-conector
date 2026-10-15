#define _GNU_SOURCE
#include <fcntl.h>
#include <stdio.h>
int main(void) { printf("%#x\n", O_NOFOLLOW); return O_NOFOLLOW == 0x20000 ? 0 : 1; }
