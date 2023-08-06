import time, sys, os

def pgbar(
        data,
        pre='',
        post='',
        bar_icon='=',
        space_icon=' ',
        total_display=1000,
        show_running_time=True,
        running_time_format='%02dh%02dm%02ds',
        show_cnt=True, end='\r',
        size=None):
    'PRE [PGBAR] [000%|0000/0000] [00h00m00s] POST'
    
    if not size:
        size = len(data)
    tsize, _ = os.get_terminal_size()
    bsize = tsize - len(pre) - len(post) - 13

    if show_running_time:
        bsize -= 12
    if show_cnt:
        bsize -= len(str(size)) * 2
    if len(pre) > 0:
        pre = ' %s' % pre
        bsize -= 1

    start_time = time.time()

    for i, d in enumerate(data):
        bar = bar_icon * (bsize * (i + 1) // size // len(bar_icon))
        space = space_icon * (bsize - len(bar))

        total_time = int(time.time() - start_time)
        hour = total_time // 3600
        minute = total_time % 3600 // 60
        second = total_time % 60

        info = ''
        if show_running_time:
            running_time = running_time_format % (hour, minute, second)
            if not show_cnt:
                info = ' [%s]' % running_time
            else:
                info = running_time

        if show_cnt:
            cnt = '%%0%dd/%d' % (len(str(size)), size)
            cnt = cnt % (i + 1)
            if show_running_time:
                info = ' [%s|%s]' % (running_time[:-1], cnt)
            else:
                info = ' [%s]' % cnt

        if size < total_display or i % (size // total_display) == 0 or i == size - 1:
            print('%s [%s%s] [%3d%%]%s %s' % (pre, bar, space, 100 * (i + 1) // size, info, post), end=end)
        if i == size - 1:
            print()

        time.sleep(0.1)
        yield d

        if i == size - 1:
            break

