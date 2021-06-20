# wicked_cranium_rarity_order  
  
Quick little script to calculate the rarity order of Craniums using a basic weighting approach.  
  
6 traits each. Just adds the total of the trait value. The lower the total weight, the 'rarer' it is.  

Might not be 100% accurate, but if someone wants to make any ammendments feel free :)  
  
Metadata dump from: https://cdn.discordapp.com/attachments/845548151162535978/856261703591264266/metadata.json  
Trait totals from: https://pastebin.com/PgpDrQSK  
  
Have uploaded both of the above to repo for ever lasting life and goodness.
  
Results are in the following format:  

```
Name | weighting | metadata link
```
  
Usage:  

```
python3 order.py
```
