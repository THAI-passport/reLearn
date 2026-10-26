/* identities.c: one plain function and two MBA-rewritten versions of it.
 * All three compute x + y on 32-bit unsigned integers (that is, modulo 2^32). */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

__attribute__((noinline)) uint32_t add_plain(uint32_t x, uint32_t y) {
    return x + y;
}

__attribute__((noinline)) uint32_t add_mba1(uint32_t x, uint32_t y) {
    return (x ^ y) + 2 * (x & y);
}

__attribute__((noinline)) uint32_t add_mba2(uint32_t x, uint32_t y) {
    return (x | y) + (x & y) + 3 * (~(x | y) - ~x - ~y + ~(x & y) + 1) - 3;
}

int main(int argc, char **argv) {
    uint32_t x = argc > 1 ? (uint32_t)strtoul(argv[1], NULL, 0) : 1234567;
    uint32_t y = argc > 2 ? (uint32_t)strtoul(argv[2], NULL, 0) : 4000000000u;
    printf("plain %u\nmba1  %u\nmba2  %u\n", add_plain(x, y), add_mba1(x, y), add_mba2(x, y));
    return 0;
}
