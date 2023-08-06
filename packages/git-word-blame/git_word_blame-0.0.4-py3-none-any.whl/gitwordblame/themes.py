THEMES = {
    'solarized-light': """
body {
    border: 10px solid #eee8d5;
    background-color: #fdf6e3;
    color: #586e75;
}

#content > a:hover, #content > a.hovered {
    background: #93a1a1;
    color: #fdf6e3;
}
""",
   'black-and-white': """
body {
    margin: 10px;
    border: 1px solid #ececec;
}

#content > a:hover, #content > a.hovered {
    background: black;
    color: white;
}
""",
    'solarized-dark': """
body {
    background-color: #2d363a;
    color: #94a3a5;
}

#content > a:hover, #content > a.hovered {
    background: #94a3a5;
    color: #2d363a;
}
""",
}

COMMON_CSS = """
body {
    margin: 0;
    padding: 10px;
}
#content > a {
    color: inherit;
    text-decoration: none;
}
#content {
    white-space: pre-wrap;
    word-wrap: anywhere;
    margin-top: 0;
} 
#content > a:hover, #content > a.hovered {
    cursor: pointer;
}
"""