/* record.h: the on-disk record used by stamp.c and layout.c. */
#ifndef RECORD_H
#define RECORD_H
#include <stdint.h>

struct record {
    uint8_t  version;
    uint16_t flags;
    int32_t  delta;
    uint64_t id;
    float    ratio;
};

#endif
