/* vault.c: keeps a token in three pieces, one in a global, one on the heap, one on the stack.
 * It prints each piece's number, address, and length, and writes the memory around the pieces to a dump file.
 *
 * Compile-time inputs (-D):
 *   P_GLOBAL, P_HEAP, P_STACK     the three pieces (strings)
 *   N_GLOBAL, N_HEAP, N_STACK     the piece number (1, 2, 3) each region holds
 *   DECOY1 .. DECOY6              filler strings placed before and after each piece
 */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

struct cell {
    char before[16];
    char piece[16];
    char after[16];
};

struct entry { int number; const void *addr; size_t len; };

static struct cell global_cell = { DECOY1, P_GLOBAL, DECOY2 };

static void fill(struct cell *c, const char *before, const char *piece, const char *after) {
    memset(c, 0, sizeof(*c));
    strcpy(c->before, before);
    strcpy(c->piece, piece);
    strcpy(c->after, after);
}

static int by_number(const void *a, const void *b) {
    return ((const struct entry *)a)->number - ((const struct entry *)b)->number;
}

static void put_u64(FILE *f, uint64_t v) {
    for (int i = 0; i < 8; i++)
        fputc((int)(v >> (8 * i)) & 0xff, f);
}

int main(int argc, char **argv) {
    if (argc != 2) {
        fprintf(stderr, "usage: %s <dump-file>\n", argv[0]);
        return 2;
    }
    struct cell *heap_cell = malloc(sizeof(*heap_cell));
    struct cell stack_cell;
    fill(heap_cell, DECOY3, P_HEAP, DECOY4);
    fill(&stack_cell, DECOY5, P_STACK, DECOY6);

    struct entry list[3] = {
        { N_GLOBAL, global_cell.piece, strlen(global_cell.piece) },
        { N_HEAP,   heap_cell->piece,  strlen(heap_cell->piece)  },
        { N_STACK,  stack_cell.piece,  strlen(stack_cell.piece)  },
    };
    const struct cell *cells[3] = { &global_cell, heap_cell, &stack_cell };

    FILE *f = fopen(argv[1], "wb");
    if (!f) {
        perror("fopen");
        return 1;
    }
    fwrite("MEMD", 1, 4, f);
    fputc(3, f); fputc(0, f); fputc(0, f); fputc(0, f);
    for (int i = 0; i < 3; i++) {
        put_u64(f, (uint64_t)(uintptr_t)cells[i]);
        put_u64(f, sizeof(struct cell));
        fwrite(cells[i], 1, sizeof(struct cell), f);
    }
    fclose(f);

    qsort(list, 3, sizeof(list[0]), by_number);
    for (int i = 0; i < 3; i++)
        printf("piece %d at %p length %zu\n", list[i].number, list[i].addr, list[i].len);
    free(heap_cell);
    return 0;
}
