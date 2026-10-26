/* cstrings.c: a C string is bytes up to the first NUL. */
#include <stdio.h>
#include <string.h>

int main(void) {
    char a[] = "hello";                     /* 5 letters + NUL */
    char b[8] = "hi";                       /* the rest of the array is zero-filled */
    char c[] = {'h', 'e', 'y'};            /* no NUL: not a string */
    const char *d = "hello";               /* pointer to read-only data */

    printf("sizeof(a) = %zu, strlen(a) = %zu\n", sizeof(a), strlen(a));
    printf("sizeof(b) = %zu, strlen(b) = %zu\n", sizeof(b), strlen(b));
    printf("sizeof(c) = %zu (no NUL)\n", sizeof(c));
    printf("sizeof(d) = %zu (a pointer), strlen(d) = %zu\n", sizeof(d), strlen(d));
    printf("bytes of a:");
    for (size_t i = 0; i < sizeof(a); i++)
        printf(" %02x", (unsigned char)a[i]);
    printf("\n");
    a[2] = '\0';                            /* writing a NUL shortens the string; the bytes after it stay */
    printf("after a[2] = 0: strlen(a) = %zu, a = \"%s\", a + 3 = \"%s\"\n", strlen(a), a, a + 3);
    return 0;
}
