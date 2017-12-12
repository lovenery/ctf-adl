int main() {
    int sum = 0;
    for (int i = 0; i <= 0x9; i++) {
        for (int j = 0; j < i; j++) {
            sum = i*j;
        }
    }
    return 0;
}
