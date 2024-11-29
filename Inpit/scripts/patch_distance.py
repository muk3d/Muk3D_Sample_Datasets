# Muk3D script

from core.util.command import MCommand, commandRegistry, ParameterField, ResultField
import sys
from core.util.geom import get_solution, get_rtree, get_distance, create_bounding_box
from core.model.geometry import MPolyLine
from core.util.maths.offset3 import tupleToVec, intersectLines
from core.commands.curve.line_distance import ShowClosePoints 





def execute(self, params):
    
    
    box_size = params['max_search_distance'] * 2
    l1 = self.Helper.select_line('Select first line', param_field='line1', params=params)

    if l1 is None:
        return

    l2 = self.Helper.select_line('Select second line', param_field='line2', params=params)
    if l2 is None:
        return

    if l2['node'] == l1['node'] and l2['cellId'] == l1['cellId']:
        # same object
        self.Helper.writeError('Same line was selected twice.')
        return None


    lines1 = [('l1', l1['points']), ]

    points2 = l2['points']
    idx = get_rtree(lines1)

    solutions = get_solution(idx, points2, box_size)

    lines2 = [('l2', l2['points']), ]
    idx2 = get_rtree(lines2)

    min_dist = None

    distances = MPolyLine()
    min_location = MPolyLine()
    threshold_distance = params['max_search_distance']

    segments = []

    for k, v in solutions.items():
        if v is None:
            continue

        if v[3] < threshold_distance:
            p0 = v[4]
            p1 = v[2]
            p1z = v[1][1][2]
            distances.addFromPoints([p0, (p1[0], p1[1], p1z)])

            segments.append([p0, (p1[0], p1[1], p1z)])

        if min_dist is None:
            min_dist = v
            continue

        if v[3] < min_dist[3]:
            min_dist = v

    if min_dist is None:
        # couldn't find a close point within that distace.
        self.Helper.writeError('The minimum search distance was smaller than the minimum distance between the two selected lines.  Try again with a larger search distance.')
        self.add_result_field('min_distance', -1)
        self.add_result_field('location_of_minimum', [(0,0,0), (0,0,0)])
        return

    self.Helper.uWriteLength('Minimum distance', min_dist[3])

    p0 = min_dist[4]
    p1 = min_dist[2]
    p1z = min_dist[1][1][2]
    distances.addFromPoints([p0, (p1[0], p1[1], p1z)])

    min_location.addFromPoints([p0, (p1[0], p1[1], p1z)])
    min_d = self.Helper.addGeometryToScene2('location_of_min', min_location, style='red', overwrite=True)
    min_d.setLineWidth(10)

    self.add_result_field('location_of_minimum', [p0, (p1[0], p1[1], p1z)])
    self.add_result_field('min_distance', min_dist[3])

    # non_intersecting = MPolyLine()
    # for s in segments:
        # # print p
        # pbox = create_bounding_box(s[0], s[1])
        # hits = idx2.intersection(pbox, objects='raw')
        # p0 = s[0]
        # p1 = s[1]
        # add = True
        # for h in hits:
            # p2 = h[1][0]
            # p3 = h[1][1]
            # r, d1, d2 = intersectLines(tupleToVec(p0), tupleToVec(p1), tupleToVec(p2), tupleToVec(p3))
            # self.Helper.writeOutput( d1, d2)
            # d1 = round(d1, 6)
            # d2 = round(d2, 6)
            # if 0.0 < d1 < 1.0 and 0.0 < d2 < 1.0:
                # # self.Helper.writeOutput(p0, p1, '--', p2, p3)
                # # self.Helper.writeOutput('=====', d1, d2)
                # add = False
                # break
        # if add:
            # non_intersecting.addFromPoints(s)
    # self.Helper.addGeometryToScene2('segments_below_threshold', non_intersecting, overwrite=True)


ShowClosePoints.execute = execute