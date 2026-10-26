/* gate.c: challenge source. The transformation lives in a header that build.py
 * generates from your seed into a temporary folder and deletes after compiling.
 * It defines GATE_EXPR(x), an MBA-obfuscated function of x, and TARGET. */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include "gate_expr.h"

__attribute__((noinline)) static uint32_t gate(uint32_t x) {
    return GATE_EXPR(x);
}

int main(int argc, char **argv) {
    if (argc != 2) {
        fprintf(stderr, "usage: %s NUMBER\n", argv[0]);
        return 2;
    }
    uint32_t x = (uint32_t)strtoul(argv[1], NULL, 0);
    if (gate(x) == (uint32_t)TARGET) {
        puts("open");
        return 0;
    }
    puts("closed");
    return 1;
}
