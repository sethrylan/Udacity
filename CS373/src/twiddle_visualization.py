#!/usr/bin/python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Visualising the Greedy Goat for udacity CS373 unit5-16
#
# unit0516_param_optim_svg.py
# http://pastebin.com/3T7Hu6NP
#
# Custom modules:
#   vegesvgplot.py        http://pastebin.com/6Aek3Exm
#
#-------------------------------------------------------------------------------


'''Visualisation of PID optimisation in Unit 5-16

Description:
  This Python program runs the a PID parameter optimiser for the robot
  car presented in unit 5-16 (the car with badly misaligned steering).
  The output is written to a Scalable Vector Graphic file named
  “output.svg”.

Author(s):
  Daniel Neville
  Prof. Sebastian Thrun, udacity (original robot simulation)

Copyright, Licence:
  Code by Daniel Neville: Public domain
  Code snarfed from udacity: See http://www.udacity.com/legal/

Platform:
  Python 2.5


INDEX


Imports

Fun stuff:

  Snarfed and modified robot code
  RenderToSVG(Data)
  TwiddleAndPlot(InitialCTE, Tolerance, YScale, ErrFnIx, Data)

Main:

  Main()

'''


#-------------------------------------------------------------------------------


import math

from math import (
  pi, sqrt, hypot, sin, cos, tan, asin, acos, atan, atan2, radians, degrees,
  floor, ceil
)

import random

# The SVG Plotting for Vegetables module can be found at
# http://pastebin.com/6Aek3Exm

from vegesvgplot import (

  # Shape constants
  Pt_Break, Pt_Anchor, Pt_Control,
  PtCmdWithCoordsSet, PtCmdSet,

  # Indent tracker class
  tIndentTracker,

  # Affine matrix class
  tAffineMtx,

  # Affine matrix creation functions
  AffineMtxTS, AffineMtxTRS2D, Affine2DMatrices,

  # Utility functions
  ValidatedRange, MergedDictionary, Save,
  ArrayDimensions, NewMDArray, CopyArray, At, SetAt,

  # Basic vector functions
  VZeros, VOnes, VStdBasis, VDim, VAug, VMajorAxis,
  VNeg, VSum, VDiff, VSchur, VDot,
  VLengthSquared, VLength, VManhattan,
  VScaled, VNormalised,
  VPerp, VCrossProduct, VCrossProduct4D,
  VScalarTripleProduct, VVectorTripleProduct,
  VProjectionOnto,
  VTransposedMAV,
  VRectToPol, VPolToRect,
  VLerp,

  # Shape functions
  ShapeFromVertices, ShapePoints, ShapeSubpathRanges, ShapeCurveRanges,
  ShapeLength, LineToShapeIntersections, TransformedShape, PiecewiseArc,

  # Output formatting functions
  MaxDP, GFListStr, GFTupleStr, HTMLEscaped, AttrMarkup, ProgressColourStr,

  # SVG functions
  SVGStart, SVGEnd, SVGPathDataSegments, SVGPath, SVGText,
  SVGGroup, SVGGroupEnd, SVGGrid

)


#-------------------------------------------------------------------------------
# Fun stuff
#-------------------------------------------------------------------------------


# BEGIN CODE SNARFED FROM UDACITY

# NOTE: The function run() has been modified to return a list of
# position vectors in addition to the best error score.


# ------------------------------------------------
#
# this is the robot class
#

