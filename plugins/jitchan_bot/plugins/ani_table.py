import http.client
import json
from datetime import datetime

def ani_table(peer, command, outputs):
    day = ['일', '월', '화', '수', '목', '금', '토']
    input_day = command[1]
    cur_day = datetime.now().isoweekday()
    if input_day in ['내일', '어제', '그저께', '그제', '모레', '내일모레']:
        if input_day == '내일':
            cur_day += 1
        elif input_day in ['내일모레', '모레']:
            cur_day += 2
        elif input_day == '어제':
            cur_day -= 1
        elif input_day in ['그저께', '그제']:
            cur_day -= 2
    elif input_day[0] in day:
        cur_day = day.index(input_day[0])
    cur_day %= 7
    conn = http.client.HTTPConnection('www.anissia.net')
    conn.request('GET','/anitime/list?w='+str(cur_day))
    res = conn.getresponse()
    ani_data = res.read().decode('utf-8')
    conn.close()

    ani_data = json.loads(ani_data)
    content = ['{}:{} | {}'.format(item['t'][:2], item['t'][2:], item['s']) for item in ani_data];
    content.insert(0, ' Time | Title\n```\n```')
    msg = '*{day}요일 애니편성표*\n```\n{content}\n```'.format(
        day=day[cur_day],
        content='\n'.join(content)
    )
    outputs.append([peer, msg])
