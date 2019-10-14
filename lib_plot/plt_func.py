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


class MakeGraph :
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
        self.color_list = ["red", "blue", "green", "yellow", "black"]
        self.hatches = ["//", "x", "..", "||"]
        self.markers = ["o", "s", "+", "^"]
        
    
    def read_settings(self, ):
        """
        設定ファイルの読み込み
        """
        filepath = os.path.dirname(__file__) + "/settings.json"
        with open(filepath, "r") as fr:
            settings = json.load(fr)
        
        for key, val in settings.items():
            plt.rcParams[key] = val
    
    
    def calculate_mean(self, y=None, transpose=False):
        """
        平均値，標準偏差，標準誤差を計算する関数
        
        y: list型  1または2次元配列
        transpose: boolen型
        
        """
        if y is None:
            y = self.y_copy
        
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
    
    
    def bar_graph_from_scratch(self, error_bar="SE", xlabel=None, ylabel=None, title=None):
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
        mean_list, std_list, se_list = self.calculate_mean()
        
        if error_bar=="SE":
            fig, ax = self.bar_graph_by_mean(x=self.x, y=mean_list, yerr=se_list, xlabel=xlabel, ylabel=ylabel, title=title)
        elif error_bar=="STD":
            fig, ax = self.bar_graph_by_mean(x=self.x, y=mean_list, yerr=std_list, ylabel=ylabel, title=title)
        else:
            yerr = [ 0 for i in range( len(mean_list) ) ]
            fig, ax = self.bar_graph_by_mean(x=self.x, y=mean_list, yerr=yerr, xlabel=xlabel, ylabel=ylabel, title=title)
        
        
        return fig, ax
    
    
    def bar_graph_by_mean(self, x=None, y=None, yerr=None, width=0.8, color="blue", log=False, xlabel=None, ylabel=None, title=None):
        """
        棒グラフ 2つの比較，複数の比較
        平均，標準偏差（標準誤差）が分かっているときに用いる関数
        
        parameters
        ---------------------------
        yerr: list型
        x: list型
        y: list型
        width: float型
        color: str型
        log: boolen型
        ---------------------------
        
        """
        if x is None:
            x = self.x
        if self.x is None:
            x = [i for i in range(1, len(y)+1)]
        
        if y is None:
            y = self.y_copy
        
        if yerr is None:
            yerr = self.yerr
        if yerr is None:
            yerr = [0 for i in range(len(y))]
        
        self.axis_.bar(
            x=x, 
            height=y, 
            width=width,
            hatch=self.hatches[0],
            fill=None,
            yerr=yerr,
            ecolor="black",
            capsize=9,
            log=log,
            )
        
        self.axis_.set_xlabel(xlabel)
        self.axis_.set_ylabel(ylabel)
        self.axis_.set_title(title)
        plt.tight_layout()
        
        
        return self.figure, self.axis_
    
    
    def multiple_bar_graph(self, legends, x=None, y=None, width=None, error_type="SE", xlabel=None, ylabel=None, title=None):
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
        if x is None:
            x = self.x
        if y is None:
            y = self.y_copy
        
        bar_num = len(legends)  # 1ラベルに対する棒グラフの数
        left = np.arange(len(x)).astype(np.float64)
        mean_list, std_list, se_list = self.calculate_mean(y=y)  # 2次元配列が返ってくる
        
        # widthの計算
        if bar_num<=4:
            width = 0.8 / bar_num
        else:
            pass
        
        if error_type=="SE":
            for i in range(bar_num):
                self.axis_.bar(left, mean_list[i], yerr=se_list[i], capsize=9, hatch=self.hatches[i], width=width, align="center", label=legends[i], fill=None)
                left += width
        elif error_type=="STD":
            for i in range(bar_num):
                self.axis_.bar(left, mean_list[i], yerr=std_list[i], capsize=9, hatch=self.hatches[i], width=width, align="center", label=legends[i], fill=None)
                left += width
        else:
            for i in range(bar_num):
                self.axis_.bar(left, mean_list[i], hatch=self.hatches[i], width=width, align="center", label=legends[i], fill=None)
                left += width
        
        # ラベルを付ける
        if bar_num==2:
            self.axis_.set_xticks(np.arange(bar_num)+width/2)
            self.axis_.set_xticklabels(x)
        elif bar_num==3:
            self.axis_.set_xticks(np.arange(len(x))+width)
            self.axis_.set_xticklabels(x)
        elif bar_num==4:
            self.axis_.set_xtics(np.arange(len(x))+3*width/2)
            self.axis_.set_xticklabels(x)
        else:
            self.axis_.set_xtics(np.arange(len(x))+2*width)
            self.axis_.set_xticklabels(x)
        
        # 凡例
        self.axis_.legend(loc="best", fontsize=13)
        self.axis_.set_xlabel(xlabel)
        self.axis_.set_ylabel(ylabel)
        self.axis_.set_title(title)
        plt.tight_layout()
        
        
        return self.figure, self.axis_
    
    
    def cumulative_bar_graph(self, legends, xlabel=None, ylabel=None, title=None):
        """
        積み上げ棒グラフ 2つの棒グラフの比較，複数の棒グラフの比較
        
        height: 1または2次元配列
        legends: list型  凡例
        
        """
        # print( type( np.array(self.y_copy)[0] ) == np.ndarray )
        if not ( type( np.array(self.y_copy)[0] ) == np.ndarray ):
            raise ValueError("y 内の配列の長さが異なるためグラフを作成することができない")
        else:
            pass

        mean_list, std_list, se_list = self.calculate_mean(y=self.y.copy)
        
        sum_arr = np.array([0 for _ in range(len(self.x))])
        for i in range(len(self.x)):
            if i==0:
                self.axis_.bar(self.x, self.y_copy[i], label=legends[i], hatch=self.hatches[i], fill=None) 
                sum_arr += np.array(self.y_copy[i])
            else:
                self.axis_.bar(self.x, self.y_copy[i], bottom=sum_arr, label=legends[i], hatch=self.hatches[i], fill=None)
                sum_arr += np.array(self.y_copy[i])
        

        self.axis_.legend(loc="best", fontsize=13)
        self.axis_.set_xlabel(xlabel)
        self.axis_.set_ylabel(ylabel)
        self.axis_.set_title(title)
        
        plt.tight_layout()
        
        
        return self.figure, self.axis_
    
    
    def line_graph(self, legends, x=None, xlabel=None, ylabel=None, title=None, yrange=[]):
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
        linestyles = ["solid", "dashed", "dotted", "dashdot"]
        markers = ["o", "s", "+", "^"]
        if x is None:
            x = self.x
        
        for i,arr in enumerate(self.y_copy):
            self.axis_.plot(
                self.x, 
                arr, 
                label=legends[i], 
                linestyle=linestyles[i], 
                color="k", 
                marker=self.markers[i], 
                markersize=11
                )
        
        self.axis_.set_xlabel(xlabel)
        self.axis_.set_ylabel(ylabel)
        
        if yrange==[]:
            pass
        else:
            self.axis_set_ylim(yrange)
        
        self.axis_.set_title(title)
        
        plt.legend(loc="best", fontsize=13)
        plt.tight_layout()
        
        return self.figure, self.axis_
    
    
    def box_whisker_graph(self, xlabel=None, ylabel=None, title=None):
        """
        箱ひげ図の作成
        
        """
        self.axis_.boxplot(self.y_copy, whis="range")
        self.axis_.set_xticklabels(self.x)
        
        self.axis_.set_xlabel(xlabel)
        self.axis_.set_ylabel(ylabel)
        self.axis_.set_title(title)
        self.axis_.grid()
        plt.tight_layout()
        
        
        return self.figure, self.axis_
    
    
    def histogram_graph(self, y=None, bins=50, normed=False, xlabel=None, ylabel=None, title=None):
        """
        ヒストグラムの作成
        
        y: list型  1次元配列
        bins: int型  ビンの数
        normed: boolen型  Trueの場合，縦軸の和が1.0になるように正規化
        
        """
        if y is None:
            y = self.y_copy
        
        self.axis_.hist(y, bins=bins, normed=True)
        self.axis_.set_xlabel(xlabel)
        self.axis_.set_ylabel(ylabel)
        self.axis_.set_title(title)
        
        
        return self.figure, self.axis_
    
    
    def scatter_graph(self, legends, x=None, y=None, xlabel=None, ylabel=None, title=None):
        """
        散布図を作成
        
        Parameters
        ---------------------------------
        legends: 
        x: list型 1or2次元
        y: list型 1or2次元  xとyは同じ次元，同じ長さである必要がある
        xlabel:
        ylabel:
        title:
        ---------------------------------
        
        """
        if x is None:
            x = self.x
        
        if y is None:
            y = self.y_copy
        
        for i in range(len(x)):
            self.axis_.scatter(x[i], y[i], s=30, marker=self.markers[i], c="black", edgecolors="black", label=legends[i])
        
        self.axis_.set_xlabel(xlabel)
        self.axis_.set_ylabel(ylabel)
        self.axis_.set_title(title)
        
        plt.legend(loc="best", fontsize=13)
        plt.tight_layout()
        
        
        return self.figure, self.axis_

        