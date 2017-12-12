int main() {
    int i = 0xa;
    int j = 0;
    if (i == 0xa) {
        goto labelA;
    } else {
        goto labelB;
    }

    labelA:
        return 1;
    labelB:
        j = 2;
        return 0;
}
