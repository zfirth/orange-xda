"""
<name>Scatterplot Matrix</name>
<description>Scatterplot visualization.</description>
<contact>Stefan Novak (stefan.louis.novak@gmail.com)</contact>
<priority>1000</priority>
"""
import orngEnviron, orngAddOns

from OWWidget import *
from OWScatterPlotGraph import *

from PyQt4.QtCore import *
from PyQt4.QtGui import *

class OWScatterPlotMatrix(OWWidget):
    
    scatterPlotCollection = []
    scatterPlotTargetLayout = None
    dataset = None
    keys = []

    def __init__(self, parent=None, signalManager=None):
        OWWidget.__init__(self, parent, signalManager, 'SampleDataA')
        
        # Define inputs & outputs for widget
        self.inputs = [("Data", ExampleTable, self.setData)]
        self.outputs = [("Sampled Data", ExampleTable)]
        
        # Right now, target the main layout for the scatter plot matrix.
        # This should change as the layout evolves.
        self.scatterPlotTargetLayout = self.mainArea.layout()
        

        # We can force a redraw, but we should wait until there's data?
        #self.redrawLayout()
                
    def redrawLayout(self, dataset = dataset):
        '''
            Remove all scatter plot objects from the layout and redraw
            the corresponding layout.
        '''
        
        self.scatterPlotCollection = []
        
        # Remove all widgets from the target layout
        while self.scatterPlotTargetLayout.count() > 0:
            item = self.scatterPlotTargetLayout.takeAt(0)
            if not item:
                continue
            w = item.widget()
            if w:
                w.deleteLater()
                
        # Create the scatter plot matrix widget and 
        scatterPlotMatrix = QWidget()
        scatterPlotMatrixLayout = QGridLayout()
        
        # Step through the first few attributes and create
        # a scatter plot for them. The dataset we're using has
        # 80 attributes or so - which is way to much to plot in
        # a scatter plot matrix. We need to fix this at some point.
        for row,rowTitle in enumerate(self.keys[0:3]):
            for col,colTitle in enumerate(self.keys[0:row]):
                
                # Create the scatter plot graph object.
                scatterPlot = OWScatterPlotGraph(None)
                scatterPlot.setData(self.dataset)
                scatterPlot.updateData(colTitle,rowTitle,"")
                
                # Attach the scatter plot graph to our collection
                # and add it to the layout.
                self.scatterPlotCollection.append(scatterPlot)
                scatterPlotMatrixLayout.addWidget(scatterPlot, row, col)
        
        # Take the layout and assign it to our widget
        scatterPlotMatrix.setLayout(scatterPlotMatrixLayout)
        
        # Attach the widget to the target layout
        self.scatterPlotTargetLayout.addWidget(scatterPlotMatrix)
        
    def setData(self, dataset):
        if dataset:
            self.dataset = dataset
            self.keys = [attr.name for attr in self.dataset.domain.variables]
            self.redrawLayout()

if __name__=="__main__":
    '''
        Test our widget.
    '''
    a=QApplication(sys.argv)
    ow=OWScatterPlotMatrix()
    ow.show()
    
    # Load in demo data
    data = orange.ExampleTable(r"../../doc/datasets/brown-selected.tab")

    ow.setData(data)
    a.exec_()
