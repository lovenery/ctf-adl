# 練習從組語轉成C程式

```
objdump -d -M intel bin1
gcc -g -m32 01.c ; gdb a.out
```

## 4

```
lea eax, [ebp-0x8] ; 將某個記憶體位址搬到eax
```

## 8

```
test eax,eax ; eax是否為零。test用and來判斷結果=0，會設定ZF(zero flag)=1
jne 804840b ; eax不是零，跳走
mov BYTE PTR [ebp-0x5],0x61 ; eax是零
```

## 25

```
$ gdb bin25
gdb-peda$ disassemble main
gdb-peda$ x/s 0x8048520
0x8048520:	"%10s"
gdb-peda$ x/s 0x8048525
0x8048525:	"My name is %s"
```

## 27

- Function pointer

## 28

- movsx: 從低位元搬到高位元，前面會補0或F
