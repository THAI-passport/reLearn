/* pointers.c: pointer arithmetic, array decay, sizeof inside and outside a function. */
#include <stdint.h>
#include <stdio.h>

static size_t inside(int arr[8]) {      /* the [8] is ignored: arr is an int * here */
    return sizeof(arr);
}

int main(void) {
    int arr[8] = {10, 20, 30, 40, 50, 60, 70, 80};
    int *p = arr;                       /* the array decays to a pointer to its first element */
    uint8_t bytes[4] = {1, 2, 3, 4};

    printf("sizeof(arr) in main: %zu, sizeof(arr) inside a function: %zu\n", sizeof(arr), inside(arr));
    printf("p     = %p\n", (void *)p);
    printf("p + 1 = %p  (+%td bytes, one int)\n", (void *)(p + 1), (char *)(p + 1) - (char *)p);
    printf("p + 3 = %p  *(p + 3) = %d, p[3] = %d, 3[p] = %d\n", (void *)(p + 3), *(p + 3), p[3], 3[p]);
    printf("&arr[5] - &arr[1] = %td elements\n", &arr[5] - &arr[1]);
    printf("(char *)&arr[5] - (char *)&arr[1] = %td bytes\n", (char *)&arr[5] - (char *)&arr[1]);
    printf("*(int *)bytes = 0x%08x (the same 4 bytes read as one int)\n", *(int *)bytes);
    return 0;
}
