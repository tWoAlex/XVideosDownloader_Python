from XVideo import XVideo as xv

# link='https://www.xvideos.com/video68984225/_erasmus_'
# link = 'https://www.xvideos.com/video7388507/_'
link='https://www.xvideos.com/video49521087/_._'

a=xv(URL=link)
a.Retrieve()
print(a.title)
print(a.preview_name)

with open(a.preview_name,'wb') as result:
    result.write(a.preview_bytes)