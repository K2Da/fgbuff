<!DOCTYPE html>
% from bottle import request
<html lang="en">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
        <meta http-equiv="x-ua-compatible" content="ie=edge">
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-alpha.5/css/bootstrap.min.css" integrity="sha384-AysaV+vQoT3kOAXZkl02PThvDr8HYKPZhNT5h/CXfBThSRXQ6jW5DO2ekP5ViFdi" crossorigin="anonymous">
        <link href="https://cdnjs.cloudflare.com/ajax/libs/flag-icon-css/2.3.1/css/flag-icon.min.css" rel="stylesheet"/>
        <script src='https://cdnjs.cloudflare.com/ajax/libs/riot/3.0.1/riot+compiler.js'></script>
        <script src='/static/js/lib/superagent.js'></script>
        <script src='/static/js/lib/riotcontrol.js'></script>
        <script src='/static/js/Comment.js'></script>
        <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>

        % if title :
            <title>Crouch Tech: {{title}}</title>
        % else :
            <title>Crouch Tech</title>
        % end
        <style>
            .table td, .table th { padding: 0.25em; }
            .flag-icon { box-shadow: 1px 1px gray; }
        </style>
    </head>
    <body>
        % include('analytics.tpl')
        <div class="container theme-showcase" role="main" style="margin-left: 0">
            % include('nav.tpl')

            <div class="row" style="padding: 1rem 2rem">
                {{!base}}
            </div>
        </div>
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.0.0/jquery.min.js" integrity="sha384-THPy051/pYDQGanwU6poAc/hOdQxjnOEXzbT+OuUAFqNqFjL+4IGLBgCJC3ZOShY" crossorigin="anonymous"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/tether/1.2.0/js/tether.min.js" integrity="sha384-Plbmg8JY28KFelvJVai01l8WyZzrYWG825m+cZ0eDDS1f7d/js6ikvy1+X+guPIB" crossorigin="anonymous"></script>
        <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-alpha.5/js/bootstrap.min.js" integrity="sha384-BLiI7JTZm+JWlgKa0M0kGRpJbF2J8q+qreVrKBC47e3K6BW78kGLrCkeRX6I9RoK" crossorigin="anonymous"></script>
        <script type="riot/tag">
            % include('tags/comment.tpl')
        </script>

        <script>
            riot.mount('comment', { page_url: '{{!request.path}}' })
            $(function () { $('[data-toggle="tooltip"]').tooltip() })
        </script>
    </body>
</html>
