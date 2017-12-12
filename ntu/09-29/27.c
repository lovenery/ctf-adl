int func(int a, int b) {
    return a+b;
}

int main() {
    int (*pFunc)(int, int);
    pFunc = &func;
    (*pFunc)(0x5, 0xa);
    return 0;
}
