import requests
from bs4 import BeautifulSoup
import New_way_to_Course_download as Course_download
import re
from timer import timer

# headers = {   #This is for bypass the bot
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36'
#
# }

login_data = {
    'libraryCardPasswordVerify': "",
    'org': 'freelibrary.org',
    # This is the organization. For me i open my lynda library account from the freelibrary.org. In your case it may be dif.
    'currentView': 'login'
}


def path_download(Path_url, parent_dir):
    with requests.Session() as s:
        authentication(s)
        course_url_list = []

        r = requests.get(Path_url)
        soup = BeautifulSoup(r.content, 'html5lib')
        div = soup.findAll('div', attrs={'class': 'title-author-info'})

        for i in div:
            h2 = i.find('h2')
            h2 = h2.text
            h2 = re.sub('[^A-Za-z0-9 ]+', ' ', h2)
            search = 'https://www.lynda.com/search?q=' + h2
            r2 = requests.get(search)
            try:
                soup = BeautifulSoup(r2.content, 'html5lib')
                srch = soup.find('a', attrs={'class': 'first-hidden'})
                course_url_list.append(srch['href'])
            except:
                print(h2, "this course is not found")

        # print(course_url_list)
        print(f"This Learning path have {len(course_url_list)} courses in it")
        print("\n\t\t\t\t\t\t\t\t--------Learning path Downloading--------\n")

        course_number = 1
        for i in course_url_list:
            if 'https://www.lynda.com/' in i:
                Course_download.main(s, i, parent_dir, course_number)
                course_number += 1
            else:
                print("This course cannot be downloaded: ", i)
                course_number += 1
                continue


def authentication(s):
    url = 'https://www.lynda.com/portal/patron?org=freelibrary.org'  # as my library card is form the free library. It may be dif for you.
    r = s.get(url)  # Use headers=headers in here if you get any bot type error
    soup = BeautifulSoup(r.content, 'html5lib')
    login_data['seasurf'] = soup.find('input', attrs={'name': 'seasurf'})['value']
    s.post(url, data=login_data)  # Use headers=headers in here if you get any bot type error


def main():
    print("------------------------Lynda videos Downloader------------------------")
    print("1) One video download")
    print('2) One Course download')
    print("3) Full Learning path download")
    print("4) Multiple path download\n")
    choose = input("Enter your choose: ")
    choose = int(choose)
    login_data['libraryCardNumber'] = input("Enter your library card number: ")
    login_data['libraryCardPin'] = input("Enter your library card pin: ")

    if choose == 1:
        with requests.Session() as s:
            authentication(s)
            url = input("Enter the video url: ")
            folder_path = input("Enter the folder path where you want to save: ")
            video_name = input("Enter the video name: ")
            video_path = folder_path + '/' + video_name + '.mp4'
            Course_download.One_video_Download(url, video_path, folder_path, s)

    elif choose == 2:
        with requests.Session() as s:
            authentication(s)
            course_url = input("Enter the course url to download: ")
            parent_dir = input(
                "Enter the file directory where you want to save: ")
            course_number = input("Enter the course number: ")
            Course_download.main(s, course_url, parent_dir, course_number)

    elif choose == 3:
        Path_url = input("Enter the Learning path url: ")
        parent_dir = input("Enter the file directory where you want to save: ")
        path_download(Path_url, parent_dir)

    elif choose == 4:
        Path_url_list = input("Enter the list of Path url with coma: ")
        Path_url_list = Path_url_list.split(',')
        parent_dir_list = input("Enter the list of file directory with coma: ")
        parent_dir_list = parent_dir_list.split(',')

        if len(Path_url_list) == len(parent_dir_list):
            for i in range(len(Path_url_list)):
                path_download(Path_url_list[i], parent_dir_list[i])

    else:
        exit()


if __name__ == '__main__':
    t = timer(1, 1)
    t(main)
