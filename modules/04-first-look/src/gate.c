/* gate.c: checks a password given on the command line.
 * The expected password is never stored whole: it is put together at run time from two pieces.
 * Inputs (-D): PIECE_A, PIECE_B (string literals), FIRST, SECOND (which of the two names comes first).
 */
#include <stdio.h>
#include <string.h>

static const char *piece_a = PIECE_A;
static const char *piece_b = PIECE_B;

static int matches(const char *given) {
    char want[64];
    strcpy(want, FIRST);
    strcat(want, SECOND);
    return strcmp(given, want) == 0;
}

int main(int argc, char **argv) {
    if (argc != 2) {
        fprintf(stderr, "usage: %s <password>\n", argv[0]);
        return 2;
    }
    if (matches(argv[1])) {
        puts("access granted");
        return 0;
    }
    puts("access denied");
    return 1;
}
