# urlShortedService

### type_id

>public = 1
>private = 2 
>authorized = 3 


## create public short-link  

you do not need to log in to create a link or follow it

``` JSON 
{
    "url":"https://www.youtube.com/",
    "alias_url":"youtube",
    "type_id":1
}

```
in postman

* http://127.0.0.1:5000/youtube 

or

* http://127.0.0.1:5000/aifhCqd$



## create authorized and private short-link

you need to log in to create private and authorized links

authorized:
``` JSON 
{
    "url":"https://www.youtube.com/",
    "alias_url":"youtube",
    "type_id":3
}

```

private:
``` JSON 
{
    "url":"https://www.youtube.com/",
    "alias_url":"youtube",
    "type_id":2
}

```

in postman

* http://127.0.0.1:5000/youtube 

or

* http://127.0.0.1:5000/aifhCqd$

