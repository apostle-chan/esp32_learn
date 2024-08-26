import micropython

# 查看栈堆
mem_info = micropython.mem_info()
print(mem_info)

# 查看集成的Flash存储空间大小
import esp
print(esp.flash_size())
print(esp.flash_size()/1024/1024, "M")