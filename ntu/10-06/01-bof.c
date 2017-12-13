#include<stdio.h>

void www() {
    puts("Yaaaa");
    system("/bin/sh");
}

int main() {
    char buf[0x20];
    setvbuf(stdout, 0, 2, 0);
    puts("Go buffer overflow");
    prinf("Input... :");
    read(0, buf, 100);
    return 0;
}
