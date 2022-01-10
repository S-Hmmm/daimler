import pytest
import subprocess

pytest.main(['-m del_item '])  # '--html=report/html_report/get_item.html', '--self-contained-html'
subprocess.run('allure generate report/raw_report/ -o report/allure_report/ -c', shell=True)
