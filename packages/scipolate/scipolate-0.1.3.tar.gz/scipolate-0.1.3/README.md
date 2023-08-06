SciPolate
=========

Scipolate offers a small helper class that can be used to perform 
2D interpolation tasks using scipy. It is meant to be used as a common 
interface to run and validate the task automated in the same way.

Installation
============

Install Scipolate using pip:

```bash
pip install scipolate
```

Note
====

Scipolate was originally a part of a interpolation web-app used in one of my 
lectures. That means it was used in an API. Hence, the parameters are set in 
one single JSON-like dictionary, which is un-pythonic.
For the same reason, the class does provide an output *Report* including the 
result as a base64 encoded image. Nevertheless, the class can be used outside 
of a web-application context. Mind that performance was not important during 
development. In case you need a fast algorithm, use scipy directly, or 
something like the [interpolation](https://pypi.org/project/interpolation/) 
library.

With the new version the Interpolation itself is outsourced into a class on 
its own. All the image processing and transformation used for the reporting 
tools in my web based applications, a class called `WebInterface` is implemented.

Usage
=====

There are two main interfaces that can be used:

* The *Interpolator* class, which is the core class performing the 
interpolation.

* The *WebInterface* class which is meant to be used in a API, as it takes the
arguments as JSON and returns JSON along with base64 encoded images.

 
 Example
 -------
 
 An Example will follow.