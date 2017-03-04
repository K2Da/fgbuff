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
            % if len(winner) == 1:
                % p = winner[0]
                {{!p.flag_span}} {{!p.link}}
            % end
            % if len(winner) > 1:
                {{len(winner)}} players
            % end
        </td>
        <td style="vertical-align: middle;">
            <span class="tag tag tag-primary">{{t.version.short}}</span>
            % for p in t.props:
                <span class="tag tag tag-info">{{p.short}}</span>
            % end
        </td>
        <td>{{t.date_string}}</td>
    </tr>
% end
</table>
