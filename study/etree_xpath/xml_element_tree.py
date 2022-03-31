import xml.etree.ElementTree as et


tree = et.parse('an.xml')
root = tree.getroot()
ls = ''

for q in root.find('Questions'):
    n = 1
    que = q.find('QuestionText').text
    ls += '\n' + 'question: ' + que + '\n' + 'answer:' + '\n'
    for a in q.findall('Answer'):
        if a.get('correct') == 'true':
            ls += str(n) + '.' + a.text + '\n'
            n += 1

with open('answer.txt', 'w', encoding='utf-8') as f:
    f.write(ls)
