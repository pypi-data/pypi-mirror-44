smallanglescattering (sas)
==========================

.. automodule:: jscatter.smallanglescattering
    :noindex:

Smear/desmear 1D
----------------
.. autosummary::
    smear
    desmear
    prepareBeamProfile
    resFunct
    getBeamWidth
    plotBeamProfile
    transmissionCorrection
    waterXrayScattering
    AgBeReference

2D sasImage
-----------
.. automodule:: jscatter.sasimagelib
.. autosummary::
    sasImage

sasImage methods
""""""""""""""""
  .. autosummary::
    ~SubArray.attr
    ~SubArray.showattr
    ~sasImage.setAttrFromImage
    ~sasImage.setDetectorDistance
    ~sasImage.setBeamcenter
    ~sasImage.maskReset
    ~sasImage.maskRegion
    ~sasImage.maskFromImage
    ~sasImage.maskRegion
    ~sasImage.maskRegions
    ~sasImage.maskbelowLine
    ~sasImage.maskTriangle
    ~sasImage.mask4Polygon
    ~sasImage.maskCircle
    ~sasImage.maskSectors
    ~sasImage.asImage
    ~sasImage.saveAsTIF
    ~sasImage.pickBeamcenter
    ~sasImage.findCenterOfIntensity
    ~sasImage.radialAverage
    ~sasImage.lineAverage
    ~sasImage.recalibrateDetDistance
    ~sasImage.gaussianFilter
    ~sasImage.showPolar
    ~sasImage.reduceSize
    ~sasImage.show
    ~sasImage.getfromcomment
    ~sasImage.array
    ~sasImage.asdataArray
    ~sasImage.interpolateMaskedRadial

2D sasImage convenience
-----------------------
.. currentmodule:: jscatter.sasimagelib
.. autosummary::
    createLogPNG
    createImageDescriptions
    readImages


Housekeeping
------------
.. currentmodule:: jscatter.smallanglescattering
.. autosummary::
    readpdh
    autoscaleYinoverlapX
    removeSpikesMinmaxMethod
    removeSpikes
    locateFiles
    copyFiles
    addXMLParameter
    moveSAXSPACE


---------

.. automodule:: jscatter.smallanglescattering
    :members:
    :undoc-members:
    :show-inheritance:

.. automodule:: jscatter.sasimagelib
    :members:
    :undoc-members:
    :show-inheritance:

.. autoclass:: jscatter.sasimagelib.sasImage
    :members:
    :undoc-members:

 .. autoclass:: jscatter.sasimagelib.SubArray
    :members:
    :undoc-members:

   