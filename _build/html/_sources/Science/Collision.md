# Collision


:::::{div} full-width
::::{grid} 4
:::{grid-item}
:columns: 3
**Audience**

- Ross
- Mark

**Key Litterature**:
- {cite:p}`Walrafen1972`
- 2

**Links**

:::
:::{grid-item}
:columns: 6

Description

:::

:::{grid-item-card}
:class-header: bg-light
:columns: 3

Teaching ✏️
^^^

<p class="emphase">Planet formation</p>

<br>

**Link**: 


[<img src="https://img.shields.io/badge/Teaching-Bitesize/Astronomy/Planet_formation_bottom-top-purple.svg?logo=data:Docs/SFP-logo.png">](https://deugz.github.io/nb-teaching/_build/html/Bitesize/Astronomy/Planet_formation_bottom-top/Planet_formation_bottom-top.html) 

<br>

[<img src="https://img.shields.io/badge/Teaching-Bitesize/Astronomy/Planet_formation_top-bottom-purple.svg?logo=data:Docs/SFP-logo.png">](https://deugz.github.io/nb-teaching/_build/html/Bitesize/Astronomy/Planet_formation_top-bottom/Planet_formation_top-bottom.html) 
:::

::::

:::::


## Bouncing barrier

### Growth mechanism

Particles are coupled to the gas (Orbiting at Keplerian speed) and this is what drives the relative speed of &micro;m dust grains (ie more or less head wind relative to their size). Dust orbits the protostar at very high velocities but the relative velocities between particles in collisions can be very slow (few cm or a few mm per second). At such velocities a “bouncing barrier” exists {cite:p}`Zsom2010`. Up to mm sizes the sticking is dominated by <span class="hovertext" data-hover="Description">Van der Waals type forces</span>, leading to the formation of fluffy aggregates. Past the km scale, gravity dominates {cite:p}`Gutler2010`.



::::::{div} full-width
:::::{grid} 2

::::{grid-item-card}
:class-header: bg-light
:columns: 6
**Experiment**
^^^

```{figure} Docs/Bouncing_lab.PNG
---
name: Bouncing_lab
width: 500px
---
source: 
```



::::

::::{grid-item-card}
:class-header: bg-light
:columns: 6
**Model**
^^^

:::{figure-md} markdown-fig
<img src="Docs/Bouncing_model.PNG" alt="fishy" class="bg-primary mb-1" width="600px">

This is a caption in **Markdown**!
:::




::::
:::::
::::::


Those two figures comes from {cite:p}`Testi2014`


**models of grain growth** 

Alongside the size of the colliding particles the relative velocity is also important

## Collision Experiments

In the laboratory, a plethora of collision experiments have been conducted which clearly define the sticking bouncing and fragmentation regimes for small dusty particles at low velocities {cite:p}`Blum2010`. Those experiments, carried out with different dust composition (SiO2 / Carbon dust), have shown that in “pure dust” collisions, the dust material is less 
important than the **grain size, the surface roughness and porosity**.

- All of those could be investigated by SEM

- Lab is often in microgravity to reach low velocity while avoiding sedimentation {cite:p}`Blum2000` 

The outcomes of these collisions provide vital data to modellers who want to understand how collision properties and outcomes impact the broader processes of planet formation. [23] 

### Icy particles collision

Ice enhnaces the stickiness of interstellar grains {cite:p}`Gundlach2015`. No collisions between amorphous ice particles has been performed to date (even though they are present in PPD), the reason being the complex and metastable nature of amorphous ice which makes it difficult to produce, store and use. This is what I was trying to solve

## HGW ice grains 

I designed an experiment to produce Amorphous Ice grain analogues. HGW is similar to ASW.

### HGW Setup 

- OU / Helen Fraser

::::::{div} full-width
:::::{grid} 2

::::{grid-item}
:columns: 7


```{figure} ../Docs/Bench_And_Glovebox_Assembly_20-12-2019_IMG3.jpg
---
name: Experiment
width: 600px
---
source: 
```

::::

::::{grid-item}
:columns: 5

The purpose of this experiment is to produce **&micro;m HGW ice particles**. This is achieved by spraying &micro;m water droplets in liquid ethane, the most suited cryoliquid to achieve high cooling rates. This is a technique used in cryobiologie to freeze biological samples.

```{note}

Hence, this setup could open the doors for sample preparation that extend far beyond the scope of astronomy! 

- Important to mention for business case

```

::::

:::::
::::::


### Initial results

:::::{grid} 2

::::{grid-item}
:columns: 6

**Neutron Scattering**

```{figure} Docs/ISIS-plot4sample2.PNG
---
name: Experiment
width: 600px
---
source: 
```

::::

::::{grid-item}
:columns: 6

**Optical Microscopy**



```{figure} Docs/2017_10_06_3rd010.jpg
---
name: Experiment
width: 600px
---
source: 
```

::::

:::::

Initial Neutron scattering results show that our ices present some amorphicity. 


#### Comment on Microscopy

:::::{grid} 2

::::{grid-item}
:columns: 6

```{figure} Docs/20190927_102827.jpg
---
name: Experiment
width: 300px
---
source: 
```

::::

::::{grid-item}
:columns: 6

```{figure} Docs/20190927_102859.jpg
---
name: Experiment
width: 300px
---
source: 
```

::::

:::::

What I would like to stress out here is that I have tried to do the science I needed with what we had available (Optical microscoy with cold plate). This technique is not well suited for amorphous ice (and the experiments done have used crystaline ices, produced in liquid Nitrogen) - ie we had to make compromises. I somehow found a solution that allowed us to pour the liquid Nitrogen + ice mixture into the container you see in Figure 7, cooled by the plate you see in figure 6, but it was very difficult for the following reasons:

- We have to pour the ice/liquid nitrogen mixture within the "cell", the mixture is very turbulent due to LN2 evaporation and make the observation very difficult (unreliable focus ...)

- The experiment are performed at ambiant pressure so lots of condensation (impurities)

- Even though the Ice container could be cool to liquid Nitrogen temperature, it is not sure that the ice is at this temperature (and liquid droplets can be seen on figure 5)

A cryostage would greatly improve my observations


#### SEM ?

Cryo Electron microscopy would be of incredible help by offering:

- A dedicated, state of the art, experimental setup to maintain the particles at cold temperature after they have been produced, and during their characterisation.
    - This is mandatory if I want to properly caracterise the particles in their amorphous state.
    
- The particles are produced in ethane and are stored in cryo-vials.
    - For safety reasons, having a controled atmosphere within the SEM, would help in **safe** sample preparation

- Shape and size distribution as well as unveiling the processes at play during the aggregation phase, like {cite:p}`Gundlach2018` could be achieved with a cryo SEM


### Ice manipulation

One of the most difficult aspect when dealing with amorphous ices is that when pulled out of their cold medium, they will very quickly warm up and crystalise. Having an in-house characerision technique is the best option to mitigate those problems

::::::{div} full-width
:::::{grid} 3 

::::{grid-item}

**Inside Glove box**

```{figure} Docs/20191118_145124.jpg
---
name: Experiment
width: 600px
---
source: 
```

::::

::::{grid-item}

**Storage**

```{figure} Docs/20191122_115552.jpg
---
name: Experiment
width: 600px
---
source: 
```

::::

::::{grid-item}

**Prep chamber**

I have been working with Anita on achieving accoustic levitation within a cooled Glove-box. This could be handed to the EM-suite for sample preparation. 
```{note}

Ask me more if you need

```

::::

:::::


#### Experimental limitations

- Particles need to remain at liquid nitrogen temperature or they will crystalise

- Ethane is present so may be best to have a prep lab in-house

## One Step further


### From micron to mm-cm size amophous aggregates.

Producing HGW &micro;m ICE grains is only the first step toward unveiling the role that ASW could play in overcoming the bouncing barrier. Indeed, this barrier lies at sizes around the cm size and growing such big aggregates is another big challenge. 

```{figure} Docs/Ice_aggregation.png
---
name: Experiment
width: 600px
---
source: 
```

```{note}

- Insert Accoustic trap video

```



We (Anita mostly) have developped at the OU an accoustic levitation technique that can work at temperature of -20 degree to allow for the aggregation of those monomers in a similar fashion than in space


### Grain shape vs IR spectroscopy

Grain shape affect the IR spectral signature (ie right wing)

Electron microscopy would be a great addition to our future IR work.


## Comments

<script src="https://utteranc.es/client.js"
        repo="Deugz/nb-museum"
        issue-term="pathname"
        theme="github-light"
        crossorigin="anonymous"
        async>
</script>