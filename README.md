# TensorFlow Decode DICOM

## Operations

Decode DICOM contains two Tensorflow Operations that allow reading information from DICOM files.

### Decode DICOM Image
    loads a dicom image file and returns its pixel information in the specified output format.

### Decode DICOM Data
    loads a dicom image file and returns a sting tensor with the values of each of the supplied tags.


#### Inputs

##### contents:
        * Description: byte string with the file bytes. Use tf.io.read_file to read the file contents into a string.
        * Type: string

#### Attributes

##### dtype:
    * Description: Type for the output tensor
    * Type: Dtype
    * Possible Values: uint8, uint16, uint32, uint64, float, float16, double
    * Default Value: uint16

##### color_dim:
    * Description: Whether or not to include the color_dimension. If decoded image is monochrome and this attribute is True the output tensor will have an extra singleton dimension for the color.
    * Type: Bool
    * Default Value: True
    
##### on_error:
    * Description: This attribute establishes the behavior in case an error occurs on opening the image or if the output type cannot accomodate all the possible input values. *'strict'* throws an error, *'skip'* returns 0 and *'lossy'* continues with the operation as if no error occurred.
    * Possible Values: 'strict', 'skip', 'lossy'
    * Default Value: 'skip'

##### scale:
    * Description: This attribute establishes what to do with the scale of the input values. *'auto'* will autoscale the input values, if the output type is integer, *'auto'* will use the maximum output scale, if the output is float, *'auto'* will scale to [0,1]. *'preserve'* keeps the values as they are, an input value greater than the maximum possible output will be clipped.  
    * Possible Values: 'auto', 'preserve'
    * Default Value: 'preserve'

#### Outputs

##### output:
    * Description: Pixel data of the DICOM image
    * Type: Tensor of selected type (see attribute dtype)
    * Dimensions: [F, I, J, C]
        * F: Number of frames
        * I: Number of rows
        * J: Number of columns
        * C: Color dimensions


## Installation

    ```bash
        pip install gradient-decode-dicom
    ```
