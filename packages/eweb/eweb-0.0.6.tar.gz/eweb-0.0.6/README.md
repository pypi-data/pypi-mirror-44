# eweb
**eweb**(easy web) is a fast and simple micro-framework for small web applications. Its goal is to enable you to develop
web applications in a simple and understandable way. 

With it, you don't need to know the HTTP protocol, or how Python communicates with JavaScript. 

## Usage

### Step1
Create a file, such as `main.py`:   
```python
from eweb import Server


def hello(name):
    return 'hello %s!' % name


if __name__ == '__main__':
    server = Server(port=5000)
    server.services['hello'] = hello

    server.run()

```

### Step2
 1. Create a folder named `static`
 2. Create a HTML file in the `static` folder, such as `index.html`:   
 ```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>index</title>
    <script src="/service.js"></script>
</head>
<body>
<script>
    //say hello
    service.call('hello', {'name': 'eweb'}, function(data){
        alert(data);
        /**
        ...
        Anything you want to do
        ...
        */
    });
</script>
</body>
</html>
```
 
### Step3
Run the `main.py`. Then, visit `http://localhost:5000/index.html` in your browser.
You will get alert message "hello eweb!".  

It's also easy if you want to develop desktop applications with **eweb**. At this point, usually, you need a callback function and a random port to start the server.
What you need to do will be like this:   
```python
from eweb import Server


def hello(name):
    return 'hello %s!' % name


def callback():
    print('Server startup completed!')
    import webbrowser
    webbrowser.open('http://localhost:%s/index.html' % server.port)
    

if __name__ == '__main__':
    server = Server(port=None)
    server.services['hello'] = hello

    server.run()

```

Run `main.py`, then, after the server is started, the `index.html` page will open automatically in the browser.

## Note
The `static` folder is a resource folder, and files under this folder can be accessed directly. So, usually, HTML, CSS, and JavaScript files should be placed in this folder, and other private files should not be placed in this folder.
