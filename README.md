# Scrapy_39
## Project Description:
Use scrapy in python to crawl: http://ypk.39.net/AllCategory <br />
This is a basic web-crawling example. I become familar with how a spider and items work.  <br />

## Set up
1) Install scrapy package and make sure it can functions in your project environment <br />

## Special Notice
1) Although this is a basic scrapy task, it's not completely easy to finish and get highly organized data. Each medicine has many possible kinds of missing value, so you need to pay attention to null-check through your looping.
2) Moderate comprehension of xpath is highly recommanded. I think most of difficult parts lie in how to handle with selector, i.e. how to tell selector which element(s) to choose using xpath. A simple tutorial: https://www.tutorialspoint.com/xpath/xpath_expression.htm

## Additional Feature: saving data into your database
For info about how to save data into your database using pipeline, please check my Scrapy_IKang repo: https://github.com/Thomaswang0822/Scrapy_Ikang

## Special Thanks
Special thanks to Harry Wang, https://github.com/harrywang <br />
for his fantastic end-to-end tutorial (it has 5 parts), https://towardsdatascience.com/a-minimalist-end-to-end-scrapy-tutorial-part-i-11e350bcdec0  <br />
and his scrapy-selenium-demo, https://github.com/harrywang/scrapy-selenium-demo <br />
