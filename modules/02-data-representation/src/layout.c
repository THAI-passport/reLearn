/* layout.c: type sizes, field offsets, and padding. */
#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#include "record.h"

struct reordered {        /* the same fields, largest first */
    uint64_t id;
    int32_t  delta;
    float    ratio;
    uint16_t flags;
    uint8_t  version;
};

struct wasteful { char a; double b; char c; };   /* 1 + 7 pad + 8 + 1 + 7 pad */
struct compact  { double b; char a; char c; };   /* 8 + 1 + 1 + 6 pad */

int main(void) {
    printf("char %zu, short %zu, int %zu, long %zu, long long %zu, pointer %zu, float %zu, double %zu\n",
           sizeof(char), sizeof(short), sizeof(int), sizeof(long), sizeof(long long),
           sizeof(void *), sizeof(float), sizeof(double));
    printf("struct record: size %zu, align %zu\n", sizeof(struct record), _Alignof(struct record));
    printf("  version @%zu  flags @%zu  delta @%zu  id @%zu  ratio @%zu\n",
           offsetof(struct record, version), offsetof(struct record, flags),
           offsetof(struct record, delta), offsetof(struct record, id),
           offsetof(struct record, ratio));
    printf("struct reordered: size %zu\n", sizeof(struct reordered));
    printf("struct wasteful: size %zu, struct compact: size %zu\n",
           sizeof(struct wasteful), sizeof(struct compact));
    return 0;
}
