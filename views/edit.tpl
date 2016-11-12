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
        <script src='https://cdnjs.cloudflare.com/ajax/libs/riot/2.3.18/riot+compiler.js'></script>
        <script src='https://cdnjs.cloudflare.com/ajax/libs/awesomplete/1.1.1/awesomplete.js'></script>
        <script src='/static/js/lib/superagent.js'></script>
        <script src='/static/js/lib/riotcontrol.js'></script>
        <script src='/static/js/Store.js'></script>
    </head>
    <body>
        <app></app>

        <script type="riot/tag">
            % include('tags/matches.tag')
            % include('tags/player_input.tag')
            % include('tags/players.tag')
            % include('tags/bracket.tag')
            % include('tags/app.tag')
            % include('tags/participants_li.tag')
            % include('tags/participant_input.tag')
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