class robot:

    # --------
    # init:
    #    creates robot and initializes location/orientation to 0, 0, 0
    #

    def __init__(self, length = 20.0):
        self.x = 0.0
        self.y = 0.0
        self.orientation = 0.0
        self.length = length
        self.steering_noise = 0.0
        self.distance_noise = 0.0
        self.steering_drift = 0.0

    # --------
    # set:
    #	sets a robot coordinate
    #

    def set(self, new_x, new_y, new_orientation):

        self.x = float(new_x)
        self.y = float(new_y)
        self.orientation = float(new_orientation) % (2.0 * pi)


    # --------
    # set_noise:
    #	sets the noise parameters
    #

    def set_noise(self, new_s_noise, new_d_noise):
        # makes it possible to change the noise parameters
        # this is often useful in particle filters
        self.steering_noise = float(new_s_noise)
        self.distance_noise = float(new_d_noise)

    # --------
    # set_steering_drift:
    #	sets the systematical steering drift parameter
    #

    def set_steering_drift(self, drift):
        self.steering_drift = drift

    # --------
    # move:
    #    steering = front wheel steering angle, limited by max_steering_angle
    #    distance = total distance driven, most be non-negative

    def move(self, steering, distance,
             tolerance = 0.001, max_steering_angle = pi / 4.0):

        if steering > max_steering_angle:
            steering = max_steering_angle
        if steering < -max_steering_angle:
            steering = -max_steering_angle
        if distance < 0.0:
            distance = 0.0


        # make a new copy
        res = robot()
        res.length         = self.length
        res.steering_noise = self.steering_noise
        res.distance_noise = self.distance_noise
        res.steering_drift = self.steering_drift

        # apply noise
        steering2 = random.gauss(steering, self.steering_noise)
        distance2 = random.gauss(distance, self.distance_noise)

        # apply steering drift
        steering2 += self.steering_drift

        # Execute motion
        turn = tan(steering2) * distance2 / res.length

        if abs(turn) < tolerance:

            # approximate by straight line motion

            res.x = self.x + (distance2 * cos(self.orientation))
            res.y = self.y + (distance2 * sin(self.orientation))
            res.orientation = (self.orientation + turn) % (2.0 * pi)

        else:

            # approximate bicycle model for motion

            radius = distance2 / turn
            cx = self.x - (sin(self.orientation) * radius)
            cy = self.y + (cos(self.orientation) * radius)
            res.orientation = (self.orientation + turn) % (2.0 * pi)
            res.x = cx + (sin(res.orientation) * radius)
            res.y = cy - (cos(res.orientation) * radius)

        return res




    def __repr__(self):
        return '[x=%.5f y=%.5f orient=%.5f]'  % (self.x, self.y, self.orientation)


# ------------------------------------------------------------------------
#
# run - does a single control run.


def run(params, InitialCTE=1.0, ErrFnIx=0, printflag = False):

    myrobot = robot()
    myrobot.set(0.0, InitialCTE, 0.0)
    speed = 1.0
    err = 0.0
    N = 100
    # myrobot.set_noise(0.1, 0.0)
    myrobot.set_steering_drift(10.0 / 180.0 * pi) # 10 degree steering error

    Path = [(myrobot.x, myrobot.y)] #<<<<

    LastCTE = myrobot.y
    LastDeltaCTE = 0.0
    iCTE = 0.0

    for i in range(N * 2):

        CTE = myrobot.y
        dCTE = CTE - LastCTE
        ddCTE = dCTE - LastDeltaCTE
        iCTE += CTE

        steer = - params[0] * CTE  \
            - params[1] * dCTE \
            - iCTE * params[2]
        myrobot = myrobot.move(steer, speed)

        if ErrFnIx == 0:
          if i >= N:
              err += (CTE ** 2)
        elif ErrFnIx == 1:
          #err += CTE ** 2 + 1.0 * (dCTE**2 / (0.01 + CTE**2))
          err += (CTE + 4.0 * dCTE) ** 2 + (20.0 * ddCTE ** 2)
        else:
          raise Error('Unhandled error function index %s.' % str(ErrFnIx))

        LastCTE = CTE
        LastDeltaCTE = dCTE

        if printflag:
            print myrobot, steer
        Path.append((myrobot.x, myrobot.y)) #<<<<

    return err / float(N), Path


# END CODE SNARFED FROM UDACITY


#-------------------------------------------------------------------------------


