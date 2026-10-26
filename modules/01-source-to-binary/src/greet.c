#include <stdio.h>
#include "greet.h"

#define GREETING "Hello"

int greet_count = 0;              /* global: visible to other files */
static int calls_this_file = 0;   /* static: private to this file */

static void bump(void) {          /* static function: private to this file */
    greet_count++;
    calls_this_file++;
}

void greet(const char *name) {
    bump();
    printf("%s, %s!\n", GREETING, name);
}
