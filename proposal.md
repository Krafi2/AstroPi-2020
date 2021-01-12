# **Proposal for the Astro-pi experiment**

## Theme: Life in space
**Team**: K-Gang
**Members**: Ekaterina Danilina, Jakub Havlíček, Katarína Horská
**Country**: Czech Republic
**Mentor**: Sylva Jarošová

## Our experiment 
We are going to use purely the instruments on the Ed model Astro Pi computer to calculate some of the orbital attributes of the ISS. We will use primarily measurements from the magnetometer and then measurements from the accelerometer and gyroscope to confirm our results. This experiment is quite fascinating to us as we will be able to observe the ISS’s orbit without actually “looking” outside.

## Magnetometer
The first step in characterising the orbit is to measure the orbital period. We presume that data from the magnetometer will contain some sort of periodical signal, which we can isolate using the Fourier transform. This will be done by transforming the data into its component frequencies and selecting the lowest one.

## Gyroscope
The data we obtain from the magnetometer may be noisy due to external factors such as solar radiation, which may result in false or imprecise results. Because of this we want to verify our results using an entirely different instrument. The gyroscope is a good candidate for this because it relies on a completely unrelated phenomena. Now about our actual method; Since we know that the ISS rotates in such a way as to be always facing the Earth, we can deduce that the gyroscope should measure a 360 degree rotation after an orbital period has been completed. We can then simply measure the time between full rotation and get the period we are after. Undoubtedly this is not the best method as we have to assume that the satellite we are measuring from rotates in a specific way, but it should suffice as a means of confirming our results from the magnetometer.

## Accelerometer
If the history of spaceflight has taught us anything, it is that things can and do go wrong. Because of this we would like to verify our verification data from the gyroscope using the accelerometer. The data from the gyroscope is reliable as long as the Astro Pi computer itself doesn’t move relative to the ISS. The computer however isn’t anchored to the station’s structure particularly solidly, so we expect there to be at least a small amount of noise caused by the astronauts working in the module. We cannot correct for this noise but at least we can detect it. This is the part where the accelerometer comes in. Normally we wouldn’t measure any acceleration even though the ISS is still in the Earth’s gravity field because the space station is in free fall, but any output from the gyroscope will be caused by vibrations and movement of the computer. This output should then be tightly correlated with output from the accelerometer. This way we can at the very least confirm that our data is inaccurate and not give it too much thought when comparing it to the results from the magnetometer.

## LED Matrix
On the Ed’s LED Matrix we are going to display a flag of our country: Czech Republic. If we detect high levels of vibrations or movement we will display a message telling the astronauts to be careful.




## What will we be able to calculate?
* **Distance from the center of the Earth**
We can use Kepler’s third law to calculate the distance using the orbital period and Earth’s mass.
* **Orbit length**
Since we already know the distance from the center of the Earth and circulation time, we can calculate the length of the orbit.
* **Orbital velocity**
We know the orbit length and the circulation time, so we can easily calculate the speed.

We can find the route of the ISS at the time we were recording our measurements online. In the end, we will be able to fully describe the route of ISS for the time we were given. If we record something unusual, like very high vibrations, we will know exactly at what time and place that happened. 

## Earth measurements
To achieve more accurate results, we are going to make a few measurements here on Earth with the Astro-Pi computer that we will receive to test the accuracy of the sensors. Additionally we will attempt to explain possible sources of noise.



