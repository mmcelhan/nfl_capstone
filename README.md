# nfl_capstone
 
![Data Flow Diagram](diagrams/data_flow_diagram.png)


I think we have everything we need in terms of raw data in the raw_players folder-a few things.

1. The draft order is linked to each player. This is useful later in the output section but I don't want it to leak into the input since it won't be known when the model is running
2. We'll need to fuzzy match player name to Madden Number


Large tasks:
1. Data acquisiton
   a. Madden Data - These exists in spreadsheets. I have found 2017 to 2020 data.
   b. Faces - can someone build a web crawler?
   c. Edina's water idea - I love this...what else could we use?
2. Data transformation
   a. The toughest part is linking the player to a unique ID. Madden has an ID, but I think we'll need to fuzzy match to it. Name, college, posision, or pro teams are means to do this.
   b. Missing values - Some people skip some or all of the combine workouts. Sometimes because they're hurt, sometimes because they know it will only hurt their draft stock. I don't know the right answer for this
   c. Players without Madden rankings - this means they're likely not in the league anymore. Should we assign a 0? The lowest number that exists in the dataset?
3. Modelling - I see this as the easiest portion after all the data wrangling. A neural network would be neat but an random forest is a known commodity.


   
