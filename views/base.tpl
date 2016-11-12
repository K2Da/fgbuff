<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
        <meta http-equiv="x-ua-compatible" content="ie=edge">
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-alpha.5/css/bootstrap.min.css" integrity="sha384-AysaV+vQoT3kOAXZkl02PThvDr8HYKPZhNT5h/CXfBThSRXQ6jW5DO2ekP5ViFdi" crossorigin="anonymous">
        % if title :
            <title>Crouch Tech: {{title}}</title>
        % else :
            <title>Crouch Tech</title>
        % end
        <style>
            .table td, .table th { padding: 0.25em; }
        </style>
    </head>
    <body>
        % include('analytics.tpl')
        <div class="container theme-showcase" role="main">
            <nav class="navbar navbar-light">
                <div class="collapse navbar-toggleable-xs" id="navbar-header">
                    <a class="navbar-brand" href="/">Crouch Tech</a>
                    <ul class="nav navbar-nav">
                        <li class="nav-item">
                            <a class="nav-link" href="/tournaments">Tournaments</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="/players">Players</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="/vstable/">CPT Table</a>
                        </li>
                    </ul>
                </div>
            </nav>
            <div class="row" style="padding: 1rem 2rem">
                {{!base}}
            </div>
        </div>
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.0.0/jquery.min.js" integrity="sha384-THPy051/pYDQGanwU6poAc/hOdQxjnOEXzbT+OuUAFqNqFjL+4IGLBgCJC3ZOShY" crossorigin="anonymous"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/tether/1.2.0/js/tether.min.js" integrity="sha384-Plbmg8JY28KFelvJVai01l8WyZzrYWG825m+cZ0eDDS1f7d/js6ikvy1+X+guPIB" crossorigin="anonymous"></script>
        <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-alpha.5/js/bootstrap.min.js" integrity="sha384-BLiI7JTZm+JWlgKa0M0kGRpJbF2J8q+qreVrKBC47e3K6BW78kGLrCkeRX6I9RoK" crossorigin="anonymous"></script>
    </body>
</html>
