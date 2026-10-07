"""
Full maze audit: find every pellet cell and classify it as reachable or unreachable.
No game imports needed - pure maze analysis.
Results written to audit_output.txt
"""

MAZE = [
    "#####################",
    "#o........#........o#",
    "#.###.###.#.###.###.#",
    "#...................#",
    "#.###.#.#####.#.###.#",
    "#.....#...#...#.....#",
    "#####.###.#.###.#####",
    "#####.#.......#.#####",
    "#####.#.## ##.#.#####",
    "#.......#   #.......#",
    "#.###.#.#####.#.###.#",
    "#.###.#.......#.###.#",
    "#o..#...........#..o#",
    "#####################",
]
ROWS = len(MAZE)
COLS = len(MAZE[0])
HOUSE_CELLS  = {(8,10),(9,9),(9,10),(9,11)}
PLAYER_START = (11, 10)

def is_wall(r, c):
    return not (0 <= r < ROWS and 0 <= c < COLS) or MAZE[r][c] == "#"

# Build pellet set (same as reset())
all_pellets = {(r,c) for r,row in enumerate(MAZE) for c,v in enumerate(row) if v in ".o"}

# BFS from PLAYER_START over cells the player can actually enter
from collections import deque
visited = set()
queue = deque([PLAYER_START])
visited.add(PLAYER_START)
while queue:
    r, c = queue.popleft()
    for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
        nr, nc = r+dr, c+dc
        if (nr,nc) in visited:
            continue
        if is_wall(nr, nc):
            continue
        if (nr,nc) in HOUSE_CELLS:
            continue
        visited.add((nr,nc))
        queue.append((nr,nc))

reachable_pellets   = all_pellets & visited
unreachable_pellets = all_pellets - visited

lines = []
lines.append(f"Total pellets in MAZE  : {len(all_pellets)}")
lines.append(f"Reachable pellet cells : {len(reachable_pellets)}")
lines.append(f"UNREACHABLE pellets    : {len(unreachable_pellets)}")
lines.append("")

if unreachable_pellets:
    lines.append("=== UNREACHABLE PELLET CELLS ===")
    for (r,c) in sorted(unreachable_pellets):
        ch = MAZE[r][c]
        # Show context: what are its 4 neighbors?
        neighbors = []
        for dr,dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            nr,nc = r+dr, c+dc
            if 0<=nr<ROWS and 0<=nc<COLS:
                nch = MAZE[nr][nc]
                in_house = (nr,nc) in HOUSE_CELLS
                neighbors.append(f"  ({nr},{nc})={repr(nch)}{'[HOUSE]' if in_house else ''}")
            else:
                neighbors.append(f"  ({nr},{nc})=OOB")
        lines.append(f"  ({r},{c}) = {repr(ch)}   neighbors:")
        lines += neighbors
else:
    lines.append("No unreachable pellets found.")

lines.append("")
lines.append(f"PLAYER_START {PLAYER_START} char = {repr(MAZE[PLAYER_START[0]][PLAYER_START[1]])}")
lines.append(f"PLAYER_START in all_pellets  : {PLAYER_START in all_pellets}")
lines.append(f"PLAYER_START in visited      : {PLAYER_START in visited}")
lines.append(f"PLAYER_START in reachable    : {PLAYER_START in reachable_pellets}")

# Show all pellet positions sorted
lines.append("")
lines.append("=== ALL PELLET POSITIONS ===")
for (r,c) in sorted(all_pellets):
    ch = MAZE[r][c]
    reach = "REACHABLE" if (r,c) in reachable_pellets else "!!! UNREACHABLE !!!"
    lines.append(f"  ({r:2d},{c:2d}) = {repr(ch)}  {reach}")

out = "\n".join(lines)
with open("audit_output.txt", "w") as f:
    f.write(out)
print("Done. See audit_output.txt")
print(f"Unreachable: {len(unreachable_pellets)}")
if unreachable_pellets:
    for p in sorted(unreachable_pellets):
        print(f"  {p} = {repr(MAZE[p[0]][p[1]])}")
