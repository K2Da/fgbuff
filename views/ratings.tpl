% from operator import attrgetter
% rebase('base.tpl', title='Ratings')
<h4 class="display-4">Ratings</h4>

% include('labels.tpl')

<table class="table">
% for pair in sorted(pool.ratings.items(), key=lambda x: x[1].rating, reverse=True):
    % index, rate = pair[0], pair[1]
    % player = pool.players[index]
    % if rate.rd > 50:
        % continue
    % end
    <tr>
        <td>{{player.name}}</td>
        <td class="text-xs-right">{{rate.rating}}</td>
        <td class="text-xs-right">{{rate.rd}}</td>
        <td class="text-xs-center">{{rate.range[0]}} - {{rate.range[1]}}</td>
    </tr>
% end
</table>