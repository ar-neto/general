## Sodium acetate Simulation ##

Sodium acetate is acompound with a variety of usas, ranging from beign a food additive to a hand warmer. In 2016, its market size was estimated to be over USD 120 million (https://www.gminsights.com/industry-analysis/sodium-acetate-market), and it still expects growth. In order to tap into said growth, one would have to build a production plant.
For that end, I bring you this simulation - made using the DWSIM simulation software.

In this project, the simulation is made to produce 27936000 kg of anhydrous sodium acetate (at a purity of 99%) per year. With an initial investment of 6420000 USD, the this investment is planned to be recovered in during the second year of operation, if this product is sold at 5 USD/kg. The process diagram is shown below.

![Process diagram](https://github.com/hzeri/general/blob/main/sodium_acetate_production/process%20diagram.PNG)

Here, the process is shown. The production is made through the reaction between acetic acid and sodium hyfroxide, present in the feed. Their reaction can be exlpained as:

CH3COOH (aq.) + NaOH (aq.) -> NaCH3COO (aq.) + H2O (l)

Afterwards, the reacton producrs as well as the unreacted reagents are fed into a distillation column, where the top (i.e. the distillate) current contains mostly water and sodium acetate, whereas the bottoms contains mostly the unreacted components and water. FInally, the top is fed into an evaporator to eliminate the water, thus only the sodium acetate remains. regarding impurities, the sodium acetate will contain a small percentage of water(under 1%), which in turn will react with the salt, thus originating sodium acetate tryhydrate. The results of each output are shown below.

![Process diagram](https://github.com/hzeri/general/blob/main/sodium_acetate_production/results.PNG)
