#include <stdio.h>

struct Item {
    int id;
    int price;
}
int main() {
    struct Item item;
    item.id = 1;
    item.price = 0xe9;

    printf("id=%d, price=%d", item.id, item.price);
    return 0;
}
