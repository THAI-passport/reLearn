/* greet.h: the interface main.c sees. Declarations only, no code. */
#ifndef GREET_H
#define GREET_H

extern int greet_count;           /* defined in greet.c */
void greet(const char *name);     /* defined in greet.c */

#endif
