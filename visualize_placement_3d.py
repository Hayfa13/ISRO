import json
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

def draw_box(ax, start, end, label, color='skyblue'):
    x, y, z = start['width'], start['depth'], start['height']
    dx = end['width'] - x
    dy = end['depth'] - y
    dz = end['height'] - z

    verts = [
        [(x, y, z), (x + dx, y, z), (x + dx, y + dy, z), (x, y + dy, z)],
        [(x, y, z + dz), (x + dx, y, z + dz), (x + dx, y + dy, z + dz), (x, y + dy, z + dz)],
        [(x, y, z), (x + dx, y, z), (x + dx, y, z + dz), (x, y, z + dz)],
        [(x + dx, y, z), (x + dx, y + dy, z), (x + dx, y + dy, z + dz), (x + dx, y, z + dz)],
        [(x + dx, y + dy, z), (x, y + dy, z), (x, y + dy, z + dz), (x + dx, y + dy, z + dz)],
        [(x, y + dy, z), (x, y, z), (x, y, z + dz), (x, y + dy, z + dz)],
    ]

    box = Poly3DCollection(verts, alpha=0.5, facecolor=color, edgecolor='black')
    ax.add_collection3d(box)
    ax.text(x + dx/2, y + dy/2, z + dz/2, label, color='black', fontsize=8, ha='center')
    ax.text(
    x + dx/2, y + dy/2, z + dz + 3,  # move label *above* the box
    label,
    color='black',
    fontsize=9,
    ha='center',
    va='bottom',
    zorder=10
)


def visualize_placement(json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)

    fig = plt.figure(figsize=(14, 8))
    ax = fig.add_subplot(111, projection='3d')

    placements = data.get('placements', [])
    id_to_name = {item['itemId']: item['name'] for item in data.get('items', [])}  # Optional addition

    for item in placements:
        start = item['position']['startCoordinates']
        end = item['position']['endCoordinates']
        item_id = item['itemId']
        name = id_to_name.get(item_id, "")  # Fallback in case name is not present
        label = f"{item_id}\n{name}"  # Show ID + Name
        draw_box(ax, start, end, label)

    ax.set_xlabel('Width')
    ax.set_ylabel('Depth')
    ax.set_zlabel('Height')
    ax.set_title('3D Cargo Placement Visualization')

    plt.tight_layout()
    plt.show()

# Call the function
visualize_placement('placement_output.json')
