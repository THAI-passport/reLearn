/* overflow.c: an off-by-one write past a heap buffer. Build with -fsanitize=address. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(void) {
    const char *name = "reverse";            /* 7 letters, 8 bytes with the NUL */
    char *copy = malloc(strlen(name));        /* BUG: forgot the byte for the NUL */
    strcpy(copy, name);
    printf("copy = %s\n", copy);
    free(copy);
    return 0;
}
