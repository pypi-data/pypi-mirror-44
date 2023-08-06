from sgwc import get_official, Official

official = get_official('LOL313298553')
print(official)
official = Official.from_url(official.url)
print(official)


