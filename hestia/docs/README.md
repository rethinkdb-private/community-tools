Best resource on DYMO label file formats: http://developers.dymo.com/2010/03/23/understanding-label-file-formats-in-dymo-label-software-v-8-overview/
Full schema for the XML file format: http://www.labelwriter.com/software/dls/sdk/LabelFile.xsd

DYMO blog posts worth reading:
  - Working with printers and printing multiple labels: http://developers.dymo.com/2011/11/17/javascript-library-samples-printers-and-multiple-labels-printing/
  - Advanced text formatting: http://developers.dymo.com/2011/10/04/dymo-label-framework-javascript-library-advanced-text-formatting/
  - Printing multiple labels: http://developers.dymo.com/2010/06/17/dymo-label-framework-javascript-library-print-multiple-labels/
  - Generate image preview for labels: http://developers.dymo.com/2010/06/11/dymo-label-framework-javascript-library-samples-label-preview/
  - Basic example of printing a label from JS: http://developers.dymo.com/2010/06/02/dymo-label-framework-javascript-library-samples-print-a-label/

DYMO labels are generated from an XML file format that can be
used by any DYMO application. It can be used for die-cut or
continuous label layouts.

Labels can be designed in the DYMO designer, saved as XML, and
be modified in JS for bulk-printing.

Info on file formats:
  - Overview blog post of the XML file format (mirrored in [DYMO-format.md](/docs/DYMO-format.html)): http://developers.dymo.com/2010/03/23/understanding-label-file-formats-in-dymo-label-software-v-8-overview/
  - QR and barcodes http://developers.dymo.com/2011/10/05/experimental-support-for-qr-code-and-pdf417-barcodes/
  - Detailed blog post with a breakdown of label objects : http://developers.dymo.com/2010/03/24/understanding-label-file-formats-in-dymo-label-v-8-label-objects/

Here's a breakdown of an example file format:
```
<? xml version="1.0" encoding="utf-8"?>
<DieCutLabel Version="8.0" Units="twips">       # * Specifies the label type (die cut vs. continuous),
                                                # the version (DYMO 8.0), and unit of measure (twips,
                                                # or 1/440th of an inch)
    <PaperOrientation>Landscape</PaperOrientation>    # * Orientation of the label paper
    <Id>Address</Id>                                  # * Unique identifier for a label type,
                                                      # we can set this to anything we like 
                                                      # (also, it can be empty if not used 
                                                      # in the DYMO desktop software)
    <PaperName>30252 Address</PaperName>              # * Paper name as defined by the driver
    <DrawCommands>                              # * Draw commands for the label's shape -- can be ommitted
                                                # if we're only printing on the fly
        <RoundRectangle X="0" Y="0" Width="1581" Height="5040" Rx="270" Ry="270" />     # * Drawing a rounded rectangle
    </DrawCommands>
    <ObjectInfo>                                # * Specifies the position and properties for one object on the label
        <TextObject>                            # * A TextObject displays a block of text
            <Name>Text</Name>                   # * Unique identifying name for thie TextObject
            <ForeColor Alpha="255" Red="0" Green="0" Blue="0" />
            <BackColor Alpha="0" Red="255" Green="255" Blue="255" />
            <LinkedObjectName></LinkedObjectName>   # * Defines a link to content from a different object as content for this object
            <Rotation>Rotation0</Rotation>
            <IsMirrored>False</IsMirrored>
            <IsVariable>True</IsVariable>
            <HorizontalAlignment>Center</HorizontalAlignment>
            <VerticalAlignment>Middle</VerticalAlignment>
            <TextFitMode>ShrinkToFit</TextFitMode>
            <UseFullFontHeight>True</UseFullFontHeight>
            <Verticalized>False</Verticalized>
            <StyledText>                        # * Specifies the object's text and text styles
                <Element>
                    <String>Click here to enter text</String>
                    <Attributes>
                        <Font Family="Arial" Size="20" Bold="False" Italic="False" Underline="False" Strikeout="False" />
                        <ForeColor Alpha="255" Red="0" Green="0" Blue="0" />
                    </Attributes>
                </Element>
            </StyledText>
        </TextObject>
        <Bounds X="331" Y="150" Width="4560" Height="1343" />
    </ObjectInfo>
</DieCutLabel>
```
