

def c(result):
    if result.get('code') == 0:
        return '成功'
    elif result.get('code') == 1:
        return '失败'
    else:
        return '无效'
