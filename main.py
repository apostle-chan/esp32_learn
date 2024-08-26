import uasyncio as asyncio

async def do_connect():
        import json
        import network
        # 尝试读取配置文件wifi_confi.json,这里我们以json的方式来存储WIFI配置
        # wifi_config.json在根目录下
        
        # 若不是初次运行,则将文件中的内容读取并加载到字典变量 config
        try:
            with open('wifi_config.json','r') as f:
                config = json.loads(f.read())
        # 若初次运行,则将进入excpet,执行配置文件的创建        
        except:
            essid = input('wifi name:') # 输入essid
            password = input('wifi passwrod:') # 输入password
            config = dict(essid=essid, password=password) # 创建字典
            with open('wifi_config.json','w') as f:
                f.write(json.dumps(config)) # 将字典序列化为json字符串,存入wifi_config.json
                
        #以下为正常的WIFI连接流程        
        wifi = network.WLAN(network.STA_IF)  
        if not wifi.isconnected(): 
            print('connecting to network...')
            wifi.active(True) 
            wifi.connect(config['essid'], config['password']) 
            await asyncio.sleep(5) #一般睡个5-10秒,应该绰绰有余
            
            if not wifi.isconnected():
                wifi.active(False) #关掉连接,免得repl死循环输出
                print('wifi connection error, please reconnect')
                import os
                # 连续输错essid和password会导致wifi_config.json不存在
                try:
                    os.remove('wifi_config.json') # 删除配置文件
                except:
                    pass
                await do_connect() # 重新连接
            else:
                print('network config:', wifi.ifconfig())

async def do_thing():
        print("do_thing")
            
if __name__ == '__main__':
    # 创建事件循环
    loop = asyncio.get_event_loop()

    # 将任务添加到事件循环
    loop.create_task(do_connect())
    loop.create_task(do_thing())

    # 执行事件循环
    loop.run_forever()