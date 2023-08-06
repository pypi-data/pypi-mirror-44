import os
class TestImages(object):
    """
    Provide the locations of imaging test datasets, 
        or optionally provide the pythologist projects 
        or cell data frame objects

    * raw - contains a dictionary of dataset locations
    * projects - contains a dictionary of pythologist-reader projects
    * celldataframes - contains a dictionary of celldataframes 
    """
    def __init__(self):
        self.base = os.path.abspath(os.path.join(__file__,'../../data'))
        self._paths = {
            'IrisSpatialFeatures':os.path.join(self.base,'IrisSpatialFeatures','Example'),
            'Small':os.path.join(self.base,'Small','Example'),
            'Tiny':os.path.join(self.base,'Tiny','Example'),
        }
    @property
    def datasets(self): return list(self._paths.keys())

    def raw(self,dataset):
        return self._paths[dataset]

    def project(self,dataset):
        from pythologistreader.formats.inform.custom import CellProjectInFormLineArea
        from pythologistreader.formats.inform.sets import CellProjectInForm
        if dataset == 'IrisSpatialFeatures':
            return CellProjectInFormLineArea(os.path.join(self.base,'IrisSpatialFeatures','pythologist.h5'))
        return CellProjectInForm(os.path.join(self.base,dataset,'pythologist.h5'))

    def celldataframe(self,dataset):
        from pythologist import CellDataFrame
        cdf = CellDataFrame.read_hdf(os.path.join(self.base,dataset,'pythologist.cdf.h5'),'data')
        return cdf