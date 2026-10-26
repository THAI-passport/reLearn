/* stamp.c: write one struct record to a file, exactly as it sits in memory.
 * VERSION, FLAGS, DELTA, ID, RATIO and PAD are injected by build.py. */
#include <stdio.h>
#include <string.h>
#include "record.h"

int main(int argc, char **argv) {
    if (argc != 2) {
        fprintf(stderr, "usage: %s OUTPUT_FILE\n", argv[0]);
        return 2;
    }
    struct record r;
    memset(&r, PAD, sizeof r);               /* padding bytes keep this value */
    r.version = VERSION;
    r.flags = FLAGS;
    r.delta = DELTA;
    r.id = ID;
    r.ratio = RATIO;

    FILE *f = fopen(argv[1], "wb");
    if (!f) {
        perror(argv[1]);
        return 1;
    }
    size_t n = fwrite(&r, 1, sizeof r, f);
    fclose(f);
    printf("wrote %zu bytes to %s\n", n, argv[1]);
    return n == sizeof r ? 0 : 1;
}
