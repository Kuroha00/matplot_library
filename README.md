# pythonできれいめなグラフを出力するためのライブラリ

## Requirements
- Python
    - 3.6.4 or greater

## How To Use
```
$ cd matplot_library

$ python
>>> import lib_plot
or
>>> from lib_plot import MakePlot

基本的には生データを入力とし，中で平均と標準偏差，標準誤差を算出してグラフを作成する．
入力データの形状，種類に関しては生成するグラフの種類により変わる
```


## methods

- read_settings ( )  
matplotlibの設定(settings.json)を読み込んで設定する

- calculate_mean ( )  
生データから平均，標準偏差，標準誤差を算出する

- bar_graph_from_scratch ( )  


- bar_graph_by_mean ( )  
この関数のみ平均値と標準偏差/標準誤差を入力として棒グラフを出力する関数

- multiple_bar_graph ( )  
1ラベルに対して2つ以上の棒グラフを表示するグラフ  
1ラベルに対する棒グラフの数が凡例に対応する  
Args  
legends: 凡例，  
x:  横軸ラベル  
y:  生データ  
yの形状が(3,2,100)である場合，2が横軸のラベル数，3が凡例数, 100がデータ数に対応する  


- cumulative_bar_graph ( )  
積み上げグラフを作成  


- line_graph ( )  
折れ線グラフを作成


- box_whisker_graph ( )  
箱ひげ図を作成


- histogram_graph ( )  
ヒストグラフを作成

