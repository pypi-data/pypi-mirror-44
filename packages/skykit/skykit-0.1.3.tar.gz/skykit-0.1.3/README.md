# Sky Kit

Easy to use out-of-the-box satellite imagery package for Python aficionado.

Adding **fun** to satellites coolness 😎

> Warning: This is still a work in progress. Please do not use in production, yet.

## Seriously, what is it? 🧐

Sky kit is an ensemble of methods to ease satellite imagery processing, from and to developers and data scientists. Working with any satellite imagery provider, should be as easy as:

```
from skykit.providers import <ProviderName>
```

## Install 🚀

As with any python package, **pip** is your friend:

```
pip install skykit
```

## Usage 🎡

### Quick Start

The following shows details of a tile from Sentinel-2, that includes Paris (France), from 01/03/2019 to 08/03/2019:

```python
from datetime import date
from skykit.providers import Sentinel2

sat = Sentinel2(username="xxx", password="yyy")

tiles = sat.query(
    coordinates=(2.349014, 48.864716),     # Paris (FR) coordinates
    dates=(date(2019,3,1), date(2019,3,8)) # From march 1, 2019 to march 8, 2019
    )

len(tiles) # returns 6

tile = tiles[0]         # Pick any tile you want, or filter more
print(tile['summary'])  # returns 'Date: 2019-03-02T10:50:29.024Z, Instrument: MSI, Mode: , Satellite: Sentinel-2, Size: 730.27 MB'
```

In the previous example, the `tiles` variable will include meta information of every tile returned from Sentinel-2 query.

## Features

### Connecting to satellite images providers

Actually, Sky kit support the following ticked providers (others coming):

- [ ] Sentinel 1
- [x] Sentinel 2
- [ ] Landsat 7
- [ ] Landsat 8
- [ ] Modis
- [ ] Cbers-4
- [ ] Aqua

All image providers are grouped into `skykit.providers` module. Invoking a provider (like Sentinel-2) can be done like this:

```python
from skykit.providers import Sentinel2
```

We then need to initialize the connection with the provider. eg with Sentinel-2:

```python
sat = Sentinel2(username="xxx", password="yyy")
```

> Nota: Sentinel 1 & 2 require having credentials to connect to [Copernicus Open Access Hub](https://scihub.copernicus.eu/). Once created, insert your credentials in the code above.

## Todo 🔭

- [ ] Write a better documentation. Look for readthedocs.io
- [ ] Add providers
- [ ] Create a reusable abstraction of `Tile`, to create a uniform use of tiles, no matter which provider
- [ ] Ease working with tiles meta data (usually about the scene and satellite)
- [x] Allow querying using a polygon
- [ ] Allow querying using an address
- [ ] Use friendly dates (like text: `"26/03/2019"`), of use `from="..."` and `to="..."` instead of `date=(...)`
- [ ] Allow working on specific bands. Something like:

```python
image = tile.get('b04') # or tile.b04() ???
```

- [ ] More tests <-- ⚠ URGENT
- [ ] Create a CI/CD pipeline to publish **tags** into PyPi

This list is not exhaustive.

## Contribution 💪

Please suggest contributions using Github's **Pull Requests**.

## License 🤮

Read the [LICENSE.txt](LICENSE.txt) file.

Thanks 🙏
