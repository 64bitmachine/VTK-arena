#!/usr/bin/env python

import re
from collections import Counter

# noinspection PyUnresolvedReferences
import vtkmodules.vtkInteractionStyle
# noinspection PyUnresolvedReferences
import vtkmodules.vtkRenderingOpenGL2
from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkFiltersModeling import vtkLinearExtrusionFilter
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer
)
from vtkmodules.vtkRenderingFreeType import vtkVectorText


def main():
    fileName = get_program_parameters()

    colors = vtkNamedColors()

    # Here we read the file keeping only the alpha characters
    #  and calculate the frequency of each letter.
    with open(fileName) as f:
        freq = Counter()
        for x in f:
            remove_digits = re.sub('[\d_]', '', x.strip().lower())
            freq += Counter(re.findall('\w', remove_digits, re.UNICODE))
    maxFreq = max(list(freq.values()))
    keys = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ'.lower())

    #
    # graphics stuff
    #
    ren = vtkRenderer()
    renWin = vtkRenderWindow()
    renWin.AddRenderer(ren)
    iren = vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)
    #
    # Setup letters
    #
    letters = list()
    extrude = list()
    mappers = list()
    actors = list()
    i = 0
    for k in keys:
        letters.append(vtkVectorText())
        letters[i].SetText(k.upper())

        extrude.append(vtkLinearExtrusionFilter())
        extrude[i].SetInputConnection(letters[i].GetOutputPort())
        extrude[i].SetExtrusionTypeToVectorExtrusion()
        extrude[i].SetVector(0, 0, 1.0)
        extrude[i].SetScaleFactor(float(freq[k]) / maxFreq * 2.50)

        mappers.append(vtkPolyDataMapper())
        mappers[i].SetInputConnection(extrude[i].GetOutputPort())
        mappers[i].ScalarVisibilityOff()

        actors.append(vtkActor())
        actors[i].SetMapper(mappers[i])
        actors[i].GetProperty().SetColor(colors.GetColor3d('Peacock'))

        if freq[k] <= 0:
            actors[i].VisibilityOff()
        ren.AddActor(actors[i])
        i += 1

    # Position the actors.
    y = 0.0
    for j in range(0, 2):
        x = 0.0
        for i in range(0, 13):
            actors[j * 13 + i].SetPosition(x, y, 0.0)
            x += 1.5
        y += -3.0

    ren.ResetCamera()
    ren.SetBackground(colors.GetColor3d('Silver'))
    ren.GetActiveCamera().Elevation(30.0)
    ren.GetActiveCamera().Azimuth(-30.0)
    ren.GetActiveCamera().Dolly(1)
    ren.ResetCameraClippingRange()

    renWin.SetSize(900, 900)
    renWin.SetWindowName('AlphaFrequency')

    # Interact with the data.
    iren.Start()


def get_program_parameters():
    import argparse
    description = 'Linearly extruded fonts to show letter frequency in text.'
    epilogue = '''
    Any file containing text can be used. 
    '''
    parser = argparse.ArgumentParser(description=description, epilog=epilogue,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('filename', help='Gettysburg.txt.')
    args = parser.parse_args()
    return args.filename


if __name__ == '__main__':
    main()
