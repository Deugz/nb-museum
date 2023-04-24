# Planets Building Blocks

***

<h3> <strong> <u>  Introduction </u></strong> </h3>

:::::{div} full-width
::::{grid} 2

:::{grid-item}
:columns: 7

Intro paragraph

:::

:::{grid-item}
:columns: 5

**Plan**

- [**Interstellar Dust**](content:references:Title1) 
    - Dust Light Interaction

<br>

- **Summary**

:::

::::
:::::

::::{margin}
:::{grid-item-card}
:class-header: bg-light

**Page**
^^^

- Status: ![flag alt >](../../Docs/Svg_icons/Under_construction.svg)
  
- Reviewed: &#x274C;
       
- Updated: 04/02/2023
   
:::
::::



::::::{grid-item-card}
:class-header: bg-light

**Notes**
^^^
:::::{grid} 2
::::{grid-item}

```{admonition} To Do
:class: note, dropdown

- Think about coherent plan
- Implement

```

::::

::::{grid-item}

```{admonition} Colaboration
:class: tip, dropdown

Star formation is not my expertise so if you want to help, feel free to comment the contribution you could make

```
::::
:::::  
::::::


```{note}

Speak about snowline

- Grain shape, grain properties SED !

```

## From molecular clouds to PPD

- {cite:p}`Hirashita2013`: Numerical modelling (formation of μm-sized grains in dense cores of molecular clouds), results: coreshine (mid-IR emission due to scattering from μm-sized grains in dense cores) must come from long-lived entities rather than dynamically transient objects (based on free-fall time for typical hydrogen densities around 105 cm-3)

### Water in the ISM

- **Review**: {cite:p}`Vandishoeck2011`: observations (80 sources), molecules: H2O/H218O/CO/13CO/C18O/OH+/H2O+/dust continuum, lack of water in cold gas, strong water emission from shocks, UV radiational heating of gas in outflow, H2O generally not the dominant coolant in warm dense gas around protostars.  

```{note}

To (print) read !!

```



## Dust observation in PPD

- {cite:p}`Min2012`:modelling (understand effects of dust particle structure/size-dependent grain settling/instrumental properties), different dust particle models and disk structures, particle size and shape have strong effect on brightness/detectability of disk, realistic models give very different results than homogeneous sphere model, need to also simulate telescope effects before interpretation of results



(content:references:Title1)=
## Interstellar Dust
    
```{warning}

- [Dustpy](https://stammler.github.io/dustpy/) - Python package to model dust in PPD
    **Check in more detail**

```

### Grain shape

- {cite:p}`Mutschke2009`: Lab and calculated dust extinction spectra often not in good agreement, modelling with distribution of form factors (DFF) to match lab results -> later grain shapes can be derived from model fits independently.



## Ice

<p class="emphase"> Is the ice amorphous, crystaline, something else ...</p>

- {cite:p}`Ehrenfreund2003`: cold ISM: dust particles covered in ultrathin icy layers, drive rich chemistry in star-forming regions, polar caps of terrestrial planets and outer solar system satellites covered in ice, earth atmosphere, weather etc., are lab ices good analogues?, bulk structure, surface catalytic properties, ice + dust experiments (1 + 0 g) + models, proposed experiments for ISS.

### Processing


```{figure} Docs/Dust-grains-ice-process.png

{cite:p}`Boogert2015`

```



### Surface

- {cite:p}`Fraser2002`: experiment designed to study surface ice chemistry in the lab (solid-gas interactions), 7 – 500 K, pressures 103 larger than in protoplanetary disks, gas composition H2 & CO, mass-spec/RAIRS/quartz crystal microbalance all in one chamber.


### Crystaline

- {cite:p}`Schegerer2010`: spectroscopic detection of crystalline water ice in young stellar object, predominantly small grains (0.1 – 0.3 μm), few large grains, evidence for grain growth, crystallinity increases in upper layers of circumstellar disk, only amorphous grains exist in bipolar envelope, crystallization close to disk atmosphere, where water ice is shielded from hard radiation.



