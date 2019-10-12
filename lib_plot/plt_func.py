import json
import copy
import json
import os
import sys

import matplotlib.pyplot as plt
import numpy as np


"""
（きれいな）グラフを書くためのライブラリ
"""


class MakePlot :
    def __init__(self, y, x=None, yerr=None):
        """
        コンストラクタ
        """
        self.read_settings()
        
        self.figure = plt.figure()
        self.axis_ = self.figure.add_subplot(111)
        
        self.x = x
        self.y_copy = copy.deepcopy(y)
        self.yerr = yerr
        self.color_list = ["red", "blue"]
    
    
    def read_settings(self, ):
        """
        設定ファイルの読み込み
        """
        filepath = os.path.dirname(__file__) + "/settings.json"
        with open(filepath, "r") as fr:
            settings = json.load(fr)
        
        for key, val in settings:
            plt.rcParams[key] = val
    
    
    def calculate_mean(self, y=self.y_copy, transpose=False):
        """
        平均値，標準偏差，標準誤差を計算する関数
        
        y: list型  1または2次元配列
        transpose: boolen型
        
        """
        # 転置したいとき
        if transpose:
            if type( np.array(y)[0] ) == np.ndarray:
                y = np.array(y).T
            else:
                raise ValueError("y 内の配列の長さが異なるため転置できません")
        
        mean_list = []
        std_list = []
        se_list = []
        if np.array(y).ndim==2:
            for arr in y:
                mean_list.append( np.mean(arr) )
                std_list.append( np.std(arr) )
                se_list.append( np.std(arr) / np.sqrt(len(arr)) )
        elif np.array(y).ndim==3:
            for arr in y:
                tmp_mean_list = []
                tmp_std_list = []
                tmp_se_list = []
                for arr2 in arr:
                    tmp_mean_list.append( np.mean(arr2) )
                    tmp_std_list.append( np.std(arr2) )
                    tmp_se_list.append( np.std(arr2) / np.sqrt(len(arr2)) )
                mean_list.append(tmp_mean_list)
                std_list.append(tmp_std_list)
                se_list.append(tmp_se_list)
        
        
        return mean_list, std_list, se_list
    
    
    def bar_graph_from_scratch(self, x=self.x, error_bar="SE", xlabel=None, ylabel=None, title=None):
        """
        データから平均値, 標準偏差（標準誤差）を計算し，棒グラフを計算する
        
        Parameters
        ----------------------------------
        x: list型
        error_bar: str型 "SE" or "STD"
        xlabel: 
        ylabel: 
        ----------------------------------
        
        """
        mean_list, std_list, se_list = calculate_mean(self.y_copy)
        
        if error_bar=="SE":
            fig, ax = self.bar_graph_by_mean(x=x, y=mean_list, yerr=se_list, xlabel=xlabel, title=title)
        elif error_bar=="STD":
            fig, ax = self.bar_graph_by_mean(x=x, y=mean_list, yerr=std_list, ylabel=ylabel, title=title)
        else:
            yerr = [ 0 for i in range( len(mean_list) ) ]
            fig, ax = self.bar_graph_by_mean(x=x, y=mean_list, yerr=yerr, xlabel=xlabel, ylabel=ylabel, title=title)
        
        
        return fig, ax
    
    
    def bar_graph_by_mean(self, x=self.x, y=self.y_copy, yerr=self.yerr, width=0.8, color="blue", log=False, xlabel=None, ylabel=None, title=None):
        """
        棒グラフ 2つの比較，複数の比較
        平均，標準偏差（標準誤差）が分かっているときに用いる関数
        yerr: list型
        x: list型
        y: list型
        width: float型
        color: str型
        log: boolen型
        
        """
        if x is None:
            x = [i for i in range(1, len(y)+1)]
        
        self.axis_.bar(
            x=x, 
            height=y, 
            width=width,
            color=color,
            yerr=yerr,
            ecolor="black",
            capsize=8,
            log=log,
            )
        
        self.axis_.set_xlabel(xlabel)
        self.axis_.set_ylabel(ylabel)
        self.axis_.set_title(title)
        plt.tight_layout()
        
        
        return self.figure, self.axix_
    
    
    def multiple_bar_graph(self, legends, y=self.y_copy, x=self.x, width=None, error_type="SE", xlabel=None, ylabel=None, title=None):
        """
        1つのラベルに対して2個以上の棒グラフを作成
        
        Parameters
        -----------------------------
        legends: list型  凡例
        y: list型  
        x: list型  横軸
        width: float型  棒グラフの幅
        -----------------------------
        
        """
        bar_num = len(legends)  # 1ラベルに対する棒グラフの数
        left = np.arange(len(x))
        mean_list, std_list, se_list = calculate_mean(y)  # 2次元配列が返ってくる
        
        # widthの計算
        if bar_num<=4:
            width = 0.8 / bar_num
        else:
            pass
        
        if error_type=="SE":
            for i in range(len(x)):
                self.axis_.bar(left, mean_list[i], yerr=se_list, color=self.color_list[i], width=width, align="center", label=legends[i])
                left += width
        elif error_type=="STD":
            for i in range(len(x)):
                self.axis_.bar(left, std_list[i], yerr=se_list, color=self.color_list[i], width=width, align="center", label=legends[i])
                left += width
        else:
            for i in range(len(x)):
                self.axis_.bar(left, mean_list[i], color=self.color_list[i], width=width, align="center", label=legends[i])
                left += width
        
        # ラベルを付ける
        if bar_num==2:
            self.axis_.set_xtics(np.arange(len(x))+width/2, x)
        elif bar_num==3:
            self.axis_.set_xtics(np.arange(len(x))+width, x)
        elif bar_num==4:
            self.axis_.set_xtics(np.arange(len(x))+3*width/2, x)
        else:
            self.axis_.set_xtics(np.arange(len(x))+2*width, x)
        
        # 凡例
        self.axis_.legend(loc="best")
        self.axis_.set_xlabel(xlabel)
        self.axis_.set_ylabel(ylabel)
        self.axis_.set_title(title)
        plt.tight_layout()
        
        
        return self.figure, self.axis_
    
    
    def cumulative_bar_graph(self, legends, xlabel=None, ylabel=None, title=None):
        """
        積み上げ棒グラフ 2つの比較，複数の比較
        
        height: 1または2次元配列
        legends: list型  凡例
        
        """
        if type( np.array(self.y_copy)[0] ) == np.ndarray:
            raise ValueError("y 内の配列の長さが異なるためグラフを作成することができない")
        

        sum_arr = np.array([0 for _ in range(len(self.x))])
        for i in range(len(self.x)):
            if i==0:
                self.axis_.bar(self.x, self.y_copy[i], color=self.color_list[i], label=legends[i]) 
                sum_arr += np.array(self.y_copy[i])
            else:
                self.axis_.bar(self.x, self.y_copy[i], bottom=sum_arr, color=self.color_list[i], label=legends[i])
                sum_arr += np.array(self.y_copy[i])
        
        self.axis_.legend(loc="best")
        self.axis_.set_xlabel(xlabel)
        self.axis_.set_ylabel(ylabel)
        self.axis_.set_title(title)
        
        plt.tight_layout()
        
        
        return self.figure, self.axis_
    
    
    def line_graph(self, legends, x=self.x, xlabel=None, ylabel=None, title=None, yrange=[]):
        """
        折れ線グラフ作成関数
        
        Parameters
        -----------------------------
        legends: list型  凡例
        x: list型  横軸
        xlabel: str型  横軸のラベル
        ylabel: str型  縦軸のラベル
        yrange: list型  y軸の範囲
        -----------------------------
        
        """
        for i,arr in enumerate(self.y_copy):
            self.axis_.plot(self.x, arr, label=legends[i])
        
        self.axis_.set_xlabel(xlabel)
        self.axis_.set_ylabel(ylabel)
        
        if yrange==[]:
            pass
        else:
            self.axis_set_ylim(yrange)
        
        self.axis_.set_title(title)
        
        plt.legend(loc="best")
        plt.tight_layout()
        
        return self.figure, self.axis_
    
        
    def box_whisker_graph(self, xlabel=None, ylabel=None, title=None):
        """
        箱ひげ図の作成
        
        
        """
        self.axis_.boxplot(self.y_copy)
        self.axis_.set_xticklabels(self.x)
        
        self.axis_.set_xlabel(xlabel)
        self.axis_.set_ylabel(ylabel)
        self.axis_.grid()
        self.axis_.set_title(title)
        
        
        return self.figure, self.axis_
    
    
    def histogram_graph(self, y=self.y_copy, bins=50, normed=False, xlabel=None, ylabel=None, title=None):
        """
        ヒストグラムの作成
        
        y: list型  1次元配列
        bins: int型  ビンの数
        normed: boolen型  Trueの場合，縦軸の和が1.0になるように正規化
        
        """
        self.axis_.hist(y, bins=bins, normed=True)
        self.axis_.set_xlabel(xlabel)
        self.axis_.set_ylabel(ylabel)
        self.axis_.set_title(title)


if __name__ == "__main__":
    
    # 準備
    import numpy as np
    x = np.arange(10)
    y = np.random.randn(10)
    
    
    