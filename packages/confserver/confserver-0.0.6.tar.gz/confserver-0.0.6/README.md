
Установка
---------

    apt-get update
    apt-get install --yes mc python3 python3-pip
    pip3 install confserver


Запуск
------

    python -m confserver --path example


Обновление
==========

Windows
-------

    pip install --user --upgrade wheel setuptools twine
    python setup.py sdist bdist_wheel
    C:\Users\vda\AppData\Roaming\Python\Python36\Scripts\twine upload -u dgrapes -p XXXXX dist/*
