#!/usr/bin/env python
# coding: utf-8

# In[2]:


def FB(i):
    for i in range(1 ,100):
        if i % 5 == 0 and i % 3 == 0:
            print('FizzBuzz')
        elif i % 3 == 0:
            print('Fizz')
        elif i % 5 == 0:
            print('Buzz')
        else:
            print(i)
FB(159)


# In[3]:


for i in range(100):
    print(i, "fizz"*(i%3==0) + "Buzz"*(i%5==0))


# In[ ]:




