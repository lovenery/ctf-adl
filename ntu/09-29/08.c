int main() {
    int a = 0xa;
    char b;
    switch (a) {
        case 0x0:
            b = 0x61;
            break;
        case 0x1:
            b = 0x62;
            break;
        case 0x2:
            b = 0x63;
            break;
        default:
            b = 0x64;
            break;
    }
    return 0;
}
