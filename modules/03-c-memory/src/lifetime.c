/* lifetime.c: global, heap, and stack lifetimes. The last case is a bug on purpose. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int counter;                                  /* lives for the whole run */

static int *make_local(void) {
    int local = 1234;
    return &local;                            /* BUG: the frame is gone after return */
}

static void clobber(void) {
    volatile int scratch[32];
    for (int i = 0; i < 32; i++)
        scratch[i] = 0x41414141;
}

int main(void) {
    int *heap = malloc(sizeof(int));
    *heap = 99;
    counter++;
    int *dangling = make_local();
    int first = *dangling;                   /* read before any other call reuses the stack */
    clobber();
    int second = *dangling;
    printf("heap block after other calls: %d, global counter: %d\n", *heap, counter);
    printf("dangling pointer, read before clobber(): %d, after: 0x%x\n", first, second);
    free(heap);
    return 0;
}
