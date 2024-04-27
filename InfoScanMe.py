import requests
import re
import socket


# url_ip = (re.findall(r"([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})", url))[0] IP
# url_ip = (re.findall(r"([0-9.a-zA-Z-]+[.][a-z]*)", url))[0] url

def output_data(urls, comments, mails):
    if len(urls) > 0:
        print('\n -------------------------------- URLs --------------------------------')
        for i in urls:
            print(i)
    if len(comments) > 0:
        print('\n-------------------------------- COMMENTs --------------------------------')
        for i in comments:
            print(i)
    if len(mails) > 0:
        print('\n-------------------------------- MAILs -------------------------------- ')
        for i in mails:
            print(i)


def search_ip(user_url):
    url = f"{user_url}"
    try:
        url_ip = (re.findall(r"([0-9.a-zA-Z-]+[.][a-z]*)", url))[0]
        ip = socket.gethostbyname(url_ip)
    except socket.gaierror:
        try:
            url_ip = (re.findall(r"([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})", url))[0]
            ip = socket.gethostbyname(url_ip)
        except IndexError:
            print('Network error')
            return
    except IndexError:
        print('Network error')
        return
    print(f" \n-------------------------------- INFO --------------------------------")
    print(f"Domain: {url_ip}")
    print(f"IP: {ip}")
    print(f"Wait, please. I`am scanning resourses")



def get_scheme(user_url):
    check_scheme = "https:"
    if check_scheme not in user_url:
        check_scheme = "http:"
    return check_scheme


def parse_url(user_url):
    url = f"{user_url}"
    check_scheme = get_scheme(url)

    try:
        r = requests.get(url)
    except:
        url = f"http://{user_url}"
        r = requests.get(url)
    text = r.text
    all_url = []
    all_comment = []
    all_mails = []

    hrefs_log = re.findall(r'(href=".*?[0-9a-zA-Z.?\-_=/%#]*")', text)  # href
    src_log = re.findall(r'(src=".*?[0-9a-zA-Z.?\-_=/%#]*")', text)  # src
    paths_log = re.findall(r'([path]{4}?=".*?[0-9a-zA-Z.?\-_=/%#]*")', text)  # path
    mails_log = re.findall(r'([a-zA-Z0-9_]{2,}@[a-zA-Z]*\.[a-zA-Z]*)', text)  # mails
    comments_log = re.findall(r'([<!\-]{4}.*[\->]{3})', text)  # comments
    comment_js_log_1 = re.findall(r'/\*!?[\s\S]*?\*/', text)  # comments JS
    comment_js_log_3 = re.findall(r'/\*.*?\*/', text)  # comments JS
    if ".js" in url:
        comment_js_log_2 = re.findall(r"(\n\s*/{2}.+)", text)  # comments JS
        for i in comment_js_log_2:
            all_comment.append(i)

    for i in hrefs_log:
        if i[6:10] != 'http':
            if i[6:8] == "//":
                new_url = f"{check_scheme}{i[6:-1]}"
                all_url.append(new_url)
            else:
                new_url = url + i[6:-1]
                all_url.append(new_url)
        else:
            all_url.append(i[6:-1])

    for i in src_log:
        if i[5:9] != 'http':
            if i[5:7] == "//":
                new_url = f"{check_scheme}{i[5:-1]}"
                all_url.append(new_url)
            else:
                new_url = url + i[6:-1]
                all_url.append(new_url)
        else:

            all_url.append(i[5:-1])

    for i in paths_log:
        if i[6:10] != 'http':
            if i[6:8] == "//":
                new_url = f"{check_scheme}{i[6:-1]}"
                all_url.append(new_url)
            else:
                new_url = url + i[6:-1]
                all_url.append(new_url)
        else:
            all_url.append(i[6:-1])

    for i in comments_log:
        all_comment.append(i)

    for i in comment_js_log_1:
        all_comment.append(i)

    for i in comment_js_log_3:
        all_comment.append(i)

    for i in mails_log:
        all_mails.append(i)

    output_data(set(all_url), set(all_comment), set(all_mails))


# def file_export():
#     with open("save_result/example.txt", "r+") as f:
#         lines = set(f)
#         for i in lines:
#             print(i)
#             f.write(i)

print("Example: \n\thttps://example.com/")
url_input = input('Enter URL: ')

if __name__ == "__main__":
    try:
        search_ip(url_input)
        parse_url(url_input)
    except requests.exceptions.ConnectionError:
        pass
