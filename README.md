# intel-oneAPI

#### Team Name -
#### Problem Statement - 
#### Team Leader Email -

## A Brief of the Prototype:
This project is an implementation of the Fast Fourier Transform algorithm FFT in C++/C. It is a traditional implementation that does not make use of any parallel processing 
apis or libraries, CUDA, GPU etc. That does not preclude from these apis being added at any time in the future. This includes the intel SYS CL libraries and the intel-oneAPI
toolkit. 

Applications of FFT are endless and range from codecs for media/broadcasting to machine learning, computer vision etc.  
  
## Tech Stack: 
   List Down all technologies used to Build the prototype **Clearly mentioning Intel® AI Analytics Toolkits, it's libraries and the SYCL/DCP++ Libraries used**
This library uses C++/C and the CMake build system.
   
## Step-by-Step Code Execution Instructions:
Just type make to compile and then run 'prog_name' to run program
  
## What I Learned:
Mostly about the FFT algorithm and its implementation details. Already studied fft in college and hence was easier. There still were nuances to understand. The theory behind eigen 
values/FFT is quite complex and can trip up the best of PhD holders and was no different for me. C++ being a systems programming language is the best suited for writing 
FFT. 
	At the heart of the FFT is the butterfly pattern that ties two data points, either real or complex together. These butterlfies are quite costly to compute and since 
	they contribute to the magnification of the input, they cannot be done away altogether either. A variation of the FFT uses Bit Manipulation to simplify computation and 
	can speed things up quite a bit. However, a 8-point DFT requires 5 of these butterflies which is quite too many. And most of it is going to be thrown away in the end. The entire 
	imaginary part for example. Hence further optimizations are still possible.
	Thankfully not all algorithms are about performance/speed. There are applications of FFT that can gain from signal fidelity rather than just speed e.g deep learning.
FFT is by far the best method to digest the information in the input(s) totally and then to reproduce it when needed even if its takes a bit of computing hardware.

Many of the principles of FFT are inlaid in modern artificial intelligence programs and toolkits like tensorflow for machine learning. One can see them in the form
of convolutional neural networks in a layer of the neural net. 
There was a time when FFT was used for image and video compression. Since then, the focus has shifted from compression to retaining as much of the original 
input as possible and still deliver high bandwidth rates. The result of this can be viewed in modern MPEG4 streams which have set out with ambitious goals and have
managed to achieve them as well.
	I also learned further research is required into FFT. More specifically into how one can make more use of the fft signal instead of the original signal to 
extract information. Running the inverse FFT every time can be cumbersome and given the nature of FFT, I don't see how it can be avoided. But research might prove
 useful in this regard.

	
	
	
