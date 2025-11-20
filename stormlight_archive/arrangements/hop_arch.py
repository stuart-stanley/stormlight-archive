# todo: ABC of api
from strands import ArchStrand


class HopArch(object):
    def __init__(self, display, strand_count):
        self.__display = display
        self.__strand_count = strand_count

        x = 0
        y = 0
        z = 0
        strands = []
        p = 38
        for s in range(0, strand_count):
            strand = ArchStrand(self.__display, p, 26, 36, (x, y, z))
            strands.append(strand)
            p = 38
            z = z - 60

        self.__display.set_limits(100, 1, strand_count)
