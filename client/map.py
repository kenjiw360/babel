from itertools import chain
from typing import cast

from vpython import (
	color,
	compound,
	extrusion,
	norm,
	paths,
	pi,
	shapes,
	standardAttributes,
	vector,
)


def mid_point(p1: list[float], p2: list[float]):
	return vector(0.5*(p1[1]+p2[1]), 0, 0.5*(p1[0]+p2[0]))

def path_to_points(path: list[vector]) -> list[list[float]]:
	return [[0.5 * v.x, -0.5 * v.z] for v in path]

FLOOR_COLOR = vector(0.42, 0.09, 0.09)
WALL_COLOR = color.white

HEX_SHAPE = cast(list[list[float]], shapes.hexagon(length=6))
WALL_SHAPE = shapes.rectangle(width=6, height=3)
ARCH_SHAPE = path_to_points(paths.arc(radius=1, angle1=0, angle2=pi)) + [[-0.5, -1.49], [0.5, -1.49], [0.5, 0]]

CONTINUOUS_TOP = True
BOTTOM = -1.5
HEIGHT = 3
PADDING = 0.2
MARGIN = 0.1
DIVISIONS = 4
HRULES = [[-2.52, -0.7], [0.7, 2.52]]
DY = (HEIGHT - 2 * PADDING - (DIVISIONS - 1) * MARGIN) / DIVISIONS

BOOK_SHELVES_SHAPES = list(chain.from_iterable([[
	[x0, BOTTOM + PADDING + i * (DY + MARGIN)],
	[x1, BOTTOM + PADDING + i * (DY + MARGIN)],
	[x1, BOTTOM + PADDING + i * (DY + MARGIN) + DY],
	[x0, BOTTOM + PADDING + i * (DY + MARGIN) + DY],
	[x0, BOTTOM + PADDING + i * (DY + MARGIN)]
] for x0, x1 in HRULES] for i in range(DIVISIONS)))

if CONTINUOUS_TOP:
	BOOK_SHELVES_SHAPES = BOOK_SHELVES_SHAPES[:-len(HRULES)] + [[
		[HRULES[0][0] , BOTTOM + PADDING + (DIVISIONS - 1) * (DY + MARGIN)],
		[HRULES[-1][1], BOTTOM + PADDING + (DIVISIONS - 1) * (DY + MARGIN)],
		[HRULES[-1][1], BOTTOM + PADDING + (DIVISIONS - 1) * (DY + MARGIN) + DY],
		[HRULES[0][0] , BOTTOM + PADDING + (DIVISIONS - 1) * (DY + MARGIN) + DY],
		[HRULES[0][0] , BOTTOM + PADDING + (DIVISIONS - 1) * (DY + MARGIN)]
	]]

colors = [color.red, color.blue, color.green, color.yellow, color.magenta, color.orange, color.cyan]
inward_wall = [-1, 3, 4, 5, 0, 1, 2]

hex_walls = [[HEX_SHAPE[i], HEX_SHAPE[i+1]] for i in range(6)]
mid_points = [mid_point(p1, p2) for p1, p2 in hex_walls]
origins = [vector(0, 0, 0)] + [vector(p.x * 2, 0, p.z * 2) for p in mid_points]

class BookModel:
	spine: str = ""
	def __init__(self, origin: vector, width: float, n: int):
		pass

class BookShelfModel:
	books: list[BookModel]
	origin: vector
	def __init__(self, shape: list[list[float]]):
		pass

class WallModel:
	book_shelves: list[BookShelfModel]
	wall: extrusion
	shelves: extrusion
	def __init__(self, n: int, m: int):		
		unit_norm = norm(mid_points[m])
		from_point = origins[n] + mid_points[m] + vector(0, 1.5, 0)
		wall_point = from_point - unit_norm * 0.1
		shelves_point = from_point - unit_norm * 0.5
		self.wall = extrusion(path=[from_point, wall_point], shape=[WALL_SHAPE, ARCH_SHAPE], color=WALL_COLOR)
		self.shelves = extrusion(path=[wall_point, shelves_point], shape=[WALL_SHAPE, ARCH_SHAPE, *BOOK_SHELVES_SHAPES], color=vector(0.33, 0.2, 0.2))

class CellModel:
	walls: list[WallModel]
	floor: extrusion
	
	def __init__(self, n: int):
		self.floor = extrusion(path=[origins[n], origins[n]+vector(0, -0.1, 0)], shape=[HEX_SHAPE], color=FLOOR_COLOR)
		self.walls = [WallModel(n, m) for m in range(6)]

class LevelModel:
	model: compound
	cells: list[CellModel] 
	def __init__(self):
		self.cells = [CellModel(i) for i in range(7)]
		self.model = compound(list(chain.from_iterable([cell.floor] + list(chain.from_iterable([wall.shelves, wall.wall] for wall in cell.walls)) for cell in self.cells)))