<!doctype html>

<html>
    <head>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, user-scalable=no" />
        <meta name="apple-mobile-web-app-capable" content="yes" />
        <title>{{title}}</title>
        <meta name="description" content="${description}" />
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-alpha.4/css/bootstrap.min.css" integrity="sha384-2hfp1SzUoho7/TsGGGDaFdsuuDL0LX2hnUp6VkX3CUQ2K4K+xjboZdsXyp4oUHZj" crossorigin="anonymous">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/awesomplete/1.1.1/awesomplete.css" crossorigin="anonymous">
        <script src='https://cdnjs.cloudflare.com/ajax/libs/riot/3.0.1/riot+compiler.js'></script>
        <script src='https://cdnjs.cloudflare.com/ajax/libs/awesomplete/1.1.1/awesomplete.js'></script>
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.0.0/jquery.min.js" integrity="sha384-THPy051/pYDQGanwU6poAc/hOdQxjnOEXzbT+OuUAFqNqFjL+4IGLBgCJC3ZOShY" crossorigin="anonymous"></script>
        <script src='/static/js/lib/superagent.js'></script>
        <script src='/static/js/lib/riotcontrol.js'></script>
        <script src='/static/js/Store.js'></script>
    </head>
    <body>
        <app></app>

        <script type="riot/tag">
            % include('tags/matches.tpl')
            % include('tags/player_input.tpl')
            % include('tags/players.tpl')
            % include('tags/bracket.tpl')
            % include('tags/group.tpl')
            % include('tags/app.tpl')
            % include('tags/participants_li.tpl')
            % include('tags/participant_input.tpl')
        </script>

        <script>
            match_width = 450
            TOURNAMENT_URL = '{{url}}'

            var store = new Store()
            RiotControl.addStore(store)
            riot.mount('*')
        </script>
    </body>
</html>
