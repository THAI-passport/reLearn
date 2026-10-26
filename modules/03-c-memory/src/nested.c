/* nested.c: a struct with nested arrays, walked with plain pointers. */
#include <stddef.h>
#include <stdint.h>
#include <stdio.h>

struct packet {
    uint16_t id;
    char     tag[6];
    uint32_t samples[4];
    struct { uint8_t lo, hi; } range;
};

int main(void) {
    struct packet pk = {0x0102, "ab", {100, 200, 300, 400}, {3, 9}};
    unsigned char *base = (unsigned char *)&pk;

    printf("sizeof(struct packet) = %zu\n", sizeof(pk));
    printf("id @%zu  tag @%zu  samples @%zu  range @%zu\n",
           offsetof(struct packet, id), offsetof(struct packet, tag),
           offsetof(struct packet, samples), offsetof(struct packet, range));
    printf("samples[2] via arithmetic: %u\n", *(uint32_t *)(base + offsetof(struct packet, samples) + 2 * sizeof(uint32_t)));
    printf("range.hi via arithmetic:   %u\n", *(base + offsetof(struct packet, range) + 1));
    printf("raw bytes:");
    for (size_t i = 0; i < sizeof(pk); i++)
        printf(" %02x", base[i]);
    printf("\n");
    return 0;
}
