from .IllustrationBase import *

__all__ = ['StampsIllustration']


class StampsIllustration(IllustrationBase):
    illustrationtype = 'Stamps'

    def __init__(self, cubes=[], names=[], aspectratio=np.inf,
                        hspace=0.08, wspace=0.08,
                        left=0.05, right=0.95,
                        bottom=0.15, top=0.82,
                        **kwargs):

        each = 3.2
        N = len(cubes)
        cols = np.minimum(np.ceil(np.sqrt(N) * aspectratio), N).astype(np.int)
        rows = np.maximum(np.ceil(N / cols), 1).astype(np.int)
        wsize = each * cols * (1 + (cols - 1) * wspace) / (right - left)
        hsize = each * rows * (1 + (rows - 1) * hspace) / (top - bottom)
        print(wsize, hsize)
        IllustrationBase.__init__(self, rows, cols,
                                  figkw=dict(figsize=(wsize, hsize)),
                                  hspace=hspace, wspace=wspace,
                                  left=left, right=right,
                                  bottom=bottom, top=top, **kwargs)

        for i in range(rows):
            for j in range(cols):

                if len(cubes) == 0:
                    break

                ax = plt.subplot(self.grid[i, j])
                c = cubes.pop(0)
                try:
                    n = names[i * cols + j]
                except IndexError:
                    n = (i, j)

                self.frames[n] = imshowFrame(illustration=self, ax=ax, data=c)
