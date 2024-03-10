CMSC 174 Laboratory 3: Image Blending
Gio Carlo Ciudadano

ABOUT
In this laboratory course, we were tasked to seamlessly combine two images together using Gaussian and Laplacian stacks. Gaussian stacks are created when an image is passed through a Gaussian filter several times and pushed to a stack, while Laplacian stacks are created when the image in the current layer of the Gaussian stack is subtracted from the image in the previous layer of the Gaussian stack.

This laboratory document makes use of Gaussian and Laplacian stacks by creating a Laplacian stack for two images to be combined, and adding each layer in the stack together to seemlessly blend two images together. The supplied image masks on the other hand defines the weights for each pixel in the blended image. For example, darker pixels in the image mask tell the program that the blend should bias towards the first image, while lighter pixels should bias towards the second image. This laboratory document makes use of a Gaussian stack of the image mask to determine the blend biases for each layer in the two Laplacian stacks so that the two supplied images are more seamless when being blended together.

In this laboratory document, two blended images are supplied: (A) A simpler blended image between an apple and an orange with a vertical slice image mask, and (B) A more complex blended image between a penguin and the pyramids with a complex-shape image mask. When the user launches this program, they will then be prompted to select and view one of the two blended images being supplied. The original and blended images being blended are found in this folder for reference.

DIRECTORY
blending.py - Contains the source code for the image blending.
left.png, right.png - Contains the original images (apple and orange) for the simpler blended image.
blendvert.png - Result for the simpler blended image.
verticalmask.png - Defines the vertical mask for the simpler blended image.
crazyone.png, crazytwo.png - Contains the original images (penguin and pyramids) for the more complex blended image.
crazymask.png - Defines the complex-shape image mask for the more-complex blended image.
blendcrazy.png - Result for the more-complex blended image.
