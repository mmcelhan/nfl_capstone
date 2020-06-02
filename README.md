# nfl_capstone

### Data flow diagram
![Data Flow Diagram](documentation/data_flow_diagram.png)

General thesis: We can create a model to predict NFL player effectiveness through college statistics and workout numbers.

### Model thesis diagram
![Model Thesis](documentation/model_thesis.png)

I think we have everything we need in terms of raw data in the raw_players folder-a few things.

1. The draft order is linked to each player. This is useful later in the output section but I don't want it to leak into the input since it won't be known when the model is running
2. We'll need to fuzzy match player name to Madden Number

Large tasks:
1. Data acquisiton
   1. Madden Data - These exists in spreadsheets. I have found 2017 to 2020 data.
   2. Faces - can someone build a web crawler?
   3. Edina's water idea - I love this...what could we use as something that's not thought of but useful?
2. Data transformation
   1. The toughest part is linking the player to a unique ID. Madden has an ID, but I think we'll need to fuzzy match to it. Name, college, posision, or pro teams are means to do this.
   2. Missing values - Some people skip some or all of the combine workouts. Sometimes because they're hurt, sometimes because they know it will only hurt their draft stock. I don't know the right answer for this
   3. Players without Madden rankings - this means they're likely not in the league anymore. Should we assign a 0? The lowest number that exists in the dataset?
3. Modelling - I see this as the easiest portion after all the data wrangling. A neural network would be neat but an random forest is a known commodity.


   
