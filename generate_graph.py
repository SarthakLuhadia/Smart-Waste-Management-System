import json
import math
import pygame
import sys
import heapq

class GraphGenerator:
    def __init__(self, name):
        pygame.init()

        self.name = name
        self.map = pygame.image.load(f'data/maps/{self.name}/{self.name}.png')
        self.screen = pygame.display.set_mode((self.map.get_width(), self.map.get_height()))
        self.screen.blit(self.map, (0, 0))

        self.graph = {}
        self.num_of_nodes = 0
        self.current_node_idx = 0

        self.first_point = None

    def node_exists(self, pos):
        for node in self.graph:
            if self.distance(pos, [self.graph[node]['pos']['x'], self.graph[node]['pos']['y']]) <= 5:
                return node
        return None

    def distance(self, node1, node2):
        return math.sqrt((node2[0] - node1[0])**2 + (node2[1] - node1[1])**2)

    def add_node(self, pos, type):
        self.graph[self.current_node_idx] = {'pos': {'x': pos[0], 'y': pos[1]}, 'type': type, 'neighbors': {}}
        self.current_node_idx += 1
        self.num_of_nodes += 1

    def delete_node(self, idx):
        self.graph.pop(idx)
        self.num_of_nodes -= 1
        for node in self.graph.copy():
            for neighbor in self.graph[node]['neighbors'].copy():
                if neighbor == idx:
                    self.graph[node]['neighbors'].pop(neighbor)

    def add_edge(self, neighbor):
        self.graph[self.first_point]['neighbors'][neighbor] = self.distance([self.graph[self.first_point]['pos']['x'], self.graph[self.first_point]['pos']['y']], [self.graph[neighbor]['pos']['x'], self.graph[neighbor]['pos']['y']])
        self.graph[neighbor]['neighbors'][self.first_point] = self.distance([self.graph[self.first_point]['pos']['x'], self.graph[self.first_point]['pos']['y']], [self.graph[neighbor]['pos']['x'], self.graph[neighbor]['pos']['y']])

    def update_graph(self):
        self.screen.blit(self.map, (0, 0))
        for node in self.graph:
            if self.graph[node]['type'] == 'bin':
                pygame.draw.circle(self.screen, (255,0,0), (self.graph[node]['pos']['x'], self.graph[node]['pos']['y']), 5)
            elif self.graph[node]['type'] == 'intersection':
                pygame.draw.circle(self.screen, (0,255,0), (self.graph[node]['pos']['x'], self.graph[node]['pos']['y']), 5)
            elif self.graph[node]['type'] == 'garage':
                pygame.draw.circle(self.screen, (0,0,255), (self.graph[node]['pos']['x'], self.graph[node]['pos']['y']), 5)

            for neighbor in self.graph[node]['neighbors']:
                pygame.draw.line(self.screen, (255, 0, 0), (self.graph[node]['pos']['x'], self.graph[node]['pos']['y']), (self.graph[neighbor]['pos']['x'], self.graph[neighbor]['pos']['y']))

    def update(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    print("Saving graph")
                    with open(f'data/maps/{self.name}/{self.name}.json', 'w') as file:
                        file.write(json.dumps(self.graph))

                if event.key == pygame.K_RETURN:
                    print("Generating shortest path graph")
                    shortest_path_graph = generate_shortest_path_graph(self.graph)
                    print("Shortest path graph generated")
                    print("Updating graph display")
                    self.graph = shortest_path_graph
                    print("Graph display updated")

                if event.key == pygame.K_x:
                    pos = pygame.mouse.get_pos()
                    node_nearby = self.node_exists(pos)
                    if node_nearby is not None:
                        print("Deleting node")
                        self.delete_node(node_nearby)

            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                node_nearby = self.node_exists(pos)

                if node_nearby == None:
                    if (event.button == 1):
                        print("Adding intersection")
                        self.add_node(pos, 'intersection')

                    if (event.button == 2):
                        print("Adding bin")
                        self.add_node(pos, 'bin')

                    if (event.button == 3):
                        print("Adding garage")
                        self.add_node(pos, 'garage')
                
                else:
                    print("Node exists")
                    if self.first_point is None:
                        print("First point selected, click on next point to create edge")
                        self.first_point = node_nearby

                    else:
                        print("Second point selected, creating edge")
                        self.add_edge(node_nearby)
                        self.first_point = None

        self.update_graph()
        pygame.display.update()

def dijkstra_shortest_paths(graph, source):
    dist = {node: float('inf') for node in graph}
    dist[source] = 0
    visited = set()
    queue = [(0, source)]
    prev = {}

    while queue:
        current_distance, current_node = heapq.heappop(queue)

        if current_node in visited:
            continue

        visited.add(current_node)

        for neighbor, weight in graph[current_node]['neighbors'].items():
            distance = current_distance + weight
            if distance < dist[neighbor]:
                dist[neighbor] = distance
                prev[neighbor] = current_node  # Update the predecessor for the neighbor node
                heapq.heappush(queue, (distance, neighbor))

    return dist, prev


def shortest_path(graph, source, target, prev):
    path = []
    node = target
    while node != source:
        path.append(node)
        node = prev[node]
    path.append(source)
    path.reverse()
    return path

def generate_shortest_path_graph(graph):
    shortest_path_graph = {}
    garage_node = next((node for node, data in graph.items() if data['type'] == 'garage'), None)
    
    if garage_node is not None:
        shortest_distances, prev = dijkstra_shortest_paths(graph, garage_node)
        
        # Add all nodes to shortest path graph
        for node, data in graph.items():
            shortest_path_graph[node] = {'pos': data['pos'], 'type': data['type'], 'neighbors': {}}
        
        # Connect bin nodes to garage node using shortest paths
        for bin_node in shortest_path_graph:
            if shortest_path_graph[bin_node]['type'] == 'bin':
                shortest_path_to_bin = shortest_path(graph, garage_node, bin_node, prev)
                for i in range(len(shortest_path_to_bin) - 1):
                    current_node = shortest_path_to_bin[i]
                    next_node = shortest_path_to_bin[i + 1]
                    shortest_path_graph[current_node]['neighbors'][next_node] = graph[current_node]['neighbors'][next_node]
                    shortest_path_graph[next_node]['neighbors'][current_node] = graph[next_node]['neighbors'][current_node]

    return shortest_path_graph


def main():
    graph_generator = GraphGenerator("pondicherry_india")
    
    running = True

    while running:
        graph_generator.update()

if __name__ == "__main__":
    main()



