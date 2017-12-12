#include <stdio.h>

int main() {
    char name[30];
    scanf("%30s", &name);

    if (strcmp(name, "Weber") == 0) {
        puts("Hi Weber!");
    } else {
        puts("You are not Weber")
    }
    return 0;
}
