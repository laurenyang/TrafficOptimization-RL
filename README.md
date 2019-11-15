# TrafficOptimization-RL

## The Problem 
Cities around the world, from Los Angeles to Sao Paolo to New York City, suffer from traffic congestion. Whether it is the morning rush to get to work or the afternoon one to return home, cities cycle through daily and seasonal periods of high intensity traffic. A 2018 study concluded that drivers on average wasted 97 hours annually in traffic, with especially congested cities eating up even more time, as is the case with Boston, where drivers spent 164 hours annually in idle [Inrix]. Beyond the time wasted, traffic is a source of pollution, stress, excess fuel consumption, and loss of productivity. In fact, monetary losses due to traffic cost New York City $33.7 billion cumulatively in 2018, and on a national level cost U.S. commuters $305 billion in 2017 [Inrix]. 

## Current Solution
To address this problem, we want to improve the traffic light system. Currently, traffic lights have three tiers of intelligence. The lowest level of intelligence is timed sequences, where the lights are hard coded to remain their respective colors based on previously researched time intervals [Practical Engineering]. While this will work for a steady volume of traffic, inefficiencies begin to surface when the traffic volume is stochastic. The next level of intelligence is called actuated signal control, which takes external input from traffic detection technology to determine light durations [Practical Engineering]. Although this additional layer of information can handle varying volumes of traffic, the lights are isolated entities as they only have access to the intersection they are at. Most traffic lights are at this second level of intelligence. The last level of intelligence is called adaptive signal control technologies (ASCT) and allows for intelligent control for a network of lights [Practical Engineering]. Lights using ASCT are acting under a centralized system with traffic data from across the network, with decisions being made to optimize on a larger, neighborhood or even city like scale. ASCT is still in development and is not deployed in many cities. In this project, we plan on designing our own city-level ASCT system to reduce traffic congestion. 

The Role of Decision Making
Designing an ASCT is a decision making problem where the decision involves when to change a light from one color to another.

First, we consider the situation for a single intersection. For example, if there are no cars on a green light intersection, then it would be the best decision to switch to yellow and red. Similarly, if there are many cars queued up behind a red light and no cars in the cross-direction, the optimal decision may be to switch the light to green.

Additionally, if we increase the scope of the problem to multiple intersections across a city, the decision-making problem can become very complex. For example, changing the light at one of the traffic lights may influence the traffic flow at other lights, which could be detrimental. Thus, at each instant, at each intersection, there is a very large number of factors to consider.

The ideal decision at each intersection would allow the cars waiting at the stoplight to all clear the intersection. In off-peak hours, this is not too difficult, but during rush hour, this is not always possible due to the sheer volume of cars. In these cases, the green light duration could be increased to minimize the amount of time for cars to start moving and clear the intersection (which are the times that the intersection is not fully utilized) [Practical Engineering]. The length of the yellow light is another decision to be considered. The ideal yellow light duration is long enough for drivers to recognize the light change and to slow down to a stop at a safe rate. A general rule of thumb is one second of yellow light duration for every 10 miles per hour on the speed limit around the intersection, but this time could change based on the surrounding terrain and other factors [Practical Engineering]. Since cars are allowed to enter the intersection on a yellow light, a decision has to be made on how long to keep all lights red to allow the intersection to clear completely. This time is typically around a second, but can be changed based on conditions similar to those considered with the yellow light duration [Practical Engineering].

## Sources of Uncertainty
There are quite a few different sources of uncertainty when it comes to traffic intersections. The actions of every car, while predictable most of the time, can deviate from the expectation based on factors that are not necessarily measurable, like if the driver of a particular car is aggressive or conservative or if there is something on the road that cars swerve to avoid hitting. Also, cars can vary speed quite often and the presence of uncontrolled intersections, such as stop signs, introduce more variability. Finally, we sometimes will not know how a car will turn, such as in the right hand lane, a car may be able to turn right on red, which we will have to model and consider. In addition, the volume of traffic is not known beforehand, so the optimal traffic light sequence must be determined online. 

## Our Solution and Approach
We plan to randomly create grid structures to model streets with cells that could represent stop signs or traffic lights. We could try to optimize for the least amount of time on average that each car has to stay stopped at a light through the area that we simulate. Though we have not quite covered material to fully have a solution in mind, we were thinking that we could sample car speeds and trajectories from a distribution to introduce sources of randomness and uncertainty, similar to driving in the real world. We could then test our model against several baselines, such as the naive method of having each traffic light change after a constant amount of time or the current traffic signal methodology.
