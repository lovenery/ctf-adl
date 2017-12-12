#include <stdio.h>

union X {
    int a;
    int b;
};
int main() {
    union X x;
    x.a = 1;
    x.b = 2;
    return 0;
}
