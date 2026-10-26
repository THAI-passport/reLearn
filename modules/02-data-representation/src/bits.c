/* bits.c: masks, shifts, two's complement, sign extension, endianness. */
#include <stdint.h>
#include <stdio.h>

static void show(const char *label, uint32_t v) {
    printf("%-14s 0x%08x  ", label, v);
    for (int i = 31; i >= 0; i--) {
        putchar((v >> i) & 1 ? '1' : '0');
        if (i % 4 == 0 && i != 0)
            putchar('_');
    }
    putchar('\n');
}

int main(void) {
    uint32_t x = 0x2A;                       /* 42 */
    show("x", x);
    show("x << 4", x << 4);
    show("x >> 1", x >> 1);
    show("x & 0xF", x & 0xF);
    show("x | 0x100", x | 0x100);
    show("x ^ 0xFF", x ^ 0xFF);
    show("~x", ~x);

    int32_t neg = -42;
    show("-42", (uint32_t)neg);
    printf("-42 read as unsigned: %u\n", (uint32_t)neg);

    int8_t s8 = -1;
    uint8_t u8 = 0xFF;
    int32_t from_signed = s8;               /* sign extension */
    int32_t from_unsigned = u8;             /* zero extension */
    printf("int8_t  0xFF widened: %d (0x%08x)\n", from_signed, (uint32_t)from_signed);
    printf("uint8_t 0xFF widened: %d (0x%08x)\n", from_unsigned, (uint32_t)from_unsigned);

    uint32_t wrap = (uint32_t)INT32_MAX + 1;
    printf("INT32_MAX + 1 as unsigned: %u, same bits as int32_t: %d\n", wrap, (int32_t)wrap);

    int32_t m = -20;
    printf("-20 >> 2 (signed): %d, (uint32_t)-20 >> 2: %u\n", m >> 2, (uint32_t)m >> 2);

    uint32_t word = 0x11223344;
    unsigned char *p = (unsigned char *)&word;
    printf("0x11223344 in memory, lowest address first: %02x %02x %02x %02x\n",
           p[0], p[1], p[2], p[3]);
    return 0;
}
