## Команды для запуска 
### issue-01 
```python
python3 -m doctest -v issue-01.py > .\result_01.txt
```
### issue-02 
```python
python3 -m pytest -v issue-02.py > .\result_02.txt
```
### issue-03 
```python
python3 -m unittest -v issue-03.py 2> .\result_03.txt 
```
### issue-04
```python
python3 -m pytest -v issue-04.py > .\result_04.txt
```
### issue-05
## запусн
```python
python3 -m unittest -v issue-05.py 2> .\result_05.txt
```
### для получения отсчета покрытия
```python
python3 -m coverage run -m unittest issue-05.py
python3 -m coverage html
```