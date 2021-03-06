import requests
from bs4 import BeautifulSoup
import os
import re
import concurrent.futures


def make_course_directory(soup, parent_dir):
    Number_of_video = soup.findAll('a', attrs={'class': 'item-name video-name ga'})

    course_name_attribute = soup.find('h1', attrs={'class': 'default-title'})
    course_folder_name = course_name_attribute.text

    print(course_folder_name," this course is downloading......")
    print(f"And it has {len(Number_of_video)} videos")

    directory = course_folder_name

    path = os.path.join(parent_dir, directory)
    try:
        os.mkdir(path)
    except:
        print('Folder is already there')
    return path


def check(video_name, folder_path):
    file = os.listdir(folder_path)
    mp4_file = []
    for i in file:
        if '.mp4' in i:
            mp4_file.append(i)

    if video_name in mp4_file:
        return False
    else:
        return True


def One_video_Download(url, video_path, folder_path, s):
    video_name_lis = video_path.split('/')
    video_name = video_name_lis[len(video_name_lis)-1]
    value = check(video_name, folder_path)

    if value == True:
        r = s.get(url)
        soup_for_dw = BeautifulSoup(r.content, 'html5lib')

        video_url = soup_for_dw.find('video', attrs={'class': 'player'})
        video = video_url['data-src']

        chunk_size = 1024 * 1024 * 5
        r = requests.get(video, stream=True)
        print(f"{video_name} is downloding")
        with open(video_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=chunk_size):
                f.write(chunk)


def Thread_fun(presentation_ul, j, inner_path, s, count_for_videos):
    video_name = presentation_ul[j].text.strip()
    video_name = re.sub('[^A-Za-z0-9 ]+', ' ', video_name)
    video_name = str(count_for_videos) + '. ' + video_name + ".mp4"
    video_name = video_name.strip()
    url = presentation_ul[j]['href']

    video_path = inner_path + '/' + video_name

    One_video_Download(url, video_path, inner_path, s)
    return f"{video_name} is downloded..."


def main(s, course_url, parent_dir):

    r = s.get(course_url)
    soup = BeautifulSoup(r.content, 'html5lib')
    course_folder_path = make_course_directory(soup, parent_dir)

    opere_ul = soup.find('ul', attrs={'class': 'toc-container'})
    count_for_videos = 1
    course_folder_path = course_folder_path + '/'
    presentation = opere_ul.findAll('li', attrs={'role': 'presentation'}, recursive=False)

    for i in range(len(presentation)):
        if i == 0:
            presentation_div = presentation[i].find('div')
            coure_section_name = presentation_div.find('h4').text
            coure_section_name = re.sub('[^A-Za-z0-9 ]+', ' ', coure_section_name)
            coure_section_name = '0. ' + coure_section_name
            print(coure_section_name)
        else:
            presentation_div = presentation[i].find('div')
            coure_section_name = presentation_div.find('h4').text
            coure_section_name = re.sub('[^A-Za-z0-9 ]+', ' ', coure_section_name)
            print(coure_section_name)

        directory = coure_section_name
        inner_path = os.path.join(course_folder_path, directory)
        try:
            os.mkdir(inner_path)
        except:
            print('Folder is already there')

        presentation_ul = presentation[i].find('ul')
        presentation_ul = presentation_ul.findAll('a')

        #for j in range(len(presentation_ul)):
        if len(presentation_ul) % 2 == 1:
            i = 0
            for j in range(int(len(presentation_ul) / 2)):
                with concurrent.futures.ThreadPoolExecutor() as excutor:
                    f1 = excutor.submit(Thread_fun, presentation_ul, i, inner_path, s, count_for_videos)
                    i += 1
                    count_for_videos += 1
                    f2 = excutor.submit(Thread_fun, presentation_ul, i, inner_path, s, count_for_videos)
                    i += 1
                    count_for_videos += 1
                    print(f1.result())
                    print(f2.result())

            Thread_fun(presentation_ul, i, inner_path, s, count_for_videos)
        else:
            i = 0
            for j in range(int(len(presentation_ul) / 2)):
                with concurrent.futures.ThreadPoolExecutor() as excutor:
                    f1 = excutor.submit(Thread_fun, presentation_ul, i, inner_path, s, count_for_videos)
                    i += 1
                    count_for_videos += 1
                    f2 = excutor.submit(Thread_fun, presentation_ul, i, inner_path, s, count_for_videos)
                    i += 1
                    count_for_videos += 1
                    print(f1.result())
                    print(f2.result())



