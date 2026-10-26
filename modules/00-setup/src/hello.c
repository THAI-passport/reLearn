#include <stdio.h>

/* TOKEN is injected at build time by build.py so the answer is unique per learner. */
static const char secret[] = TOKEN;

int main(void) {
    printf("Hello, reverse engineer.\n");
    /* The secret is never printed. It only exists as bytes inside the binary. */
    return secret[0] == 0;
}