### Ferroelectric Ice

```{note}

Definition + link toward physic course on ferroelectrecity

```


- {cite:p}`Fukazawa2015`: Characterisation (neutron diffraction, D2O with impurities (KOD, NaOD, LiOD, DCl, ND3, Ca(OD)2), atmospheric pressure) of “ferroelectric ice” (= ice XI, can generate giant electric fields), stable @ 57 – 74 K, can be important for planet formation, results: ferroelectric ice forms with dopants that produce L-defects (KOD, NaOD), no ferroelectricity observed for samples with D-defect.

- {cite:p}`Iedema1998`: Characterisation experiments (partially proton-ordered ice Ic (vapour deposited on Pt(111) substrate), 40 – 150 K, Kelvin probe), result: slight preference for O aiming away from surface, 0.2 % net dipole per H2O molecule (@ 40 K) = -3 mV/monolayer, decreases with deposition T (exp(-T/27K)), when ice changes from amorphous to crystalline (130, 140, 150 K), dielectric properties become active, vapour-deposited ice in space may develop large electric fields.




### Dust Light Interaction

:::::{div} full-width
::::{grid} 3 

:::{grid-item}

**Energy absorbed by grain**

```{image} Docs/Equation/Eabs.svg
:alt: Eabs
:width: 200px
:align: center
```

:::

:::{grid-item}

**Energy emitted by grain**

```{image} Docs/Equation/Eem.svg
:alt: Eem
:width: 200px
:align: center
```

:::

:::{grid-item}

**Equilibrium dust temperature**

```{image} Docs/Equation/Tdust_eq.svg
:alt: Tdust_eq
:width: 300px
:align: center
```
:::
::::

:::::


#### Processing



::::{div} full-width
```{figure} Docs/Ice-process-PPD1.png
---
name: Bouncing_lab
width: 1400px
---
```
::::


- Up to protostar - {cite:p}`Oberg2011`



### Dust evolution

#### Grain-Grain collisions

foundation for theoratical models of dust evolution in disks
- cf next chapters


## Interplanetary Dust Particles

:::::{div} full-width

::::{grid} 2

:::{grid-item}

<p class="emphase"> What we can sample that is most similar to what was originaly present in the Solar Nebula</p>

:::

:::{grid-item}

```{figure} Docs/Porous_chondriteIDP.jpg
---
name: Interplanetary Dust
width: 800px
---
[Source](https://upload.wikimedia.org/wikipedia/commons/1/1c/Porous_chondriteIDP.jpg)

```

:::
::::
:::::







{cite:p}`Bradley2013`


How can we catch those grains ? Well this has been achieved by the Stardust mission that we will describe below


### StarDust mission

First **sample return mission**, launched by NASA in 1999

- StarDust [website](https://solarsystem.nasa.gov/stardust/home/index.html)

### Properties

{cite:p}`Mann2005`



### Chemical evolution

{cite:p}`Eistrup2022b`



## Comets

- {cite:p}`Weidenschilling1997`: Modelling (numerical simulation (growth of cometesimals), beginning with uniform mixture of microscopic grains in nebular gas, coagulation, settling => small aggregates in central plane, gas drag, radial motion, velocity dispersion prevents gravitational instability to grow bodies > 10 m), results: size-distribution of cometesimals shows narrow peak @ 10’s – 100’s m, resulting bodies have low mechanical strength, macroscopic voids, small scale porosity.


### Cometesimals

- {cite:p}`Lorek2015`


## Ice in space

- {cite:p}`Gundlach2011`: Characterisation of ice aggregates, built of μm-sized H2O ice particles (formed by spraying water into liquid N2), porosity of aggregates depends on production method: 0.11 – 0.72 volume filing factor, critical rolling friction force ice: 114.8 x 10-10 N (silica: 12.1 x 10-10 N), adhesive bonding for ice stronger than for SiO2, specific surface energy ice: 0.19 J/m2



