import asyncio
from pyppeteer import launch
import time

browser, page, frame = None, None, None
input_list = ["input"]
click_list = ["label","button"]
link_list = ["a"]
# input_id_list = []
# click_id_list = []
input_id_list = {'M': [] }
click_id_list = {'M': [] }
link_id_list = {'M': [] }
# input_id_list = {'M': [] , 'F1' : [] ,'F2' : [] ,'F3' : [] ,'F4' : [] ,'F5' : [] }
# click_id_list = {'M': [] , 'F1' : [] ,'F2' : [] ,'F3' : [] ,'F4' : [] ,'F5' : [] }
# link_id_list = {'M': [] , 'F1' : [] ,'F2' : [] ,'F3' : [] ,'F4' : [] ,'F5' : [] }
page_frames = []
url_list = []

finded_link = [] #找到的链接
clicked_link = [] #点击过的链接，不再点击

root_url = "http://0.0.0.0:8080/"
root_url2 = "http://192.168.0.1/"



#async def css_selector_list(page,p,fnum):#识别页面元素

async def get_element_list(page,p,fnum):#识别页面元素
    global url_list,input_id_list ,click_id_list
    print("getting",p)
    element_id_list = []
    try:
        element_list = await page.querySelectorAll(p)
        for element in element_list:
            id = await page.evaluate('(element) => element.id', element)
            id_null = False
            name_null = False
            if id == "":
                id_null = True
                name = await page.evaluate('(element) => element.name', element)
                # if name =="":
                #     name_null = True
                #     value = await page.evaluate('(element) => element.value', element)
            if_input = True    
            element_type = await page.evaluate('(element) => element.onclick', element)
            if element_type == "hidden":
                if_input = False
                     
            try:

                if p == "input":
                    element_type = await page.evaluate('(element) => element.type', element)
                    element_click = await page.evaluate('(element) => element.onclick', element)
                    
                    #print(element_click)
                    if  element_click != None or element_type == "submit":
                        input_click = []
                        if id_null:
                            if name_null:
                                input_click.append(p+"[value="+value + "]")
                            else:
                                input_click.append(p+"[name="+name + "]")
                        else:    
                            input_click.append("#"+id)
                        
                        if_input = False
                        tem_list = click_id_list[fnum] + input_click
                        click_id_list[fnum] = tem_list
                        #click_id_list.append(input_click)
                    #print(element_type)
                    if element_type == "hidden":
                        if_input = False
                elif p == "a":

                    url = await page.evaluate('(element) => element.href', element)
                    #print(url[0:20])
                    #if url[0:19] != root_url:
                    #url_list.append(url)
                    lens = len(root_url)
                    if url[0:lens] != root_url:
                        if_input = False
                    else:
                        if url  not in url_list:
                            url_list.append(url)
                            if id_null:
                                url = url[lens:]
                                link_click = []
                                #print(url)
                                link_click.append(p+"[href='"+ url+ "']")
                                tem_list = link_id_list[fnum] + link_click
                                link_id_list[fnum] = tem_list
                                if_input = False

                        # url_list.append(url)
                        # tem_link = []
                        # tem_link.append("#"+id)
                        # tem_list = link_id_list[fnum] + tem_link
                        # link_id_list[fnum] = tem_list
                    #print(url)
                else:
                    element_click = await page.evaluate('(element) => element.onclick', element)
                    #print(element_click )
                    if  element_click == None:
                        if_input = False
            except:
                print("error")
            #print(id,if_input)
            if if_input:
                if id_null:
                    element_id_list.append(p+"[name="+name + "]")
                else:
                    element_id_list.append("#"+id)
                #print(element_id_list)
    except:
        print("no",p)
    return element_id_list


async def get_id_list(page,fnum,p_type):

    global input_id_list,click_id_list
    if p_type == 1:#input
        for p in input_list:
            id_list = await get_element_list(page,p,fnum)
            tem_list = input_id_list[fnum] + id_list
            input_id_list[fnum] = tem_list
        print(input_id_list)
    elif p_type == 2:
        for p in click_list:
            id_list = await get_element_list(page,p,fnum)
            tem_list = click_id_list[fnum] + id_list
            click_id_list[fnum] = tem_list
        print(click_id_list)
    elif p_type == 3:
        for p in link_list:
            id_list = await get_element_list(page,p,fnum)
            tem_list = link_id_list[fnum] + id_list
            link_id_list[fnum] = tem_list
        print(link_id_list)
    #click_id_list.append(id_list)


