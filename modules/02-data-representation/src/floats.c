/* floats.c: the three fields of an IEEE 754 single-precision float. */
#include <math.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>

static void show(float f) {
    uint32_t bits;
    memcpy(&bits, &f, sizeof bits);          /* copy the raw bytes, no conversion */
    unsigned sign = bits >> 31;
    unsigned exponent = (bits >> 23) & 0xFF;
    unsigned mantissa = bits & 0x7FFFFF;
    printf("%-10g 0x%08x  sign %u  exponent %3u (2^%-4d)  mantissa 0x%06x\n",
           f, bits, sign, exponent, (int)exponent - 127, mantissa);
}

int main(void) {
    float samples[] = {1.0f, -1.0f, 1.5f, 2.0f, 0.75f, -13.375f, 0.1f, 0.0f, -0.0f, INFINITY, NAN};
    for (size_t i = 0; i < sizeof samples / sizeof samples[0]; i++)
        show(samples[i]);

    float a = 0.1f, b = 0.2f;
    printf("0.1f + 0.2f == 0.3f ? %s\n", (a + b == 0.3f) ? "yes" : "no");
    printf("0.1 + 0.2 == 0.3 (double) ? %s\n", (0.1 + 0.2 == 0.3) ? "yes" : "no");
    return 0;
}
