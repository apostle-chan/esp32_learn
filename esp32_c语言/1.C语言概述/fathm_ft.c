#include <stdio.h>
int main(void)
{
    int feet, fathoms; // 声明变量

    fathoms = 2; // 变量初始化/赋值
    feet = 6 * fathoms;
    printf("there are %d fet in %d fathoms!\n", feet, fathoms);
    printf("yes, i said %d feet!\n", 6 * fathoms);

    return 0;
}