# TensorFlow Decode DICOM

## Operations

Decode DICOM contains two Tensorflow Operations that allow reading information from DICOM files.

### Decode DICOM Image
    loads a dicom image file and returns its pixel information in the specified output format

#### Inputs
    contents:
        * Description: byte string with the file bytes. Use tf.io.read_file to read the file contents into a string.
        * Type: string

#### Attributes

##### T:
    * Description: Type for the output tensor
    * Type: Dtype
    * Possible Values: uint8, uint16, uint32, uint64, float, double
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
    * Type: Tensor of type T (see attribute T)
    * Dimensions: [F, I, J, C]
        * F: Number of frames
        * I: Number of rows
        * J: Number of columns
        * C: Color dimensions

### Decode DICOM Data

## Installation

### From Docker Container

**Pull the container:**
```bash
    docker pull tensorflow/tensorflow:nightly-custom-op
    docker run -it -v /host/work/dir:/container/work/dir tensorflow/tensorflow:nightly-custom-op
```

**Clone the repository:**
```bash
    git clone https://github.com/gradienthealth/tensorflow_dicom.git
    cd tensorflow_dicom
```

**Build PIP Package with Bazel:**
```bash
    ./configure.sh
    bazel build build_pip_pkg
    bazel-bin/build_pip_pkg artifacts
```
**Build PIP Package with Make:**
```bash
    make pip_pkg
```

**Install PIP Package:**
```bash
    pip install artifacts/*.whl
```

### From Sources

**Dependencies:**
* rsync
* python
* python-pip
* [DCMTK](https://dicom.offis.de/dcmtk.php.en)
* [Bazel](https://www.bazel.build/) (only for bazel build)


**Install Dependencies:**
```bash
    sudo apt-get update
    sudo apt-get install python python-pip rsync libdcmtk-dev
```

**Clone the repository:**
```bash
    git clone https://github.com/gradienthealth/tensorflow_dicom.git
    cd tensorflow_dicom
```

**Build PIP Package:**
```bash
    ./configure.sh
    make pip_pkg
```

**Install PIP Package:**
```bash
    pip install artifacts/*.whl
```


## Examples

## Decode DICOM Image

The file example/image_example.py uses the decode DICOM image op to display sample dicom files. (link)[https://barre.nom.fr/medical/samples/]

```bash
    cd example
    python image_example.py
```

## Decode DICOM Data

The file example/data_example.py uses the decode DICOM data op to extract tag values from sample dicom files. (link)[https://barre.nom.fr/medical/samples/]

```bash
    cd example
    python data_example.py
```