def RenderToSVG(Data):

  '''Return data rendered to an SVG file in a string.

  Grid is a dictionary with the keys:

    Title: This title is rendered and is embedded in the SVG header.
    Grid: See SVGGrid().
    Paths: A list of Shapes to be rendered in red-to-indigo rainbow colours.
    BadPaths: A list of Shapes to be rendered in a faded colour.

  '''

  #-----------------------------------------------------------------------------

  def Field(Name, Default):
    return Data[Name] if Name in Data else Default

  #-----------------------------------------------------------------------------

  IT = tIndentTracker('  ')
  Result = ''

  Title = Field('Title', '(Untitled)')

  Result += SVGStart(IT, Title, {
    'width': '28cm',
    'height': '19cm',
    'viewBox': '0 0 28 19',
  })

  Result += IT('<defs>')
  IT.StepIn()
  Result += IT(
    '<marker id="ArrowHead"',
    '    viewBox="0 0 10 10" refX="0" refY="5"',
    '    markerUnits="strokeWidth"',
    '    markerWidth="16" markerHeight="12"',
    '    orient="auto">'
    '  <path d="M 0,0  L 10,5  L 0,10  z"/>',
    '</marker>'
  )
  # More marker, symbol and gradient definitions can go here.
  IT.StepOut()
  Result += IT('</defs>')

  # Background

  Result += IT(
    '<!-- Background -->',
    '<rect x="0" y="0" width="28" height="19" stroke="none" fill="white"/>'
  )

  # Outer group

  Result += IT('<!-- Outer group -->')
  Result += SVGGroup(IT, {'stroke': 'black', 'stroke-width': '0.025'})

  # Plots of both rejected and tentatively accepted paths

  Result += IT('<!-- Grid -->')
  Result += SVGGrid(IT, Data['Grid'])

  # Rejected paths

  BadPaths = Field('BadPaths', None)
  if BadPaths is not None:

    Result += IT('<!-- Rejected paths -->')
    Result += SVGGroup(IT, {
      'opacity': '0.10', 'stroke': '#ff0099'
    })

    NumBadPaths = len(BadPaths)

    for PathIx, Path in enumerate(BadPaths):
      Result += SVGPath(IT, Path)

    Result += SVGGroupEnd(IT)

  # Axes

  Result += IT('<!-- Axes -->')
  RangeMin = Data['Grid']['RangeMinima']
  RangeMax = Data['Grid']['RangeMaxima']
  Result += SVGGroup(IT, {
    'stroke': 'black',
    'stroke-width': '0.05',
    'stroke-linecap': 'square',
    'marker-end': 'url(#ArrowHead)'
  })
  Result += SVGPath(IT,
    [(Pt_Anchor, (RangeMin[0], 0.0)), (Pt_Anchor, (RangeMax[0] + 0.1, 0.0))]
  )
  Result += SVGPath(IT,
    [(Pt_Anchor, (0.0, RangeMin[1])), (Pt_Anchor, (0.0, RangeMax[1] + 0.1))]
  )
  Result += SVGGroupEnd(IT)

  # Paths in rainbow colours

  Paths = Field('Paths', None)
  if Paths is not None:

    NumPaths = len(Paths)

    Result += IT('<!-- Paths in rainbow colours -->')
    for PathIx, Path in enumerate(Paths):
      if NumPaths >= 2:
        Progress = float(PathIx) / float(NumPaths - 1)
      else:
        Progress = 1.0
      Opacity = 1.0 if Progress in [0.0, 1.0] else 0.60 + 0.00 * Progress
      ColourStr = ProgressColourStr(Progress, Opacity)
      Result += IT('<!-- Path %d, (%.1f%%) -->' % (PathIx, 100.0 * Progress))
      Result += SVGPath(IT, Path, {"stroke": ColourStr})

  # End of plot

  Result += SVGGroupEnd(IT)

  # Title and legend

  Result += IT('<!-- Title background -->')
  Result += IT(
    '<rect x="0" y="0" width="28" height="1.1" stroke="none" fill="white"/>'
  )

  Result += IT('<!-- Title group -->')
  Result += SVGGroup(IT, {
    'font-family': 'sans-serif',
    'font-size': '0.36',
    'font-weight': 'normal',
    'fill': 'black',
    'stroke': 'none'
  })

  Result += IT('<!-- Title -->')
  Result += SVGText(IT, (0.5, 0.82), Title, {
    'font-size': '0.72',
    'font-weight': 'bold'
  })

  Result += IT('<!-- Legend line labels-->')
  Result += SVGText(IT, (23.5, 0.82), 'Initial')
  Result += SVGText(IT, (26.0, 0.82), 'Final')

  Result += IT('<!-- Legend lines -->')
  Result += SVGGroup(IT, {
    'fill': 'none',
    'stroke-width': '0.1',
    'stroke-linecap': 'round'
  })

  Result += SVGPath(IT,
    [(Pt_Anchor, (22.5, 0.7)), (Pt_Anchor, (23.3, 0.7))],
    {'stroke': ProgressColourStr(0.0)}
  )

  Result += SVGPath(IT,
    [(Pt_Anchor, (25.0, 0.7)), (Pt_Anchor, (25.8, 0.7))],
    {'stroke': ProgressColourStr(1.0)}
  )

  Result += SVGGroupEnd(IT)

  # End of title group

  Result += SVGGroupEnd(IT)

  # End of outer group

  Result += SVGGroupEnd(IT)

  Result += SVGEnd(IT)

  return Result


#-------------------------------------------------------------------------------


