from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.files.base_reader import BaseReader

__all__ = [
    'OFF',
    'OFFReader',
]


class OFF(object):
    """Read and write files in *OFF* format.

    Notes
    -----
    GeomView Object File Format

    References
    ----------
    * http://shape.cs.princeton.edu/benchmark/documentation/off_format.html
    * http://www.geomview.org/docs/html/OFF.html
    * http://segeval.cs.princeton.edu/public/off_format.html

    """

    def __init__(self, address):
        self.reader = OFFReader(address)


class OFFReader(BaseReader):
    """Read the contents of an *off* file.
    Arguments
    ---------
    location: str or Path object
        Path or URL to the file.

    Attributes
    ----------
    vertices : list
        Vertex coordinates.
    faces : list
        Face objects, referencing the list of vertices.
    number_of_vertices : int
        Vertex count stated in beginning of file
    number_of_faces : int
        Face count stated in beginning of file
    number_of_faces : int
        Edge count stated in beginning of file

    """
    FILE_SIGNATURE = {'content': b'OFF', 'offset': 0}

    def __init__(self, address):
        super(OFFReader, self).__init__(address)
        self.vertices = []
        self.faces = []
        self.number_of_vertices = None
        self.number_of_faces = None
        self.number_of_edges = None
        self.read_off()

    @property
    def is_valid(self):
        return self.is_file_signature_correct() and not self.is_binary

    def read_off(self):
        """Read the contents of the file, line by line.

        OFF
        # comments

        v f e
        x y z
        ...
        x y z
        degree list of vertices

        """
        if not self.is_valid:
            raise Exception('Failed to parse file as an OFF-file')

        first_iter_line_passed = False
        line_buffer = []
        complete_lines = []

        for line in self.iter_lines():

            # ignore file signature and empty lines
            if line == self.FILE_SIGNATURE['content'].decode('utf-8') or len(line.strip()) == 0:
                continue

            line_buffer.append(line.rstrip())

            # need two lines to check for multi line property
            if len(line_buffer) < 2:
                first_iter_line_passed = True
                # Second time this happens is at EOF
                if not first_iter_line_passed:
                    continue

            if line_buffer[-1].startswith(r'\\'):
                continuation_of_line = line_buffer.pop()

                # Concatenate continuation to previous line
                line_buffer[-1] += ' {}'.format(continuation_of_line.strip().replace('\\\\', '', 1))

                continue

            # after passing checks above line_buffer holds the complete line
            complete_lines.append(line_buffer.pop(0))

        for line in complete_lines:

            # Ignore comments in file
            if line.startswith('#'):
                continue

            parts = line.split()

            if len(parts) == 3:
                if self.number_of_vertices is None and self.number_of_faces is None and self.number_of_vertices is None:
                    self.number_of_vertices, self.number_of_faces, self.number_of_edges = int(parts[0]), int(parts[1]), int(parts[2])
                else:
                    self.vertices.append([float(axis) for axis in parts])
            elif len(parts) > 3:
                f = int(parts[0])
                if f == len(parts[1:]):
                    self.faces.append([int(index) for index in parts[1:]])


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    import compas

    off = OFF(compas.get('cube.off'))

    print(off.reader.vertices)
    print(off.reader.faces)
