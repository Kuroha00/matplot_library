import numpy as np
import matplotlib.pyplot as plt

from lib_plot import MakeGraph


def main():
    # x = ["hello", "world", "chao", "konnnitiha"]
    x = ["hello", "world"]
    
    data = [
        [
            [1,2,3,4,5],
            [2,3,4,5,6]
        ],
        [
            [1,2,8,4,5],
            [2,9,4,5,6]
        ],
        [
            [1,2,8,10,5],
            [2,9,1,5,6]
        ]
    ]
    
    # graph = MakeGraph(x=x, y=data)
    
    # graph.bar_graph_from_scratch(
    #     xlabel="test", 
    #     ylabel="testtest", 
    #     title="world"
    #     )
    
    
    # graph.cumulative_bar_graph(
    #     legends=["aa", "bb", "cc"],
    #     xlabel="xlabel",
    #     ylabel="ylabel",
    #     title="title"
    # )
    
    # graph.multiple_bar_graph(
    #     legends=["aa", "bb", "cc"], 
    #     xlabel="test", 
    #     ylabel="testtest", 
    #     title="world",
    #     error_type="SE"
    #     )
    
    data = [
        [
            1,2,3,2,3,4,5,4,5,2,3,4,3,6,1,3,4,5,0,3
        ],
        [
            2,5,3,6,5,4,1,4,3,2,5,8,10,-2,4,3,7,6,4,3
        ],
        [
            2,3,7,8,4,3,1,4,6,8,3,1,3,1,1,4,2,3,2,6
        ],
        [
            5,3,2,3,4,3,3,4,6,1,3,5,3,7,7,4,3,8,6,7
        ]
    ]
    
    # x = np.arange(len(data[0]))
    # legends = ["hello", "world", "chao", "konnnitiha"]
    # graph.line_graph(
    #     legends=legends,
    #     xlabel="test",
    #     ylabel="testtest",
    #     title="title",
    # )
    
    x = [
        [
            1,2,3,4,3,2,3,4
        ],
        [
            3,5,4,2,5,7,6,4
        ],
        [
            6,5,3,6,5,4,5,3
        ],
        [
            7,6,5,4,3,4,3,5
        ]
    ]
    data = [
        [
            4,2,4,5,6,4,3,5
        ],
        [
            7,4,3,2,5,6,7,8
        ],
        [
            1,4,3,2,5,6,8,9
        ],
        [
            1,5,4,7,9,5,3,6
        ]
    ]
    
    x = np.random.randn(4, 40)
    data = np.random.randn(4, 40)
    
    graph = MakeGraph(x=x, y=data)
    graph.scatter_graph(
        legends=["aa", "bb", "cc", "dd"],
        xlabel="xlabel",
        ylabel="ylabel",
        title="title"
        )
    
    # plt.show()
    plt.savefig("test.pdf")


if __name__ == "__main__":
    main()