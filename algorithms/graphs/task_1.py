import sys
sys.path.append('../graphs')

from collections import defaultdict
from heapq import heappop, heappush

from utils import(
    Result, 
    BaseGraph, 
    load_graph, 
    load_decoder_and_encoder, 
    save_neighbours_and_nodes, 
    save_pages
)


PAGELINKS_PATH = '/Users/nikitaseleznev/Downloads/simple_english_wiki/simple_english_wiki_pagelinks.csv'
PAGES_PATH = '/Users/nikitaseleznev/Downloads/simple_english_wiki/simple_english_wiki_pages.csv'

SAVE_TO = '/Users/nikitaseleznev/Downloads/simple_english_wiki/'


class WikiraceGrapth(BaseGraph):
    def __init__(self):
        super().__init__()
        self.decoder = None
        self.encoder = None

    def decode(self, vertex):
        if self.decoder is not None:
            return self.decoder[vertex]
        return [vertex]

    def encode(self, vertex):
        if self.encoder is not None:
            return self.encoder[vertex]
        return vertex

    def load_graph(self, path: str,
                   neighbours_file_name: str = 'neighbours_dict', 
                   nodes_file_name: str = 'nodes_dict') -> None:


        self.neighbours, self.nodes = load_graph(path, 
                                                 neighbours_file_name, 
                                                 nodes_file_name)

    def load_decoder_and_encoder(self, path: str) -> None:
        self.decoder, self.encoder = load_decoder_and_encoder(path)

    def extended_deijkstra(self,
                           start, end = None, 
                           is_allow_length: bool = False) -> Result:

        if len(self.decode(start)) > 1:
            raise ValueError(f'start page name {start} has several id {self.decode(start)}')
        
        if len(self.decode(end)) > 1:
            raise ValueError(f'start page name {end} has several id {self.decode(end)}')

        start, end = self.decode(start)[0], self.decode(end)[0]

        heap, seen_vertices, min_distances = [(0, start)], set(), {start: 0}

        shortest_path = defaultdict(list)
        shortest_path[start].append(start)

        while heap:
            current_distance, current_vertex = heappop(heap)
            if current_vertex not in seen_vertices:
                for _, next_vertex, distance in self[current_vertex]:
                    if next_vertex in seen_vertices:
                        continue
                    distance = distance if not is_allow_length else len(self.encode(next_vertex))
                    prev_min_distance = min_distances.get(next_vertex)
                    new_distance = current_distance + distance
                    

                    if prev_min_distance is None or new_distance < prev_min_distance:
                        min_distances[next_vertex] = new_distance
                        heappush(heap, (new_distance, next_vertex))

                        shortest_path[next_vertex] = shortest_path[current_vertex].copy()
                        shortest_path[next_vertex].append(next_vertex)
                        shortest_path
            
                seen_vertices.add(current_vertex)
                
                if end is not None and current_vertex == end:
                    break

        path = shortest_path[current_vertex]

        result = Result(min_distances[current_vertex], self.encode(path[-2]))

        return result


if __name__ == '__main__':

    ## save
    # save_neighbours_and_nodes(csv_path=PAGELINKS_PATH, 
    #                           src_col='pl_from', dst_col='pl_to', 
    #                           save_to=SAVE_TO)

    # save_pages(csv_path=PAGES_PATH, save_to=SAVE_TO)

    graph = WikiraceGrapth()

    graph.load_graph(path=SAVE_TO)
    graph.load_decoder_and_encoder(path=SAVE_TO)

    result_12 = graph.extended_deijkstra(start='Analytics', 
                                        end='Algorithm', 
                                        is_allow_length=False)

    result_34 = graph.extended_deijkstra(start='Analytics', 
                                        end='Algorithm', 
                                        is_allow_length=True)
    print(*result_12)
    print(*result_34)
