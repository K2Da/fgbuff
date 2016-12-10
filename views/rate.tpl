% from operator import attrgetter
% ratings = [pool.rating_log(p) for p in player_urls]
% rebase('base.tpl', title='rating')

<div class="col-xs-12">
    <p class="display-4">Rating Log</p>
    % include('labels.tpl')
</div>

<div class="col-xs-2">
    <table class="table">
        % for pair in sorted(pool.ratings.items(), key=lambda x: x[1].rating, reverse=True):
            % index, rate = pair[0], pair[1]
            % player = pool.players[index]
            % if rate.rd > 50:
                % continue
            % end
            <tr>
                <td>
                    % if player.url in player_urls:
                        % if len(player_urls) > 1:
                            <a type="button" class="btn btn-danger" style="padding: 0px; width: 1.5em;"
                               href="/rate/{{'/'.join([u for u in player_urls if u != player.url])}}"
                            >-</a>
                        % else:
                            <a type="button" class="btn btn-danger" style="padding: 0px; width: 1.5em;">!</a>
                        % end
                    % else:
                        <a type="button" class="btn btn-primary" style="padding: 0px; width: 1.5em;"
                           href="/rate/{{'/'.join(player_urls) + '/' + player.url}}"
                        >+</a>
                    % end
                </td>
                <td style="vertical-align: middle;"><a href="/player/{{player.url}}">{{player.name}}</a></td>
            </tr>
        % end
    </table>
</div>

<div class="col-xs-10">
    <div id='chart_div' style='width: 880px; height: 400px;'></div>
    <script type='text/javascript'>
        google.charts.load('current', {'packages': ['annotationchart']});
        google.charts.setOnLoadCallback(drawChart);

        function drawChart() {
            var data = new google.visualization.DataTable()
            data.addColumn('date',   'Date')

            % for rate in ratings:
                data.addColumn('number', '{{ rate.player.name }}')
                data.addColumn('string', '{{ rate.player.name }} title')
                data.addColumn('string', '{{ rate.player.name }} text')
            % end

            % tournaments = []
            % for rate in ratings:
            %    tournaments += rate.tournaments
            % end

            data.addRows([
                % first = None
                % for e in sorted(list(set([t.end_at for t in tournaments]))):
                    % if first is None:
                        % first = e
                    % end
                    [new Date({{e.year}}, {{e.month - 1}}, {{e.day}})
                    % for rate in ratings:
                        , {{rate.rate_at(first, e)}}, '{{rate.tournament_name_at(e)}}', '{{rate.rank_at(e)}}'
                    % end
                    ],
                % end
            ])

            var chart = new google.visualization.AnnotationChart($('#chart_div')[0])
            var options = { displayAnnotations: true, displayZoomButtons: false, table: { sortColumn: 0 }, thickness: 2}
            chart.draw(data, options)
        }
    </script>
</div>
