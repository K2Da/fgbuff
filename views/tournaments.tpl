% from operator import attrgetter
% rebase('base.tpl', title='Tournaments')

<h4 class="display-4">Tournaments</h4>

% include('labels.tpl')

<table class="table">
% for t in sorted(pool.tournaments.values(), key=attrgetter('end_at_desc')):
    <tr>
        <td>{{!t.flag_span}} {{!t.a}}</td>
        <td>
            % winner = t.player_at_rank(1)
            % if len(winner) > 0:
                % p = t.player_at_rank(1)[0]
                {{!p.flag_span}} {{!p.link}}
            % end
        </td>
        <td style="vertical-align: middle;"><small>{{!t.labels_short}}</small></td>
        <td>{{t.date_string}}</td>
    </tr>
% end
</table>
