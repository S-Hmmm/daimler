from src.resp import c


def test_cov():
    result = {
        'code': 0
    }
    assert c(result) == '成功'
    result = {
        'code': 1
    }
    assert c(result) == '失败'
    result = {
        'code': 2
    }
    assert c(result) == '无效'
