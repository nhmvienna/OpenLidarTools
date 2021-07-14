# -*- coding: utf-8 -*-

"""
/***************************************************************************
 OpenLidarTools
                                 A QGIS QGISplugin
 Open LiDAR Toolbox
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2021-03-10
        copyright            : (C) 2021 by Benjamin Štular, Edisa Lozić, Stefan Eichert
        email                : stefaneichert@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 3 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

__author__ = 'Benjamin Štular, Edisa Lozić, Stefan Eichert'
__date__ = '2021-03-10'
__copyright__ = '(C) 2021 by Benjamin Štular, Edisa Lozić, Stefan Eichert'

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = '$Format:%H$'

"""
Model exported as python.
Name : Lidar Pipeline
Group : OpenLidarToolbox
With QGIS : 31604
"""

import inspect
import os

from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import QgsProcessingUtils
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterFile
from qgis.core import QgsProcessingParameterFileDestination
import processing



class ToClassLas(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):

        self.addParameter(
            QgsProcessingParameterFile('InputFilelaslaz', 'Input LAS/LAZ File', behavior=QgsProcessingParameterFile.File,
                                       fileFilter='Lidar Files (*.las *.laz)', defaultValue=None))
        self.addParameter(
            QgsProcessingParameterFileDestination('LAS', 'Output classified LAS/LAZ', fileFilter='Lidar Files (*.laz *.las)',
                                                  defaultValue=None, optional=False, createByDefault=False))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(6, model_feedback)
        results = {}
        outputs = {}

        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}


        # lasground1
        alg_params = {
            'ADDITIONAL_OPTIONS': '',
            'BY_FLIGHTLINE': False,
            'CPU64': False,
            'GRANULARITY': 4,
            'GUI': False,
            'HORIZONTAL_FEET': False,
            'IGNORE_CLASS1': 8,
            'INPUT_LASLAZ': parameters['InputFilelaslaz'],
            'NO_BULGE': False,
            'OUTPUT_LASLAZ': QgsProcessingUtils.generateTempFilename('lasground1.laz'),
            'TERRAIN': 4,
            'VERBOSE': True,
            'VERTICAL_FEET': False
        }
        outputs['Lasground1'] = processing.run('LAStools:lasground', alg_params, context=context, feedback=feedback,
                                               is_child_algorithm=True)
        lasground1file = alg_params['OUTPUT_LASLAZ']

        feedback.setCurrentStep(2)
        if feedback.isCanceled():
            return {}

        # lasheight
        alg_params = {
            'ADDITIONAL_OPTIONS': '-ignore_class 0 1 3 4 5 6 7 8 9 10 11 12',
            'CPU64': False,
            'DROP_ABOVE': False,
            'DROP_ABOVE_HEIGHT': 100,
            'DROP_BELOW': False,
            'DROP_BELOW_HEIGHT': -2,
            'GUI': False,
            'IGNORE_CLASS1': 0,
            'IGNORE_CLASS2': 0,
            'INPUT_LASLAZ': lasground1file,
            'OUTPUT_LASLAZ': QgsProcessingUtils.generateTempFilename('lasheight.laz'),
            'REPLACE_Z': False,
            'VERBOSE': True
        }

        lasheightfile = alg_params['OUTPUT_LASLAZ']
        outputs['Lasheight'] = processing.run('LAStools:lasheight', alg_params, context=context, feedback=feedback,
                                              is_child_algorithm=True)

        feedback.setCurrentStep(3)
        if feedback.isCanceled():
            return {}

        # lasclassify
        alg_params = {
            'ADDITIONAL_OPTIONS': '-small_trees',
            'CPU64': False,
            'GUI': False,
            'HORIZONTAL_FEET': False,
            'IGNORE_CLASS1': 0,
            'IGNORE_CLASS2': 0,
            'INPUT_LASLAZ': lasheightfile,
            'OUTPUT_LASLAZ': QgsProcessingUtils.generateTempFilename('lasclassify.laz'),
            'VERBOSE': True,
            'VERTICAL_FEET': False
        }
        lasclassifyfile = alg_params['OUTPUT_LASLAZ']
        outputs['Lasclassify'] = processing.run('LAStools:lasclassify', alg_params, context=context, feedback=feedback,
                                                is_child_algorithm=True)

        feedback.setCurrentStep(4)
        if feedback.isCanceled():
            return {}

        # lasground2
        alg_params = {
            'ADDITIONAL_OPTIONS': '-ignore_class 6 7',
            'BY_FLIGHTLINE': False,
            'CPU64': False,
            'GRANULARITY': 4,
            'GUI': False,
            'HORIZONTAL_FEET': False,
            'IGNORE_CLASS1': 0,
            'INPUT_LASLAZ': lasclassifyfile,
            'NO_BULGE': False,
            'OUTPUT_LASLAZ': QgsProcessingUtils.generateTempFilename('lasground2.laz'),
            'TERRAIN': 1,
            'VERBOSE': True,
            'VERTICAL_FEET': False
        }
        lasground2file = alg_params['OUTPUT_LASLAZ']
        outputs['Lasground2'] = processing.run('LAStools:lasground', alg_params, context=context, feedback=feedback,
                                               is_child_algorithm=True)

        feedback.setCurrentStep(5)
        if feedback.isCanceled():
            return {}

        # lasheight_classify
        alg_params = {
            'ADDITIONAL_OPTIONS': '',
            'CLASSIFY_ABOVE': 6,
            'CLASSIFY_ABOVE_HEIGHT': 2,
            'CLASSIFY_BELOW': 8,
            'CLASSIFY_BELOW_HEIGHT': -0.25,
            'CLASSIFY_BETWEEN1': 3,
            'CLASSIFY_BETWEEN1_HEIGHT_FROM': -0.2,
            'CLASSIFY_BETWEEN1_HEIGHT_TO': 0.2,
            'CLASSIFY_BETWEEN2': 4,
            'CLASSIFY_BETWEEN2_HEIGHT_FROM': 0.5,
            'CLASSIFY_BETWEEN2_HEIGHT_TO': 2,
            'CPU64': False,
            'GUI': False,
            'IGNORE_CLASS1': 7,
            'IGNORE_CLASS2': 8,
            'INPUT_LASLAZ': lasground2file,
            'OUTPUT_LASLAZ': parameters['LAS'],
            'REPLACE_Z': False,
            'VERBOSE': True
        }
        lasheightclassifyfile = alg_params['OUTPUT_LASLAZ']
        outputs['Lasheight_classify'] = processing.run('LAStools:lasheight_classify', alg_params, context=context,
                                                       feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(6)
        if feedback.isCanceled():
            return {}
        results['classifiedLAZ'] = lasheightclassifyfile
        return results

    def name(self):
        return 'ToClassLas'

    def displayName(self):
        return 'Classify LAS/LAZ'

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr(self.groupId())

    def icon(self):
        cmd_folder = os.path.split(inspect.getfile(inspect.currentframe()))[0]
        icon = QIcon(os.path.join(os.path.join(cmd_folder, 'icons/2_1_Classify_LASLAZ.png')))
        return icon

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return ''

    def shortHelpString(self):
        return """<html><body><h2>Algorithm description</h2>
    <p>The algorithm will classify an airborne LiDAR point cloud. This process – also known as &quot;filtering&quot; or semantic labeling of the point cloud – is optimized for archaeology, but is also useful for other purposes.</p>
    <h2>Input parameters</h2>
    <h3>Input LAS/LAZ File</h3>
    <p>Unclassified point cloud in LAS or LAZ format. Noise classified as ASPRS class 7 will be exempt from the processing, all other preexisting classification will be ignored.
    <b>Point clouds with more than 30 million points will fail or will take very long to process.</b></p>
    <h2>Outputs</h2>
    <p><h3>Classified LAZ/LAS</h3>
    Classified point cloud. QGIS cannot load point clouds so it must be saved as a LAZ/LAS file. Please Specify folder and file name.</p>
    <br>Output is a LAZ/LAS point cloud classified into ground (2), low vegetation (3; 0.5-2 m), high vegetation (5; 2-100m), and buildings (6); there are also likely some points remaining that have not been classified (0).
    <h2>FAQ</h2>
    <h3>The quality of classification does not meet my expectations, how can I improve it?</h3>
    <p>This tool is a one-size-fits-all and is designed for the simplicity. As any other such tool without any user defined parameters it is designed to produce OK results for any dataset, but will by definition never be the best possible. Feel free to experiment with other dedicated software, e.g., LAStools or Whitebox tools.</p>
    <br>
    <p><b>Literature:</b> Štular, Lozić, Eichert 2021 (in press).</p>
    <br><a href="https://github.com/stefaneichert/OpenLidarTools">Website</a>
    <br><p align="right">Algorithm author: Benjamin Štular, Edisa Lozić, Stefan Eichert </p><p align="right">Help author: Benjamin Štular, Edisa Lozić, Stefan Eichert</p></body></html>"""

    def tr(self, string):
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return ToClassLas()