def TwiddleAndPlot(InitialCTE, Tolerance, YScale, ErrFnIx, Data):

  '''Find the best PID values for the robot car, graphing the results to Data.

  The optimal PID values (Proportional, Differential and Integral) are
  returned as a tuple.

  InitialCTE is the initial cross-track error of the car in metres.
  Tolerance is the sum of the adjustments required for the greedy goat
    to consider the PID parameters optimal.
  YScale is the vertical magnification used in the output plot.
  ErrFnIx, the error function index selects the fitness function to use.
  Data is a dictionary to which the output is written.

  '''

  #-----------------------------------------------------------------------------

  # Adaptor function

  def Evaluate(P, OtherParams):
    return run(*((P,) + OtherParams))

  #-----------------------------------------------------------------------------

  Title = 'Unit5-16: Parameter Optimisation'

#  if YScale != 1.0:
#    Title += u' (y × %g)' % (YScale)

  Data['Title'] = Title

  Grid = {
    'CanvasMinima': (0.5, 1.5),
    'CanvasMaxima': (27.5, 18.5),
    'RangeMinima': (0, -10),
    'RangeMaxima': (100, 10),
    'YIsUp': True,
    'Transpose': False,
    'SquareAlignment': 'Corner',
    'DrawGrid': True,
    'DrawUnitAxes': False,
    'GridLineAttributes': {
      'stroke-width': '0.075', 'stroke': 'rgba(0, 192, 255, 0.5)'
    },
    'GeneralAttributes': {
      'stroke-width': '0.15', 'stroke': 'red'
    }
  }

  AM = AffineMtxTS((0.0, 0.0), (1.0, YScale))

  # Additional simulation paramters
  OtherParams = (InitialCTE, ErrFnIx)

  P = [0.0, 0.0, 0.0]
  DeltaP = [1.0, 1.0, 1.0]

  Paths = []
  BadPaths = []

  BestErr, Path = Evaluate(P, OtherParams)
  S = ShapeFromVertices(Path, 1)
  if YScale != 1.0:
    S = TransformedShape(AM, S)
  Paths.append(S)

  while sum(DeltaP) > Tolerance:

    for i in range(len(P)):

      # Try positive delta

      P[i] += DeltaP[i]
      Err, Path = Evaluate(P, OtherParams)

      if Err < BestErr:

        # Positive was good.

        BestErr = Err
        DeltaP[i] *= 1.1
        Paths.append(TransformedShape(AM, ShapeFromVertices(Path, 1)))

      else:

        # Positive delta was bad.

        BadPaths.append(TransformedShape(AM, ShapeFromVertices(Path, 1)))

        # Try negative delta instead

        P[i] -= 2.0 * DeltaP[i]
        Err, Path = Evaluate(P, OtherParams)

        if Err < BestErr:

          # Negative was good.

          BestErr = Err
          DeltaP[i] *= 1.1
          Paths.append(TransformedShape(AM, ShapeFromVertices(Path, 1)))

        else:

          # Neither positive nor negative was good.

          BadPaths.append(TransformedShape(AM, ShapeFromVertices(Path, 1)))

          # Try a smaller delta next time.

          P[i] += DeltaP[i]
          DeltaP[i] *= 0.9

    print "P = %s, |?P| = %s" % (GFListStr(P), GFListStr(DeltaP))
    #print BestErr

  Data['Grid'] = Grid
  Data['Paths'] = Paths

  # Uncomment to see the paths rejected by the Greedy Goat.
  #Data['BadPaths'] = BadPaths

  return P


#-------------------------------------------------------------------------------
# Main
#-------------------------------------------------------------------------------


def Main():

  ERRFNIX_STANDARD = 0
  ERRFNIX_ENHANCED = 1

  InitialCTE = 1.0
  Tolerance = 0.001
  YScale = 10.0
  ErrFnIx = ERRFNIX_STANDARD
  OutputFileName = 'output.svg'

  print 'Initial cross-track error = %g' % (InitialCTE)
  print 'Paramter tolerance = %g' % (Tolerance)

  Data = {}
  P = TwiddleAndPlot(InitialCTE, Tolerance, YScale, ErrFnIx, Data)

  print 'Best PID paramters:\n' + \
    '  Pprop = %g, Pdiff = %g Pint = %g' % (P[0], P[1], P[2])

  print 'Rendering SVG...'
  SVG = RenderToSVG(Data)
  print 'Done.'

  print 'Saving SVG to "' + OutputFileName + '"...'
  Save(SVG.encode('utf_8'), OutputFileName)
  print 'Done.'


#-------------------------------------------------------------------------------
# Command line trigger
#-------------------------------------------------------------------------------


if __name__ == '__main__':
  Main()


#-------------------------------------------------------------------------------
# End
#-------------------------------------------------------------------------------