async def force_inputorclick(page):#点击页面元素,填充以数字填充
    #mode = open("PROXY_MODE_FILE", 'w+')
    mode = open("PROXY_MODE_FILE", 'w+')
    mode.write('1')
    print("---------------change mode 1------------")
    #print(mode.readline())
    mode.close()
    frames = page.mainFrame
    global input_id_list,click_id_list
    print(frames)
    if frames.childFrames == []:
        navigationPromise = asyncio.ensure_future(page.waitForNavigation())
        M_input_id_list = input_id_list['M']
        M_click_id_list = click_id_list['M']
        for In in M_input_id_list:

            try:
                await page.type(In, "")
            except:
                print("could not input")
        for Cl in M_click_id_list:

            try:
                await page.click(Cl)
                await navigationPromise
                print("new page")
                await page.waitFor(300)
                #finalResponse = await page.waitForResponse(lambda res: res.url == page.url and res.status == 200)
                sshotname = "screenshot/"+ Cl + ".png"
                await page.screenshot({'path': sshotname})
            except:
                print("could not click")
    else:
        num = 1
        for frame in frames.childFrames:
            print(frame)
            fnum = 'F'+ str(num)
            M_input_id_list = input_id_list[fnum]
            M_click_id_list = click_id_list[fnum]
            for In in M_input_id_list:
                print("input",In)
                try:
                    await frame.type(In, "admin")
                except:
                    print("could not input")

            for Cl in M_click_id_list:
                print("click",Cl)
                try:
                    element = await frame.querySelector(Cl)
                    print(element)
                    await frame.click(Cl)
                    await frame.waitForNavigation()
                    print("new page")
                    sshotname = "screenshot/"+ Cl + ".png"
                    await page.screenshot({'path': sshotname})
                except:
                    print("could not click")

            num = num + 1

 
async def goto_link(page):
    navigationPromise = asyncio.ensure_future(page.waitForNavigation())
    num = 1
    for link in url_list:
        try:
            if link in clicked_link:
                print("have clicked")
            else:    
                await page.goto(link)
                clicked_link.append(link)
                await navigationPromise
                
                await page.waitFor(300)
                #finalResponse = await page.waitForRes  ponse(lambda res: res.url == page.url and res.status == 200)
                sshotname = "screenshot/"+ str(num) + ".png"
                await page.screenshot({'path': sshotname})
                #await page.screenshot({'path': 'example.png'})
                await page.goback()
                print("could reach")
        except:
            print("could not reach")
        num = num + 1

async def click_link(page,struc,link_id):#点击链接 测试并截图
    
    try:
        print(link_id)
        navigationPromise = asyncio.ensure_future(page.waitForNavigation())
        element = await page.querySelector(link_id)
        print("find",element)
        print(".....click1.....",link_id)                  
                    
        await page.click(link_id)

        clicked_link.append(link_id)

        print("clicked",clicked_link)
        await navigationPromise
        #await page.waitForNavigation()
        mode = open("PROXY_MODE_FILE", 'w+')
        mode.write('0')
        mode.close()
        print("---------------change mode 0------------")
        print(".....click2.....",link_id)
        #await get_id_list(page,struc,1)
                    
        #await get_id_list(page,struc,2)
        await get_id_list(page,struc,3)
        #print(".....click3.....",link_id)
        # sshotname = "screenshot/"+ link_id + ".png"
        # await page.screenshot({'path': sshotname})
        print("start inputorclick")

        print("***************change mode")

    except:
        print("could not reach")

async def goto_subpage(page):#前往子页面
        
    frames = page.mainFrame
    print(frames)
    if frames.childFrames == []:
        #get input element id
        for link_id in link_id_list['M']:
            if link_id in clicked_link :
                continue
            else:

                await click_link(page,'M',link_id)
    else:
        num = 0
        for struc in page_frames:
            x  = 0
            for link_id in link_id_list[struc]:
                if link_id in clicked_link :
                    continue
                else:
                    print(num,link_id)
                    frame = frames.childFrames[num]
                    await click_link(frame,struc,link_id)
            num = num + 1


async def current_page(page):
    frames = page.mainFrame
    global input_id_list,click_id_list,link_id_list
    print(frames)
    if frames.childFrames == []:
        #get input element id
        input_id_list['M'] = []
        click_id_list['M'] = []
        link_id_list['M'] = []
        await get_id_list(page,'M',1)               
        #get click element id
        await get_id_list(page,'M',2)
        #get link element id
        await get_id_list(page,'M',3)

    else:

        num = 1
        for frame in frames.childFrames:
            print(frame)
            fnum = 'F'+ str(num)
            input_id_list[fnum] = []
            click_id_list[fnum] = []
            link_id_list[fnum] = []
            page_frames.append(fnum)
            print(fnum)
            #get input element id
            await get_id_list(frame,fnum,1)
            #get click element id
            await get_id_list(frame,fnum,2)
            #get link element id
            await get_id_list(frame,fnum,3)


            #print(url_list)
            print("input\n",input_id_list)
            print("click\n",click_id_list)
            num = num + 1


     

