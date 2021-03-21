#!/usr/bin/python3
from imports import *

BLACK_LISTS = ["_"]
PASS_KEY = "(password&)|(pwd&)|(passwd&)"

def process(PCAP_DIR):
    index_file = open(os.path.join(PCAP_DIR, "index.config"), "a+")
    cf_write = myparser()
    cf_read = myparser()
    cf_read.read(os.path.join(PCAP_DIR, "index.config"))
    login = []
    login_candidate = []
    login_2_candidate = []
    depend_candidate = []
    get_pages = []
    post_params = {}
    for item in cf_read.options("GET"):
        if "login." in item.lower():
            login_candidate.append(item)
        if not re.search("-0$", item):
            page, params = re.match("GET-(.*)-[\d]+-(.*)", item).groups()
            if re.search(PASS_KEY, params.lower()):
                login_2_candidate.append(item)
            
        else:
            page = re.match("GET-(.*)-0", item)
            # method, page = re.match("(GET)-([^-]*)", item).groups()
            # pass
        get_pages.append(item)
            
    for item in cf_read.options("POST"):
        if "login." in item.lower():
            login_candidate.append(item)
        num, params = re.search("-([\d]+)-(.*)", item).groups()
        if re.search(PASS_KEY, params.lower()):
            login_2_candidate.append(item)
        params = params.rstrip("&").split("&")
        for param in params:
            if param in post_params:
                post_params[param] += 1
            else:
                post_params[param] = 1
    # print(get_params)
    # print(post_params)
    # print(login_candidate)

    for item in login_candidate:
        if re.search(PASS_KEY, item.lower()):
            login.append(item)
    if len(login) == 0:
        for item in login_2_candidate:
            login.append(item)
    if(len(login) == 1):
        print("[+]Login pcap is %s" %login[0])
        try:
            content = cf_read.get("POST", login[0])
        except:
            content = cf_read.get("GET", login[0])
        cf_write.add_section("LOGIN")
        cf_write.set("LOGIN", login[0], content)
    else:
        print("[+]There are some candidate login pcaps")
        print(login)

    if len(post_params) == 0:
        cf_write.write(index_file)
        index_file.close()
        return
    #Now analyse some dependences
    post_order = sorted(post_params.items(),key=lambda x:x[1],reverse=True) 
    # print(post_order)
    for i in range(2):
        param = post_order[i][0]
        for page in get_pages:
            if param in page:
                depend_candidate.append(page)
    if len(depend_candidate) != 0:
        print("[+]candidate dependency: %s" %str(depend_candidate))
        content = cf_read.get("GET", depend_candidate[0])
        cf_write.add_section("DEPENDENCY")
        cf_write.set("DEPENDENCY", depend_candidate[0], content)
    
    cf_write.write(index_file)
    index_file.close()



def main():
    if (len(sys.argv) == 1):
        print("[+]Usage: ./parse.py DIR_TO_PCAPS")
        return False
    else:
        path = sys.argv[1]
    PCAP_DIR = os.path.join(path, "PCAPS")
    HTML_DIR = os.path.join(path, "HTML")

    process(PCAP_DIR)
    return True


if __name__ == '__main__':
    main()
