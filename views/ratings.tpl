% from operator import attrgetter
% import util.glicko2
% rebase('base.tpl', title='Ratings')
<h4 class="display-4">Ratings</h4>
<p>
    Ratings based on Glicko2 system, with {{'{:,}'.format(pool.rating_match_count)}} match results.
    Unrated players' ratings {{'{:,}'.format(util.glicko2.RATE)}}, RD {{util.glicko2.RD}} and volatality is {{util.glicko2.VOLATALITY}}.
    Players having RD > {{util.glicko2.DISPLAY_RD}} are not displayed.
</p>

% include('labels.tpl')

<table class="table">
    <tr>
        <td></td>
        <td></td>
        <td class="text-xs-center">rate</td>
        <td class="text-xs-center">RD</td>
        <td class="text-xs-center">95% range</td>
    </tr>
% for pair in sorted(pool.ratings.items(), key=lambda x: x[1].rating, reverse=True):
    % index, rate = pair[0], pair[1]
    % player = pool.players[index]
    % if rate.rd > util.glicko2.DISPLAY_RD:
        % continue
    % end
    <tr>
        <td class="text-xs-right">{{!player.flag_span}}</td>
        <td><a href="/rate/{{player.url}}">{{player.name}}</a></td>
        <td class="text-xs-right">{{'{:,}'.format(rate.rating)}}</td>
        <td class="text-xs-right">{{rate.rd}}</td>
        <td class="text-xs-center">{{'{:,}'.format(rate.range[0])}} - {{'{:,}'.format(rate.range[1])}}</td>
    </tr>
% end
</table>