async def main():
    global browser, page, frame, input_id_list, click_id_list, url_list
    browser = await launch({

        'headless': True, # 关闭无头模式
        'devtools': True, # 打开 chromium 的 devtools
        'executablePath': '/home/zhw/.local/share/pyppeteer/chrome',
        'args': [ 
            '--disable-extensions',
            '--hide-scrollbars',
            '--disable-bundled-ppapi-flash',
            '--mute-audio',
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--disable-gpu',
        ],
        'dumpio': True,  
    })
    print("-----------------login-------------------")
    page = await browser.newPage()

    await page.setViewport({'width': 1366, 'height': 768})
    navigationPromise = asyncio.ensure_future(page.waitForNavigation())
    await page.goto(root_url)
    #await page.waitFor(3000)
    await navigationPromise

    print(".................start get page's element_id.................")

    await current_page(page)

    print(".................start input/click...................")

    await force_inputorclick(page)
    
    #input.buttonBig:nth-child(3)#menu > div:nth-child(2) > a:nth-child(2)
    print("-----------------first step-------------------")

    # new_url = page.url3459
    # print(new_url)
    # if new_url in url_list:
    #     print("not goto")
    # else:
    #     print("new page")
    #     url_list.append(new_url)

     
    await current_page(page)
    #print(link_id_list)
    await goto_subpage(page)
    print(url_list)
    #await current_page(page)

    await force_inputorclick(page)
    #frames = page.mainFrame

    # print(frames)<a class="label" href="setup.php">setup</a>

    # if frames.childFrames == []:
    

    #     element = await page.querySelector("a[href='setup.php']")
    #     print(element)
    #     # await frame.click("#a22")#input.buttonBig:nth-child(2)
    #     await page.click("a[href='setup.php']")
        


    # else:
    #     print("********************")
    #     num = 1

    #     for frame in frames.childFrames:
    #         # print(frame)
            
    #         # for p in input_list:
    #         #     id_list = await get_element_list(frame,p)
    #         #     input_id_list.append(id_list)
    #         # print(input_id_list)       

    #         # for p in click_list:
    #         #     id_list = await get_element_list(frame,p)
    #         #     click_id_list.append(id_list)
    #         # print(click_id_list)
    #         # print(url_list)
    #         try:

    #             element = await frame.querySelectorAll("#a2")

    #             # await frame.click("#a22")#input.buttonBig:nth-child(2)
    #             await frame.click("#a2")
    #             await page.waitFor(3000)
    #             await page.screenshot({'path': 'example.png'})
    #             fnum = 'F'+ str(num) 
    #             print(fnum)
    #             # await get_id_list(page,fnum,1)
    #             # print("#####")   
    #             # await get_id_list(page,fnum,2)
    #             # try:
    #             #     element = await frame.querySelectorAll("[name] = 'NewDev'")
    #             # except:
    #             #     print("123")
    #             #print(element)

    #             # new_url = page.url
    #             # print(new_url)   

    #         except:
    #             print("----------------------not click")
    #         num = num + 1
    #await current_page(page)

    #await force_inputorclick(page)

    # frames = page.mainFrame

    # print(frames)
    # if frames.childFrames == []:
    #     for p in input_list:
    #         id_list = await get_element_list(page,p)
    #         input_id_list.append(id_list)
    #     print(input_id_list)       

    #     for p in click_list:
    #         id_list = await get_element_list(page,p)
    #         click_id_list.append(id_list)
    #     print(click_id_list)

    # else:
    #     print("********************")
    #     num = 1

    #     for frame in frames.childFrames:
    #         try:
    #             element = await frame.querySelector("input[name]")
    #             name = await frame.evaluate('(element) => element.name', element)
    #             print(name)
    #             element = await frame.querySelector("input[name = EnWps]")
    #             print(element)
    #         except:
    #             print("123")
            # print(frame)
    # await page.screenshot({'path': 'example.png'})
    # for frame in frames.childFrames:
    #     input_id_list = []
    #     click_id_list = []
    #     for p in input_list:
    #         id_list = await get_element_list(frame,p)
    #         input_id_list.append(id_list)
    #     print(input_id_list)       

    #     for p in click_list:
    #         id_list = await get_element_list(frame,p)
    #         click_id_list.append(id_list)
    #     print(click_id_list)
    #finalRequest = await page.waitForRequest(lambda req: req.url == url_list[3] and req.method == 'GET')  
    #print(finalRequest)  
    #await page.waitForRequest(url_list[3])
    #await goto_link(page)
    await page.waitFor(3000)
    await page.screenshot({'path': 'example.png'})    
    await browser.close()
    #print(cookies)

asyncio.get_event_loop().run_until_complete(main())
