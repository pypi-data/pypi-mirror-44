# sekg
this is library for software engineering knowledge graph.

## description
1. including wrapper for neo4j by py2neo.
2. the preprocess tool for stack overflow html.
3. graph2vec library
...
todo

## todo
1. add version helper out of setup

## support
python 3.5 is need, py2neo 4.1.0 must be install in python 3


## Update the library
1. 
    1. update code and test,
    2. update the __version__ in sekg/meta.py, 
    3. update the dependency library in "root/requirements.txt" and in "root/setup.py".
    4. commit it and push to the github
   
2. login the 87 server, and goto project/sekg/

(Or use the <code>screen</code> to go to "sekgPublisher" screen, create if not found).

run git pull , update the code.

3. run command
```
./upload.sh
twine upload dist/*.tar.gz
```
the new version pip install package is uploaded to the pipy.

---
OR:
In windows, run command
```
.\upload.bat
```

4. you can use following command to update the package.

```
pip install sekg
pip install -U sekg
pip install -U sekg -i https://pypi.douban.com/simple
pip install -U sekg -i https://pypi.python.org/
pip install -U sekg -i https://pypi.tuna.tsinghua.edu.cn/simple

```
