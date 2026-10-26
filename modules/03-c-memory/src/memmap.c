/* memmap.c: where do globals, locals, heap blocks, code, and constants live? */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

int initialized = 42;          /* .data  */
int uninitialized;             /* .bss   */
const char literal[] = "constant text";   /* read-only data */

static void here(void) {}

int main(int argc, char **argv) {
    int local = 7;
    int *block = malloc(64);
    printf("pid          %d\n", getpid());
    printf("code         %p  (function here)\n", (void *)here);
    printf("rodata       %p  (const array literal)\n", (const void *)literal);
    printf("data         %p  (initialized global)\n", (void *)&initialized);
    printf("bss          %p  (uninitialized global)\n", (void *)&uninitialized);
    printf("heap         %p  (malloc(64))\n", (void *)block);
    printf("stack        %p  (local in main)\n", (void *)&local);
    printf("libc         %p  (function printf)\n", (void *)printf);
    if (argc > 1 && strcmp(argv[1], "--pause") == 0) {
        printf("paused: inspect this process from another terminal, then press Enter here.\n");
        fflush(stdout);
        getchar();
    }
    free(block);
    return 0;
}
