#include <stdio.h>
int main(void)
{
    int i = 4;
    switch (i)
    {
    case 1:
        printf("1\n");
        break;
    case 2...8:
        printf("%d\n", i);
        break;
    default:
        printf("default!\n");
        break;
    }
    return 0;
}