---
---
> This article originally appeared on [DYMO's blog](http://developers.dymo.com/2010/03/24/understanding-label-file-formats-in-dymo-label-v-8-label-objects/)

> veuzubv. "Understanding Label File Formats in DYMO Label V.8 – Label Objects." DYMO: Label Inside Out. DYMO, 24 Mar. 2010. Web. 10 May 2014.

# Understanding Label File Formats in DYMO Label v.8 – Label Objects

In a previous post we looked at the new label file format used by DYMO
Label v.8 software (DLS) from a bird’s eye view. Now it’s a time to
look a little closer. The most important thing in a label file are
label objects. Label objects contain data and formatting properties and
define the label’s content. All object types and most of their
properties are available through the DLS UI and are pretty
straightforward. In this post we will briefly describe all label
objects and will  look at most important properties as well as at
properties not available through the UI.

Let’s look at [this](/docs/UndestandingLabelFileFormat-AllObjects.label)
label file (_included in
/docs/UndestandingLabelFileFormat-AllObjects.label_). It contains all
the different object types supported by DLS. If you open the label in
DLS it will look like this:

![Label image](/docs/undestandinglabelfileformatallobjects-label.png)

```
001 <?xml version="1.0" encoding="utf-8"?>
002 <DieCutLabel Version="8.0" Units="twips">
003     <PaperOrientation>Landscape</PaperOrientation>
004     <Id>LargeShipping</Id>
005     <PaperName>30256 Shipping</PaperName>
006     <DrawCommands>
007         <RoundRectangle X="0" Y="0" Width="3331" Height="5715" Rx="270" Ry="270" />
008     </DrawCommands>
009     <ObjectInfo>
010         <TextObject>
011             <Name>BarcodeText</Name>
012             <ForeColor Alpha="255" Red="0" Green="0" Blue="0" />
013             <BackColor Alpha="0" Red="255" Green="255" Blue="255" />
014             <LinkedObjectName></LinkedObjectName>
015             <Rotation>Rotation0</Rotation>
016             <IsMirrored>False</IsMirrored>
017             <IsVariable>False</IsVariable>
018             <HorizontalAlignment>Left</HorizontalAlignment>
019             <VerticalAlignment>Top</VerticalAlignment>
020             <TextFitMode>AlwaysFit</TextFitMode>
021             <UseFullFontHeight>False</UseFullFontHeight>
022             <Verticalized>False</Verticalized>
023             <StyledText>
024                 <Element>
025                     <String>BARCODE</String>
026                     <Attributes>
027                         <Font Family="Arial" Size="12" Bold="False" Italic="False"
028                                      Underline="False" Strikeout="False" />
029                         <ForeColor Alpha="255" Red="0" Green="0" Blue="0" />
030                     </Attributes>
031                 </Element>
032             </StyledText>
033         </TextObject>
034         <Bounds X="336" Y="132.900024414063" Width="2265" Height="345" />
035     </ObjectInfo>
036     <ObjectInfo>
037         <ShapeObject>
038             <Name>Shape</Name>
039             <ForeColor Alpha="255" Red="0" Green="0" Blue="0" />
040             <BackColor Alpha="0" Red="255" Green="255" Blue="255" />
041             <LinkedObjectName></LinkedObjectName>
042             <Rotation>Rotation0</Rotation>
043             <IsMirrored>False</IsMirrored>
044             <IsVariable>False</IsVariable>
045             <ShapeType>Ellipse</ShapeType>
046             <LineWidth>45</LineWidth>
047             <LineAlignment>Center</LineAlignment>
048             <FillColor Alpha="0" Red="255" Green="255" Blue="255" />
049         </ShapeObject>
050         <Bounds X="3004" Y="2187.89990234375" Width="2670" Height="570" />
051     </ObjectInfo>
052     <ObjectInfo>
053         <AddressObject>
054             <Name>Address</Name>
055             <ForeColor Alpha="255" Red="0" Green="0" Blue="0" />
056             <BackColor Alpha="0" Red="255" Green="255" Blue="255" />
057             <LinkedObjectName></LinkedObjectName>
058             <Rotation>Rotation0</Rotation>
059             <IsMirrored>False</IsMirrored>
060             <IsVariable>True</IsVariable>
061             <HorizontalAlignment>Left</HorizontalAlignment>
062             <VerticalAlignment>Top</VerticalAlignment>
063             <TextFitMode>ShrinkToFit</TextFitMode>
064             <UseFullFontHeight>True</UseFullFontHeight>
065             <Verticalized>False</Verticalized>
066             <StyledText>
067                 <Element>
068                     <String>DYMO
069 </String>
070                     <Attributes>
071                         <Font Family="Arial" Size="12" Bold="True" Italic="False"
072                                      Underline="False" Strikeout="False" />
073                         <ForeColor Alpha="255" Red="0" Green="0" Blue="0" />
074                     </Attributes>
075                 </Element>
076                 <Element>
077                     <String>828 SAN PABLO AVE
078 </String>
079                     <Attributes>
080                         <Font Family="Arial" Size="12" Bold="False" Italic="True"
081                                      Underline="False" Strikeout="False" />
082                         <ForeColor Alpha="255" Red="0" Green="0" Blue="0" />
083                     </Attributes>
084                 </Element>
085                 <Element>
086                     <String>ALBANY CA 94706-1567</String>
087                     <Attributes>
088                         <Font Family="Arial" Size="12" Bold="False" Italic="False"
089                                      Underline="True" Strikeout="False" />
090                         <ForeColor Alpha="255" Red="0" Green="0" Blue="0" />
091                     </Attributes>
092                 </Element>
093             </StyledText>
094             <ShowBarcodeFor9DigitZipOnly>True</ShowBarcodeFor9DigitZipOnly>
095             <BarcodePosition>BelowAddress</BarcodePosition>
096             <LineFonts>
097                 <Font Family="Arial" Size="12" Bold="True" Italic="False"
098                              Underline="False" Strikeout="False" />
099                 <Font Family="Arial" Size="12" Bold="False" Italic="True"
100                              Underline="False" Strikeout="False" />
101                 <Font Family="Arial" Size="12" Bold="False" Italic="False"
102                              Underline="True" Strikeout="False" />
103             </LineFonts>
104         </AddressObject>
105         <Bounds X="336" Y="885" Width="4380" Height="960" />
106     </ObjectInfo>
107     <ObjectInfo>
108         <CircularTextObject>
109             <Name>CURVED-TEXT</Name>
110             <ForeColor Alpha="255" Red="0" Green="0" Blue="0" />
111             <BackColor Alpha="0" Red="255" Green="255" Blue="255" />
112             <LinkedObjectName></LinkedObjectName>
113             <Rotation>Rotation0</Rotation>
114             <IsMirrored>False</IsMirrored>
115             <IsVariable>False</IsVariable>
116             <Text>Double-click to enter text</Text>
117             <Font Family="Arial" Size="12" Bold="False" Italic="False" Underline="False"
118                          Strikeout="False" />
119             <StartAngle>0</StartAngle>
120             <Mode>ArcTextTop</Mode>
121             <CircleAlignment>CenterAtTop</CircleAlignment>
122             <TextAlignment>Center</TextAlignment>
123             <VerticalAlignment>Middle</VerticalAlignment>
124         </CircularTextObject>
125         <Bounds X="4204" Y="2739" Width="1470" Height="510" />
126     </ObjectInfo>
127     <ObjectInfo>
128         <BarcodeObject>
129             <Name>Barcode</Name>
130             <ForeColor Alpha="255" Red="0" Green="0" Blue="0" />
131             <BackColor Alpha="0" Red="255" Green="255" Blue="255" />
132             <LinkedObjectName>BarcodeText</LinkedObjectName>
133             <Rotation>Rotation0</Rotation>
134             <IsMirrored>False</IsMirrored>
135             <IsVariable>True</IsVariable>
136             <Text>BARCODE</Text>
137             <Type>Code128Auto</Type>
138             <Size>Medium</Size>
139             <TextPosition>Bottom</TextPosition>
140             <TextFont Family="Arial" Size="8" Bold="False" Italic="False"
141                              Underline="False" Strikeout="False" />
142             <CheckSumFont Family="Arial" Size="8" Bold="False" Italic="False"
143                                  Underline="False" Strikeout="False" />
144             <TextEmbedding>None</TextEmbedding>
145             <ECLevel>0</ECLevel>
146             <HorizontalAlignment>Center</HorizontalAlignment>
147             <QuietZonesPadding Left="0" Top="0" Right="0" Bottom="0" />
148         </BarcodeObject>
149         <Bounds X="2524" Y="150" Width="3150" Height="720" />
150     </ObjectInfo>
151     <ObjectInfo>
152         <DateTimeObject>
153             <Name>DateTime</Name>
154             <ForeColor Alpha="255" Red="0" Green="0" Blue="0" />
155             <BackColor Alpha="0" Red="255" Green="255" Blue="255" />
156             <LinkedObjectName>Counter</LinkedObjectName>
157             <Rotation>Rotation0</Rotation>
158             <IsMirrored>False</IsMirrored>
159             <IsVariable>False</IsVariable>
160             <HorizontalAlignment>Left</HorizontalAlignment>
161             <VerticalAlignment>Top</VerticalAlignment>
162             <TextFitMode>ShrinkToFit</TextFitMode>
163             <UseFullFontHeight>True</UseFullFontHeight>
164             <Verticalized>False</Verticalized>
165             <DateTimeFormat>WeekdayLongMonthDayLongYear</DateTimeFormat>
166             <Font Family="Arial" Size="12" Bold="False" Italic="False" Underline="False"
167                          Strikeout="False" />
168             <PreText>Pre Text 001</PreText>
169             <PostText></PostText>
170             <IncludeTime>False</IncludeTime>
171             <Use24HourFormat>False</Use24HourFormat>
172         </DateTimeObject>
173         <Bounds X="381" Y="2982.89990234375" Width="2880" Height="165" />
174     </ObjectInfo>
175     <ObjectInfo>
176         <CounterObject>
177             <Name>Counter</Name>
178             <ForeColor Alpha="255" Red="0" Green="0" Blue="0" />
179             <BackColor Alpha="0" Red="255" Green="255" Blue="255" />
180             <LinkedObjectName></LinkedObjectName>
181             <Rotation>Rotation0</Rotation>
182             <IsMirrored>False</IsMirrored>
183             <IsVariable>False</IsVariable>
184             <HorizontalAlignment>Left</HorizontalAlignment>
185             <VerticalAlignment>Top</VerticalAlignment>
186             <TextFitMode>ShrinkToFit</TextFitMode>
187             <UseFullFontHeight>True</UseFullFontHeight>
188             <Verticalized>False</Verticalized>
189             <Font Family="Arial" Size="12" Bold="False" Italic="False" Underline="False"
190                          Strikeout="False" />
191             <PreText>Pre Text </PreText>
192             <PostText></PostText>
193             <Start>1</Start>
194             <Current>1</Current>
195             <Increment>1</Increment>
196             <FormatWidth>3</FormatWidth>
197             <UseLeadingZeros>True</UseLeadingZeros>
198         </CounterObject>
199         <Bounds X="336" Y="2589" Width="2160" Height="330" />
200     </ObjectInfo>
201     <ObjectInfo>
202         <ImageObject>
203             <Name>Graphic</Name>
204             <ForeColor Alpha="255" Red="0" Green="0" Blue="0" />
205             <BackColor Alpha="0" Red="255" Green="255" Blue="255" />
206             <LinkedObjectName></LinkedObjectName>
207             <Rotation>Rotation0</Rotation>
208             <IsMirrored>False</IsMirrored>
209             <IsVariable>False</IsVariable>
210             <Image>iVBORw0KGgoAAAANSUhEUgAAAYgAAAF2CAYAAAB02w9PAAAACXBIWXMAAA7DAAAOwwHHb6hkAA
507             B/w9ijrFQSeOvwgAAAABJRU5ErkJggg==</Image>
508             <ScaleMode>Uniform</ScaleMode>
509             <BorderWidth>0</BorderWidth>
510             <BorderColor Alpha="255" Red="0" Green="0" Blue="0" />
511             <HorizontalAlignment>Center</HorizontalAlignment>
512             <VerticalAlignment>Center</VerticalAlignment>
513         </ImageObject>
514         <Bounds X="4860" Y="852.900024414063" Width="691.203186035156" Height="615" />
515     </ObjectInfo>
516     <ObjectInfo>
517         <ImageObject>
518             <Name>Graphic-Clone</Name>
519             <ForeColor Alpha="255" Red="0" Green="0" Blue="0" />
520             <BackColor Alpha="0" Red="255" Green="255" Blue="255" />
521             <LinkedObjectName>Graphic</LinkedObjectName>
522             <Rotation>Rotation0</Rotation>
523             <IsMirrored>False</IsMirrored>
524             <IsVariable>False</IsVariable>
525             <ImageLocation/>
526             <ScaleMode>Uniform</ScaleMode>
527             <BorderWidth>0</BorderWidth>
528             <BorderColor Alpha="255" Red="0" Green="0" Blue="0" />
529             <HorizontalAlignment>Center</HorizontalAlignment>
530             <VerticalAlignment>Center</VerticalAlignment>
531         </ImageObject>
532         <Bounds X="5091.28344726562" Y="1602.90002441406" Width="582.716552734375"
533                   Height="390" />
534     </ObjectInfo>
535     <ObjectInfo>
536         <ImageObject>
537             <Name>GoogleLogo</Name>
538             <ForeColor Alpha="255" Red="0" Green="0" Blue="0" />
539             <BackColor Alpha="0" Red="255" Green="255" Blue="255" />
540             <LinkedObjectName></LinkedObjectName>
541             <Rotation>Rotation0</Rotation>
542             <IsMirrored>False</IsMirrored>
543             <IsVariable>False</IsVariable>
544             <ImageLocation>http://www.google.com/intl/en_ALL/images/logo.gif</ImageLocation>
546             <ScaleMode>Uniform</ScaleMode>
547             <BorderWidth>0</BorderWidth>
548             <BorderColor Alpha="255" Red="0" Green="0" Blue="0" />
549             <HorizontalAlignment>Center</HorizontalAlignment>
550             <VerticalAlignment>Center</VerticalAlignment>
551         </ImageObject>
552         <Bounds X="3465" Y="2292.90002441406" Width="1905.34887695313" Height="375" />
553     </ObjectInfo>
554 </DieCutLabel>
```

_Note: lines ##211-506 contain image data and were deleted because the
real image content is irrelevant to our discussion._

## Common Properties

### Name

```
011             <Name>BarcodeText</Name>
```

__Name__ is one of the most important properties. It serves as a unique
identifier for an object. Usually it is used to refer to the object
from code that uses the DYMO Label SDK. There are no restrictions how
to name the object. The name can contain any Unicode character and the
name length has no limit. Still, it is a good practice to only use
alpha-numeric characters and keep the name length short. It is not
required to assign a name to the object – if the object is not going to
be referenced it is perfectly OK to have empty name. It is also OK (but
not very useful) to have two or more objects with the same name. The
DYMO Label Runtime will use the first object found with a specified
name. There is no guarantee which object with the same name will be
used. Names are case sensitive, so “Name”, “NAME”, and “name” are
treated as different names.

### LinkedObjectName

```
128         <BarcodeObject>
129             <Name>Barcode</Name>
132             <LinkedObjectName>BarcodeText</LinkedObjectName>
```

__LinkedObjectName__ property defines a link where you can content from
a different object as content for the current object. For example, look
at line #124. It specifies that the text for the barcode object named
“Barcode” should be taken from an object named “BarcodeText”. In the
DYMO Label application it is only possible to link a barcode object to
a text object. But in code it is possible to link any objects by
specifying __LinkedObjectName__ property directly in the label file.

```
517         <ImageObject>
518             <Name>Graphic-Clone</Name>
521             <LinkedObjectName>Graphic</LinkedObjectName>
```

Line #432 directs the Runtime to get image data for the graphic object
named “Graphic-Clone” from the graphic object named “Graphic”. As a
result the label file contains only one copy of the image data: that
significantly decreases its size.

## Text Object
The __Text__ object displays a block of text.

### StyledText
The __StyledText__ property specifies the object’s text and text
style(s). the following attributes are available on a per character
basis:

- font name
- font size
- font style: bold, italic, underline, strikeout
- color (character foreground color)

```
066             <StyledText>
067                 <Element>
068                     <String>DYMO
069 </String>
070                     <Attributes>
071                         <Font Family="Arial" Size="12" Bold="True" Italic="False"
072                                      Underline="False" Strikeout="False" />
073                         <ForeColor Alpha="255" Red="0" Green="0" Blue="0" />
074                     </Attributes>
075                 </Element>
076                 <Element>
077                     <String>828 SAN PABLO AVE
078 </String>
079                     <Attributes>
080                         <Font Family="Arial" Size="12" Bold="False" Italic="True"
081                                      Underline="False" Strikeout="False" />
082                         <ForeColor Alpha="255" Red="0" Green="0" Blue="0" />
083                     </Attributes>
084                 </Element>
085                 <Element>
086                     <String>ALBANY CA 94706-1567</String>
087                     <Attributes>
088                         <Font Family="Arial" Size="12" Bold="False" Italic="False"
089                                      Underline="True" Strikeout="False" />
090                         <ForeColor Alpha="255" Red="0" Green="0" Blue="0" />
091                     </Attributes>
092                 </Element>
093             </StyledText>
``

The example above specifies that the text contains three lines, with
each line formatted differently. The __Element__ tag specifies a range
of characters with the same formatting. The __String__ tag specifies
text/characters, while the __Attributes__ tag specifies text formatting
attributes.

__Adding Line Breaks__

To include a new line separator just put a new line/carriage return
symbol(s) into the __String__ tag. The text specified by above __StyledText__
will be displayed like this:

> __DYMO__
> 828 SAN PABLO AVE
> ALBANY CA 94706-1567

### UseFullFontHeight

```
021             <UseFullFontHeight>False</UseFullFontHeight>
```
The __UseFullFontHeight__ property can be used to increase font size to
the maximum possible size when shrink-to-fit or auto-fit are applied to
the object. When __UseFullFontHeight__ is True (the default) the line
height is calculated based on the font metrics. So, the height is the
same regardless of the text content. When __UseFullFontHeight__ is
False the line height is calculated based on the height of each
character’s “black box” (an area where glyph outline is drawn). Because
usually a character’s “black box” height is smaller than its font
height a bigger font size can be used to draw text.  This property
might be useful in scenarios where printable area is limited but you
want to make the text as large as possible, e.g. for tape labels. For
example, below is the same label with only __UseFullFontHeight__
property changed.

_UseFullFontHeight=True_

![UseFullFontHeight=True](/docs/fullfontheight-true.png)

_UseFullFontHeight=False_

![UseFullFontHeight=False](/docs/fullfontheight-false.png)

## Address Object

The __Address__ object is similar to the Text object. It is used to
display address information. If the address is a valid US address then
the Address object can also display and Intelligent Mail barcode.

## Barcode Object
The __Barcode__ object is used to display barcodes on the label.

## Image Object
The __Image__ object is used to display bitmap images on the label.

### Image
The __Image__ property specifies image data. Image data is encoded
using base64 encoding and the image data itself is in PNG format.

### ImageLocation
```
544             <ImageLocation>http://www.google.com/intl/en_ALL/images/logo.gif</ImageLocation>
```

The __ImageLocation__ property is another way to specify image data. In
this case image data is not stored inside the label but is loaded on
demand from the specified URI. The URI can be a path to a local file,
e.g. “C:UsersUserNameDocumentsMyImage.png” or “http://”, “https://” or
“file://” URLs. The URI can point not only to PNG files but to any
image file type supported by the DYMO Label Software (BMP, JPG, GIF,
TIF, PNG). __ImageLocation__ can be used in scenario when there is a
set of label files that should share same image, e.g. a company logo.

Note: the specified URI will be accessed on demand, basically when a
label is being printed or previewed. If the URI specifies a remote
resource there can be a delay or even an exception if the URI is
inaccessible.

## Date and Time Object
The __Date and Time__ object is a special kind of the Text object
designed to display current date and/or time.

## Counter Object
The __Counter__ object is a special kind of the Text object designed to
print auto-incremented numbers. Every time the label is printed the
__Current__ property of the __Counter__ object is updated based on the
__Increment__ property. So, the next time the label is printed the new
updated value for the __Counter__ will be used.

Note: To preserve the value __Current__ property between an application
runs (so, the next time application runs the __Counter__ continues from
its last value), the label should be saved when the application exits.
To avoid unnecessary label modifications we do not recommend to use
__Counter__ objects in SDK applications. Use Text object instead and
format its text according to the application’s logic. The “current”
counter value can be fetched for example from a database or from a
web-server in a way the application fully controls and understands.

## Shape Object
The __Shape__ object displays simple geometric figures like rectangles
and ellipses as well as vertical and horizontal lines.

## Circular Text Object
The __Circular Text__ object display text on a curve. Usually it is
used on CD/DVD labels.
