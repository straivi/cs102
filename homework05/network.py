from api import get_friends, names
import igraph
from igraph import Graph, plot


def get_network(users_ids, as_edgelist=True):
    # PUT YOUR CODE HERE
    # Создание вершин и ребер
    matrix = [[0] * len(users_ids) for _ in range(len(users_ids))]
    edges = []
    for user in users_ids:
        print(users_ids.index(user) + 1, names[users_ids.index(user)])
        friends = get_friends(user, "")
        for friend in friends:
            if friend in users_ids:
                edges.append((users_ids.index(user), users_ids.index(friend)))
                matrix[users_ids.index(user)][users_ids.index(friend)] = 1
    if as_edgelist:
        return edges
    else:
        return matrix

def plot_graph(edges: list, vertices: list = []) -> None:
    if vertices == 0: vertices = [i for i in range(edges)]
    print("строим график")
    graph = Graph(vertex_attrs={"label": vertices},
              edges=edges, directed=False)
    # Задаем стиль отображения графа
    verticesCount = len(vertices)
    visual_style = {}
    visual_style["layout"] = graph.layout_fruchterman_reingold(
        maxiter=1000,
        area=verticesCount**3,
        repulserad=verticesCount**3)
    graph.simplify(multiple=True, loops=True)
    visual_style = {
        "vertex_size": 30,
        "bbox": (2000, 2000),
        "margin": 100,
        "vertex_label_dist": 3,
        "vertex_label_size": 25,
        "edge_color": "gray",
        "autocurve": True,
        "layout": graph.layout_fruchterman_reingold(
            maxiter=100000,
            area=verticesCount ** 2,
            repulserad=verticesCount ** 2)
    }

    clusters = graph.community_multilevel()
    pal = igraph.drawing.colors.ClusterColoringPalette(len(clusters))
    graph.vs['color'] = pal.get_many(clusters.membership)
    plot(graph, **visual_style)

id = 141614829
users, names = get_friends(id), names(id)
ids = []
for i in range(len(users)):
    ids.append(users[i]['id'])
ed = get_network(ids)
plot_graph(ed, names)