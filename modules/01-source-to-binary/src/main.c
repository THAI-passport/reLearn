#include <stdio.h>
#include "greet.h"

int main(int argc, char **argv) {
    greet(argc > 1 ? argv[1] : "reverser");
    greet("world");
    printf("greeted %d times\n", greet_count);
    return 0;
}
