# Smart-Waste-Management-System

# before and after
![WhatsApp Image 2024-08-04 at 15 24 39_ba835a34](https://github.com/user-attachments/assets/80105d14-2c54-4b50-a977-06d5b867b1aa)
![WhatsApp Image 2024-08-04 at 15 26 47_d6442e35](https://github.com/user-attachments/assets/5e3dc6bd-77bb-4a7e-a76f-beb7553f6301)

# Smart Waste Management System

This project is a Smart Waste Management System that uses a map interface to place bins, intersections, and garages. It uses Dijkstra's algorithm to calculate the shortest paths for waste collection.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/Smart-Waste-Management-System.git
    cd Smart-Waste-Management-System
    ```

2. Install the required libraries:

    ```bash
    pip install pygame
    ```

## Usage

### Graph Generator

The Graph Generator allows you to create and modify the map, adding nodes and edges as necessary.

1. Run the Graph Generator:

    ```bash
    python graph_generator.py
    ```

2. Use the following controls to interact with the map:

    - **Left-click:** Add an intersection.
    - **Middle-click:** Add a bin.
    - **Right-click:** Add a garage.
    - **Space:** Save the graph to a JSON file.
    - **Enter:** Generate the shortest path graph.
    - **X:** Delete a node (click on a node to delete it).



### Graph Loader

The Graph Loader allows you to load and view the saved map and graph data.

1. Run the Graph Loader:

    ```bash
    python graph_loader.py --town_name pondicherry_india
    ```

2. Use the following controls to interact with the map:

    - **Q:** Quit the application.

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -m 'Add some feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Open a Pull Request.

