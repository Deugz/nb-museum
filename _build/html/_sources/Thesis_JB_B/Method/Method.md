# &#9999; **Chapter 2.B**  

## Method


:::{note}
Implement later, Neutron scattering should go in Mat et Meth 
:::

## 2.1 Neutron Scattering

### 2.1.1 Theory

Neutron scattering is a well-suited non-destructive technique to study the structural properties of materials. Compared to X-Rays, neutrons do not interact with the electronic cloud but with the nucleus of atoms making light atoms such as Hydrogen or Deuterium more visible. We use the ISIS Neutron and Muon spallation source (source) at the Rutherford Appleton Laboratory campus which is a spallation source. The Neutron beam is pulsed, meaning that the neutron energy is determined by the Time of flight (TOF) from the source to the detector, passing through the sample.
The scattering of a neutron by a sample is characterized by a change in its momentum P (wavevector) and Energy E (frequency). In our case, we assume that there is no energy exchange between the neutron and our sample, i.e. that the scattering is purely elastic. It can thus be described by Q, the momentum transfer and is equal to ki – kf where ki is the incident and kf the scattered wavevector. Q can be expressed as:

 Q =  (4π sin⁡θ)/λ
 
Where θ is the scattering angle and λ the incident wavelength of the neutron.
Neutrons are scattered when their wavelengths are comparable to the distance between objects within the sample. Thus, the larger the wavelength (lambda), the smaller is Q.
We use NIMROD (Near and Inter-Mediate Range Order Diffractometer) (56), a neutron scattering instrument located in the Target Station 2 (TS2) at ISIS, that can measure continuous length scale from 1 to 300 Angstrom. That allows us to probe both the bulk structure at high Q, and the surface structure at low Q as shown in Figure 7

:::{note}
Include (redo)  sabrina Neutron scattering plot
:::

A neutron scattering experiment measures the number of neutrons scattered in various directions (described by spherical coordinates). This can be expressed by the differential cross section which is the ratio of the scattered neutrons per solid angle unit, divided by the total number of incident neutrons per unit area of beam. The cross section depends on the scattering length of the atom and can be defined as a mean value, the coherent scattering that features all the sample structural information and the incoherent scattering which correspond to a featureless background. The scattering length is isotope specific and Hydrogen has a very high incoherent scattering cross section (80.27 barns) compared to Deuterium (2.05 barns) so H2O will have a low signal on a high background whereas D2O a high signal on a low background. This mean that to obtain a clear neutron scattering signal we need to use D2O to produce our particles at ISIS. (does this modify the resulting cooling efficiency?)

