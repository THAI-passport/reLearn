/* vault.c: challenge source. build.py compiles it to an object file only (never linked here).
 * ENTRY, DECOY, SINK, KEY, STEP, BLOB and LEN are injected from the learner's seed. */

extern void SINK(const char *message);   /* not defined anywhere: you provide it */

static const unsigned char blob[LEN] = BLOB;

static void decode(char *out) {
    for (int i = 0; i < LEN; i++)
        out[i] = (char)(blob[i] ^ (unsigned char)(KEY + i * STEP));
    out[LEN] = '\0';
}

void DECOY(void) {
    SINK("nothing in here, keep looking");
}

void ENTRY(void) {
    char buf[LEN + 1];
    decode(buf);
    SINK(buf);
}
