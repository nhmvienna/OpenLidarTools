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
from qgis.core import QgsProcessing
from qgis.core import QgsProcessingUtils
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterBoolean
from qgis.core import QgsProcessingParameterRasterLayer
from qgis.core import QgsProcessingParameterString
import processing



class visualise(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterRasterLayer('DFMDEM', 'DFM/DEM', defaultValue=None))
        self.addParameter(QgsProcessingParameterString('prefix', 'Name prefix for layers', multiLine=False, defaultValue='', optional=True))
        self.addParameter(QgsProcessingParameterBoolean('VisualisationVAT', 'Visualisation VAT', optional=False, defaultValue=True))
        self.addParameter(QgsProcessingParameterBoolean('VisualisationSVF', 'Visualisation SVF', optional=False, defaultValue=True))
        self.addParameter(QgsProcessingParameterBoolean('VisualisationOPN', 'Visualisation Openness', optional=False, defaultValue=True))
        self.addParameter(QgsProcessingParameterBoolean('VisualisationDfME', 'Visualisation DME', optional=False, defaultValue=True))
        self.addParameter(QgsProcessingParameterBoolean('VisualisationHS', 'Visualisation Hillshade', optional=False, defaultValue=True))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(7, model_feedback)
        results = {}
        outputs = {}

        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}
        DFMPatched = parameters['DFMDEM']



        if parameters['VisualisationSVF']:
            # RVT Sky-view factor
            alg_params = {
                'FILL_NO_DATA': False,
                'FILL_METHOD': 0,
                'INPUT': DFMPatched,
                'KEEP_ORIG_NO_DATA': False,
                'NOISE_REMOVE': 0,
                'NUM_DIRECTIONS': 16,
                'RADIUS': 10,
                'SAVE_AS_8BIT': False,
                'VE_FACTOR': 1,
                'OUTPUT': QgsProcessingUtils.generateTempFilename('SKF.tif')
            }
            outputs['RvtSkyviewFactor'] = processing.run('rvt:rvt_svf', alg_params, context=context, feedback=feedback,
                                                         is_child_algorithm=True)

            # Load layer into project
            alg_params = {
                'INPUT': outputs['RvtSkyviewFactor']['OUTPUT'],
                'NAME': parameters['prefix'] + 'Visualisation SVF'
            }
            outputs['LoadLayerIntoProject'] = processing.run('native:loadlayer', alg_params, context=context,
                                                             feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(2)
        if feedback.isCanceled():
            return {}

        if parameters['VisualisationVAT']:
            # RVT Blender
            alg_params = {
                'BLEND_COMBINATION': 0,
                'FILL_NO_DATA': False,
                'FILL_METHOD': 0,
                'INPUT': DFMPatched,
                'KEEP_ORIG_NO_DATA': False,
                'OUTPUT': QgsProcessingUtils.generateTempFilename('vat.tif'),
                'TERRAIN_TYPE': 0
            }
            outputs['RvtBlender'] = processing.run('rvt:rvt_blender', alg_params, context=context, feedback=feedback,
                                                   is_child_algorithm=True)

            feedback.setCurrentStep(3)
            if feedback.isCanceled():
                return {}

            # Load layer into project
            alg_params = {
                'INPUT': outputs['RvtBlender']['OUTPUT'],
                'NAME': parameters['prefix'] + 'Visualisation VAT'
            }
            outputs['LoadLayerIntoProject'] = processing.run('native:loadlayer', alg_params, context=context,
                                                             feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(4)
        if feedback.isCanceled():
            return {}

        if parameters['VisualisationOPN']:
            # RVT Openness
            alg_params = {
                'FILL_NO_DATA': False,
                'FILL_METHOD': 0,
                'INPUT': DFMPatched,
                'KEEP_ORIG_NO_DATA': False,
                'NOISE_REMOVE': 0,
                'NUM_DIRECTIONS': 16,
                'OPNS_TYPE': 0,
                'RADIUS': 10,
                'SAVE_AS_8BIT': False,
                'VE_FACTOR': 1,
                'OUTPUT': QgsProcessingUtils.generateTempFilename('OPN.tif')
            }
            outputs['RvtOpenness'] = processing.run('rvt:rvt_opns', alg_params, context=context, feedback=feedback,
                                                    is_child_algorithm=True)



            # Load layer into project
            alg_params = {
                'INPUT': outputs['RvtOpenness']['OUTPUT'],
                'NAME': parameters['prefix'] + 'Visualisation Openness'
            }
            outputs['LoadLayerIntoProject'] = processing.run('native:loadlayer', alg_params, context=context,
                                                             feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(5)
        if feedback.isCanceled():
            return {}

        if parameters['VisualisationDfME']:
            # DiffFromMeanElev
            alg_params = {
                'filterx': 10,
                'filtery': 10,
                'input': DFMPatched,
                'output': QgsProcessingUtils.generateTempFilename('DME.tif')
            }
            outputs['Difffrommeanelev'] = processing.run('wbt:DiffFromMeanElev', alg_params, context=context,
                                                         feedback=feedback, is_child_algorithm=True)

            # Set style for raster layer
            folder = os.path.split(inspect.getfile(inspect.currentframe()))[0]
            styleFile = os.path.join(os.path.join(folder, 'DfME.qml'))

            alg_params = {
                'INPUT': outputs['Difffrommeanelev']['output'],
                'STYLE': styleFile
            }
            outputs['SetStyleForRasterLayer'] = processing.run('qgis:setstyleforrasterlayer', alg_params,
                                                               context=context,
                                                               feedback=feedback, is_child_algorithm=True)

            # Load layer into project
            alg_params = {
                'INPUT': outputs['Difffrommeanelev']['output'],
                'NAME': parameters['prefix'] + 'Visualisation DME'
            }
            outputs['LoadLayerIntoProject'] = processing.run('native:loadlayer', alg_params, context=context,
                                                             feedback=feedback, is_child_algorithm=True)
        feedback.setCurrentStep(6)
        if feedback.isCanceled():
            return {}

        if parameters['VisualisationHS']:
            # Hillshade
            alg_params = {
                'AZIMUTH': 300,
                'INPUT': DFMPatched,
                'V_ANGLE': 40,
                'Z_FACTOR': 1,
                'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
            }
            outputs['Hillshade'] = processing.run('native:hillshade', alg_params, context=context, feedback=feedback,
                                                  is_child_algorithm=True)


            # Load layer into project
            alg_params = {
                'INPUT': outputs['Hillshade']['OUTPUT'],
                'NAME': parameters['prefix'] + 'Visualisation Hillshade'
            }
            outputs['LoadLayerIntoProject'] = processing.run('native:loadlayer', alg_params, context=context,
                                                             feedback=feedback, is_child_algorithm=True)
        feedback.setCurrentStep(7)
        if feedback.isCanceled():
            return {}

        return results

    def name(self):
        return 'Visualise'

    def displayName(self):
        return 'Visualisations (from DFM)'

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr(self.groupId())

    def icon(self):
        cmd_folder = os.path.split(inspect.getfile(inspect.currentframe()))[0]
        icon = QIcon(os.path.join(os.path.join(cmd_folder, '3_3_Visualisations.png')))
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
    <p>This algorithm takes a digital feature model (DFM, which is archaeology-specific DEM) or any DEM to produce the most commonly used archaeological visualisations.</p>
    <h2>Input parameters</h2>
    <h3>DFM/DEM</h3>
    <p>DFM or DEM in any raster format supported by QGIS, e.g., GeoTIFF.</p>
    <h3>Name prefix for layers</h3>
    <p>The output layers are added to the map as temporary layers with default names. They can be saved as files afterwards. In order to distinguish them from previously created files with the same tool a prefix should be defined to avoid the same names for different layers</p>
    <h3>Outputs:</h3>
    <p><b>VAT: </b> Visualisation for archaeological topography</p>
    <p><b>SVF: </b> Sky view factor</p>
    <p><b>Opennes: </b> Openness – positive</p>
    <p><b>DME: </b> Difference from mean elevation</p>
    <p><b>Hillshade: </b> Analytical hillshade</p>
    <h2>FAQ</h2>
    <h3>The edges of my outputs are black</h3>
    <p>This is due to the so called edge effect. In many steps the values are calculated from surrounding points; since at the edge there are no surrounding points, the output values are "strange", e.g., showing as black on most visualisations. This cannot be avoided and the only solution is to process larger areas or to create overlapping mosaics.</p>
    <p></p>
    <br><br>
    <p><b>Literature:</b> Štular, Lozić, Eichert 2021 (in press).</p>
    <br><a href="https://github.com/stefaneichert/OpenLidarTools">Website</a>
    <br><p align="right">Algorithm author: Benjamin Štular, Edisa Lozić, Stefan Eichert </p><p align="right">Help author: Benjamin Štular, Edisa Lozić, Stefan Eichert</p></body></html>"""

    def tr(self, string):
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return visualise()
