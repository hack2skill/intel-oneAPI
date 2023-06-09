import pycristoforo as pyc
country = pyc.get_shape("India")
points = pyc.geoloc_generation(country, 100, "India")
pyc.geoloc_print(points, ',')
